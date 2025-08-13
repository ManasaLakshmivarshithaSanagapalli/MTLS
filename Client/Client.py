import requests

url = 'https://localhost:4443'
# resp = requests.get(url, cert=('client.crt', 'client.key'), verify='../CA/myCA.crt')
resp = requests.get(url, cert=('client2.crt', 'client2.key'), verify='../CA/myCA.crt')
print(resp.text)
