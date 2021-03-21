import json
from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyJSON:
    def json(self, as_string=False):
        serialized_json = json.dumps(self, cls=AlchemyEncoder)
        if as_string:
            return serialized_json
        return json.loads(serialized_json)

class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            def field_filter(_x):
                return not _x.startswith('_') \
                    and not _x.startswith('query') \
                    and _x not in ['senha', 'metadata', 'registry', 'json']

            for field in [x for x in dir(o) if field_filter(x)]:
                try:
                    data = o.__getattribute__(field)
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        if isinstance(o, list):
            return [json.loads(json.dumps(e, cls=AlchemyEncoder)) for e in o]

        return json.JSONEncoder.default(self, o)
