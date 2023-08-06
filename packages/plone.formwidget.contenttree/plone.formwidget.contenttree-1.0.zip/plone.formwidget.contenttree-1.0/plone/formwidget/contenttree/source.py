from Acquisition.interfaces import IAcquirer
from zope.interface import implements
from zope.component import getMultiAdapter

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm

from zope.app.component.hooks import getSite

from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.vocabularies.catalog import parse_query

from Products.CMFCore.utils import getToolByName
from Products.ZCTextIndex.ParseTree import ParseError

from plone.formwidget.contenttree.interfaces import IContentSource
from plone.formwidget.contenttree.interfaces import IContentFilter


class CustomFilter(object):
    """A filter that can be used to test simple values in brain metadata and
    indexes.

    Limitations:

    - Will probably only work on FieldIndex, KeywordIndex and PathIndex indexes
    """
    implements(IContentFilter)

    def __init__(self, **kw):
        self.criteria = {}
        for key, value in kw.items():
            if (not isinstance(value, (list, tuple, set, frozenset)) and
                not key == 'path'):
                self.criteria[key] = [value]
            elif isinstance(value, (set, frozenset)):
                self.criteria[key] = list(value)
            else:
                self.criteria[key] = value

    def __call__(self, brain, index_data):
        for key, value in self.criteria.items():
            test_value = index_data.get(key, None)
            if test_value is not None:
                if (not isinstance(test_value, (list, tuple, set, frozenset))
                    and not key == 'path'):
                    test_value = set([test_value])
                elif isinstance(value, (list, tuple)):
                    test_value = set(test_value)
                if key == 'path':
                    if not test_value.startswith(value['query']):
                        return False
                elif not test_value.intersection(value):
                    return False
        return True


class PathSource(object):
    implements(IContentSource)

    def __init__(self, context, selectable_filter, navigation_tree_query=None):
        self.context = context

        query_builder = getMultiAdapter((context, self),
                                        INavigationQueryBuilder)
        query = query_builder()

        if navigation_tree_query is None:
            navigation_tree_query = {}

        # Copy path from selectable_filter into the navigation_tree_query
        # normally it does not make sense to show elements that wouldn't be
        # selectable anyway and are unneeded to navigate to selectable items
        if ('path' not in navigation_tree_query and
            'path' in selectable_filter.criteria):
            navigation_tree_query['path'] = selectable_filter.criteria['path']

        query.update(navigation_tree_query)

        self.navigation_tree_query = query
        self.selectable_filter = selectable_filter

        self.catalog = getToolByName(context, "portal_catalog")

        portal_tool = getToolByName(context, "portal_url")
        self.portal_path = portal_tool.getPortalPath()

    # Tokenised vocabulary API

    def __iter__(self):
        return [].__iter__()

    def __contains__(self, value):
        try:
            brain = self._brain_for_path(self._path_for_value(value))
            return self._filter(brain)
        except KeyError:
            return False

    def getTermByToken(self, token):
        brain = self._brain_for_path(self._path_for_token(token))
        if not self._filter(brain):
            raise LookupError(token)
        return self._term_for_brain(brain)

    def getTerm(self, value):
        brain = self._brain_for_path(self._path_for_value(value))
        if not self._filter(brain):
            raise LookupError(value)
        return self._term_for_brain(brain)

    # Query API - used to locate content, e.g. in non-JS mode

    def search(self, query, limit=20):
        catalog_query = self.selectable_filter.criteria.copy()
        catalog_query.update(parse_query(query, self.portal_path))

        if limit and 'sort_limit' not in catalog_query:
            catalog_query['sort_limit'] = limit

        try:
            results = (self._term_for_brain(brain, real_value=False)
                       for brain in self.catalog(**catalog_query))
        except ParseError:
            return []

        return results

    # Helper functions

    def _filter(self, brain):
        index_data = self.catalog.getIndexDataForRID(brain.getRID())
        return self.selectable_filter(brain, index_data)

    def _path_for_token(self, token):
        return self.portal_path + token

    def _path_for_value(self, value):
        return self.portal_path + value

    def _brain_for_path(self, path):
        rid = self.catalog.getrid(path)
        return self.catalog._catalog[rid]

    def _term_for_brain(self, brain, real_value=True):
        path = brain.getPath()[len(self.portal_path):]
        return SimpleTerm(path, path, brain.Title)


class ObjPathSource(PathSource):

    def _path_for_value(self, value):
        return '/'.join(value.getPhysicalPath())

    def _term_for_brain(self, brain, real_value=True):
        path = brain.getPath()[len(self.portal_path):]
        if real_value:
            return SimpleTerm(brain._unrestrictedGetObject(),
                              path,
                              brain.Title)
        else:
            return SimpleTerm(path, path, brain.Title)


class PathSourceBinder(object):
    implements(IContextSourceBinder)

    path_source = PathSource

    def __init__(self, navigation_tree_query=None, **kw):
        self.selectable_filter = CustomFilter(**kw)
        self.navigation_tree_query = navigation_tree_query

    def __call__(self, context):
        content = context

        if not IAcquirer.providedBy(content):
            content = getSite()
        return self.path_source(
            content,
            selectable_filter=self.selectable_filter,
            navigation_tree_query=self.navigation_tree_query)


class ObjPathSourceBinder(PathSourceBinder):
    path_source = ObjPathSource
