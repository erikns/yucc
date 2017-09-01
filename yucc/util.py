import getpass

def credentials_prompt():
    username = raw_input('Username: ')
    password = getpass.getpass('Password: ')
    return {'username': username, 'password': password}
