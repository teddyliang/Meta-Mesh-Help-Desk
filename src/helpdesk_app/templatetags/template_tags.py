from django import template
register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.simple_tag
def get_company_name(value):
    if value == "long":
        return "Community Internet Solutions"
    else:
        return "CIS"


def categories_display(resource):
    categories = list(resource.categories.all())
    if len(categories) > 0:
        return ', '.join(map(str, categories))
    else:
        return 'None'


register.filter('categories_display', categories_display)
