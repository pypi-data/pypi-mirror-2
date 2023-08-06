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

"""Manage QAction objects"""

from PyQt4 import QtGui

def getAction(parent, widgetaction):
    if widgetaction:
        return QtGui.QWidgetAction(parent)
    else:
        return QtGui.QAction(parent)

def createAction(*a, **kw):
    """creates and returns a QAction object"""

    # collect params
    parent = kw['parent']
    text = kw['text']
    slot = kw.get('slot', None)
    shortcut = kw.get('shortcut', '')
    actionicon = kw.get('actionicon', '')
    tip = kw.get('tip', '')
    checkable = kw.get('checkable', False)
    #signal = kw.get('signal', 'triggered()')
    widgetaction = kw.get('widgetaction', False)
    action = getAction(parent, widgetaction)
    action.setText(text)

    if actionicon:
        action.setIcon(actionicon.getQIcon())
    if shortcut:
        action.setShortcut(shortcut)
    if tip:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        action.triggered.connect( slot )
    if checkable:
        action.setCheckable(True)
    return action

def addActions(target, actions):
    """add action objects to menus, menubars, and toolbars
    if action is None, add a separator.
    """
    for action in actions:
        if action is None:
            target.addSeparator()
        else:
            target.addAction(action)

