from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.similarcontent import SimilarContentPortletMessageFactory as _

import math

class ISimilarContentPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    num = schema.Int(title=_(u"Number of Results"),
                     description=_(u"Number of similar items to return"),
                     default=10,
                     required=True)

    ttc = schema.Int(title=_(u"Number of terms to consider"),
                     description=_(u"This is the number of terms we use to search for similar content. The more terms the more accurate, but slower"),
                     default=20,
                     required=True)


    indexname = schema.TextLine(title=_(u"Index to use"),
                                description=_(u"This is the index we will use to find similar content"),
                                default=u"SearchableText",
                                required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ISimilarContentPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self, num=10, ttc=20, indexname="SearchableText"):
        self.num = num
        self.ttc = ttc
        self.indexname = indexname

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Similar Content Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('similarcontentportlet.pt')

    def similar(self):
        zc = self.context.portal_catalog
        cat = zc._catalog
        idx = cat.indexes[self.data.indexname].index
        wordinfo = idx._wordinfo
        docweight = idx._docweight
        num = self.data.num
        ttc = self.data.ttc
        

        # Get the currrent object's path and rid (=docid)
        path = '/'.join(self.context.getPhysicalPath())
        rid = zc.getrid(path)

        # Get all the words in the document, and total length
        wids = idx.get_words(rid)
        N = float(len(docweight))

        # Calculate the most 'important' words in this document and
        # we then use those as our query. More efficient than using
        # all words in the document.
        rwids = []
        Wd = docweight[rid]
        for wid in set(wids):
            d2w = wordinfo[wid]
            wqt = math.log(1.0 + N / float(len(d2w)))
            wdt = d2w.get(rid, 0) * Wd
            rwids.append((wqt*wdt, wid))

        # sort the wids by 'importance' and get the top 20
        rwids.sort()
        wids = [ wid for (wqt, wid) in rwids[1-ttc:] ]

        # Do the actual search. We use okapiindex._search_wids here 
        # to to the bulk of the work
        res = {}
        rget = res.get
        widres = idx._search_wids(wids)
        # union of all the results, we should be able to us
        # mass_weightedUnion for this, but I couldn't get it to work
        for r,w in widres:
            for docid, weight in r.items():
                res[docid] = rget(docid,0)+weight
        
        # We don't want to include ourself
        del res[rid]

        # Sort and un-decorate the document list
        res = [ (score,docid) for (docid,score) in res.items() ]
        res.sort()
        res.reverse()

        similar = []
        for score, docid in res[:num]:
            similar.append(cat[docid])
        
        return similar


        


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ISimilarContentPortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ISimilarContentPortlet)
