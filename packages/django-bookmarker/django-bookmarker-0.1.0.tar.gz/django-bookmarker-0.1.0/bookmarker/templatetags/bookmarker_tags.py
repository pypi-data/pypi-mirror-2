from copy import copy

from django import template
from django.utils.http import urlquote

from bookmarker.settings import DESCRIPTIONS, SERVICES

register = template.Library()

@register.inclusion_tag('bookmarker/links.html')
def bookmark_links(url, title):
    url = urlquote(url) 
    title = urlquote(title)

    services = []
    for name in SERVICES:
        try:
            service = copy(DESCRIPTIONS[name])
        except KeyError:
            raise Exception('Unknown service: %s' % name)
        service['url'] %= {'url': url, 'title': title}
        services.append(service)

    return {'url': url,
            'title': title,
            'services': services,
            }
