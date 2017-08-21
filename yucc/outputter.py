
def _format_from_kind(kind):
    if kind == 'zone':
        return lambda x: '{}  {}'.format(x['id'], x['description']), None
    elif kind == 'template':
        return lambda x: '{}  {}'.format(x['uuid'], x['title']), None
    elif kind == 'server':
        return lambda x: '{}  {}  {}  {}MB RAM  {}CPU  {}'.format(x.uuid, x.hostname, x.title,
                    x.memory_amount, x.core_number, x.state)
    else:
        raise Error

def output(kind, data, **kwargs):
    fmt = _format_from_kind(kind)
    for row in data:
        print fmt(row)

