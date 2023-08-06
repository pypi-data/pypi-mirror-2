import unittest

class Test_warn_deprecation(unittest.TestCase):
    def setUp(self):
        import warnings
        self.oldwarn = warnings.warn
        warnings.warn = self._warn
        self.warnings = []

    def tearDown(self):
        import warnings
        warnings.warn = self.oldwarn
        del self.warnings
        
    def _callFUT(self, text, version, stacklevel):
        from webob.util import warn_deprecation
        return warn_deprecation(text, version, stacklevel)

    def _warn(self, text, type, stacklevel=1):
        self.warnings.append(locals())

    def test_not_1_2(self):
        self._callFUT('text', 'version', 1)
        self.assertEqual(len(self.warnings), 2)
        unknown_version_warning = self.warnings[0]
        self.assertEqual(unknown_version_warning['text'],
                         "Unknown warn_deprecation version arg: 'version'")
        self.assertEqual(unknown_version_warning['type'], RuntimeWarning)
        self.assertEqual(unknown_version_warning['stacklevel'], 1)
        deprecation_warning = self.warnings[1]
        self.assertEqual(deprecation_warning['text'], 'text')
        self.assertEqual(deprecation_warning['type'], DeprecationWarning)
        self.assertEqual(deprecation_warning['stacklevel'], 2)
        
    def test_is_1_2(self):
        self._callFUT('text', '1.2', 1)
        self.assertEqual(len(self.warnings), 1)
        deprecation_warning = self.warnings[0]
        self.assertEqual(deprecation_warning['text'], 'text')
        self.assertEqual(deprecation_warning['type'], DeprecationWarning)
        self.assertEqual(deprecation_warning['stacklevel'], 2)
        
    
