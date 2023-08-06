# -*- coding: utf-8 -*-
# Copyright (c) 2007, 2008, Benoît Chesneau
# Copyright (c) 2007 Simon Willison, original work on django-openid
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#      * Redistributions of source code must retain the above copyright
#      * notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#      * notice, this list of conditions and the following disclaimer in the
#      * documentation and/or other materials provided with the
#      * distribution.  Neither the name of the <ORGANIZATION> nor the names
#      * of its contributors may be used to endorse or promote products
#      * derived from this software without specific prior written
#      * permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import datetime
from django.utils import simplejson
from django.http import HttpResponseRedirect, get_host, Http404, \
                         HttpResponseServerError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.conf import settings
from askbot.conf import settings as askbot_settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils.http import urlquote_plus
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.views.defaults import server_error

from openid.consumer.consumer import Consumer, \
    SUCCESS, CANCEL, FAILURE, SETUP_NEEDED
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import sreg
# needed for some linux distributions like debian
try:
    from openid.yadis import xri
except ImportError:
    from yadis import xri

import re
import urllib

from askbot import forms as askbot_forms
from askbot.deps.django_authopenid import util
from askbot.deps.django_authopenid import decorators
from askbot.deps.django_authopenid.models import UserAssociation, UserPasswordQueue, ExternalLoginData
from askbot.deps.django_authopenid import forms
from askbot.deps.django_authopenid.backends import AuthBackend
from django import forms as django_forms
import logging
from askbot.utils.forms import get_next_url

EXTERNAL_LOGIN_APP = settings.LOAD_EXTERNAL_LOGIN_APP()

#todo: decouple from askbot
def login(request,user):
    from django.contrib.auth import login as _login
    from askbot.models import signals

    if settings.USE_EXTERNAL_LEGACY_LOGIN == True:
        EXTERNAL_LOGIN_APP.api.login(request,user)

    #1) get old session key
    session_key = request.session.session_key
    #2) get old search state
    search_state = None
    if 'search_state' in request.session:
        search_state = request.session['search_state']

    #3) login and get new session key
    _login(request,user)
    #4) transfer search_state to new session if found
    if search_state:
        search_state.set_logged_in()
        request.session['search_state'] = search_state
    #5) send signal with old session key as argument
    logging.debug('logged in user %s with session key %s' % (user.username, session_key))
    #todo: move to auth app
    signals.user_logged_in.send(user=user,session_key=session_key,sender=None)

#todo: uncouple this from askbot
def logout(request):
    from django.contrib.auth import logout as _logout#for login I've added wrapper below - called login
    if 'search_state' in request.session:
        request.session['search_state'].set_logged_out()
        request.session.modified = True
    _logout(request)

def get_url_host(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    host = escape(get_host(request))
    return '%s://%s' % (protocol, host)

def get_full_url(request):
    return get_url_host(request) + request.get_full_path()

def ask_openid(
            request,
            openid_url,
            redirect_to,
            on_failure=None,
            sreg_request=None
        ):
    """ basic function to ask openid and return response """
    request.encoding = 'UTF-8'
    on_failure = on_failure or signin_failure
    
    trust_root = getattr(
        settings, 'OPENID_TRUST_ROOT', get_url_host(request) + '/'
    )
    if xri.identifierScheme(openid_url) == 'XRI' and getattr(
            settings, 'OPENID_DISALLOW_INAMES', False
    ):
        msg = _("i-names are not supported")
        logging.debug('openid failed because i-names are not supported')
        return on_failure(request, msg)
    consumer = Consumer(request.session, util.DjangoOpenIDStore())
    try:
        auth_request = consumer.begin(openid_url)
    except DiscoveryFailure:
        msg = _(u"OpenID %(openid_url)s is invalid" % {'openid_url':openid_url})
        logging.debug(msg)
        return on_failure(request, msg)

    logging.debug('openid seemed to work')
    if sreg_request:
        logging.debug('adding sreg_request - wtf it is?')
        auth_request.addExtension(sreg_request)
    redirect_url = auth_request.redirectURL(trust_root, redirect_to)
    logging.debug('redirecting to %s' % redirect_url)
    return HttpResponseRedirect(redirect_url)

def complete(request, on_success=None, on_failure=None, return_to=None):
    """ complete openid signin """
    on_success = on_success or default_on_success
    on_failure = on_failure or default_on_failure
    
    logging.debug('in askbot.deps.django_authopenid.complete')
    
    consumer = Consumer(request.session, util.DjangoOpenIDStore())
    # make sure params are encoded in utf8
    params = dict((k,smart_unicode(v)) for k, v in request.GET.items())
    openid_response = consumer.complete(params, return_to)

    try:
        logging.debug(u'returned openid parameters were: %s' % unicode(params))
    except Exception, e:
        logging.critical(u'fix logging statement above ' + unicode(e))
    
    if openid_response.status == SUCCESS:
        logging.debug('openid response status is SUCCESS')
        return on_success(
                    request,
                    openid_response.identity_url,
                    openid_response
                )
    elif openid_response.status == CANCEL:
        logging.debug('CANCEL')
        return on_failure(request, 'The request was canceled')
    elif openid_response.status == FAILURE:
        logging.debug('FAILURE')
        return on_failure(request, openid_response.message)
    elif openid_response.status == SETUP_NEEDED:
        logging.debug('SETUP NEEDED')
        return on_failure(request, 'Setup needed')
    else:
        logging.debug('BAD OPENID STATUS')
        assert False, "Bad openid status: %s" % openid_response.status

def default_on_success(request, identity_url, openid_response):
    """ default action on openid signin success """
    logging.debug('')
    request.session['openid'] = util.from_openid_response(openid_response)
    logging.debug('performing default action on openid success %s' % get_next_url(request))
    return HttpResponseRedirect(get_next_url(request))

def default_on_failure(request, message):
    """ default failure action on signin """
    logging.debug('default openid failure action')
    return render_to_response('openid_failure.html', {
        'message': message
    })


def not_authenticated(func):
    """ decorator that redirect user to next page if
    he/she is already logged in."""
    def decorated(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(get_next_url(request))
        return func(request, *args, **kwargs)
    return decorated

def complete_oauth_signin(request):
    if 'next_url' in request.session:
        next_url = request.session['next_url']
        del request.session['next_url']
    else:
        next_url = reverse('index')

    if 'denied' in request.GET:
        return HttpResponseRedirect(next_url)
    if 'oauth_problem' in request.GET:
        return HttpResponseRedirect(next_url)

    try:
        oauth_token = request.GET['oauth_token']
        logging.debug('have token %s' % oauth_token)
        oauth_verifier = request.GET['oauth_verifier']
        logging.debug('have verifier %s' % oauth_verifier)
        session_oauth_token = request.session['oauth_token']
        logging.debug('have token from session')
        assert(oauth_token == session_oauth_token['oauth_token'])

        oauth_provider_name = request.session['oauth_provider_name']
        logging.debug('have saved provider name')

        oauth = util.OAuthConnection(oauth_provider_name)

        user_id = oauth.get_user_id(
                                oauth_token = session_oauth_token,
                                oauth_verifier = oauth_verifier
                            )
        logging.debug('have %s user id=%s' % (oauth_provider_name, user_id))

        user = authenticate(
                    oauth_user_id = user_id,
                    provider_name = oauth_provider_name,
                    method = 'oauth'
                )

        logging.debug('finalizing oauth signin')

        request.session['email'] = ''#todo: pull from profile
        request.session['username'] = ''#todo: pull from profile
        request.session['user_identifier'] = user_id
        request.session['login_provider_name'] = oauth_provider_name

        return finalize_generic_signin(
                            request = request,
                            user = user,
                            user_identifier = user_id,
                            login_provider_name = oauth_provider_name,
                            redirect_url = next_url
                        )

    except Exception, e:
        logging.critical(e)
        msg = _('Unfortunately, there was some problem when '
                'connecting to %(provider)s, please try again '
                'or use another provider'
            ) % {'provider': oauth_provider_name}
        request.user.message_set.create(message = msg)
        return HttpResponseRedirect(next_url)

#@not_authenticated
def signin(
        request,
        newquestion = False,#todo: not needed
        newanswer = False,#todo: not needed
    ):
    """
    signin page. It manages the legacy authentification (user/password) 
    and openid authentification
    
    url: /signin/
    
    template : authopenid/signin.htm
    """
    logging.debug('in signin view')
    request.encoding = 'UTF-8'
    on_failure = signin_failure
    email_feeds_form = askbot_forms.SimpleEmailSubscribeForm()

    next_url = get_next_url(request)
    logging.debug('next url is %s' % next_url)

    if next_url == reverse('user_signin'):
        next_url = '%(next)s?next=%(next)s' % {'next': next_url}

    login_form = forms.LoginForm(initial = {'next': next_url})

    #todo: get next url make it sticky if next is 'user_signin'
    if request.method == 'POST':

        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():

            provider_name = login_form.cleaned_data['login_provider_name']
            if login_form.cleaned_data['login_type'] == 'password':

                password_action = login_form.cleaned_data['password_action']
                if password_action == 'login':
                    user = authenticate(
                                username = login_form.cleaned_data['username'],
                                password = login_form.cleaned_data['password'],
                                provider_name = provider_name,
                                method = 'password'
                            )
                    if user is None:
                        login_form.set_password_login_error()
                    else:
                        login(request, user)
                        #todo: here we might need to set cookies
                        #for external login sites
                        return HttpResponseRedirect(next_url)
                elif password_action == 'change_password':
                    if request.user.is_authenticated():
                        new_password = login_form.cleaned_data['new_password']
                        AuthBackend.set_password(
                                        user=request.user,
                                        password=new_password,
                                        provider_name=provider_name
                                    )
                        request.user.message_set.create(
                                        message = _('Your new password saved')
                                    )
                        return HttpResponseRedirect(next_url)
                else:
                    logging.critical(
                        'unknown password action %s' % password_action
                    )
                    raise Http404

            elif login_form.cleaned_data['login_type'] == 'openid':
                #initiate communication process
                logging.debug('processing signin with openid submission')

                #todo: make a simple-use wrapper for openid protocol

                sreg_req = sreg.SRegRequest(optional=['nickname', 'email'])
                redirect_to = "%s%s?%s" % (
                        get_url_host(request),
                        reverse('user_complete_signin'), 
                        urllib.urlencode({'next':next_url})
                )
                return ask_openid(
                            request, 
                            login_form.cleaned_data['openid_url'],
                            redirect_to,
                            on_failure=signin_failure,
                            sreg_request=sreg_req
                        )

            elif login_form.cleaned_data['login_type'] == 'oauth':
                try:
                    #this url may need to have "next" piggibacked onto
                    callback_url = reverse('user_complete_oauth_signin')

                    connection = util.OAuthConnection(
                                        provider_name,
                                        callback_url = callback_url
                                    )

                    connection.start()

                    request.session['oauth_token'] = connection.get_token()
                    request.session['oauth_provider_name'] = provider_name
                    request.session['next_url'] = next_url#special case for oauth

                    oauth_url = connection.get_auth_url(login_only = False)
                    return HttpResponseRedirect(oauth_url)

                except util.OAuthError, e:
                    logging.critical(unicode(e))
                    msg = _('Unfortunately, there was some problem when '
                            'connecting to %(provider)s, please try again '
                            'or use another provider'
                        ) % {'provider': provider_name}
                    request.user.message_set.create(message = msg)

            elif login_form.cleaned_data['login_type'] == 'facebook':
                #have to redirect for consistency
                #there is a requirement that 'complete_signin'
                try:
                    #this call may raise FacebookError
                    user_id = util.get_facebook_user_id(request)

                    user = authenticate(
                                method = 'facebook',
                                facebook_user_id = user_id
                            )

                    return finalize_generic_signin(
                                    request = request,
                                    user = user,
                                    user_identifier = user_id,
                                    login_provider_name = 'facebook',
                                    redirect_url = next_url
                                )

                except util.FacebookError, e:
                    logging.critical(unicode(e))
                    msg = _('Unfortunately, there was some problem when '
                            'connecting to %(provider)s, please try again '
                            'or use another provider'
                        ) % {'provider': 'Facebook'}
                    request.user.message_set.create(message = msg)

            else:
                #raise 500 error - unknown login type
                pass
        else:
            logging.debug('login form is not valid')
            logging.debug(login_form.errors)
            logging.debug(request.REQUEST)

    if request.method == 'GET' and request.user.is_authenticated():
        view_subtype = 'change_openid'
    else:
        view_subtype = 'default'

    return show_signin_view(
                        request,
                        login_form = login_form,
                        view_subtype = view_subtype
                    )

def show_signin_view(
                request,
                login_form = None,
                account_recovery_form = None,
                account_recovery_message = None,
                sticky = False,
                view_subtype = 'default'
            ):
    """url-less utility function that populates
    context of template 'authopenid/signin.html'
    and returns its rendered output
    """

    allowed_subtypes = (
                    'default', 'add_openid', 
                    'email_sent', 'change_openid',
                    'bad_key'
                )

    assert(view_subtype in allowed_subtypes) 

    if sticky:
        next_url = reverse('user_signin')
    else:
        next_url = get_next_url(request)

    if login_form is None:
        login_form = forms.LoginForm(initial = {'next': next_url})
    if account_recovery_form is None:
        account_recovery_form = forms.AccountRecoveryForm()#initial = initial_data)

    #if request is GET
    if request.method == 'GET':
        logging.debug('request method was GET')

    #todo: this sthuff must be executed on some signal
    #because askbot should have nothing to do with the login app
    from askbot.models import AnonymousQuestion as AQ
    session_key = request.session.session_key
    logging.debug('retrieving anonymously posted question associated with session %s' % session_key)
    qlist = AQ.objects.filter(session_key=session_key).order_by('-added_at')
    if len(qlist) > 0:
        question = qlist[0]
    else:
        question = None

    from askbot.models import AnonymousAnswer as AA
    session_key = request.session.session_key
    logging.debug('retrieving posted answer associated with session %s' % session_key)
    alist = AA.objects.filter(session_key=session_key).order_by('-added_at')
    if len(alist) > 0:
        answer = alist[0]
    else:
        answer = None

    if request.user.is_authenticated():
        existing_login_methods = UserAssociation.objects.filter(user = request.user)

    if view_subtype == 'default':
        page_title = _('Please click any of the icons below to sign in')
    elif view_subtype == 'email_sent':
        page_title = _('Account recovery email sent')
    elif view_subtype == 'change_openid':
        if len(existing_login_methods) == 0:
            page_title = _('Please add one or more login methods.')
        else:
            page_title = _('If you wish, please add, remove or re-validate your login methods')
    elif view_subtype == 'add_openid':
        page_title = _('Please wait a second! Your account is recovered, but ...')
    elif view_subtype == 'bad_key':
        page_title = _('Sorry, this account recovery key has expired or is invalid')

    logging.debug('showing signin view')
    data = {
        'page_class': 'openid-signin',
        'view_subtype': view_subtype, #add_openid|default
        'page_title': page_title,
        'question':question,
        'answer':answer,
        'login_form': login_form,
        'account_recovery_form': account_recovery_form,
        'openid_error_message':  request.REQUEST.get('msg',''),
        'account_recovery_message': account_recovery_message,
    }

    major_login_providers = util.get_major_login_providers()
    minor_login_providers = util.get_minor_login_providers()

    active_provider_names = None
    if request.user.is_authenticated():
        data['existing_login_methods'] = existing_login_methods
        active_provider_names = [
                        item.provider_name for item in existing_login_methods
                    ] 

    util.set_login_provider_tooltips(
                        major_login_providers,
                        active_provider_names = active_provider_names
                    )
    util.set_login_provider_tooltips(
                        minor_login_providers,
                        active_provider_names = active_provider_names
                    )

    data['major_login_providers'] = major_login_providers.values()
    data['minor_login_providers'] = minor_login_providers.values()

    return render_to_response(
                'authopenid/signin.html',
                data,
                context_instance=RequestContext(request)
            )

@login_required
def delete_login_method(request):
    if request.is_ajax() and request.method == 'POST':
        provider_name = request.POST['provider_name']
        try:
            login_method = UserAssociation.objects.get(
                                                user = request.user,
                                                provider_name = provider_name
                                            )
            login_method.delete()
            return HttpResponse('', mimetype = 'application/json')
        except UserAssociation.DoesNotExist:
            #error response
            message = _('Login method %(provider_name)s does not exist')
            return HttpResponse(message, status=500, mimetype = 'application/json')
        except UserAssociation.MultipleObjectsReturned:
            logging.critical(
                    'have multiple %(provider)s logins for user %(id)s'
                ) % {'provider':provider_name, 'id': request.user.id}
            message = _('Sorry, there was some error, we will look at it')
            return HttpResponse(message, status=500, mimetype = 'application/json')
    else:
        raise Http404

def complete_signin(request):
    """ in case of complete signin with openid """
    logging.debug('')#blank log just for the trace
    return complete(
                request, 
                on_success = signin_success, 
                on_failure = signin_failure,
                return_to = get_url_host(request) + reverse('user_complete_signin')
            )

def signin_success(request, identity_url, openid_response):
    """
    this is not a view, has no url pointing to this

    this function is called when OpenID provider returns
    successful response to user authentication

    Does actual authentication in Django site and
    redirects to the registration page, if necessary
    or adds another login method.
    """

    logging.debug('')
    openid_data = util.from_openid_response(openid_response) #create janrain OpenID object
    request.session['openid'] = openid_data

    openid_url = str(openid_data)
    user = authenticate(
                    openid_url = openid_url,
                    method = 'openid'
                )

    next_url = get_next_url(request)
    provider_name = util.get_provider_name(openid_url)

    request.session['email'] = openid_data.sreg.get('email', '')
    request.session['username'] = openid_data.sreg.get('username', '')
    request.session['user_identifier'] = openid_url
    request.session['login_provider_name'] = provider_name

    return finalize_generic_signin(
                        request = request,
                        user = user,
                        user_identifier = openid_url,
                        login_provider_name = provider_name,
                        redirect_url = next_url
                    )

def finalize_generic_signin(
                    request = None, 
                    user = None,
                    login_provider_name = None,
                    user_identifier = None,
                    redirect_url = None
                ):
    """non-view function
    generic signin, run after all protocol-dependent details
    have been resolved
    """

    if request.user.is_authenticated():
        #this branch is for adding a new association
        if user is None:
            #register new association
            UserAssociation(
                user = request.user,
                provider_name = login_provider_name,
                openid_url = user_identifier,
                last_used_timestamp = datetime.datetime.now()
            ).save()
            return HttpResponseRedirect(redirect_url)

        elif user != request.user:
            #prevent theft of account by another pre-existing user
            logging.critical(
                    'possible account theft attempt by %s,%d to %s %d' % \
                    (
                        request.user.username,
                        request.user.id,
                        user.username,
                        user.id
                    )
                )
            logout(request)#log out current user
            login(request, user)#login freshly authenticated user
            return HttpResponseRedirect(redirect_url)
        else:
            #user just checks if another login still works
            msg = _('Your %(provider)s login works fine') % \
                    {'provider': login_provider_name}
            request.user.message_set.create(message = msg)
            return HttpResponseRedirect(redirect_url)
    else:
        if user is None:
            #need to register
            return register(request)
        else:
            #authentication branch
            login(request, user)
            logging.debug('login success')
            return HttpResponseRedirect(redirect_url)


def is_association_exist(openid_url):
    """ test if an openid is already in database """
    is_exist = True
    try:
        uassoc = UserAssociation.objects.get(openid_url__exact = openid_url)
    except UserAssociation.DoesNotExist:
        is_exist = False
    logging.debug(str(is_exist))
    return is_exist

@not_authenticated
def register(request, provider_name = None):
    """
    register view that processes
    new user registratioins using openid or oauth
    this function is also called directly from "signin_succes"
    
    If user is already a member he can associate their openid with 
    their account.
    
    A new account could also be created and automaticaly associated
    to the openid.
    
    url : /complete/
    
    template : authopenid/complete.html
    """
    
    logging.debug('')

    next_url = get_next_url(request)

    if 'login_provider_name' not in request.session \
        or 'user_identifier' not in request.session:
        logging.critical('illegal attempt to register')
        return HttpResponseRedirect(reverse('user_signin'))

    user = None
    is_redirect = False
    username = request.session.get('username', '')
    email = request.session.get('email', '')
    logging.debug('request method is %s' % request.method)

    register_form = forms.OpenidRegisterForm(
                initial={
                    'next': next_url,
                    'username': request.session.get('username', ''),
                    'email': request.session.get('email', ''),
                }
            )
    email_feeds_form = askbot_forms.SimpleEmailSubscribeForm()

    if request.method == 'POST':

        logging.debug('trying to create new account associated with openid')
        register_form = forms.OpenidRegisterForm(request.POST)
        email_feeds_form = askbot_forms.SimpleEmailSubscribeForm(request.POST)
        if not register_form.is_valid():
            logging.debug('OpenidRegisterForm is INVALID')
        elif not email_feeds_form.is_valid():
            logging.debug('SimpleEmailSubscribeForm is INVALID')
        else:
            logging.debug('OpenidRegisterForm and SimpleEmailSubscribeForm are valid')
            is_redirect = True
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']

            user = User.objects.create_user(username, email)
            
            logging.debug('creating new openid user association for %s')

            UserAssociation(
                openid_url = request.session['user_identifier'],
                user = user,
                provider_name = request.session['login_provider_name'],
                last_used_timestamp = datetime.datetime.now()
            ).save()

            del request.session['user_identifier']
            del request.session['login_provider_name']
            
            # login 
            logging.debug('logging the user in')

            user = authenticate(method = 'force', user_id = user.id)
            if user is None:
                raise Exception('this does not make any sense')

            user.backend = 'askbot.deps.django_authopenid.backends.AuthBackend'
            login(request, user)

            logging.debug('saving email feed settings')
            email_feeds_form.save(user)

        #check if we need to post a question that was added anonymously
        #this needs to be a function call becase this is also done
        #if user just logged in and did not need to create the new account
        
        if user != None:
            if askbot_settings.EMAIL_VALIDATION == True:
                logging.debug('sending email validation')
                send_new_email_key(user, nomessage=True)
                output = validation_email_sent(request)
                set_email_validation_message(user) #message set after generating view
                return output
            if user.is_authenticated():
                logging.debug('success, send user to main page')
                return HttpResponseRedirect(reverse('index'))
            else:
                logging.debug('have really strange error')
                raise Exception('openid login failed')#should not ever get here
    
    providers = {
            'yahoo':'<font color="purple">Yahoo!</font>',
            'flickr':'<font color="#0063dc">flick</font><font color="#ff0084">r</font>&trade;',
            'google':'Google&trade;',
            'aol':'<font color="#31658e">AOL</font>',
            'myopenid':'MyOpenID',
        }
    if provider_name not in providers:
        provider_logo = provider_name
        logging.error('openid provider named "%s" has no pretty customized logo' % provider_name)
    else:
        provider_logo = providers[provider_name]
    
    logging.debug('printing authopenid/complete.html output')
    return render_to_response(
                'authopenid/complete.html',
                {
                    'openid_register_form': register_form,
                    'email_feeds_form': email_feeds_form,
                    'provider':mark_safe(provider_logo),
                    'username': username,
                    'email': email,
                    'login_type':'openid',
                    'gravatar_faq_url':reverse('faq') + '#gravatar',
                }, 
                context_instance=RequestContext(request)
            )

def signin_failure(request, message):
    """
    falure with openid signin. Go back to signin page.
    """
    request.user.message_set.create(message = message)
    return show_signin_view(request)

@not_authenticated
@decorators.valid_password_login_provider_required
def signup_with_password(request):
    """Create a password-protected account
    template: authopenid/signup_with_password.html
    """

    next = get_next_url(request)
    #this is safe because second decorator cleans this field
    provider_name = request.REQUEST['login_provider']

    logging.debug('request method was %s' % request.method)
    if request.method == 'POST':
        form = forms.ClassicRegisterForm(request.POST)
        email_feeds_form = askbot_forms.SimpleEmailSubscribeForm(request.POST)
        
        #validation outside if to remember form values
        logging.debug('validating classic register form')
        form1_is_valid = form.is_valid()
        if form1_is_valid:
            logging.debug('classic register form validated')
        else:
            logging.debug('classic register form is not valid')
        form2_is_valid = email_feeds_form.is_valid()
        if form2_is_valid:
            logging.debug('email feeds form validated')
        else:
            logging.debug('email feeds form is not valid')
        if form1_is_valid and form2_is_valid:
            logging.debug('both forms are valid')
            next = form.cleaned_data['next']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            provider_name = form.cleaned_data['login_provider']
            
            User.objects.create_user(username, email, password)
            logging.debug('new user %s created' % username)
            if provider_name != 'local':
                raise NotImplementedError('must run create external user code')

            user = authenticate(
                        username = username,
                        password = password,
                        provider_name = provider_name,
                        method = 'password'
                    )

            login(request, user)
            logging.debug('new user logged in')
            email_feeds_form.save(user)
            logging.debug('email feeds form saved')
            
            # send email
            #subject = _("Welcome email subject line")
            #message_template = loader.get_template(
            #        'authopenid/confirm_email.txt'
            #)
            #message_context = Context({ 
            #    'signup_url': askbot_settings.APP_URL + reverse('user_signin'),
            #    'username': username,
            #    'password': password,
            #})
            #message = message_template.render(message_context)
            #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, 
            #        [user.email])
            #logging.debug('new password acct created, confirmation email sent!')
            return HttpResponseRedirect(next)
        else:
            #todo: this can be solved with a decorator, maybe
            form.initial['login_provider'] = provider_name
            logging.debug('create classic account forms were invalid')
    else:
        #todo: here we have duplication of get_password_login_provider...
        form = forms.ClassicRegisterForm(
                                initial={
                                    'next':next,
                                    'login_provider': provider_name
                                }
                            )
        email_feeds_form = askbot_forms.SimpleEmailSubscribeForm()
    logging.debug('printing legacy signup form')
    context_data = {
                'form': form, 
                'email_feeds_form': email_feeds_form 
            }
    return render_to_response(
                'authopenid/signup_with_password.html', 
                context_data,
                context_instance=RequestContext(request))
    #what if request is not posted?

@login_required
def signout(request):
    """
    signout from the website. Remove openid from session and kill it.

    url : /signout/"
    """
    logging.debug('')
    try:
        logging.debug('deleting openid session var')
        del request.session['openid']
    except KeyError:
        logging.debug('failed')
        pass
    logout(request)
    logging.debug('user logged out')
    return HttpResponseRedirect(get_next_url(request))
    
def xrdf(request):
    url_host = get_url_host(request)
    logging.debug('what does this do??')
    return_to = [
        "%s%s" % (url_host, reverse('user_complete_signin'))
    ]
    return render_to_response('authopenid/yadis.xrdf', { 
        'return_to': return_to 
        }, context_instance=RequestContext(request))

@login_required
def account_settings(request):
    """
    index pages to changes some basic account settings :
     - change password
     - change email
     - associate a new openid
     - delete account

    url : /

    template : authopenid/settings.html
    """
    logging.debug('')
    msg = request.GET.get('msg', '')
    is_openid = True

    try:
        uassoc = UserAssociation.objects.get(
                user__username__exact=request.user.username
        )
    except:
        is_openid = False


    return render_to_response('authopenid/settings.html', {
        'msg': msg,
        'is_openid': is_openid
        }, context_instance=RequestContext(request))

def find_email_validation_messages(user):
    msg_text = _('your email needs to be validated see %(details_url)s') \
        % {'details_url':reverse('faq') + '#validate'}
    return user.message_set.filter(message__exact=msg_text)

def set_email_validation_message(user):
    messages = find_email_validation_messages(user)
    msg_text = _('your email needs to be validated see %(details_url)s') \
        % {'details_url':reverse('faq') + '#validate'}
    if len(messages) == 0:
        user.message_set.create(message=msg_text)

def clear_email_validation_message(user):
    messages = find_email_validation_messages(user)
    messages.delete()

def set_new_email(user, new_email, nomessage=False):
    if new_email != user.email:
        user.email = new_email
        user.email_isvalid = False
        user.save()
        if askbot_settings.EMAIL_VALIDATION == True:
            send_new_email_key(user,nomessage=nomessage)

def _send_email_key(user):
    """private function. sends email containing validation key
    to user's email address
    """
    subject = _("Email verification subject line")
    message_template = loader.get_template('authopenid/email_validation.txt')
    import settings
    message_context = Context({
    'validation_link': askbot_settings.APP_URL + reverse(
                                                    'user_account_recover',
                                                    kwargs={'key':user.email_key}
                                                )
    })
    message = message_template.render(message_context)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def send_new_email_key(user,nomessage=False):
    import random
    random.seed()
    user.email_key = '%032x' % random.getrandbits(128) 
    user.save()
    _send_email_key(user)
    if nomessage==False:
        set_email_validation_message(user)

@login_required
def send_email_key(request):
    """
    url = /email/sendkey/

    view that is shown right after sending email key
    email sending is called internally

    raises 404 if email validation is off
    if current email is valid shows 'key_not_sent' view of 
    authopenid/changeemail.html template
    """

    if askbot_settings.EMAIL_VALIDATION == True:
        if request.user.email_isvalid:
            return render_to_response('authopenid/changeemail.html',
                            { 'email': request.user.email, 
                              'action_type': 'key_not_sent', 
                              'change_link': reverse('user_changeemail')},
                              context_instance=RequestContext(request)
                              )
        else:
            send_new_email_key(request.user)
            return validation_email_sent(request)
    else:
        raise Http404

def account_recover(request, key = None):
    """view similar to send_email_key, except
    it allows user to recover an account by entering
    his/her email address

    this view will both - send the recover link and
    process it

    url name 'user_account_recover'
    """
    if request.method == 'POST':
        form = forms.AccountRecoveryForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            send_new_email_key(user, nomessage = True)
            message = _(
                    'Please check your email and visit the enclosed link.'
                )
            return show_signin_view(
                            request,
                            account_recovery_message = message,
                            view_subtype = 'email_sent'
                        )
        else:
            return show_signin_view(
                            request,
                            account_recovery_form = form
                        )
    else:
        if key is None:
            return HttpResponseRedirect(reverse('user_signin'))

        user = authenticate(email_key = key, method = 'email')
        if user:
            if request.user.is_authenticated():
                if user != request.user:
                    logout(request.user)
                    login(request, user)
            else:
                login(request, user)
            #need to show "sticky" signin view here
            return show_signin_view(
                                request,
                                view_subtype = 'add_openid',
                                sticky = True
                            )
        else:
            return show_signin_view(request, view_subtype = 'bad_key')
   

#internal server view used as return value by other views
def validation_email_sent(request):
    logging.debug('')
    return render_to_response('authopenid/changeemail.html',
                    { 'email': request.user.email, 
                    'change_email_url': reverse('user_changeemail'),
                    'action_type': 'validate', }, 
                     context_instance=RequestContext(request))

def verifyemail(request,id=None,key=None):
    """
    view that is shown when user clicks email validation link
    url = /email/verify/{{user.id}}/{{user.email_key}}/
    """
    logging.debug('')
    if askbot.settings.EMAIL_VALIDATION == True:
        user = User.objects.get(id=id)
        if user:
            if user.email_key == key:
                user.email_isvalid = True
                clear_email_validation_message(user)
                user.save()
                return render_to_response('authopenid/changeemail.html', {
                    'action_type': 'validation_complete',
                    }, context_instance=RequestContext(request))
            else:
                logging.error('hmm, no user found for email validation message - foul play?')
    raise Http404

@login_required
def changeemail(request, action='change'):
    """ 
    changeemail view. requires openid with request type GET

    url: /email/*

    template : authopenid/changeemail.html
    """
    logging.debug('')
    msg = request.GET.get('msg', None)
    extension_args = {}
    user_ = request.user

    if request.POST:
        if 'cancel' in request.POST:
            msg = _('your email was not changed')
            request.user.message_set.create(message=msg)
            return HttpResponseRedirect(get_next_url(request))
        form = forms.ChangeEmailForm(request.POST, user=user_)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            if new_email != user_.email:
                if askbot_settings.EMAIL_VALIDATION == True:
                    action = 'validate'
                else:
                    action = 'done_novalidate'
                set_new_email(user_, new_email,nomessage=True)
            else:
                action = 'keep'

    elif not request.POST and 'openid.mode' in request.GET:
        redirect_to = get_url_host(request) + reverse('user_changeemail')
        return complete(
                    request,
                    on_success = emailopenid_success,
                    on_failure = emailopenid_failure,
                    return_to = redirect_to
                )
    else:
        form = forms.ChangeEmailForm(initial={'email': user_.email},
                user=user_)
    
    output = render_to_response('authopenid/changeemail.html', {
        'form': form,
        'email': user_.email,
        'action_type': action,
        'gravatar_faq_url': reverse('faq') + '#gravatar',
        'change_email_url': reverse('user_changeemail'),
        'msg': msg 
        }, context_instance=RequestContext(request))

    if action == 'validate':
        set_email_validation_message(user_)

    return output

def emailopenid_success(request, identity_url, openid_response):
    logging.debug('')
    openid_ = util.from_openid_response(openid_response)

    user_ = request.user
    try:
        uassoc = UserAssociation.objects.get(
                openid_url__exact=identity_url
        )
    except:
        return emailopenid_failure(request, 
                _("No OpenID %s found associated in our database" % identity_url))

    if uassoc.user.username != request.user.username:
        return emailopenid_failure(request, 
                _("The OpenID %s isn't associated to current user logged in" % 
                    identity_url))
    
    new_email = request.session.get('new_email', '')
    if new_email:
        user_.email = new_email
        user_.save()
        del request.session['new_email']
    msg = _("Email Changed.")

    redirect = "%s?msg=%s" % (reverse('user_account_settings'),
            urlquote_plus(msg))
    return HttpResponseRedirect(redirect)
    

def emailopenid_failure(request, message):
    logging.debug('')
    redirect_to = "%s?msg=%s" % (
            reverse('user_changeemail'), urlquote_plus(message))
    return HttpResponseRedirect(redirect_to)
 
@login_required
def changeopenid(request):
    """
    change openid view. Allow user to change openid 
    associated to its username.

    url : /changeopenid/

    template: authopenid/changeopenid.html
    """
    logging.error('change openid view - never tested it yet!!!')

    extension_args = {}
    openid_url = ''
    has_openid = True
    msg = request.GET.get('msg', '')
        
    user_ = request.user

    try:
        uopenid = UserAssociation.objects.get(user=user_)
        openid_url = uopenid.openid_url
    except:
        has_openid = False
    
    redirect_to = get_url_host(request) + reverse('user_changeopenid')
    if request.POST and has_openid:
        form = forms.ChangeopenidForm(request.POST, user=user_)
        if form.is_valid():
            return ask_openid(request, form.cleaned_data['openid_url'],
                    redirect_to, on_failure=changeopenid_failure)
    elif not request.POST and has_openid:
        if 'openid.mode' in request.GET:
            return complete(
                        request,
                        on_success = changeopenid_success,
                        on_failure = changeopenid_failure,
                        return_to = redirect_to
                    )    

    form = forms.ChangeopenidForm(initial={'openid_url': openid_url }, user=user_)
    return render_to_response('authopenid/changeopenid.html', {
        'form': form,
        'has_openid': has_openid, 
        'msg': msg 
        }, context_instance=RequestContext(request))

def changeopenid_success(request, identity_url, openid_response):
    logging.error('never tested this worflow')
    openid_ = util.from_openid_response(openid_response)
    is_exist = True
    try:
        uassoc = UserAssociation.objects.get(openid_url__exact=identity_url)
    except:
        is_exist = False
        
    if not is_exist:
        try:
            uassoc = UserAssociation.objects.get(
                    user__username__exact=request.user.username
            )
            uassoc.openid_url = identity_url
            uassoc.save()
        except:
            uassoc = UserAssociation(user=request.user, 
                    openid_url=identity_url)
            uassoc.save()
    elif uassoc.user.username != request.user.username:
        return changeopenid_failure(request, 
                _('This OpenID is already associated with another account.'))

    request.session['openids'] = []
    request.session['openids'].append(openid_)

    msg = _("OpenID %s is now associated with your account." % identity_url) 
    redirect = "%s?msg=%s" % (
            reverse('user_account_settings'), 
            urlquote_plus(msg))
    return HttpResponseRedirect(redirect)
    

def changeopenid_failure(request, message):
    logging.error('never tested this workflow')
    redirect_to = "%s?msg=%s" % (
            reverse('user_changeopenid'), 
            urlquote_plus(message))
    return HttpResponseRedirect(redirect_to)
  
@login_required
def delete(request):
    """
    delete view. Allow user to delete its account. Password/openid are required to 
    confirm it. He should also check the confirm checkbox.
    
    url : /delete
    
    template : authopenid/delete.html
    """
    logging.error('deleting account - never tested this')
    
    extension_args = {}
    
    user_ = request.user
    
    redirect_to = get_url_host(request) + reverse('user_delete') 
    if request.POST:
        form = forms.DeleteForm(request.POST, user=user_)
        if form.is_valid():
            if not form.test_openid:
                user_.delete() 
                return signout(request)
            else:
                return ask_openid(request, form.cleaned_data['password'],
                        redirect_to, on_failure=deleteopenid_failure)
    elif not request.POST and 'openid.mode' in request.GET:
        return complete(
                    request,
                    on_success = deleteopenid_success,
                    on_failure = deleteopenid_failure,
                    return_to = redirect_to
                )
    
    form = forms.DeleteForm(user=user_)
    
    msg = request.GET.get('msg','')
    return render_to_response('authopenid/delete.html', {
        'form': form, 
        'msg': msg, 
        }, context_instance=RequestContext(request))

def deleteopenid_success(request, identity_url, openid_response):
    logging.error('never tested this')
    openid_ = util.from_openid_response(openid_response)

    user_ = request.user
    try:
        uassoc = UserAssociation.objects.get(
                openid_url__exact=identity_url
        )
    except:
        return deleteopenid_failure(request,
                _("No OpenID %s found associated in our database" % identity_url))

    if uassoc.user.username == user_.username:
        user_.delete()
        return signout(request)
    else:
        return deleteopenid_failure(request,
                _("The OpenID %s isn't associated to current user logged in" % 
                    identity_url))
    
    msg = _("Account deleted.") 
    redirect = reverse('index') + u"/?msg=%s" % (urlquote_plus(msg))
    return HttpResponseRedirect(redirect)
    

def deleteopenid_failure(request, message):
    logging.error('never tested this')
    redirect_to = "%s?msg=%s" % (reverse('user_delete'), urlquote_plus(message))
    return HttpResponseRedirect(redirect_to)

def external_legacy_login_info(request):
    logging.debug('maybe this view does not belong in this library')
    feedback_url = reverse('feedback')
    return render_to_response('authopenid/external_legacy_login_info.html', 
                    {'feedback_url':feedback_url}, 
                    context_instance=RequestContext(request))
