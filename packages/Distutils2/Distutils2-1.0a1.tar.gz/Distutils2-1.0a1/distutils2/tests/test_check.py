"""Tests for distutils.command.check."""
import unittest2

from distutils2.command.check import check
from distutils2.metadata import _HAS_DOCUTILS
from distutils2.tests import support
from distutils2.errors import DistutilsSetupError

class CheckTestCase(support.LoggingSilencer,
                    support.TempdirManager,
                    unittest2.TestCase):

    def _run(self, metadata=None, **options):
        if metadata is None:
            metadata = {}
        pkg_info, dist = self.create_dist(**metadata)
        cmd = check(dist)
        cmd.initialize_options()
        for name, value in options.items():
            setattr(cmd, name, value)
        cmd.ensure_finalized()
        cmd.run()
        return cmd

    def test_check_metadata(self):
        # let's run the command with no metadata at all
        # by default, check is checking the metadata
        # should have some warnings
        cmd = self._run()
        self.assert_(len(cmd._warnings) > 0)

        # now let's add the required fields
        # and run it again, to make sure we don't get
        # any warning anymore
        metadata = {'home_page': 'xxx', 'author': 'xxx',
                    'author_email': 'xxx',
                    'name': 'xxx', 'version': 'xxx'
                    }
        cmd = self._run(metadata)
        self.assertEquals(len(cmd._warnings), 0)

        # now with the strict mode, we should
        # get an error if there are missing metadata
        self.assertRaises(DistutilsSetupError, self._run, {}, **{'strict': 1})

        # and of course, no error when all metadata are present
        cmd = self._run(metadata, strict=1)
        self.assertEquals(len(cmd._warnings), 0)

    def test_check_restructuredtext(self):
        if not _HAS_DOCUTILS: # won't test without docutils
            return
        # let's see if it detects broken rest in long_description
        broken_rest = 'title\n===\n\ntest'
        pkg_info, dist = self.create_dist(description=broken_rest)
        cmd = check(dist)
        cmd.check_restructuredtext()
        self.assertEquals(len(cmd._warnings), 1)

        # let's see if we have an error with strict=1
        metadata = {'home_page': 'xxx', 'author': 'xxx',
                    'author_email': 'xxx',
                    'name': 'xxx', 'version': 'xxx',
                    'description': broken_rest}

        self.assertRaises(DistutilsSetupError, self._run, metadata,
                          **{'strict': 1, 'restructuredtext': 1})

        # and non-broken rest
        metadata['description'] = 'title\n=====\n\ntest'
        cmd = self._run(metadata, strict=1, restructuredtext=1)
        self.assertEquals(len(cmd._warnings), 0)

    def test_check_all(self):

        metadata = {'home_page': 'xxx', 'author': 'xxx'}
        self.assertRaises(DistutilsSetupError, self._run,
                          {}, **{'strict': 1,
                                 'restructuredtext': 1})

def test_suite():
    return unittest2.makeSuite(CheckTestCase)

if __name__ == "__main__":
    unittest2.main(defaultTest="test_suite")
