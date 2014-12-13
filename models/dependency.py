from .model import Model


class Dependency(Model):
    def __init__(self):
        self.path = ''
        self.url = ''
        self.vcs = ''
        self.branch = ''
        self.target_os = _TargetOsList()

    def ToObject(self):
        return {'path': self.path, 'url': self.url, 'vcs': self.vcs, 'branch': self.branch, 'target_os': self.target_os}

    @staticmethod
    def FromJson(json_obj):
        dependency = Dependency()
        dependency.path = json_obj['path']
        dependency.url = json_obj['url']
        dependency.vcs = json_obj['vcs']

        if 'branch' in json_obj:
            dependency.branch = json_obj['branch']

        dependency.target_os = json_obj['target_os']

        return dependency

    def __eq__(self, other):
        return self.path == other.path and self.url == other.url and self.target_os == other.target_os and self.vcs == other.vcs and self.branch == other.branch


class _TargetOsList(list):
    def add(self, target_os):
        super(_TargetOsList, self).append(target_os)
