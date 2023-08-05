# -*- coding: utf8 -*-

import logging

logger = logging.getLogger( 'camelot.core.files.storage' )

from camelot.view.model_thread import model_function

class StoredFile( object ):
    """Helper class for the File field type.
    Stored file objects can be used within the GUI thread, as none of
    its methods should block.
    """

    def __init__( self, storage, name ):
        """
    :param storage: the storage in which the file is stored
    :param name: the key by which the file is known in the storage"""
        self.storage = storage
        self.name = name

    @property
    def verbose_name( self ):
        """The name of the file, as it is to be displayed in the GUI"""
        return self.name

    def __unicode__( self ):
        return self.verbose_name

class StoredImage( StoredFile ):
    """Helper class for the Image field type Class linking an image and the
    location and filename where the image is stored"""

    @model_function
    def checkout_image( self ):
        """Checkout the image from the storage, and return a QImage"""
        from PyQt4.QtGui import QImage
        p = self.storage.checkout( self )
        return QImage( p )

    @model_function
    def checkout_thumbnail( self, width, height ):
        """Checkout a thumbnail for this image form the storage
        :return: a QImage"""
        from PyQt4.QtCore import Qt
        original_image = self.checkout_image()
        return original_image.scaled( width, height, Qt.KeepAspectRatio )

class Storage( object ):
    """Helper class that opens and saves StoredFile objects
  The default implementation stores files in the settings.CAMELOT_MEDIA_ROOT
  directory.  The storage object should only be used within the model thread,
  as all of it's methods might block.

  The methods of this class don't verify if they are called on the model
  thread, because these classes can be used on the server as well.
    """

    def __init__( self, upload_to = '', stored_file_implementation = StoredFile ):
        """
    :param upload_to: the sub directory in which to put files
    :param stored_file_implementation: the subclass of StoredFile to be used when
    checking out files from the storage
    """
        import settings
        import os
        self.upload_to = os.path.join( settings.CAMELOT_MEDIA_ROOT, upload_to )
        self.stored_file_implementation = stored_file_implementation
        #
        # don't do anything here that might reduce the startup time, like verifying the
        # availability of the storage, sinde the path might be on a slow network share
        #

    def available(self):
        """Verify if the storage is available 
        """
        import os
        try:
            if not os.path.exists( self.upload_to ):
                os.makedirs( self.upload_to )
            return True
        except Exception, e:
            logger.warn( 'Could not access or create path %s, files will be unreachable' % self.upload_to, exc_info = e )
        return False
    
    def exists( self, name ):
        """True if a file exists given some name"""
        if self.available():
            import os
            os.path.exists( self.path( name ) )
        return False
        
    def list(self, prefix='*', suffix='*'):
        """Lists all files with a given prefix and or suffix available in this storage
        :return: a iterator of StoredFile objects
        """
        import glob
        import os
        return (StoredFile(self, name) for name in glob.glob( os.path.join( self.upload_to, u'%s*%s'%(prefix, suffix) ) ) )

    def path( self, name ):
        """The local filesystem path where the file can be opened using Python’s standard open"""
        import os
        return os.path.join( self.upload_to, name )

    def checkin( self, local_path ):
        """Check the file pointed to by local_path into the storage, and
        return a StoredFile"""
        self.available()
        import tempfile
        import shutil
        import os
        root, extension = os.path.splitext( os.path.basename( local_path ) )
        ( handle, to_path ) = tempfile.mkstemp( suffix = extension, prefix = root, dir = self.upload_to, text = 'b' )
        os.close( handle )
        logger.debug( u'copy file from %s to %s', local_path, to_path )
        shutil.copy( local_path, to_path )
        return self.stored_file_implementation( self, os.path.basename( to_path ) )

    def checkin_stream( self, prefix, suffix, stream ):
        """Check the datastream in as a file into the storage
        :param prefix: the prefix to use for generating a file name
        :param suffix: the suffix to use for generating a filen name, eg '.png'
        :return: a StoredFile"""
        self.available()
        import tempfile
        import os
        ( handle, to_path ) = tempfile.mkstemp( suffix = suffix, prefix = prefix, dir = self.upload_to, text = 'b' )
        file = os.fdopen( handle, 'wb' )
        file.write( stream.read() )
        file.flush()
        file.close()
        return self.stored_file_implementation( self, os.path.basename( to_path ) )

    def checkout( self, stored_file ):
        """Check the file pointed to by the local_path out of the storage and return
    a local filesystem path where the file can be opened"""
        self.available()
        import os
        return os.path.join( self.upload_to, stored_file.name )

    def checkout_stream( self, stored_file ):
        """Check the file stored_file out of the storage as a datastream
        :return: a file object
        """
        self.available()
        import os
        return open( os.path.join( self.upload_to, stored_file.name ), 'rb' )

    def delete( self, name ):
        pass

class S3Storage( object ):
    """Helper class that opens and saves StoredFile objects into Amazon S3.

    these attibutes need to be set in your settings for S3Storage to work :
     * AWS_ACCESS_KEY_ID = '<INSERT YOUR AWS ACCESS KEY ID HERE>'
     * AWS_SECRET_ACCESS_KEY = '<INSERT YOUR AWS SECRET ACCESS KEY HERE>'
     * AWS_BUCKET_NAME = 'camelot'
     * AWS_LOCATION = S3.Location.DEFAULT
     
    Using this Storage requires the availability of S3.py on your PYTHONPATH.
    S3.py can be found on the amazon.com website
    """

    def __init__( self, upload_to = '', stored_file_implementation = StoredFile ):
        # try to work around bug S3 code which uses bad names of days
        # http://code.google.com/p/boto/issues/detail?id=140
        # but workaround doesn't work :(
        #import locale
#    locale.setlocale(locale.LC_TIME, 'en_US.utf8')
#    print 'create S3 storage'
        import settings
        import S3
        self.upload_to = upload_to
        conn = S3.AWSAuthConnection( settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY )
#        _generator = S3.QueryStringAuthGenerator( settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY )
        if ( conn.check_bucket_exists( settings.AWS_BUCKET_NAME ).status == 200 ):
            pass
        else:
            conn.create_located_bucket( settings.AWS_BUCKET_NAME, settings.AWS_LOCATION ).message
