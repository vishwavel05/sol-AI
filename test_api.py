import urllib.request
import json
import sys

def main():
    query = sys.argv[1]
    req = urllib.request.Request(
        'http://localhost:8000/api/query', 
        data=json.dumps({'query': query, 'provider': 'mock'}).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(req)
    with open('test_output.json', 'wb') as f:
        f.write(res.read())

if __name__ == '__main__':
    main()
