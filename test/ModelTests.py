import os
import unittest
from models.project import Project, _ProjectVariables
from models.dependency import Dependency

TEST_DEP = Dependency()
TEST_DEP.path = 'a/very/cool/path'
TEST_DEP.url = 'an/even/cooler/url'
TEST_DEP.vcs = 'hg'
TEST_DEP.branch = 'default'
TEST_DEP.target_os.add('cool_os')

TEST_PROJ1 = Project()
TEST_PDEP1 = TEST_PROJ1.dependencies.add()
TEST_PDEP1.path = 'a/very/cool/path'
TEST_PDEP1.url = 'an/even/cooler/url'
TEST_PDEP1.vcs = 'git'
TEST_PDEP1.branch = 'master'
TEST_PDEP1.target_os.add('cool_os')

TEST_PROJ2 = Project()
TEST_PROJ2.variables.add('testvar', 'somevalue')
TEST_PDEP2 = TEST_PROJ1.dependencies.add()
TEST_PDEP2.path = 'a/very/cool/path'
TEST_PDEP2.url = 'an/even/cooler/url'
TEST_PDEP2.vcs = 'git'
TEST_PDEP2.branch = 'master'
TEST_PDEP2.target_os.add('cool_os')


class ModelTests(unittest.TestCase):
    def check_dependency_dict_equality(self, dep_dict, template):
        self.assertIsInstance(dep_dict, dict, "Dictionary.ToObject didn't return a dict")

        self.assertEqual(dep_dict['path'], template.path)
        self.assertEqual(dep_dict['url'], template.url)
        self.assertEqual(dep_dict['vcs'], template.vcs)
        self.assertEqual(dep_dict['branch'], template.branch)

        self.assertIsInstance(dep_dict['target_os'], list, "Dictionary.ToObject['target_os'] is not a list")
        self.assertListEqual(dep_dict['target_os'], template.target_os)

    def check_project_dict_equality(self, proj_dict, template):
        self.assertIsInstance(proj_dict, dict, "Project.ToObject didn't return a dict")

        self.assertIsInstance(proj_dict['dependencies'], list, "Project.ToObject['dependencies'] is not a list")
        self.assertListEqual(proj_dict['dependencies'], template.dependencies)

        if len(template.variables) > 0:
            self.assertIsInstance(proj_dict['variables'], dict, "Project.ToObject['variables'] it not a dict")
            self.assertDictEqual(proj_dict['variables'], template.variables)
        else:
            self.assertNotIn('variables', proj_dict.keys(),
                             "Project.ToObject generates 'variables' entry in dict even though there are no variables "
                             "in the model")

    def test_transform_dependency_into_dictionary(self):
        dep_dict = TEST_DEP.to_object()
        self.check_dependency_dict_equality(dep_dict, TEST_DEP)

    def test_transform_project_into_dictionary(self):
        proj_dict = TEST_PROJ1.to_object()
        self.check_project_dict_equality(proj_dict, TEST_PROJ1)

        proj_dict = TEST_PROJ2.to_object()
        self.check_project_dict_equality(proj_dict, TEST_PROJ2)

    def test_dependency_json_transformation(self):
        json_string = TEST_DEP.to_json_string()
        json_loaded_dep = Dependency.from_json_string(json_string)

        self.assertEqual(json_loaded_dep, TEST_DEP)

    def test_project_json_transformation(self):
        json_string = TEST_PROJ1.to_json_string()
        json_loaded_proj = Project.from_json_string(json_string)

        self.assertEqual(json_loaded_proj, TEST_PROJ1)
