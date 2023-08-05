#  ============================================================================
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
#  ============================================================================

"""Tableview"""

import logging
logger = logging.getLogger( 'camelot.view.controls.tableview' )

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

from camelot.view.proxy.queryproxy import QueryTableProxy
from camelot.view.controls.filterlist import filter_changed_signal
from camelot.view.controls.view import AbstractView
from camelot.view.controls.user_translatable_label import UserTranslatableLabel
from camelot.view.model_thread import model_function, gui_function, post
from camelot.core.utils import ugettext as _

from search import SimpleSearchControl

class TableWidget( QtGui.QTableView):
    """A widget displaying a table, to be used within a TableView"""
  
    def __init__( self, parent = None ):
        QtGui.QTableView.__init__( self, parent )
        logger.debug( 'create TableWidget' )
        self.setSelectionBehavior( QtGui.QAbstractItemView.SelectRows )
        self.setEditTriggers( QtGui.QAbstractItemView.SelectedClicked | QtGui.QAbstractItemView.DoubleClicked )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )
        # set to false while sorting is not implemented in CollectionProxy
        self.horizontalHeader().setClickable( True )
        self._header_font_required = QtGui.QApplication.font()
        self._header_font_required.setBold( True )
        self._minimal_row_height = QtGui.QFontMetrics(QtGui.QApplication.font()).lineSpacing() + 10
        self.verticalHeader().setDefaultSectionSize( self._minimal_row_height )
        self.connect( self.horizontalHeader(), QtCore.SIGNAL('sectionClicked(int)'), self.horizontal_section_clicked )
    
    def horizontal_section_clicked( self, logical_index ):
        """Update the sorting of the model and the header"""
        header = self.horizontalHeader()
        order = Qt.AscendingOrder
        if not header.isSortIndicatorShown():
            header.setSortIndicatorShown( True )
        elif header.sortIndicatorSection()==logical_index:
            # apparently, the sort order on the header is allready switched when the section
            # was clicked, so there is no need to reverse it
            order = header.sortIndicatorOrder()
        header.setSortIndicator( logical_index, order )
        self.model().sort( logical_index, order )
        
    def setModel( self, model ):
        QtGui.QTableView.setModel( self, model )
        self.connect( self.selectionModel(), SIGNAL( 'currentChanged(const QModelIndex&,const QModelIndex&)' ), self.activated )
    
    def activated( self, selectedIndex, previousSelectedIndex ):
        option = QtGui.QStyleOptionViewItem()
        newSize = self.itemDelegate( selectedIndex ).sizeHint( option, selectedIndex )
        row = selectedIndex.row()
        if previousSelectedIndex.row() >= 0:
            oldSize = self.itemDelegate( previousSelectedIndex ).sizeHint( option, selectedIndex )
            previousRow = previousSelectedIndex.row()
            self.setRowHeight( previousRow, oldSize.height() )
        self.setRowHeight( row, newSize.height() )
    
class RowsWidget( QtGui.QLabel ):
    """Widget that is part of the header widget, displaying the number of rows
    in the table view"""
  
    _number_of_rows_font = QtGui.QApplication.font()
  
    def __init__( self, parent ):
        QtGui.QLabel.__init__( self, parent )
        self.setFont( self._number_of_rows_font )
    
    def setNumberOfRows( self, rows ):
        self.setText( _('(%i rows)')%rows )
    
class HeaderWidget( QtGui.QWidget ):
    """HeaderWidget for a tableview, containing the title, the search widget,
    and the number of rows in the table"""
  
    search_widget = SimpleSearchControl
    rows_widget = RowsWidget
  
    _title_font = QtGui.QApplication.font()
    _title_font.setBold( True )
  
    def __init__( self, parent, admin ):
        QtGui.QWidget.__init__( self, parent )
        self._admin = admin
        layout = QtGui.QVBoxLayout()
        widget_layout = QtGui.QHBoxLayout()
        search = self.search_widget( self )
        self.connect(search, SimpleSearchControl.expand_search_options_signal, self.expand_search_options)
        title = UserTranslatableLabel( admin.get_verbose_name_plural(), self )
        title.setFont( self._title_font )
        widget_layout.addWidget( title )
        widget_layout.addWidget( search )
        if self.rows_widget:
            self.number_of_rows = self.rows_widget( self )
            widget_layout.addWidget( self.number_of_rows )
        else:
            self.number_of_rows = None
        layout.addLayout( widget_layout )
        self._expanded_filters_created = False
        self._expanded_search = QtGui.QWidget()
        self._expanded_search.hide()
        layout.addWidget(self._expanded_search)
        self.setLayout( layout )
        self.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )
        self.setNumberOfRows( 0 )
        self.search = search
        
    def _fill_expanded_search_options(self, columns):
        from camelot.view.controls.filter_operator import FilterOperator
        layout = QtGui.QHBoxLayout()
        for field, attributes in columns:
            if 'operators' in attributes and attributes['operators']:
                widget = FilterOperator( self._admin.entity, field, attributes, self)
                self.connect( widget, filter_changed_signal,  self._filter_changed )
                layout.addWidget( widget )
        layout.addStretch()
        self._expanded_search.setLayout( layout )
        self._expanded_filters_created = True
        
    def _filter_changed(self):
        self.emit(QtCore.SIGNAL('filters_changed'))
        
    def decorate_query(self, query):
        """Apply expanded filters on the query"""
        if self._expanded_filters_created:
            for i in range(self._expanded_search.layout().count()):
                if self._expanded_search.layout().itemAt(i).widget():
                    query = self._expanded_search.layout().itemAt(i).widget().decorate_query(query)
        return query
            
    def expand_search_options(self):
        if self._expanded_search.isHidden():
            if not self._expanded_filters_created:
                post( self._admin.get_columns, self._fill_expanded_search_options )
            self._expanded_search.show()
        else:
            self._expanded_search.hide()
        
    @gui_function
    def setNumberOfRows( self, rows ):
        if self.number_of_rows:
            self.number_of_rows.setNumberOfRows( rows )
      
class TableView( AbstractView  ):
    """A generic tableview widget that puts together some other widgets.  The behaviour of this class and
  the resulting interface can be tuned by specifying specific class attributes which define the underlying
  widgets used ::
  
    class MovieRentalTableView(TableView):
      title_format = 'Grand overview of recent movie rentals'
  
  The attributes that can be specified are :
  
  .. attribute:: header_widget
  
  The widget class to be used as a header in the table view::
   
    header_widget = HeaderWidget
    
  .. attribute:: table_widget
  
  The widget class used to display a table within the table view ::
  
  table_widget = TableWidget
  
  .. attribute:: title_format
  
  A string used to format the title of the view ::
  
  title_format = '%(verbose_name_plural)s'
  
  .. attribute:: table_model
  
  A class implementing QAbstractTableModel that will be used as a model for the table view ::
  
    table_model = QueryTableProxy
  
  - emits the row_selected signal when a row has been selected
  """
  
    header_widget = HeaderWidget
    table_widget = TableWidget
  
    #
    # The proxy class to use 
    #
    table_model = QueryTableProxy
    #
    # Format to use as the window title
    #
    title_format = '%(verbose_name_plural)s'
  
    def __init__( self, admin, search_text = None, parent = None ):
        AbstractView.__init__( self, parent )
        self.admin = admin
        post( self.get_title, self.change_title )
        widget_layout = QtGui.QVBoxLayout()
        if self.header_widget:
            self.header = self.header_widget( self, admin )
            widget_layout.addWidget( self.header )
            self.connect( self.header.search, SIGNAL( 'search' ), self.startSearch )
            self.connect( self.header.search, SIGNAL( 'cancel' ), self.cancelSearch )
            if search_text:
                self.header.search.search( search_text )
        else:
            self.header = None
        widget_layout.setSpacing( 0 )
        widget_layout.setMargin( 0 )
        splitter = QtGui.QSplitter( self )
        splitter.setObjectName('splitter')
        widget_layout.addWidget( splitter )
        table_widget = QtGui.QWidget( self )
        filters_widget = QtGui.QWidget( self )
        self.table_layout = QtGui.QVBoxLayout()
        self.table_layout.setSpacing( 0 )
        self.table_layout.setMargin( 0 )
        self.table = None
        self.filters_layout = QtGui.QVBoxLayout()
        self.filters_layout.setSpacing( 0 )
        self.filters_layout.setMargin( 0 )     
        self.actions = None
        self._table_model = None
        table_widget.setLayout( self.table_layout )
        filters_widget.setLayout( self.filters_layout )
        #filters_widget.hide()
        self.set_admin( admin )
        splitter.addWidget( table_widget )
        splitter.addWidget( filters_widget )
        self.setLayout( widget_layout )
        self.closeAfterValidation = QtCore.SIGNAL( 'closeAfterValidation()' )
        self.search_filter = lambda q: q
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(QtGui.QKeySequence.Find), self)
        self.connect( shortcut, QtCore.SIGNAL( 'activated()' ), self.activate_search )
        if self.header_widget:
            self.connect( self.header, QtCore.SIGNAL('filters_changed'),  self.rebuildQuery )
        # give the table widget focus to prevent the header and its search control to
        # receive default focus, as this would prevent the displaying of 'Search...' in the
        # search control, but this conflicts with the MDI, resulting in the window not
        # being active and the menus not to work properly
        #table_widget.setFocus( QtCore.Qt.OtherFocusReason )
        #self.setFocusProxy(table_widget)
        #self.setFocus( QtCore.Qt.OtherFocusReason )
        post( self.admin.get_subclass_tree, self.setSubclassTree )
    
    def activate_search(self):
        self.header.search.setFocus(QtCore.Qt.ShortcutFocusReason)
        
    @model_function
    def get_title( self ):
        return self.title_format % {'verbose_name_plural':self.admin.get_verbose_name_plural()}
    
    @gui_function
    def setSubclassTree( self, subclasses ):
        if len( subclasses ) > 0:
            from inheritance import SubclassTree
            splitter = self.findChild(QtGui.QWidget, 'splitter' )
            class_tree = SubclassTree( self.admin, splitter )
            splitter.insertWidget( 0, class_tree )
            self.connect( class_tree, SIGNAL( 'subclassClicked' ), self.set_admin )
      
    def sectionClicked( self, section ):
        """emits a row_selected signal"""
        self.emit( SIGNAL( 'row_selected' ), section )
    
    def copy_selected_rows( self ):
        """Copy the selected rows in this tableview"""
        logger.debug( 'delete selected rows called' )
        if self.table and self._table_model:
            for row in set( map( lambda x: x.row(), self.table.selectedIndexes() ) ):
                self._table_model.copy_row( row )
                
    def select_all_rows( self ):
        self.table.selectAll()
            
    def create_table_model( self, admin ):
        """Create a table model for the given admin interface"""
        return self.table_model( admin,
                                 admin.get_query,
                                 admin.get_columns )
    
    def get_admin(self):
        return self.admin
    
    def get_model(self):
        return self._table_model
    
    @gui_function
    def set_admin( self, admin ):
        """Switch to a different subclass, where admin is the admin object of the
        subclass"""
        logger.debug('set_admin called')
        self.admin = admin
        if self.table:
            self.disconnect(self._table_model, QtCore.SIGNAL( 'layoutChanged()' ), self.tableLayoutChanged )
            self.table_layout.removeWidget(self.table)
            self.table.deleteLater()
            self._table_model.deleteLater()
        splitter = self.findChild( QtGui.QWidget, 'splitter' )
        self.table = self.table_widget( splitter )
        self._table_model = self.create_table_model( admin )
        self.table.setModel( self._table_model )
        self.connect( self.table.verticalHeader(),
                      SIGNAL( 'sectionClicked(int)' ),
                      self.sectionClicked )
        self.connect( self._table_model, QtCore.SIGNAL( 'layoutChanged()' ), self.tableLayoutChanged )
        self.tableLayoutChanged()
        self.table_layout.insertWidget( 1, self.table )
    
        def get_filters_and_actions():
            return ( admin.get_filters(), admin.get_list_actions() )
      
        post( get_filters_and_actions,  self.set_filters_and_actions )
        post( admin.get_list_charts, self.setCharts )
    
    @gui_function
    def tableLayoutChanged( self ):
        logger.debug('tableLayoutChanged')
        if self.header:
            self.header.setNumberOfRows( self._table_model.rowCount() )
        item_delegate = self._table_model.getItemDelegate()
        if item_delegate:
            self.table.setItemDelegate( item_delegate )
        for i in range( self._table_model.columnCount() ):
            self.table.setColumnWidth( i, self._table_model.headerData( i, Qt.Horizontal, Qt.SizeHintRole ).toSize().width() )
      
    @gui_function
    def setCharts( self, charts ):
        """creates and display charts"""
        pass
#    if charts:
#
#      from matplotlib.figure import Figure
#      from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as \
#                                                     FigureCanvas
#
#      chart = charts[0]
#
#      def getData():
#        """fetches data for chart"""
#        from sqlalchemy.sql import select, func
#        from elixir import session
#        xcol = getattr( self.admin.entity, chart['x'] )
#        ycol = getattr( self.admin.entity, chart['y'] )
#        session.bind = self.admin.entity.table.metadata.bind
#        result = session.execute( select( [xcol, func.sum( ycol )] ).group_by( xcol ) )
#        summary = result.fetchall()
#        return [s[0] for s in summary], [s[1] for s in summary]
#
#      class MyMplCanvas( FigureCanvas ):
#        """Ultimately, this is a QWidget (as well as a FigureCanvasAgg)"""
#
#        def __init__( self, parent = None, width = 5, height = 4, dpi = 100 ):
#          fig = Figure( figsize = ( width, height ), dpi = dpi, facecolor = 'w' )
#          self.axes = fig.add_subplot( 111, axisbg = 'w' )
#          # We want the axes cleared every time plot() is called
#          self.axes.hold( False )
#          self.compute_initial_figure()
#          FigureCanvas.__init__( self, fig )
#          self.setParent( parent )
#          FigureCanvas.setSizePolicy( self,
#                                     QSizePolicy.Expanding,
#                                     QSizePolicy.Expanding )
#          FigureCanvas.updateGeometry( self )
#
#
#        def compute_initial_figure( self ):
#          pass
#
#      def setData( data ):
#        """set chart data"""
#
#        class MyStaticMplCanvas( MyMplCanvas ):
#          """simple canvas with a sine plot"""
#
#          def compute_initial_figure( self ):
#            """computes initial figure"""
#            x, y = data
#            bar_positions = [i - 0.25 for i in range( 1, len( x ) + 1 )]
#            width = 0.5
#            self.axes.bar( bar_positions, y, width, color = 'b' )
#            self.axes.set_xlabel( 'Year' )
#            self.axes.set_ylabel( 'Sales' )
#            self.axes.set_xticks( range( len( x ) + 1 ) )
#            self.axes.set_xticklabels( [''] + [str( d ) for d in x] )
#
#        sc = MyStaticMplCanvas( self, width = 5, height = 4, dpi = 100 )
#        self.table_layout.addWidget( sc )
#
#      self.admin.mt.post( getData, setData )

    def deleteSelectedRows( self ):
        """delete the selected rows in this tableview"""
        logger.debug( 'delete selected rows called' )
        confirmation_message = self.admin.get_confirm_delete()
        confirmed = True
        if confirmation_message:
            if QtGui.QMessageBox.question(self, 
                                          _('Please confirm'), 
                                          unicode(confirmation_message), 
                                          QtGui.QMessageBox.Yes, 
                                          QtGui.QMessageBox.No) == QtGui.QMessageBox.No:
                confirmed = False
        if confirmed:
            for row in set( map( lambda x: x.row(), self.table.selectedIndexes() ) ):
                self._table_model.removeRow( row )
      
    @gui_function
    def newRow( self ):
        """Create a new row in the tableview"""
        from camelot.view.workspace import get_workspace
        workspace = get_workspace()
        form = self.admin.create_new_view( workspace,
                                           oncreate = lambda o:self._table_model.insertEntityInstance( 0, o ),
                                           onexpunge = lambda o:self._table_model.removeEntityInstance( o ) )
        workspace.addSubWindow( form )
        form.show()

    def closeEvent( self, event ):
        """reimplements close event"""
        logger.debug( 'tableview closed' )
        # remove all references we hold, to enable proper garbage collection
        del self.table_layout
        del self.table
        del self._table_model
        event.accept()  
    
    def selectTableRow( self, row ):
        """selects the specified row"""
        self.table.selectRow( row )
    
    def makeImport(self):
        pass
#        for row in data:
#            o = self.admin.entity()
#            #For example, setattr(x, 'foobar', 123) is equivalent to x.foobar = 123
#            # if you want to import all attributes, you must link them to other objects
#            #for example: a movie has a director, this isn't a primitive like a string
#            # but a object fetched from the db
#            setattr(o, object_attributes[0], row[0])
#            name = row[2].split( ' ' ) #director
#            o.short_description = "korte beschrijving"
#            o.genre = ""
#            from sqlalchemy.orm.session import Session
#            Session.object_session(o).flush([o])
#    
#    post( makeImport )
    
    def selectedTableIndexes( self ):
        """returns a list of selected rows indexes"""
        return self.table.selectedIndexes()
    
    def getColumns( self ):
        """return the columns to be displayed in the table view"""
        return self.admin.get_columns()
    
    def getData( self ):
        """generator for data queried by table model"""
        for d in self._table_model.getData():
            yield d
      
    def getTitle( self ):
        """return the name of the entity managed by the admin attribute"""
        return self.admin.get_verbose_name()
    
    def viewFirst( self ):
        """selects first row"""
        self.selectTableRow( 0 )
    
    def viewLast( self ):
        """selects last row"""
        self.selectTableRow( self._table_model.rowCount() - 1 )
    
    def viewNext( self ):
        """selects next row"""
        first = self.selectedTableIndexes()[0]
        next = ( first.row() + 1 ) % self._table_model.rowCount()
        self.selectTableRow( next )
    
    def viewPrevious( self ):
        """selects previous row"""
        first = self.selectedTableIndexes()[0]
        prev = ( first.row() - 1 ) % self._table_model.rowCount()
        self.selectTableRow( prev )
    
    def _set_query(self, query_getter):
        self._table_model.setQuery(query_getter)
        self.table.clearSelection()
        
    def rebuildQuery( self ):
        """resets the table model query"""
        from filterlist import FilterList
        
        def rebuild_query():
            query = self.admin.entity.query
            query = self.header.decorate_query(query)
            filters = self.findChild(FilterList, 'filters')
            if filters:
                query = filters.decorate_query( query )
            if self.search_filter:
                query = self.search_filter( query )
            query_getter = lambda:query
            return query_getter
      
        post( rebuild_query, self._set_query )
    
    def startSearch( self, text ):
        """rebuilds query based on filtering text"""
        from camelot.view.search import create_entity_search_query_decorator
        logger.debug( 'search %s' % text )
        self.search_filter = create_entity_search_query_decorator( self.admin, text )
        self.rebuildQuery()
    
    def cancelSearch( self ):
        """resets search filtering to default"""
        logger.debug( 'cancel search' )
        self.search_filter = lambda q: q
        self.rebuildQuery()
        
    def get_selection_getter(self):
        """:return: a function that returns all the objects corresponging to the selected rows in the
        table """

        def selection_getter():
            selection = []
            for row in set( map( lambda x: x.row(), self.table.selectedIndexes() ) ):
                selection.append( self._table_model._get_object(row) )
            return selection
        
        return selection_getter
    
    @gui_function
    def set_filters_and_actions( self, filters_and_actions ):
        """sets filters for the tableview"""
        filters, actions = filters_and_actions
        from filterlist import FilterList
        from actionsbox import ActionsBox
        logger.debug( 'setting filters for tableview' )
        filters_widget = self.findChild(FilterList, 'filters')
        if filters_widget:
            self.disconnect( filters_widget, SIGNAL( 'filters_changed' ), self.rebuildQuery )
            self.filters_layout.removeWidget(filters_widget)
            filters_widget.deleteLater()
        if self.actions:
            self.filters_layout.removeWidget(self.actions)
            self.actions.deleteLater()
            self.actions = None
        if filters:
            splitter = self.findChild( QtGui.QWidget, 'splitter' )
            filters_widget = FilterList( filters, parent=splitter )
            filters_widget.setObjectName('filters')
            self.filters_layout.addWidget( filters_widget )
            self.connect( filters_widget, SIGNAL( 'filters_changed' ), self.rebuildQuery )
            #
            # filters might have default values, so we need to rebuild the queries
            #
            self.rebuildQuery()
        if actions:
            selection_getter = self.get_selection_getter()            
            self.actions = ActionsBox( self, 
                                       self._table_model.get_collection_getter(), 
                                       selection_getter )
            
            self.actions.setActions( actions )
            self.filters_layout.addWidget( self.actions )
      
    def to_html( self ):
        """generates html of the table"""
        table = [[getattr( row, col[0] ) for col in self.admin.get_columns()]
                 for row in self.admin.entity.query.all()]
        context = {
          'title': self.admin.get_verbose_name_plural(),
          'table': table,
          'columns': [field_attributes['name'] for _field, field_attributes in self.admin.get_columns()],
        }
        from camelot.view.templates import loader
        from jinja import Environment
        env = Environment( loader = loader )
        tp = env.get_template( 'table_view.html' )
        return tp.render( context )
            
    def importFromFile( self ):
        """"import data : the data will be imported in the activeMdiChild """
        logger.info( 'call import method' )
        from camelot.view.wizard.importwizard import ImportWizard
        wizard = ImportWizard(self, self.admin)
        wizard.exec_()
