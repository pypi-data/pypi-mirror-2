#!/opt/prod/bin/python

import unittest
from Preferences import Preferences

class TestPreferences(unittest.TestCase):


    def setUp(self):
        self.base_prefs = Preferences()

    def testAdd(self):
        self.base_prefs.add({'pref1': 'Preference One', 
                'pref2': 'Preference Two'})
        self.assertEqual({'pref1':'Preference One','pref2':'Preference Two'},
            self.base_prefs.params[0])
        self.base_prefs.add({'test': 'Preference test'})
        self.assertEqual({'test': 'Preference test'}, 
            self.base_prefs.params[1])
        self.base_prefs.add({'test': 'Preference test Two'})
        self.assertEqual({'test': 'Preference test Two'},
            self.base_prefs.params[2])

    def testGet(self):
        self.assertEqual(self.base_prefs.get('Missing Key'),'')
        self.assertEqual(self.base_prefs.get('pref1'), 'Preference One')
        self.assertEqual(self.base_prefs.get('test'),
            ['Preference test', 'Preference test Two'])

    def testGetCSV(self):
        self.assertEqual(self.base_prefs.get_csv('test'),
                'Preference test, Preference test Two')
        self.assertEqual(self.base_prefs.get_csv('pref1'), 'Preference One')
        self.assertEqual(self.base_prefs.get_csv('junk'), '')

    def testHas(self):
        self.assertTrue(self.base_prefs.has('pref1', 'Preference One'))
        self.assertTrue(self.base_prefs.has('pref2', 'Preference Two'))
        self.assertFalse(self.base_prefs.has('pref3', 'Preference Three'))

    def testHasPref(self):
        self.assertTrue(self.base_prefs.has_pref('pref1'))
        self.assertTrue(self.base_prefs.has_pref('pref2'))
        self.assertFalse(self.base_prefs.has_pref('pref3'))

    def testReplaceKey(self):
        self.base_prefs.replace_key('repadd', 'Replace Test Add')
        self.assertEqual(self.base_prefs.get('repadd'), 'Replace Test Add')
        self.base_prefs.replace_key('repadd', 'Replaced')
        self.assertEqual(self.base_prefs.get('repadd'), 'Replaced')

    def testReadFile(self):
        try:
           self.base_prefs.read_file('test.prf')
        except ValueError as e:
           if e.__str__() == 'Invalid line format on 19.':
               pass
           else:
               self.fail("Wrong ValueError: %s" % e)
        else:
           self.fail("Didn't raise ValueError")
        self.assertEqual(self.base_prefs.get('p2'),[':p2','p2_2'])
        self.assertEqual(self.base_prefs.get('p3'),':dog:')
        self.assertEqual(self.base_prefs.get('p4'),'1\n2\n3')
        self.assertEqual(self.base_prefs.get('p6'),['p6','p6','p6'])
        self.assertEqual(self.base_prefs.get_csv('p2'), ':p2, p2_2')

if __name__ == '__main__':
    unittest.main()
