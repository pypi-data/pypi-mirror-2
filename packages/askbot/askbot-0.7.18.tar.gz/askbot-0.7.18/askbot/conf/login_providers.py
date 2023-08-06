"""
External service key settings
"""
from askbot.conf.settings_wrapper import settings
from askbot.deps import livesettings
from django.utils.translation import ugettext as _
from django.conf import settings as django_settings

LOGIN_PROVIDERS = livesettings.ConfigurationGroup(
                    'LOGIN_PROVIDERS',
                    _('Login provider setings')
                )

settings.register(
    livesettings.BooleanValue(
        LOGIN_PROVIDERS,
        'PASSWORD_REGISTER_SHOW_PROVIDER_BUTTONS',
        default = True,
        description=_('Show alternative login provider buttons on the password "Sign Up" page'),
    )
)

settings.register(
    livesettings.BooleanValue(
        LOGIN_PROVIDERS,
        'SIGNIN_ALWAYS_SHOW_LOCAL_LOGIN',
        default = False,
        description=_('Always display local login form and hide "Askbot" button.'),
    )
)

providers = (
    'local',
    'AOL',
    'Blogger',
    'ClaimID',
    'Facebook',
    'Flickr',
    'Google',
    'Twitter',
    'LinkedIn',
    'LiveJournal',
    #'myOpenID',
    'OpenID',
    'Technorati',
    'Wordpress',
    'Vidoop',
    'Verisign',
    'Yahoo',
    'identi.ca',
)

need_extra_setup = ('Twitter', 'Facebook', 'LinkedIn', 'identi.ca',)

for provider in providers:
    kwargs = {
        'description': _('Activate %(provider)s login') % {'provider': provider},
        'default': True,
    }
    if provider in need_extra_setup:
        kwargs['help_text'] = _(
            'Note: to really enable %(provider)s login '
            'some additional parameters will need to be set '
            'in the "External keys" section'
        ) % {'provider': provider}

    setting_name = 'SIGNIN_%s_ENABLED' % provider.upper()
    settings.register(
        livesettings.BooleanValue(
            LOGIN_PROVIDERS,
            setting_name,
            **kwargs
        )
    )
