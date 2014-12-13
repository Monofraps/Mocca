import os
from .dependency import Dependency
from .model import Model


class Project(Model):
    def __init__(self):
        self.dependencies = _ProjectDependencies()
        self.variables = _ProjectVariables()

    def to_object(self):
        representation = {'dependencies': self.dependencies}

        if len(self.variables) > 0:
            representation.update(dict(variables=self.variables))

        return representation

    @staticmethod
    def from_json(json_obj):
        project = Project()

        for dep in json_obj['dependencies']:
            project.dependencies.append(Dependency.from_json(dep))

        if 'variables' in json_obj:
            for (key, value) in json_obj['variables'].items():
                project.variables.add(key, value)

        return project

    def __eq__(self, other):
        return self.dependencies == other.dependencies


class _ProjectDependencies(list):
    def add(self):
        dependency = Dependency()
        super().append(dependency)

        return dependency


class _ProjectVariables(dict):
    def add(self, variable, value):
        super().update({variable: value})

        return value


