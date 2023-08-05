### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2008-2010 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

__docformat__ = "restructuredtext"

# import standard packages
from datetime import datetime
import logging
logger = logging.getLogger('ztfy.scheduler')

# import Zope3 interfaces
from persistent.interfaces import IPersistent
from transaction.interfaces import ITransactionManager
from ZODB.interfaces import IConnection
from zope.app.appsetup.interfaces import IDatabaseOpenedWithRootEvent
from zope.app.container.interfaces import IObjectAddedEvent, IObjectRemovedEvent
from zope.location.interfaces import ISite

# import local interfaces
from interfaces import IScheduledTaskEvent, IUnscheduledTaskEvent
from interfaces import ISchedulerHandler, IScheduler, ISchedulerTask

# import Zope3 packages
from zope.app import zapi
from zope.app.component import hooks
from zope.app.intid.interfaces import IIntIds
from zope.app.folder.folder import Folder
from zope.app.publication.zopepublication import ZopePublication
from zope.component import adapter
from zope.interface import implements, implementer

# import local packages
from apscheduler.scheduler import Scheduler as SchedulerBase

from ztfy.scheduler import _


class SchedulerHandler(object):

    implements(ISchedulerHandler)

    def __init__(self):
        self.schedulers = {}
        self.jobs = {}


@adapter(IScheduledTaskEvent)
def handleScheduledTask(event):
    handler = zapi.queryUtility(ISchedulerHandler)
    if handler is None:
        return
    intids = zapi.getUtility(IIntIds)
    handler.jobs[intids.queryId(event.object)] = event.job


@adapter(IUnscheduledTaskEvent)
def handleUnscheduledTask(event):
    handler = zapi.queryUtility(ISchedulerHandler)
    if handler is None:
        return
    task = event.object
    intids = zapi.getUtility(IIntIds)
    job = handler.jobs.get(intids.queryId(task))
    if job is not None:
        scheduler = zapi.getParent(task).getScheduler()
        if scheduler is not None:
            scheduler.unschedule_job(job)


class Scheduler(Folder):

    implements(IScheduler)

    @property
    def tasks(self):
        return [t for t in self.values() if ISchedulerTask.providedBy(t)]

    def getScheduler(self):
        handler = zapi.queryUtility(ISchedulerHandler)
        if handler is None:
            return None
        intids = zapi.getUtility(IIntIds)
        return handler.schedulers.get(intids.queryId(self))

    def start(self):
        handler = zapi.queryUtility(ISchedulerHandler)
        if handler is None:
            return
        scheduler = handler.schedulers.get(self)
        if scheduler is None:
            intids = zapi.getUtility(IIntIds)
            scheduler = handler.schedulers[intids.register(self)] = SchedulerBase()
        else:
            scheduler.shutdown(0)
        scheduler.start()
        for task in self.tasks:
            task.schedule()

    def stop(self):
        handler = zapi.queryUtility(ISchedulerHandler)
        if handler is None:
            return
        intids = zapi.getUtility(IIntIds)
        scheduler = handler.schedulers.get(intids.queryId(self))
        if scheduler is not None:
            scheduler.shutdown(0)

    def dump_jobs(self):
        scheduler = self.getScheduler()
        if scheduler is None:
            return _("No scheduler found !")
        return scheduler.dump_jobs()

    def getNextRun(self, task):
        handler = zapi.queryUtility(ISchedulerHandler)
        if handler is None:
            return None
        intids = zapi.getUtility(IIntIds)
        job = handler.jobs.get(intids.queryId(task))
        if job and job.trigger:
            now = datetime.now()
            return job.trigger.get_next_fire_time(now)


@adapter(IScheduler, IObjectAddedEvent)
def handleNewScheduler(scheduler, event):
    scheduler.start()


@adapter(IScheduler, IObjectRemovedEvent)
def handleRemovedScheduler(scheduler, event):
    scheduler.stop()


@adapter(IDatabaseOpenedWithRootEvent)
def handleOpenedDatabase(event):
    manager = zapi.queryUtility(ISchedulerHandler)
    if manager is None:
        return
    db = event.database
    connection = db.open()
    app = connection.root()[ZopePublication.root_name]
    sites = [v for v in app.values() if ISite(v, None) is not None]
    for site in sites:
        hooks.setSite(site)
        for _name, scheduler in zapi.getUtilitiesFor(IScheduler):
            logger.warning("Starting tasks scheduler")
            scheduler.start()


# IPersistent adapters copied from zc.twist package
# also register this for adapting from IConnection
@adapter(IPersistent)
@implementer(ITransactionManager)
def transactionManager(obj):
    conn = IConnection(obj) # typically this will be
    # zope.app.keyreference.persistent.connectionOfPersistent
    try:
        return conn.transaction_manager
    except AttributeError:
        return conn._txn_mgr
        # or else we give up; who knows.  transaction_manager is the more
        # recent spelling.


logger.warning("""In a ZEO context, this package must be included only once from a "master" ZEO client""")
