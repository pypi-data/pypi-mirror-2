#  ==================================================================================
#
#  Copyright (C) 2007-2008 Conceptive Engineering bvba. All rights reserved.
#  www.conceptive.be / project-camelot@conceptive.be
#
#  This file is part of the Camelot Library.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  this file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
#
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact
#  project-camelot@conceptive.be.
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#  For use of this library in commercial applications, please contact
#  project-camelot@conceptive.be
#
#  ==================================================================================

from PyQt4 import QtGui
from camelot.core.utils import ugettext_lazy as _
from camelot.view.wizard.pages.select import SelectFilePage
from camelot.view.wizard.pages.progress_page import ProgressPage
from camelot.view.art import Icon

class SelectBackupFile(SelectFilePage):
    title = _('Select backup file')
    sub_title = _(
            "Please select a backup file.  "
            "All data in this file will be overwritten."
        )
    icon = Icon('tango/32x32/actions/document-save.png')
    save = True
    
class BackupPage(ProgressPage):
    title = _('Backup in progress')
    
    def __init__(self, backup_mechanism, parent=None):
        super(BackupPage, self).__init__(parent)
        self._backup_mechanism = backup_mechanism
        
    def run(self):
        filename = self.field('datasource').toString()
        backup_mechanism = self._backup_mechanism(filename)
        for completed, total, description in backup_mechanism.backup():
            self.emit( self.update_maximum_signal, total )
            self.emit( self.update_progress_signal, completed, description )

class BackupWizard(QtGui.QWizard):
    """Wizard to perform a backup using a BackupMechanism"""
    
    window_title = _('Backup')

    def __init__(self, backup_mechanism, parent=None):
        super(BackupWizard, self).__init__(parent)
        self.setWindowTitle( unicode(self.window_title) )
        self.addPage(SelectBackupFile())
        self.addPage(BackupPage(backup_mechanism))
        
class RestorePage(ProgressPage):
    title = _('Restore in progress')
    
    def __init__(self, backup_mechanism, parent=None):
        super(RestorePage, self).__init__(parent)
        self._backup_mechanism = backup_mechanism
        
    def run(self):
        filename = self.field('datasource').toString()
        backup_mechanism = self._backup_mechanism(filename)
        for completed, total, description in backup_mechanism.restore():
            self.emit( self.update_maximum_signal, total )
            self.emit( self.update_progress_signal, completed, description )
            
class SelectRestoreFile(SelectFilePage):
    title = _('Select restore file')
    sub_title = _( "Please select a backup file from which to restore the database."
                   "All data in the database will be overwritten with data from this file" )
    icon = Icon('tango/32x32/devices/drive-harddisk.png')
    save = False
        
class RestoreWizard(QtGui.QWizard):
    """Wizard to perform a restore using a BackupMechanism"""
    
    window_title = _('Restore')

    def __init__(self, backup_mechanism, parent=None):
        super(RestoreWizard, self).__init__(parent)
        self.setWindowTitle( unicode(self.window_title) )
        self.addPage(SelectRestoreFile())
        self.addPage(RestorePage(backup_mechanism))
