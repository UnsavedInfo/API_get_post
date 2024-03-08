# Importa a biblioteca request, que é uma biblioteca HTTP feita em python 
import requests 

url= 'http://127.0.0.1:5000/age_calculate' # url onde o meu post está sendo executado (?)
#url= 'http://127.0.0.1:5000/api/post_example' # url onde o meu post está sendo executado (?)


trabo = 12 

data = {"name": "Jones Dias",
        "birthdate": "2000-09-28",
        "date": "2080-09-27"
        }  # Dados a serem enviados


#data = {'oi': 'coé'}


response = requests.post(url, json = data) # Recebe a requisição post. Manda os dados
print('la')

response = requests.post(url, json=data)
if response.status_code == 200:
    print(response.json())
else:
    print("Erro:", response.status_code)
    print(response.text)


print(response.json())

