from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Define default settings

DESCRIPTIONS = {
    'delicious': {
        'url': 'http://del.icio.us/post?v=5&noui&url=%(url)s&title=%(title)s',
        'title': _('Delicious'),
        'image': 'http://delicious.com/favicon.ico',
    },
    'reddit': {
        'url': 'http://reddit.com/submit?url=%(url)s&title=%(title)s',
        'title': _('Reddit'),
        'image': 'http://www.reddit.com/favicon.ico',
    },
    'digg': {
        'url': 'http://digg.com/submit?url=%(url)s',
        'title': _('Digg'),
        'image': 'http://digg.com/favicon.ico',
    },
    'google': {
        'url': 'http://www.google.com/bookmarks/mark?op=add&title=&bkmk=%(url)s&labels=&annotation=%(title)s',
        'title': _('Google'),
        'image': 'https://www.google.com/bookmarks/api/static/images/favicon.ico',
    },
    'yandex': {
        'url': 'http://zakladki.yandex.ru/userarea/links/addfromfav.asp?bAddLink_x=1&lurl=%(url)s&lname=%(title)s',
        'title': _('Yandex'),
        'image': 'http://zakladki.yandex.ru/favicon.ico',
    },
    'bobrdobr': {
        'title': ('Bobrdobr'),
        'url': 'http://www.bobrdobr.ru/addext.html?url=%(url)s&title=%(title)s',
        'image': 'http://static.bobrdobr.ru/img/favicon.ico',
    },
}

SERVICES = ['delicious', 'digg', 'google', 'yandex', 'bobrdobr']

# Load custom settings

if hasattr(settings, 'BOOKMARKER_DESCRIPTIONS'):
    DESCRIPTIONS.update(settings.BOOKMARKER_DESCRIPTIONS)

if hasattr(settings, 'BOOKMARKER_SERVICES'):
    SERVICES = settings.BOOKMARKER_SERVICES
