# test spaces in hierarchy
# test tabs in hierarchy
# test mixed
import unittest, os
from categories.models import Category
from categories.management.commands.import_categories import Command

class CategoryImportTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def _import_file(self, filename):
        root_cats = ['Category 1', 'Category 2', 'Category 3']
        testfile = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fixtures', filename))
        cmd = Command()
        cmd.execute(testfile)
        roots = Category.tree.root_nodes()
        
        self.assertEqual(len(roots), 3)
        for item in roots:
            assert item.name in root_cats
        
        cat2 = Category.objects.get(name='Category 2')
        cat21 = cat2.children.all()[0]
        self.assertEqual(cat21.name, 'Category 2-1')
        cat211 = cat21.children.all()[0]
        self.assertEqual(cat211.name, 'Category 2-1-1')
    
    
    def testImportSpaceDelimited(self):
        self._import_file('test_category_spaces.txt')
    
    
    def testImportTabDelimited(self):
        self._import_file('test_category_tabs.txt')
    
    
    def testMixingTabsSpaces(self):
        """
        Should raise an exception.
        """
        string1 = "cat1\n    cat1-1\n\tcat1-2-FAIL!\n"
        string2 = "cat1\n\tcat1-1\n    cat1-2-FAIL!\n"
        cmd = Command()
        
        # raise Exception
        self.assertRaises(cmd.parse_lines(string1), Command.CommandError)
        self.assertRaises(cmd.parse_lines(string2), Command.CommandError)
        