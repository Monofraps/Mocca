import unittest
from os import path
from lib.DotMoccaGrabber import FindMoccaFile, ValidateMoccaFile

SCRIPT_DIR = path.dirname(path.realpath(__file__))
PROJECT_DIR = path.abspath(path.join(SCRIPT_DIR, 'project'))
SECOND_LEVEL_DIR = path.abspath(path.join(PROJECT_DIR, 'second_level_dir'))


class MoccaFinderTests(unittest.TestCase):
    def test_finds_mocca_file_in_same_directory(self):
        mocca_file = FindMoccaFile(PROJECT_DIR)
        self.assertEqual(path.join(PROJECT_DIR, '.mocca'), mocca_file, 'Returned path for .mocca file is incorrect')

    def test_finds_mocca_file_from_subdirectory(self):
        mocca_file = FindMoccaFile(SECOND_LEVEL_DIR)
        self.assertEqual(path.join(PROJECT_DIR, '.mocca'), mocca_file, 'Returned path for .mocca file is incorrect')
