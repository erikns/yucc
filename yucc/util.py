import getpass


def credentials_prompt():
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    return {'username': username, 'password': password}


def first_in(collection, candidates):
    for candidate in candidates:
        contains = collection.get(candidate, None)
        if contains:
            return candidate


def strip_keys(collection, strip_chars):
    result = {}
    for k, v in list(collection.items()):
        result[k.strip('-')] = v
    return result


def exclude_keys(collection, keys):
    result = dict()
    for k, v in list(collection.items()):
        if k not in keys:
            result[k] = v
    return result


def strip_none(collection):
    result = dict()
    for k, v in list(collection.items()):
        if v is not None:
            result[k] = v
    return result


def replace_in_keys(collection, old, new):
    result = dict()
    for k, v in list(collection.items()):
        result[k.replace(old, new)] = v
    return result
