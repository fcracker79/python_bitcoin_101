import itertools
import typing
from pprint import pprint


def full_join(d1: typing.Optional[dict], d2: typing.Optional[dict]) -> typing.Optional[dict]:
    if d1 is None or d2 is None:
        return None
    return {k: d1.get(k, d2.get(k)) for k in itertools.chain(d1, d2)}


def left_join(d1: typing.Optional[dict], d2: typing.Optional[dict]) -> typing.Optional[dict]:
    if d1 is None:
        return None
    if d2 is None:
        return d1
    return full_join(d1, d2)


def aggregate(
        g: typing.Iterator[dict],
        extract_key: typing.Callable[[typing.Dict], str]) -> typing.Iterator[typing.List[dict]]:
    last_values = last_key = []
    for e in g:
        if not last_values:
            last_values, last_key = [e], extract_key(e)
        elif last_key == extract_key(e):
            last_values.append(e)
        else:
            yield last_values
            last_values, last_key = [e], extract_key(e)
    if last_values:
        yield last_values


def join(
        g1: typing.Iterator[dict],
        g2: typing.Iterator[dict],
        join_elements: typing.Callable[[typing.Optional[dict], typing.Optional[dict]], typing.Optional[dict]],
        extract_key: typing.Callable[[typing.Dict], str]) -> typing.Iterator[dict]:
    def yield_if_not_none(d1: typing.Optional[dict], d2: typing.Optional[dict]):
        result = join_elements(d1, d2)
        if result:
            yield result

    i1, i2 = iter(g1), iter(g2)
    o1 = o2 = None
    while True:
        if not o1:
            try:
                o1 = next(i1)
            except StopIteration:
                return
        if not o2:
            try:
                o2 = next(i2)
            except StopIteration:
                o2 = None

        if o2 is None:
            yield from yield_if_not_none(o1, None)
        else:
            k1, k2 = extract_key(o1), extract_key(o2)
            if k1 < k2:
                yield from yield_if_not_none(o1, None)
                o1 = None
            elif k1 > k2:
                yield from yield_if_not_none(None, o2)
                o2 = None
            else:
                yield from yield_if_not_none(o1, o2)
                o1 = o2 = None


if __name__ == '__main__':
    u1 = ({'user_id': 'user_{:02}'.format(i), 'field1': i} for i in range(10))
    u2 = ({'user_id': 'user_{:02}'.format(i), 'field2': i} for i in range(1, 13, 2))
    u3 = ({'user_id': 'user_{:02}'.format(i), 'field1': i, 'fieldX': i // 3} for i in range(10))
    print('Join')
    pprint(list(join(u1, u2, left_join, lambda d: d['user_id'])))
    print('Aggregate')
    pprint(list(aggregate(u3, lambda d: d['fieldX'])))
