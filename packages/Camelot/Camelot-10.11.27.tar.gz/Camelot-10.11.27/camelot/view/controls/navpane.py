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

"""left navigation pane"""

import logging
logger = logging.getLogger( 'camelot.view.controls.navpane' )

from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore

from camelot.view.model_thread import post
from camelot.action import addActions, createAction
from camelot.view.controls.modeltree import ModelItem, ModelTree

QT_MAJOR_VERSION = float('.'.join(str(QtCore.QT_VERSION_STR).split('.')[0:2]))

from camelot.view.controls.user_translatable_label import UserTranslatableLabel
from camelot.core.utils import ugettext as _


class PaneCaption(UserTranslatableLabel):
    """Navigation pane Caption"""
    def __init__(
        self, text, textbold=True, textindent=3, width=160, height=32,
        objectname='PaneCaption', parent=None
    ):

        super(UserTranslatableLabel, self).__init__(text, parent)

        if textbold:
            self.textbold()

        font = self.font()
        font.setPointSize( font.pointSize() + 2 )
        self.setFont( font )

        self.setIndent( textindent )

        self.setObjectName( objectname )

        #style = """
        #QLabel#PaneCaption {
        #  margin: 3px 0 0 3px;
        #  border: 1px solid %s;
        #  color: %s;
        #  background-color: %s;
        #}
        #""" % ( scheme.bordercolor(),
        #       scheme.captiontextcolor(),
        #       scheme.captionbackground() )

        #self.setStyleSheet( style );
        self.setFixedHeight( height )
        self.resize( width, height )

    def textbold( self ):
        font = self.font()
        font.setBold( True )
        font.setPointSize( font.pointSize() + 1 )
        self.setFont( font )


class PaneButton(QtGui.QPushButton):
    """Custom made navigation pane pushbutton"""

    section_selected_signal = QtCore.pyqtSignal(int, unicode)

    def __init__(
        self, text, buttonicon='', textbold=True, textleft=True,
        width=160, height=32, objectname='PaneButton', parent=None,
        index=0
    ):

        #QtGui.QWidget.__init__( self, parent )
        QtGui.QPushButton.__init__(self, parent)

        #if textleft:
        #    option = QtGui.QBoxLayout.LeftToRight
        #else:
        #    option = QtGui.QBoxLayout.RightToLeft
        #self.layout = QtGui.QBoxLayout( option )
        #self.layout.setSpacing( 0 )
        #self.layout.setContentsMargins( 3, 0, 0, 0 )

        self.setCheckable(True)

        if buttonicon:
            #self.icon = QtGui.QLabel()
            #self.icon.setPixmap(QtGui.QPixmap(buttonicon))
            #self.layout.addWidget(self.icon)
            self.setIcon(QtGui.QIcon(buttonicon))
            self.setIconSize(QtCore.QSize(24, 24))

        self.label = UserTranslatableLabel(text, parent)

        #self.layout.addWidget( self.label, 2 )

        #self.setLayout( self.layout )

        self.setText(str(text))

        #if textbold: self.textbold()

        self.setObjectName(objectname)

        #self.stylenormal = """
        #QWidget#PaneButton * {
        #  margin: 0;
        #  padding-left: 3px;
        #  color: %s;
        #  border-color : %s;
        #  background-color : %s;
        #}
        #""" % (scheme.textcolor(),
        #       scheme.bordercolor(),
        #       scheme.normalbackground() )

        #self.stylehovered = """
        #QWidget#PaneButton * {
        #  margin: 0;
        #  padding-left: 3px;
        #  color: %s;
        #  background-color : %s;
        #}
        #""" % (scheme.textcolor(),
        #       scheme.hoveredbackground() )

        #self.styleselected = """
        #QWidget#PaneButton * {
        #  margin: 0;
        #  padding-left: 3px;
        #  color: %s;
        #  background-color : %s;
        #}
        #""" % (scheme.selectedcolor(),
        #       scheme.selectedbackground())

        #self.styleselectedover = """
        #QWidget#PaneButton * {
        #  margin: 0;
        #  padding-left: 3px;
        #  color: %s;
        #  background-color : %s;
        #}
        #""" % (scheme.selectedcolor(),
        #       scheme.selectedbackground(inverted=True))

        #self.setStyleSheet( self.stylenormal )
        self.setFixedHeight(height)
        self.resize(width, height)
        self.selected = False
        self.index = index

    #def textbold( self ):
    #    font = self.label.font()
    #    font.setBold( True )
    #    self.label.setFont( font )

    #def enterEvent( self, event ):
    #    if self.selected:
    #        self.setStyleSheet( self.styleselectedover )
    #    else:
    #        self.setStyleSheet( self.stylehovered )

    #def leaveEvent( self, event ):
    #    if self.selected:
    #        self.setStyleSheet( self.styleselected )
    #    else:
    #        self.setStyleSheet( self.stylenormal )

    def mousePressEvent(self, event):
        if self.selected:
            return
        else:
            self.selected = True
            self.setChecked(True)
    #        self.setStyleSheet(self.styleselectedover)
            self.section_selected_signal.emit(self.index, self.label.text())

class NavigationPane(QtGui.QDockWidget):
    """ms office-like navigation pane in Qt"""

    def __init__(self, app_admin, workspace, parent):
        QtGui.QDockWidget.__init__(self, parent)
        # object name needs to be set for mainwindow save state
        self.setObjectName('NavigationPane')
        self._workspace = workspace
        self.app_admin = app_admin
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.parent = parent
        self.currentbutton = -1
        self.caption = PaneCaption('')
        self.setTitleBarWidget(self.caption)
        #self.setObjectName(objectname)
        self.buttons = []
        self.content = QtGui.QWidget()
        self.content.setObjectName('NavPaneContent')
        header_labels = ['']
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(4, 1, 1, 1)
        self.treewidget = ModelTree(header_labels, self)
        layout.addWidget( self.treewidget )
        self.setMinimumWidth(QtGui.QFontMetrics(QtGui.QApplication.font()).averageCharWidth()*40)
        self.content.setLayout(layout)
        self.setWidget(self.content)
        #
        # set minimum with to 0 as long as we are using the navigation pane as a
        # dockwidget, because this dockwidget is not collapsible
        #
        self.setMinimumWidth(0)
        # Tried selecting QDockWidget but it's not working
        # so we must undo this margin in children stylesheets :)
        #style = 'margin: 0 0 0 3px;'
        #self.setStyleSheet(style)
        self.app_admin.sections_changed_signal.connect(self.auth_update)
        self.auth_update()

    @QtCore.pyqtSlot()
    def auth_update(self):
        post(self.app_admin.get_sections, self.set_sections)

    def get_sections(self):
        return self.sections

    def set_sections(self, sections):
        logger.debug('set sections')
        from PyQt4.QtTest import QTest
        #
        # current button might no longer exisst once we set
        # the new sections
        #
        self.currentbutton = -1
        for b in self.buttons:
            b.deleteLater()
        self.sections = sections
        self.buttons = [
            PaneButton(
                section.get_verbose_name(),
                section.get_icon().getQPixmap(),
                index=i
            )
            for i,section in enumerate(sections)
        ]
        self.setcontent(self.buttons)
        # use QTest to auto select first button :)
        if len(self.buttons):
            firstbutton = self.buttons[0]
            QTest.mousePress(firstbutton, Qt.LeftButton)

    def setcontent(self, buttons):
        logger.debug('setting up pane content')

        #style = """
        #QWidget#NavPaneContent {
        #  margin-left: 3px;
        #  background-color: %s;
        #}
        #""" % scheme.bordercolor()

        #self.content.setStyleSheet(style)

        # TODO: Should a separator be added between the tree
        #       and the buttons?
        #self.treewidget = PaneTree(self)


        self.treewidget.setObjectName('NavPaneTree')

        #style = """
        #QWidget#NavPaneTree {
        #  margin-left: 3px;
        #  border: 1px solid %s;
        #  background-color: rgb(255, 255, 255);
        #}
        #""" % scheme.bordercolor()

        #self.treewidget.setStyleSheet(style)

        # context menu
        self.treewidget.contextmenu = QtGui.QMenu(self)
        newWindowAct = createAction(
            parent = self,
            text = _('Open in New Tab'),
            slot = self.pop_window,
            shortcut = 'Ctrl+Enter'
        )

        addActions(self.treewidget.contextmenu, (newWindowAct,))
        self.treewidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treewidget.customContextMenuRequested.connect(self.createContextMenu)

        if buttons:
            for b in buttons:
                self.content.layout().addWidget(b)
                b.section_selected_signal.connect(self.change_current)
            self.buttons = buttons
        else:
            self.buttons = []

    def set_items_in_tree(self, items):
        self.treewidget.clear()
        self.treewidget.clear_model_items()
        self.items = items

        if not items: return

        for item in items:
            model_item = ModelItem(self.treewidget, [item.get_verbose_name()])
            self.treewidget.modelitems.append(model_item)

        self.treewidget.update()

    @QtCore.pyqtSlot(int, unicode)
    def change_current(self, index, text):
        logger.debug('set current to %s' % text)
        if self.currentbutton != -1:
            button = self.buttons[self.currentbutton]
            #button.setStyleSheet(button.stylenormal)
            button.selected = False
            button.setChecked(False)
        self.caption.setText(text)
        self.currentbutton = index

        def get_models_for_tree():
            """Return pairs of (Admin, query) classes for items in the tree"""
            if index < len(self.sections):
                section = self.sections[index]
                return section.get_items()
            return []

        post(get_models_for_tree, self.set_items_in_tree)

    def createContextMenu(self, point):
        logger.debug('creating context menu')
        item = self.treewidget.itemAt(point)
        if item:
            self.treewidget.setCurrentItem(item)
            #self.treewidget.contextmenu.popup(self.cursor().pos())
            self.treewidget.contextmenu.popup(self.treewidget.mapToGlobal(point))

    def pop_window(self):
        """pops a model window in parent's workspace"""
        logger.debug('poping a window in parent')
        item = self.treewidget.currentItem()
        index = self.treewidget.indexFromItem(item)
        section_item = self.items[index.row()]
        new_view = section_item.get_action().run(self._workspace)
        if new_view:
            self._workspace.add_view(new_view)

