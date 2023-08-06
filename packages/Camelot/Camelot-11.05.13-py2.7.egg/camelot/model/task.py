#  ============================================================================
#
#  Copyright (C) 2007-2011 Conceptive Engineering bvba. All rights reserved.
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
"""Most users have the need to do some basic task tracking accross various
parts of the data model.

These classes provide basic task tracking with configurable statuses, 
categories and roles.  They are presented to the user as "Todo's"
"""

from elixir import Entity, using_options, Field, ManyToMany, OneToMany, ManyToOne, entities, ColumnProperty
import sqlalchemy.types
from sqlalchemy import sql

from camelot.core.utils import ugettext_lazy as _
from camelot.model import metadata
from camelot.model.authentication import getCurrentAuthentication
from camelot.model.type_and_status import type_3_status, create_type_3_status_mixin, get_status_type_class, get_status_class
from camelot.admin.entity_admin import EntityAdmin
from camelot.admin.form_action import FormActionFromModelFunction, ProcessFilesFormAction
from camelot.core.document import documented_entity
from camelot.view import forms
from camelot.view.controls import delegates
import camelot.types

import datetime

__metadata__ = metadata

class AttachFilesAction(ProcessFilesFormAction):
    
    def process_files( self, obj, file_names, _options=None ):
        document_property = TaskDocument.mapper.get_property('document')
        storage = document_property.columns[0].type.storage
        authentication = getCurrentAuthentication()
        for file_name in file_names:
            stored_file = storage.checkin( file_name )
            TaskDocument( of = obj, document=stored_file, created_by=authentication )

class Task( Entity, create_type_3_status_mixin('status') ):
    using_options(tablename='task', order_by=['-creation_date'] )
    creation_date    = Field( sqlalchemy.types.Date, required=True, default=datetime.date.today )
    due_date         = Field( sqlalchemy.types.Date, required=False, default=None )
    description      = Field( sqlalchemy.types.Unicode(255), required=True )
    status           = OneToMany( type_3_status( 'Task', metadata, entities ), cascade='all, delete, delete-orphan' )
    notes            = OneToMany( 'TaskNote', cascade='all, delete, delete-orphan' )
    documents        = OneToMany( 'TaskDocument', cascade='all, delete, delete-orphan' )
    roles            = OneToMany( 'TaskRole', cascade='all, delete, delete-orphan' )
    type             = ManyToOne('TaskType', required = False, ondelete = 'restrict', onupdate = 'cascade')
    categories = ManyToMany( 'PartyCategory',
                             tablename='party_category_task', 
                             remote_colname='party_category_id',
                             local_colname='task_id')
    
    @ColumnProperty
    def number_of_documents( self ):
        return sql.select( [sql.func.count( TaskDocument.id ) ],
                            whereclause = TaskDocument.of_id == self.id )

    @ColumnProperty
    def current_status_sql( self ):
        status_class = get_status_class('Task')
        status_type_class = get_status_type_class('Task')
        return sql.select( [status_type_class.code],
                          whereclause = sql.and_( status_class.status_for_id == self.id,
                                           status_class.status_from_date <= sql.functions.current_date(),
                                           status_class.status_thru_date >= sql.functions.current_date() ),
                          from_obj = [status_type_class.table.join( status_class.table )] ).limit(1)
    
    def __unicode__( self ):
        return self.description or ''
    
    def _get_first_note(self):
        if self.notes:
            return self.notes[0].note

    def _set_first_note(self, note):
        if note and self.id:
            if self.notes:
                self.notes[0].note = note
            else:
                self.notes.append( TaskNote( note=note, created_by=getCurrentAuthentication() ) )
 
    note = property( _get_first_note, _set_first_note )
    
    class Admin( EntityAdmin ):
        verbose_name = _('Task')
        list_display = ['creation_date', 'due_date', 'description', 'type', 'current_status_sql', 'number_of_documents']
        list_filter  = ['type.description', 'current_status_sql', 'categories.name']
        form_state = 'maximized'
        form_actions = [AttachFilesAction( _('Attach Documents'), flush=True )]
        form_display = forms.TabForm( [ ( _('Task'),    ['description', 'type', 'current_status', 
                                                          'creation_date', 'due_date',  'note',]),
                                        ( _('Category'), ['categories'] ),
                                        ( _('Roles'), ['roles'] ),
                                        ( _('Documents'), ['documents'] ),
                                        ( _('Status'), ['status'] ) ] )
        field_attributes = {'note':{'delegate':delegates.RichTextDelegate,
                                    'editable':lambda self:self.id},
                            'type':{'delegate':delegates.ManyToOneChoicesDelegate},
                            'description':{'minimal_column_width':50},
                            'current_status_sql':{'name':'Current status',
                                                  'editable':False}}
        
        def get_form_actions(self, obj):
            form_actions = EntityAdmin.get_form_actions(self, obj)
            status_type_class = get_status_type_class( 'Task' )
            
            def status_change_action( status_type ):
                return FormActionFromModelFunction( status_type.code,
                                                     lambda o:o.change_status( status_type ),
                                                     enabled = lambda o:o.current_status != status_type,
                                                     flush = True )
            
            if obj:
                current_status = obj.current_status
            else:
                current_status = None
                
            for status_type in status_type_class.query.all():
                if status_type != current_status:
                    form_actions.append( status_change_action( status_type ) )
            return form_actions
                
TaskStatusType = get_status_type_class( 'Task' )
Task = documented_entity()( Task )

class TaskType( Entity ):
    using_options(tablename='task_type', order_by=['rank', 'description'])
    description = Field( sqlalchemy.types.Unicode(48), required=True, index=True )
    rank = Field(sqlalchemy.types.Integer(), default=1)
    
    def __unicode__(self):
        return self.description or ''
    
    class Admin( EntityAdmin ):
        verbose_name = _('Task Type')
        list_display = ['description', 'rank']

class TaskRoleType( Entity ):
    using_options(tablename='task_role_type', order_by=['rank', 'description'])
    description = Field( sqlalchemy.types.Unicode(48), required=True, index=True )
    rank = Field(sqlalchemy.types.Integer(), default=1)
    
    def __unicode__(self):
        return self.description or ''
    
    class Admin( EntityAdmin ):
        verbose_name = _('Task Role Type')
        list_display = ['description', 'rank']
        

class TaskRole( Entity ):
    using_options(tablename='task_role')
    task = ManyToOne('Task', required = True, ondelete = 'cascade', onupdate = 'cascade')
    party = ManyToOne('Party', required=True, ondelete='restrict', onupdate='cascade')
    described_by = ManyToOne('TaskRoleType', required = False, ondelete = 'restrict', onupdate = 'cascade')
    rank = Field(sqlalchemy.types.Integer(), required=True, default=1)
    comment = Field( sqlalchemy.types.Unicode( 256 ) )

    class Admin(EntityAdmin):
        verbose_name = _('Role within task')
        list_display = ['party', 'described_by', 'comment', 'rank']
        field_attributes = {'described_by':{'name':_('Type'), 'delegate':delegates.ManyToOneChoicesDelegate},
                                 'rank':{'choices':[(i,str(i)) for i in range(1,5)]},
                                 }

class TaskNote( Entity ):
    using_options(tablename='task_note', order_by=['-created_at'] )
    of = ManyToOne('Task', required=True, onupdate='cascade', ondelete='cascade')
    created_at = Field( sqlalchemy.types.Date, required=True, default=datetime.date.today )
    created_by = ManyToOne('AuthenticationMechanism', required=True )
    note = Field( camelot.types.RichText() )
  
    class Admin( EntityAdmin ):
        verbose_name = _('Note')
        list_display = ['created_at', 'created_by']
        form_display = list_display + ['note']

class TaskDocumentType( Entity ):
    using_options(tablename='task_document_type', order_by=['rank', 'description'])
    description = Field( sqlalchemy.types.Unicode(48), required=True, index=True )
    rank = Field(sqlalchemy.types.Integer(), default=1)
        
    def __unicode__(self):
        return self.description or ''
    
    class Admin( EntityAdmin ):
        verbose_name = _('Document Type')
        list_display = ['description', 'rank']
  
class TaskDocument( Entity ):
    using_options(tablename='task_document')
    of = ManyToOne('Task', required=True, onupdate='cascade', ondelete='cascade')
    created_at = Field( sqlalchemy.types.Date(), default = datetime.date.today, required = True, index = True )
    created_by = ManyToOne('AuthenticationMechanism', required=True)
    type = ManyToOne('TaskDocumentType', required = False, ondelete = 'restrict', onupdate = 'cascade')
    document = Field( camelot.types.File(), required=True )
    description = Field( sqlalchemy.types.Unicode(200) )
    summary = Field( camelot.types.RichText() )
        
    class Admin(EntityAdmin):
        verbose_name = _('Document')
        list_display = ['document', 'description', 'type']
        form_display = list_display + ['created_at', 'created_by', 'summary']
        field_attributes = {'type':{'delegate':delegates.ManyToOneChoicesDelegate},
                            'created_by':{'default':getCurrentAuthentication}}
