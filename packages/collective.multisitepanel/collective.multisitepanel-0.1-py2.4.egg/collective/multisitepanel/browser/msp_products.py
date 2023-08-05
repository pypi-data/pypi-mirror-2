from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner,aq_parent
from plone.memoize.instance import memoize
from pprint import PrettyPrinter
from Products.CMFPlone import PloneMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from collective.multisitepanel.utils import *
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ProductsPanelView(BrowserView):
    
    title=_(u"Add-on Products")
    table = ViewPageTemplateFile('templates/msp_products_table.pt')
    details = ViewPageTemplateFile('templates/msp_products_details.pt')
    __call__ = ViewPageTemplateFile('templates/skeleton.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.sitesList = getSitesList(context)
        self.messages=IStatusMessage(self.request)
        self.qi = getToolByName(self.context,'portal_quickinstaller')
        tmpList = self.qi.listInstallableProducts(skipInstalled=False)
        self.productsList = []
        for product in tmpList:
            product['version'] = self.qi.getProductVersion(product['id'])
            product['description'] = self.qi.getProductDescription(product['id'])
            self.productsList.append(product)

    def back_link(self):
        return dict(label=_(u"Up to Multisite Panel"),
                    url=self.context.absolute_url())
        
    def table_view_link(self):
        return dict(label=_(u"label_custom_view",default="Display as Table"),
                    url=self.context.absolute_url() + '/products_table')

    def details_view_link(self):
        return dict(label=_(u"legend_details",default="Details"),
                    url=self.context.absolute_url() + '/products_details')
    
    def search_link(self, pid):
        if pid is None: return pid
        return dict(label=_(u"Search on Pypy"),
                    url=u"http://pypi.python.org/pypi?%3Aaction=search&term="+pid+"&submit=search")

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
    
    def getProductByPid(self,pid):
        for product in self.productsList:
            if product['id'] == pid: return product
        else: return None

    def multisite_productInstalledVersion(self,this_site,pid):
        siteQi = getToolByName(this_site,'portal_quickinstaller')
        if siteQi.isProductInstalled(pid):
            obj = siteQi._getOb(pid)
            return obj.getInstalledVersion()
        return None

    def updateSiteProduct(self,site,product):
        for thissite in self.sitesList:
            siteName,siteApp,siteQi=thissite
            siteQi = getToolByName(siteApp,'portal_quickinstaller')
        if product:
            qi.reinstallProducts(products=[product])
            message = _(u"feedback", default=_(u"Reinstalled ${product}"), mapping={'product':product})
            self.messages.addStatusMessage(message,type="info")
        return 'Redirecting ...'