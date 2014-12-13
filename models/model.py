import json


class Model:
    def to_json_string(self):
        return json.dumps(self, cls=_Encoder, indent=2)

    def to_json_file(self, file):
        json.dump(self, file, cls=_Encoder, indent=2)

    @classmethod
    def from_json_string(cls, json_str):
        return cls.from_json(json.loads(json_str))

    @classmethod
    def from_json_file(cls, file):
        return cls.from_json(json.load(file))

    @staticmethod
    def from_json(json_obj):
        raise NotImplementedError

    def to_object(self):
        raise NotImplementedError


class _Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return o.to_object()

        return json.JSONEncoder.default(self, o)
