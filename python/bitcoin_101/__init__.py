import decimal
import json


def bitjson_dumps(x):
    return json.dumps(x, indent=3, cls=_DecimalJSONEncoder)


def bitjson_loads(x):
    return json.loads(x, parse_float=decimal.Decimal)


def bitprint(*a, **kw):
    print(*(_jsonize(x) for x in a), **{k: _jsonize(v) for k, v in kw.items()})


def _jsonize(x):
    return bitjson_dumps(x) if isinstance(x, dict) else x


class _DecimalJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(_DecimalJSONEncoder, self).default(o)
