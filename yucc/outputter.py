import tabulate

def output(kind, data, **kwargs):
    print tabulate.tabulate(data, headers='keys')
