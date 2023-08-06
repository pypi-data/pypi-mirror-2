# encoding:utf-8
"""
:synopsis: views diplaying and processing main content post forms

This module contains views that allow adding, editing, and deleting main textual content.
"""
import os.path
import time
import datetime
import random
import logging
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils import simplejson
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.core import exceptions
from django.conf import settings

from askbot import auth
from askbot.views.readers import _get_tags_cache_json
from askbot import forms
from askbot import models
from askbot.skins.loaders import ENV
from askbot.utils.decorators import ajax_only
from askbot.templatetags.extra_tags import diff_date
from askbot.templatetags import extra_filters_jinja as template_filters

# used in index page
INDEX_PAGE_SIZE = 20
INDEX_AWARD_SIZE = 15
INDEX_TAGS_SIZE = 100
# used in tags list
DEFAULT_PAGE_SIZE = 60
# used in questions
QUESTIONS_PAGE_SIZE = 10
# used in answers
ANSWERS_PAGE_SIZE = 10

def upload(request):#ajax upload file to a question or answer 
    """view that handles file upload via Ajax
    """

    f = request.FILES['file-upload']
    # check upload permission
    result = ''
    error = ''
    new_file_name = ''
    try:
        #may raise exceptions.PermissionDenied
        if request.user.is_anonymous():
            msg = _('Sorry, anonymous users cannot upload files')
            raise exceptions.PermissionDenied(msg)

        request.user.assert_can_upload_file()

        # check file type
        file_extension = os.path.splitext(f.name)[1].lower()
        if not file_extension in settings.ASKBOT_ALLOWED_UPLOAD_FILE_TYPES:
            file_types = "', '".join(settings.ASKBOT_ALLOWED_UPLOAD_FILE_TYPES)
            msg = _("allowed file types are '%(file_types)s'") % \
                    {'file_types': file_types}
            raise exceptions.PermissionDenied(msg)

        # generate new file name
        new_file_name = str(
                            time.time()
                        ).replace(
                            '.', 
                            str(random.randint(0,100000))
                        ) + file_extension

        file_storage = FileSystemStorage(
                    location = settings.ASKBOT_FILE_UPLOAD_DIR,
                    base_url = reverse('uploaded_file', kwargs = {'path':''}),
                )
        # use default storage to store file
        file_storage.save(new_file_name, f)
        # check file size
        # byte
        size = file_storage.size(new_file_name)
        if size > settings.ASKBOT_MAX_UPLOAD_FILE_SIZE:
            file_storage.delete(new_file_name)
            msg = _("maximum upload file size is %(file_size)sK") % \
                    {'file_size': settings.ASKBOT_MAX_UPLOAD_FILE_SIZE}
            raise exceptions.PermissionDenied(msg)

    except exceptions.PermissionDenied, e:
        error = unicode(e)
    except Exception, e:
        logging.critical(unicode(e))
        error = _('Error uploading file. Please contact the site administrator. Thank you.')

    if error == '':
        result = 'Good'
        file_url = file_storage.url(new_file_name)
    else:
        result = ''
        file_url = ''

    #<result><msg><![CDATA[%s]]></msg><error><![CDATA[%s]]></error><file_url>%s</file_url></result>
    xml_template = "<result><msg><![CDATA[%s]]></msg><error><![CDATA[%s]]></error><file_url>%s</file_url></result>"
    xml = xml_template % (result, error, file_url)

    return HttpResponse(xml, mimetype="application/xml")

#@login_required #actually you can post anonymously, but then must register
def ask(request):#view used to ask a new question
    """a view to ask a new question
    gives space for q title, body, tags and checkbox for to post as wiki

    user can start posting a question anonymously but then
    must login/register in order for the question go be shown
    """

    if request.method == "POST":
        form = forms.AskForm(request.POST)
        if form.is_valid():

            timestamp = datetime.datetime.now()
            #todo: move this to clean_title
            title = form.cleaned_data['title'].strip()
            wiki = form.cleaned_data['wiki']
            #todo: move this to clean_tagnames
            tagnames = form.cleaned_data['tags'].strip()
            text = form.cleaned_data['text']

            if request.user.is_authenticated():

                try:
                    question = request.user.post_question(
                                                    title = title,
                                                    body_text = text,
                                                    tags = tagnames,
                                                    wiki = wiki,
                                                    timestamp = timestamp
                                                )
                    return HttpResponseRedirect(question.get_absolute_url())
                except exceptions.PermissionDenied, e:
                    request.user.message_set.create(message = unicode(e))
                    return HttpResponseRedirect(reverse('index'))

            else:
                request.session.flush()
                session_key = request.session.session_key
                summary = strip_tags(text)[:120]
                question = models.AnonymousQuestion(
                    session_key = session_key,
                    title       = title,
                    tagnames = tagnames,
                    wiki = wiki,
                    text = text,
                    summary = summary,
                    added_at = timestamp,
                    ip_addr = request.META['REMOTE_ADDR'],
                )
                question.save()
                return HttpResponseRedirect(reverse('user_signin_new_question'))
    else:
        #this branch is for the initial load of ask form
        form = forms.AskForm()
        if 'title' in request.GET:
            #normally this title is inherited from search query
            #but it is possible to ask with a parameter title in the url query
            form.initial['title'] = request.GET['title']
        else:
            #attempt to extract title from previous search query
            search_state = request.session.get('search_state',None)
            if search_state:
                query = search_state.query
                form.initial['title'] = query

    tags = _get_tags_cache_json()
    template = ENV.get_template('ask.html')
    data = {
        'active_tab': 'ask',
        'form' : form,
        'tags' : tags,
        'email_validation_faq_url':reverse('faq') + '#validate',
    }
    context = RequestContext(request, data)
    return HttpResponse(template.render(context))

@login_required
def retag_question(request, id):
    """retag question view
    """
    question = get_object_or_404(models.Question, id = id)

    try:
        request.user.assert_can_retag_question(question)
        if request.method == 'POST':
            form = forms.RetagQuestionForm(question, request.POST)
            if form.is_valid():
                if form.has_changed():
                    request.user.retag_question(
                                        question = question,
                                        tags = form.cleaned_data['tags']
                                    )
                if request.is_ajax():
                    response_data = {'success': True}
                    data = simplejson.dumps(response_data)
                    return HttpResponse(data, mimetype="application/json")
                else:
                    return HttpResponseRedirect(question.get_absolute_url())
            elif request.is_ajax():
                response_data = {
                    'message': unicode(form.errors['tags']),
                    'success': False
                }
                data = simplejson.dumps(response_data)
                return HttpResponse(data, mimetype="application/json")
        else:
            form = forms.RetagQuestionForm(question)

        data = {
            'active_tab': 'questions',
            'question': question,
            'form' : form,
            'tags' : _get_tags_cache_json(),
        }
        context = RequestContext(request, data)
        template = ENV.get_template('question_retag.html')
        return HttpResponse(template.render(context))
    except exceptions.PermissionDenied, e:
        if request.is_ajax():
            response_data = {
                'message': unicode(e),
                'success': False
            }
            data = simplejson.dumps(response_data)
            return HttpResponse(data, mimetype="application/json")
        else:
            request.user.message_set.create(message = unicode(e))
            return HttpResponseRedirect(question.get_absolute_url())

@login_required
def edit_question(request, id):
    """edit question view
    """
    question = get_object_or_404(models.Question, id = id)
    latest_revision = question.get_latest_revision()
    revision_form = None
    try:
        request.user.assert_can_edit_question(question)
        if request.method == 'POST':
            if 'select_revision' in request.POST:#revert-type edit
                # user has changed revistion number
                revision_form = forms.RevisionForm(question, latest_revision, request.POST)
                if revision_form.is_valid():
                    # Replace with those from the selected revision
                    form = forms.EditQuestionForm(question,
                        models.QuestionRevision.objects.get(question=question,
                            revision=revision_form.cleaned_data['revision']))
                else:
                    form = forms.EditQuestionForm(question, latest_revision, request.POST)
            else:#new content edit
                # Always check modifications against the latest revision
                form = forms.EditQuestionForm(question, latest_revision, request.POST)
                if form.is_valid():
                    if form.has_changed():
                        request.user.edit_question(
                                            question = question,
                                            title = form.cleaned_data['title'],
                                            body_text = form.cleaned_data['text'],
                                            revision_comment = form.cleaned_data['summary'],
                                            tags = form.cleaned_data['tags'],
                                            wiki = form.cleaned_data.get('wiki', question.wiki)
                                        )
                    return HttpResponseRedirect(question.get_absolute_url())
        else:
            revision_form = forms.RevisionForm(question, latest_revision)
            form = forms.EditQuestionForm(question, latest_revision)

        data = {
            'active_tab': 'questions',
            'question': question,
            'revision_form': revision_form,
            'form' : form,
            'tags' : _get_tags_cache_json()
        }
        context = RequestContext(request, data)
        template = ENV.get_template('question_edit.html')
        return HttpResponse(template.render(context))

    except exceptions.PermissionDenied, e:
        request.user.message_set.create(message = unicode(e))
        return HttpResponseRedirect(question.get_absolute_url())

@login_required
def edit_answer(request, id):
    answer = get_object_or_404(models.Answer, id=id)
    try:
        request.user.assert_can_edit_answer(answer)
        latest_revision = answer.get_latest_revision()
        if request.method == "POST":
            if 'select_revision' in request.POST:
                # user has changed revistion number
                revision_form = forms.RevisionForm(
                                                answer, 
                                                latest_revision,
                                                request.POST
                                            )
                if revision_form.is_valid():
                    # Replace with those from the selected revision
                    rev = revision_form.cleaned_data['revision']
                    selected_revision = models.AnswerRevision.objects.get(
                                                            answer = answer,
                                                            revision = rev
                                                        )
                    form = forms.EditAnswerForm(answer, selected_revision)
                else:
                    form = forms.EditAnswerForm(
                                            answer,
                                            latest_revision,
                                            request.POST
                                        )
            else:
                form = forms.EditAnswerForm(answer, latest_revision, request.POST)
                if form.is_valid():
                    if form.has_changed():
                        request.user.edit_answer(
                                answer = answer,
                                body_text = form.cleaned_data['text'],
                                revision_comment = form.cleaned_data['summary'],
                                wiki = form.cleaned_data.get('wiki', answer.wiki),
                                #todo: add wiki field to form
                            )
                    return HttpResponseRedirect(answer.get_absolute_url())
        else:
            revision_form = forms.RevisionForm(answer, latest_revision)
            form = forms.EditAnswerForm(answer, latest_revision)
        template = ENV.get_template('answer_edit.html')
        data = {
            'active_tab': 'questions',
            'answer': answer,
            'revision_form': revision_form,
            'form': form,
        }
        context = RequestContext(request, data)
        return HttpResponse(template.render(context))

    except exceptions.PermissionDenied, e:
        request.user.message_set.create(message = unicode(e))
        return HttpResponseRedirect(answer.get_absolute_url())

#todo: rename this function to post_new_answer
def answer(request, id):#process a new answer
    """view that posts new answer

    anonymous users post into anonymous storage
    and redirected to login page

    authenticated users post directly
    """
    question = get_object_or_404(models.Question, id=id)
    if request.method == "POST":
        form = forms.AnswerForm(question, request.user, request.POST)
        if form.is_valid():
            wiki = form.cleaned_data['wiki']
            text = form.cleaned_data['text']
            update_time = datetime.datetime.now()

            if request.user.is_authenticated():
                try:
                    follow = form.cleaned_data['email_notify']
                    answer = request.user.post_answer(
                                        question = question,
                                        body_text = text,
                                        follow = follow,
                                        wiki = wiki,
                                        timestamp = update_time,
                                    )
                    return HttpResponseRedirect(answer.get_absolute_url())
                except exceptions.PermissionDenied, e:
                    request.user.message_set.create(message = unicode(e))
            else:
                request.session.flush()
                anon = models.AnonymousAnswer(
                                       question=question,
                                       wiki=wiki,
                                       text=text,
                                       summary=strip_tags(text)[:120],
                                       session_key=request.session.session_key,
                                       ip_addr=request.META['REMOTE_ADDR'],
                                       )
                anon.save()
                return HttpResponseRedirect(reverse('user_signin_new_answer'))

    return HttpResponseRedirect(question.get_absolute_url())

def __generate_comments_json(obj, user):#non-view generates json data for the post comments
    """non-view generates json data for the post comments
    """
    comments = obj.comments.all().order_by('id')
    # {"Id":6,"PostId":38589,"CreationDate":"an hour ago","Text":"hello there!","UserDisplayName":"Jarrod Dixon","UserUrl":"/users/3/jarrod-dixon","DeleteUrl":null}
    json_comments = []
    for comment in comments:

        if user != None and user.is_authenticated():
            try:
                user.assert_can_delete_comment(comment)
                #/posts/392845/comments/219852/delete
                #todo translate this url
                is_deletable = True
            except exceptions.PermissionDenied:
                is_deletable = False
            is_editable = template_filters.can_edit_comment(comment.user, comment)
        else:
            is_deletable = False
            is_editable = False


        comment_owner = comment.get_owner()
        json_comments.append({'id' : comment.id,
            'object_id': obj.id,
            'comment_age': diff_date(comment.added_at),
            'html': comment.html,
            'user_display_name': comment_owner.username,
            'user_url': comment_owner.get_profile_url(),
            'user_id': comment_owner.id,
            'is_deletable': is_deletable,
            'is_editable': is_editable,
        })

    data = simplejson.dumps(json_comments)
    return HttpResponse(data, mimetype="application/json")

def post_comments(request):#non-view generic ajax handler to load comments to an object
    # only support get post comments by ajax now
    user = request.user
    if request.is_ajax():
        post_type = request.REQUEST['post_type']
        id = request.REQUEST['post_id']
        if post_type == 'question':
            post_model = models.Question
        elif post_type == 'answer':
            post_model = models.Answer
        else:
            raise Http404

        obj = get_object_or_404(post_model, id=id)
        if request.method == "GET":
            response = __generate_comments_json(obj, user)
        elif request.method == "POST":
            try:
                if user.is_anonymous():
                    msg = _('Sorry, you appear to be logged out and '
                            'cannot post comments. Please '
                            '<a href="%(sign_in_url)s">sign in</a>.') % \
                            {'sign_in_url': reverse('user_signin')}
                    raise exceptions.PermissionDenied(msg)
                user.post_comment(
                            parent_post = obj,
                            body_text = request.POST.get('comment')
                        )
                response = __generate_comments_json(obj, user)
            except exceptions.PermissionDenied, e:
                response = HttpResponseForbidden(
                                        unicode(e),
                                        mimetype="application/json"
                                    )
        return response
    else:
        raise Http404

@ajax_only
def edit_comment(request):
    if request.user.is_authenticated():
        comment_id = int(request.POST['comment_id'])
        comment = models.Comment.objects.get(id = comment_id)

        request.user.edit_comment(
                        comment = comment,
                        body_text = request.POST['comment']
                    )

        is_deletable = template_filters.can_delete_comment(comment.user, comment)
        is_editable = template_filters.can_edit_comment(comment.user, comment)

        return {'id' : comment.id,
            'object_id': comment.content_object.id,
            'comment_age': diff_date(comment.added_at),
            'html': comment.html,
            'user_display_name': comment.user.username,
            'user_url': comment.user.get_profile_url(),
            'user_id': comment.user.id,
            'is_deletable': is_deletable,
            'is_editable': is_editable,
        }
    else:
        raise exceptions.PermissionDenied(
                _('Sorry, anonymous users cannot edit comments')
            )

def delete_comment(request):
    """ajax handler to delete comment
    """
    try:
        if request.user.is_anonymous():
            msg = _('Sorry, you appear to be logged out and '
                    'cannot delete comments. Please '
                    '<a href="%(sign_in_url)s">sign in</a>.') % \
                    {'sign_in_url': reverse('user_signin')}
            raise exceptions.PermissionDenied(msg)
        if request.is_ajax():

            comment_id = request.POST['comment_id']
            comment = get_object_or_404(models.Comment, id=comment_id)
            request.user.assert_can_delete_comment(comment)

            obj = comment.content_object
            #todo: are the removed comments actually deleted?
            obj.comments.remove(comment)
            #attn: recalc denormalized field
            obj.comment_count = obj.comment_count - 1
            obj.save()

            return __generate_comments_json(obj, request.user)

        raise exceptions.PermissionDenied(
                    _('sorry, we seem to have some technical difficulties')
                )
    except exceptions.PermissionDenied, e:
        return HttpResponseForbidden(
                    unicode(e),
                    mimetype = 'application/json'
                )
