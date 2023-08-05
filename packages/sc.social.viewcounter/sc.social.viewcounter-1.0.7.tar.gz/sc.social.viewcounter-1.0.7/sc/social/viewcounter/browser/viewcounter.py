# -*- coding:utf-8 -*-
from datetime import datetime
from datetime import timedelta
from time import time
from zope import interface
from zope import component
from Products.CMFPlone import utils
from Products.Five import BrowserView
from zope.interface import implements
from Acquisition import aq_inner
from Products.CMFPlone.utils import getToolByName

from sqlalchemy import sql, orm
from sqlalchemy import and_
from sqlalchemy import func 
from sqlalchemy.sql.expression import desc
from sqlalchemy.exc import OperationalError, InvalidRequestError
from zope.app.cache.interfaces.ram import IRAMCache
from plone.memoize import instance, ram

from sc.social.viewcounter.pageview import session
from sc.social.viewcounter.pageview import PageView

from Acquisition import aq_inner
from plone.app.portlets.cache import get_language

import logging
logger = logging.getLogger('sc.social.viewcounter:')

def hourly_cache(fun, self, *args, **kw):
    lang = get_language(aq_inner(self.context), self.request)
    key = "%s-%s-%s" % (lang, time() // (60 * 60),str(args))
    logger.debug('SQL: Hourly cache key %s' % key)
    return key

def daily_cache(fun, self, *args, **kw):
    lang = get_language(aq_inner(self.context), self.request)
    key = "%s-%s-%s" % (lang, time() // (60 * 60 * 24),str(args))
    logger.debug('SQL: Daily cache key %s' % key)
    return key

class PageViewBV(BrowserView):
    """ Base BrowserView to PageView
    """
    session = None
    
    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        self.session = session()
        super(PageViewBV, self).__init__(context, request)
    
    def __call__(self, **kw):
        """ Create a new pageview
            Returns the pageview
        """
        session = self.session
        try:
            session.connection()
        except (OperationalError,InvalidRequestError):
            logger.info('SQL: Cannot connect to database')
            session = None
        context = self.context
        request = self.request
        mt = getToolByName(context,'portal_membership')
        
        if mt.isAnonymousUser(): # the user has not logged in
            userid = 'Anonymous'
        else:
            member = mt.getAuthenticatedMember()
            userid = member.getUserName()
        if session and hasattr(context,'UID'):
            # Creates a new PageView object
            object_uid = context.UID()
            object_path = '/'.join(context.getPhysicalPath())
            object_type = context.portal_type
            user_ip = request.get('X-Forwarded-For',request.get('REMOTE_ADDR'))
            user_name = userid
            pv = PageView(object_uid,object_path,object_type,user_ip,user_name)
            # Adds to session and commits transaction
            session.add(pv)
    


class Reports(BrowserView):
    
    session = None
    
    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        self.session = session()
        self.ct = getToolByName(self.context,'portal_catalog')
        self._pp = getToolByName(self.context,'portal_properties',None)
        if hasattr(self._pp,'sc_social_viewcounter'):
            blacklisted_types = list(self._pp.sc_social_viewcounter.getProperty("blacklisted_types") or []) + ['Discussion Item',]
        else:
            blacklisted_types = []
        self.blacklisted_types = blacklisted_types
        super(Reports, self).__init__(context, request)
    
    
    @ram.cache(hourly_cache)
    def _reportPageViews(self,dateRange=None,portal_type='',path='',**kw):
        logger.debug('Query sql.')
        session = self.session
        where=[]
        if dateRange:
            where.append(PageView.access_datetime.between(*dateRange))
        if portal_type:
            where.append(PageView.object_type==portal_type)
        if path:
            where.append(PageView.object_path==path)
        where = and_(*where)
        try:
            pvs = session.query(func.count('*'),PageView.object_uid).filter(where).order_by(desc(func.count('*'))).group_by(PageView.object_uid)
            listPvs = pvs.all()
        except OperationalError:
            logger.info('SQL Report: Cannot connect to database')
            pvs = []
            listPvs = []
        uids = [uid for (pv,uid) in pvs]
        dictByUIDs = self.dictByUIDs(uids,**kw)
        return [(uid,dictByUIDs[uid].get('Title'),dictByUIDs[uid].get('url'),pv) for (pv,uid) in listPvs if dictByUIDs.get(uid,None)]
    
    def dictByUIDs(self,uids,**kw):
        ct = self.ct
        blacklisted = self.blacklisted_types
        kw['UID'] = UID={'query':uids}
        results = ct.unrestrictedSearchResults(**kw)
        dictByUIDs = dict([(brain.UID,{'Title':brain.Title,
                                      'path':brain.getPath(),
                                      'url':brain.getURL(),
                                      'portal_type':brain.portal_type}) \
                                      for brain in results \
                                      if brain.portal_type not in blacklisted])
        return dictByUIDs
        
    @property
    @ram.cache(hourly_cache)
    def lastHour(self):
        now = datetime.now()
        delta = timedelta(0,3600)
        base_dt = (now - delta)
        start = datetime(base_dt.year,
                         base_dt.month,
                         base_dt.day,
                         base_dt.hour,
                         0,
                         0,
                        )
        end = datetime(base_dt.year,
                       base_dt.month,
                       base_dt.day,
                       base_dt.hour,
                       59,
                       59,
                       )
        return (start,end)
    
    @property
    @ram.cache(hourly_cache)
    def lastDay(self):
        now = datetime.now()
        delta = timedelta(1,0)
        base_dt = (now - delta)
        start = datetime(base_dt.year,
                         base_dt.month,
                         base_dt.day,
                         0,
                         0,
                         0,
                        )
        end = datetime(base_dt.year,
                       base_dt.month,
                       base_dt.day,
                       23,
                       59,
                       59,
                       )
        return (start,end)
    
    @property
    @ram.cache(daily_cache)
    def lastWeek(self):
        now = datetime.now()
        weekday = now.weekday()
        delta = timedelta(7+weekday,0)
        base_dt = (now - delta)
        start = datetime(base_dt.year,
                         base_dt.month,
                         base_dt.day,
                         0,
                         0,
                         0,
                        )
        delta = timedelta(1+weekday,0)
        base_dt = (now - delta)        
        end = datetime(base_dt.year,
                       base_dt.month,
                       base_dt.day,
                       23,
                       59,
                       59,
                       )
        return (start,end)
    
    
    @property
    @ram.cache(daily_cache)
    def lastMonth(self):
        now = datetime.now()
        day = now.day
        delta = timedelta(day,0)
        base_dt = (now - delta)
        start = datetime(base_dt.year,
                         base_dt.month,
                         1,
                         0,
                         0,
                         0,
                        )
        base_dt = (now - delta)        
        end = datetime(base_dt.year,
                       base_dt.month,
                       base_dt.day,
                       23,
                       59,
                       59,
                       )
        return (start,end)
        
    
    @instance.memoizedproperty
    def allTime(self):
        now = datetime.now()
        base_dt = now
        start = datetime(2000,
                         1,
                         1,
                         0,
                         0,
                         0,
                        )
        end = base_dt
        return (start,end)
        
    
    @instance.memoizedproperty
    def lastYear(self):
        now = datetime.now()
        weekday = now.weekday()
        base_dt = now
        start = datetime(base_dt.year-1,
                         1,
                         1,
                         0,
                         0,
                         0,
                        )
        delta = timedelta(1+weekday,0)
        base_dt = (now - delta)        
        end = datetime(base_dt.year-1,
                       12,
                       31,
                       23,
                       59,
                       59,
                       )
        return (start,end)
        
    
    def cleanKw(self,kw):
        newKw = {}
        for k,v in kw.items():
            if isinstance(v,list):
                v = tuple(v)
            newKw[k]=v
        return newKw
    
    def invalidateCache(self):
        ''' Invalidates cache
        '''
        cache = component.queryUtility(IRAMCache)
        if cache:
            cache.invalidate('sc.social.viewcounter.browser.viewcounter._reportPageViews')
    
    def _viewsByRange(self,range,**kw):
        results = self._reportPageViews(range, **self.cleanKw(kw))
        if not results:
            # No results, no cache
            self.invalidateCache()
        return results
    
    def viewsLastHour(self,**kw):
        range = self.lastHour
        results = self._viewsByRange(range, **self.cleanKw(kw))
        return results
    
    def viewsLastDay(self,**kw):
        range = self.lastDay
        results = self._viewsByRange(range, **self.cleanKw(kw))
        return results
    
    def viewsLastWeek(self,**kw):
        range = self.lastWeek
        results = self._viewsByRange(range, **self.cleanKw(kw))
        return results
    
    def viewsLastMonth(self,**kw):
        range = self.lastMonth
        results = self._viewsByRange(range, **self.cleanKw(kw))
        return results
    
    def viewsLastYear(self,**kw):
        range = self.lastYear
        results = self._viewsByRange(range, **self.cleanKw(kw))
        return results
    
    def viewsAllTime(self,**kw):
        # If we really want everything, let's do it :-)
        range = None
        results = self._viewsByRange(range, **self.cleanKw(kw))
        return results
