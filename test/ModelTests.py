import unittest
from models.project import Project
from models.dependency import Dependency

TEST_DEP = Dependency()
TEST_DEP.path = 'a/very/cool/path'
TEST_DEP.url = 'an/even/cooler/url'
TEST_DEP.vcs = 'hg'
TEST_DEP.branch = 'default'
TEST_DEP.target_os.add('cool_os')

TEST_PROJ = Project()
TEST_PDEP = TEST_PROJ.dependencies.add()
TEST_PDEP.path = 'a/very/cool/path'
TEST_PDEP.url = 'an/even/cooler/url'
TEST_PDEP.vcs = 'git'
TEST_PDEP.branch = 'master'
TEST_PDEP.target_os.add('cool_os')


class ModelTests(unittest.TestCase):
    def check_dependency_dict_equality(self, dep_dict, template):
        self.assertIsInstance(dep_dict, dict, "Dictionary.ToObject didn't return a dict")

        self.assertEqual(dep_dict['path'], template.path)
        self.assertEqual(dep_dict['url'], template.url)
        self.assertEqual(dep_dict['vcs'], template.vcs)
        self.assertEqual(dep_dict['branch'], template.branch)

        self.assertIsInstance(dep_dict['target_os'], list, 'Dictionary.ToObject["target_os"] is not a list')
        self.assertListEqual(dep_dict['target_os'], template.target_os)

    def check_project_dict_equality(self, proj_dict, template):
        self.assertIsInstance(proj_dict, dict, "Project.ToObject didn't return a dict")

        self.assertIsInstance(proj_dict['dependencies'], list, 'Project.ToObject["dependencies]" is not a list')
        self.assertListEqual(proj_dict['dependencies'], template.dependencies)

    def test_transform_dependency_into_dictionary(self):
        dep_dict = TEST_DEP.ToObject()
        self.check_dependency_dict_equality(dep_dict, TEST_DEP)

    def test_transform_project_into_dictionary(self):
        proj_dict = TEST_PROJ.ToObject()
        self.check_project_dict_equality(proj_dict, TEST_PROJ)

    def test_dependency_json_transformation(self):
        json_string = TEST_DEP.ToJsonString()
        json_loaded_dep = Dependency.FromJsonString(json_string)

        self.assertEqual(json_loaded_dep, TEST_DEP)

    def test_project_json_transformation(self):
        json_string = TEST_PROJ.ToJsonString()
        json_loaded_proj = Project.FromJsonString(json_string)

        self.assertEqual(json_loaded_proj, TEST_PROJ)
