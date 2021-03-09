import json
from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            def field_filter(_x):
                return not _x.startswith('_') and not _x.startswith('query') and _x != 'metadata'
            for field in [x for x in dir(o) if field_filter(x)]:
                data = o.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        if isinstance(o, list):
            return [json.dumps(e, cls=AlchemyEncoder) for e in o]

        return json.JSONEncoder.default(self, o)
