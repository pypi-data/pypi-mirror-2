# python
import os, sys

# zope
from DateTime import DateTime

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestFolderContentsWidgetView( AnzDashBoardTestCase ):
    
    def afterSetUp( self ):
        now = DateTime()
        
        # the day before yesterday
        date = now - 2
        self.folder.invokeFactory( type_name='Folder',
                                   id='folder1', title='folder 1' )
        self.folder1 = self.folder.folder1
        self.folder1.setModificationDate( date )
        self.folder1.setCreationDate( date )
        self.folder1.indexObject()
        
        self.folder1.invokeFactory( type_name='Document',
                                    id='doc1', title='doc 1' )
        self.doc1 = self.folder1.doc1
        self.doc1.setModificationDate( date )
        self.doc1.setCreationDate( date )
        self.doc1.indexObject()
        
        # yesterday
        date = now - 1
        self.folder.invokeFactory( type_name='Folder',
                                   id='folder2', title='folder 2' )
        self.folder2 = self.folder.folder2
        self.folder2.setModificationDate( date )
        self.folder2.setCreationDate( date )
        self.folder2.indexObject()
        
        self.folder2.invokeFactory( type_name='News Item',
                                    id='news1', title='news 1' )
        self.news1 = self.folder2.news1
        self.news1.setModificationDate( date )
        self.news1.setCreationDate( date )
        self.news1.indexObject()
        
        # now
        self.folder.invokeFactory( type_name='Anz Dashboard',
                                   id='dashboard1', title='dashboard 1' )
        self.folder.dashboard1.indexObject()
    
    def test_viewApplied( self ):
        view = self.doc1.restrictedTraverse( '@@folderContentsWidget', None )
        self.assert_( view is None )
        
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@folderContentsWidget', None )
        self.assert_( view is not None )
    
    def test_items( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@folderContentsWidget', None )
        
        folderPath = '/'.join( self.folder.getPhysicalPath() )
        folder1Path = '/'.join( self.folder1.getPhysicalPath() )
        folder2Path = '/'.join( self.folder2.getPhysicalPath() )
        
        # test paths
        ret = view.items( paths=[folder1Path],
                          retJson=False )
        self.assertEqual( 1, len(ret['items']) )
        
        ret = view.items( paths=[folder1Path,folder2Path],
                          retJson=False )
        self.assertEqual( 2, len(ret['items']) )
        
        # test searchSub
        ret = view.items( paths=[folder1Path],
                          searchSub=True,
                          retJson=False )
        self.assertEqual( 2, len(ret['items']) )
        
        ret = view.items( paths=[folder1Path,folder2Path],
                          searchSub=True,
                          retJson=False )
        self.assertEqual( 4, len(ret['items']) )
        
        # test types
        ret = view.items( paths=[folder1Path],
                          portal_types=['Document','News Item'],
                          retJson=False )
        self.assertEqual( 1, len(ret['items']) )
        
        ret = view.items( paths=[folderPath],
                          searchSub=True,
                          portal_types='Document,News Item',
                          retJson=False )
        self.assertEqual( 2, len(ret['items']) )
        
        # test recent days
        ret = view.items( paths=[folderPath],
                          searchSub=True,
                          recentDays=0,
                          retJson=False )
        self.assertEqual( 6, len(ret['items']) )
        
        ret = view.items( paths=[folderPath],
                          searchSub=True,
                          recentDays=1,
                          retJson=False )
        self.assertEqual( 4, len(ret['items']) )
        
        ret = view.items( paths=[folderPath],
                          searchSub=True,
                          recentDays=2,
                          retJson=False )
        self.assertEqual( 6, len(ret['items']) )
        
        # test limit
        ret = view.items( paths=[folderPath],
                          searchSub=True,
                          sort_limit=2,
                          retJson=False )
        self.assertEqual( 2, len(ret['items']) )

    def test_types( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@folderContentsWidget', None )
        ret = view.types( retJson=False )
        self.assertEqual( ret['success'], True )
        self.assert_( len(ret['types']) > 1 )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest( makeSuite(TestFolderContentsWidgetView) )
    return suite

if  __name__ == '__main__':
    framework()
