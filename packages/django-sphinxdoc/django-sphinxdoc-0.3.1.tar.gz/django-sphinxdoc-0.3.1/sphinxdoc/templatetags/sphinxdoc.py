# encoding: utf-8

from django.template import Library

from sphinxdoc.forms import SearchForm


register = Library()

@register.inclusion_tag('sphinxdoc/search_form.html', takes_context=True)
def search_form(context, search_form_id='search'):
    request = context['request']
    auto_id = 'id_%s_%%s' % search_form_id
    return {
        'form': SearchForm(initial=request.GET, auto_id=auto_id),
        'search_form_id': search_form_id,
        'action': context['search'],
    }
