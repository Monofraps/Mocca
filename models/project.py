from .dependency import Dependency
from .model import Model


class Project(Model):
    def __init__(self):
        self.dependencies = _ProjectDependencies()

    def ToObject(self):
        return {'dependencies': self.dependencies}

    @staticmethod
    def FromJson(json_obj):
        project = Project()

        for dep in json_obj['dependencies']:
            project.dependencies.append(Dependency.FromJson(dep))

        return project

    def __eq__(self, other):
        return self.dependencies == other.dependencies


class _ProjectDependencies(list):
    def add(self):
        dependency = Dependency()
        super(_ProjectDependencies, self).append(dependency)

        return dependency
