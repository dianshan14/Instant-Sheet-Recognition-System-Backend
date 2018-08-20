import requests

url = 'http://18.191.142.38/'
headers = {'Cookie': 'session=eyJ1c2VyX2lkIjoxfQ.Dll0vw.84mnMf7Zzj-V0pZBeYGm1mK6or8'}

res = requests.get(url)
print(res.text)
