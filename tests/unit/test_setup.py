from os.path import (
    abspath,
    dirname,
    isfile,
    join,
)
from shutil import rmtree
from subprocess import (
    call, DEVNULL
)
from unittest import TestCase

from w2re import (
    APPLICATION_NAME,
    __version__ as app_version,
)

SOURCES_ROOT = abspath(join(dirname(__file__), '..', '..'))

BUILD_ARTEFACTS = [
    join(SOURCES_ROOT, folder)
    for folder in ['dist', 'build', APPLICATION_NAME + '.egg-info']
]


def cleanup_build_artefacts():
    for folder in BUILD_ARTEFACTS:
        rmtree(folder, ignore_errors=True)


class BuildProcess(TestCase):
    def setUp(self):
        cleanup_build_artefacts()
        self._build_return_code = call(
            ['python', 'setup.py', 'sdist', 'bdist_wheel'],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )

    def tearDown(self):
        cleanup_build_artefacts()

    def test_it_builds_sources(self):
        self.assertEqual(0, self._build_return_code)

    def assert_file_is_build(self, suffix):
        filename = join(
            BUILD_ARTEFACTS[0],
            '{}-{}{}'.format(APPLICATION_NAME, app_version, suffix)
        )

        self.assertTrue(
            isfile(filename),
            msg="File '{}' does not exist or is not a file.".format(filename)
        )

    def test_it_creates_whl_file(self):
        self.assert_file_is_build('-py3-none-any.whl')

    def test_it_creates_tar_file(self):
        self.assert_file_is_build('.tar.gz')
