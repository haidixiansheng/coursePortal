try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url
from haystack.views import SearchView, search_view_factory, FacetedSearchView
from haystack.query import SearchQuerySet
from haystack.forms import AutocompleteModelSearchForm, FacetedSearchForm
from web.views.home import base_category

sqs = SearchQuerySet().facet('ClassAuthor')

urlpatterns = patterns('haystack.views',
    #url(r'^$', SearchView(), name='haystack_simple_search'),
    #url(r'^auto/', search_view_factory(view_class=SearchView,template='search/autoComplete.html',form_class=AutocompleteModelSearchForm), name='haystack_auto_search'),
    url(r'^$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
    
)

