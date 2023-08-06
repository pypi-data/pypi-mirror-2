#  ============================================================================
#
#  Copyright (C) 2007-2010 Conceptive Engineering bvba. All rights reserved.
#  www.conceptive.be / project-camelot@conceptive.be
#
#  This file is part of the Camelot Library.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file license.txt included in the packaging of
#  this file.  Please review this information to ensure GNU
#  General Public Licensing requirements will be met.
#
#  If you are unsure which license is appropriate for your use, please
#  visit www.python-camelot.com or contact project-camelot@conceptive.be
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#  For use of this library in commercial applications, please contact
#  project-camelot@conceptive.be
#
#  ============================================================================

"""custom tree and tree-items widgets"""

import logging
logger = logging.getLogger('camelot.view.controls.modeltree')

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from camelot.view.art import Icon
from camelot.core.utils import ugettext as _

QT_MAJOR_VERSION = float('.'.join(str(QtCore.QT_VERSION_STR).split('.')[0:2]))


class ModelItem(QtGui.QTreeWidgetItem):
    """Custom tree item widget"""

    def __init__(self, parent, columns_names):
        logger.debug('creating new modelitem')
        QtGui.QTreeWidgetItem.__init__(self, parent, columns_names)
        self.column = 0
        self.set_icon()

        self.setToolTip(self.column, _('Right click to open in New Tab'))

    def _underline(self, enable=False):
        font = self.font(self.column)
        font.setUnderline(enable)
        self.setFont(self.column, font)

    def set_icon(self, qicon=None):
        if qicon is None:
            qicon = Icon('tango/16x16/actions/window-new.png').getQIcon()
        self.setIcon(self.column, qicon)


class ModelTree(QtGui.QTreeWidget):
    """Custom tree widget"""

    def __init__(self, header_labels=[''], parent=None):
        logger.debug('creating new modeltree')
        super(ModelTree, self).__init__(parent)
        # we don't select entire rows
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        # we track mouse movement when no button is pressed
        self.setMouseTracking(True)
        self.header_labels = header_labels
        self.clear_model_items()
        self.fix_header_labels()

    def fix_header_labels(self):
        if QT_MAJOR_VERSION > 4.3:
            self.setHeaderHidden(True)
        else:
            self.setHeaderLabels(self.header_labels)

    def clear_model_items(self):
        self.modelitems = []

    def mousePressEvent(self, event):
        """Custom context menu"""
        if event.button() == Qt.RightButton:
            self.customContextMenuRequested.emit( event.pos() )
            event.accept()
        else:
            QtGui.QTreeWidget.mousePressEvent(self, event)

    def leaveEvent(self, event):
        if not self.modelitems: return
        for item in self.modelitems: item._underline(False)

    def mouseMoveEvent(self, event):
        if not self.modelitems: return
        for item in self.modelitems: item._underline(False)

        item = self.itemAt(self.mapFromGlobal(self.cursor().pos()))
        if item:
            item._underline(True)
