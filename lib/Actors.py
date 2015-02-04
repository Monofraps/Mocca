import os
import sys
import platform
import subprocess
from .MessageFormatter import mocca_info, mocca_debug
from .StringInterpolator import interpolate_string

# The OS we're running on will be used to selectively skip dependencies
target_os = sys.platform
target_arch = platform.machine()


class MoccaProject:
    """ Class wrapping business logic on top of the Project model """

    def __init__(self, project_model, project_root):
        self.model = project_model
        self.root = project_root
        self.resolved_variables = {}

        self._resolve_variables()

    def sync_dependencies(self):
        """ Syncs all dependencies in the project """
        for dependency in self.model.dependencies:
            MoccaDependency(dependency, self.root, self.resolved_variables).sync()

    def save(self):
        """ Saves the project's .mocca file """
        file_descriptor = open(os.path.join(self.root, '.mocca'), 'w')
        self.model.to_json_file(file_descriptor)
        file_descriptor.close()

    def _resolve_variables(self):
        """ Tries to resolve all project variables """
        for (key, value) in self.model.variables.items():
            if value == '<(env':
                if key not in os.environ:
                    raise RuntimeError("Unresolved project variable {0}".format(key))

                self.resolved_variables[key] = os.environ[key]


class MoccaDependency:
    """ Class wrapping business logic on top of a project's Dependency model """

    def __init__(self, dependency_model, project_root, variables):
        """
        Creates a dependency wrapper from a Dependency model and the project's root directory
        :param dependency_model: The underlying dependency model
        :param project_root: The directory containing the .mocca file. This is needed to resolve relative paths.
        :param variables: A dict containing resolved project variables
        """
        self._model = dependency_model
        self.root = project_root
        self.project_vars = variables

        if os.path.isabs(self._get_model_path()):
            self.abs_path = self._get_model_path()
        else:
            self.abs_path = os.path.abspath(os.path.join(self.root, self._get_model_path()))

        self.branch = self._get_model_branch()
        if not self.branch:
            if self._get_model_vcs() == 'git':
                self.branch = 'master'
            elif self._get_model_vcs() == 'hg':
                self.branch = 'default'

    def sync(self):
        """ Syncs the dependency """
        mocca_debug("Target OS: {0}:{1}".format(target_os, target_arch))
        if not len(self._model.target_os) == 0:
            is_target_os = False
            for tos in self._model.target_os:
                if tos.split(':')[0] != target_os:
                    continue
                if ':' in tos and tos.split(':')[1] != target_arch:
                    continue
                is_target_os = True
            if not is_target_os:
                mocca_info("Skipping {0} because target os requirement not met".format(self._model.path))
                return

        if not os.path.exists(self.abs_path):
            os.makedirs(self.abs_path)

        if not os.access(self.abs_path, os.W_OK):
            raise RuntimeError("Cannot write to {0}".format(self.abs_path))

        if self.is_cloned():
            self.pull()
        else:
            self.clone()

    def is_cloned(self):
        """ Checks whether the dependency's repo has already been cloned (i.e. whether a clone or pull is necessary)"""
        if self._model.vcs == 'git':
            return os.path.isdir(os.path.join(self.abs_path, '.git'))
        elif self._model.vcs == 'hg':
            return os.path.isdir(os.path.join(self.abs_path, '.hg'))

    def pull(self):
        """ Performs a pull """
        print("")
        mocca_info("Pulling updates from {0} {1} into {2}"
                   .format(self._get_model_url(), self.branch, self._get_model_path()))

        args = []
        if self._model.vcs == 'git':
            args += ['git', 'pull']
        elif self._model.vcs == 'hg':
            args += ['hg', 'pull']

        mocca_debug(self.abs_path)
        mocca_info(' '.join(args))
        subprocess.Popen(args, cwd=self.abs_path).wait()

        self.post_pull()

    def post_pull(self):
        """ Performs post-pull operations (i.e. branch/tag checkouts """
        print("")
        mocca_info("Running post-pull actions for {0} {1}"
                   .format(self._get_model_path(), self.branch))

        args = []
        if self._model.vcs == 'git':
            args += ['git', 'checkout', self.branch]
        elif self._model.vcs == 'hg':
            args += ['hg', 'up', self.branch]

        mocca_debug(self.abs_path)
        mocca_info(' '.join(args))
        subprocess.Popen(args, cwd=self.abs_path).wait()

    def clone(self):
        """ Performs a clone """
        print("")
        mocca_info("Cloning {0} {1} into {2}".format(self._get_model_url(), self.branch, self._get_model_path()))

        args = []
        if self._model.vcs == 'git':
            args += ['git', 'clone', self._get_model_url(), '--branch', self.branch, '--single-branch', self.abs_path]
        elif self._model.vcs == 'hg':
            args += ['hg', 'clone', '-r', self.branch, self._get_model_url(), self.abs_path]

        mocca_debug(self.abs_path)
        mocca_info(' '.join(args))
        subprocess.check_call(args)

    def _get_model_branch(self):
        return interpolate_string(self._model.branch, self.project_vars)

    def _get_model_vcs(self):
        return interpolate_string(self._model.vcs, self.project_vars)

    def _get_model_path(self):
        return interpolate_string(self._model.path, self.project_vars)

    def _get_model_url(self):
        return interpolate_string(self._model.url, self.project_vars)
