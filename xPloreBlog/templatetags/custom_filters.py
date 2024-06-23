from django import template
import hashlib
import urllib

register = template.Library()


@register.filter
def truncatechars_filled(value, arg):
    """
    Truncates a string after a certain number of characters and fills remaining space with gaps.
    Usage: {{ value|truncatechars_filled:50 }}
    """
    try:
        length = int(arg)
    except ValueError:
        return value  # Invalid argument, return the original string

    if len(value) > length:
        return value[:length] + '...'
    else:
        return value + ' ' * (length - len(value))


@register.filter(name='get_avatar_url')
def get_avatar_url(email='appstechemail@gmail.com', size=40):
    default = "https://example.com/static/images/defaultavatar.jpg"
    return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower().encode('utf-8')).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))
