import tabulate

def output(kind, data, **kwargs):
    fmt = _format_from_kind(kind)
    print tabulate.tabulate(data, headers='keys')
