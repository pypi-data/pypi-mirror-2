# -*- coding: utf-8 -*-

import grok

from ZODB.broken import PersistentBroken
from zope.component import queryMultiAdapter
from zope.container.interfaces import IContainer
from zope.i18n import translate
from zope.interface import Interface

from dolmen.app import security, layout
from dolmen.app.container import MF as _
from megrok.z3ctable import LinkColumn, ModifiedColumn, table

grok.templatedir("templates")


class FolderListing(layout.TablePage, layout.ContextualMenuEntry):
    grok.title(_(u"Content"))
    grok.context(IContainer)
    grok.require(security.CanListContent)

    batchSize = 20
    startBatchingAt = 20
    cssClassEven = u'even'
    cssClassOdd = u'odd'
    cssClasses = {'table': 'listing sortable'}
    sortOn = None
    label = _("Content of the folder")

    @property
    def values(self):
        return self.context.values()

    def update(self):
        layout.TablePage.update(self)
        self.table = self.renderTable()
        self.batch = self.renderBatch()


class Title(LinkColumn):
    """Displays the title of the item.
    """
    table(FolderListing)
    grok.context(Interface)
    grok.name('folderlisting.title')

    weight = 10
    header = _(u"Title")

    def renderCell(self, item):
        if isinstance(item, PersistentBroken):
            broken = _(
                "Broken item: ${name}",
                mapping={"name": item.__Broken_state__.get('__name__')})
            return translate(broken)

        return LinkColumn.renderCell(self, item)


class ModificationDate(ModifiedColumn):
    """Displays the last modification date.
    """
    table(FolderListing)
    grok.context(Interface)
    grok.name('folderlisting.modified')

    weight = 20
    header = _(u"Modification date")
