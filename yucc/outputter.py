import tabulate
import pprint
import json

def output(kind, data, **kwargs):
    output_format = kwargs.get('format', 'json')
    if output_format == 'table':
        print tabulate.tabulate(data, headers='keys')
    elif output_format == 'json':
        print json.dumps(data, sort_keys=True,
                indent=4, separators=(',', ': '))
    else:
        raise ValueError('Invalid output format `{}` given'.format(output_format))


def raw_output(kind, data, **kwargs):
    if kind == 'server':
        print json.dumps(data, sort_keys=True,
            indent=4, separators=(',', ': '))
    else:
        raise ValueError('Invalid data kind gived to raw_output')
