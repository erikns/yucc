
def _format_from_kind(kind):
    if kind == 'zone':
        return lambda x: '{}  {}'.format(x['id'], x['description'])
    elif kind == 'template':
        return lambda x: '{}  {}'.format(x['uuid'], x['title'])
    else:
        raise Error

def output(kind, data, **kwargs):
    fmt = _format_from_kind(kind)
    for row in data:
        print fmt(row)

