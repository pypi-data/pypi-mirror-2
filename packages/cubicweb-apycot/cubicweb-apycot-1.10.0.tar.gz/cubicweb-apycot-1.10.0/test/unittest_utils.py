from logilab.common.testlib import TestCase, unittest_main

from cubes.apycot.entities import text_to_dict

class TextToDictTC(TestCase):
    def test_multiple(self):
        self.assertEquals(text_to_dict('''muloption=1
muloption= 2
single= hop
'''),
                          {'muloption': ['1', '2'],
                           'single': 'hop'})

if __name__ == '__main__':
    unittest_main()
