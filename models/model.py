import json


class Model:
    def ToJsonString(self):
        return json.dumps(self, cls=_Encoder, indent=2)

    def ToJsonFile(self, file):
        json.dump(self, file, cls=_Encoder, indent=2)

    @classmethod
    def FromJsonString(cls, json_str):
        return cls.FromJson(json.loads(json_str))

    @classmethod
    def FromJsonFile(cls, file):
        return cls.FromJson(json.load(file))

    @staticmethod
    def FromJson(json_obj):
        raise NotImplementedError

    def ToObject(self):
        raise NotImplementedError


class _Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return o.ToObject()

        return json.JSONEncoder.default(self, o)
