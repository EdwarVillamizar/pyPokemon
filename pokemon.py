import requests
import mysql.connector

'''
Consumir de la Poké API (https://pokeapi.co/) los siguientes datos para todos los pokemones: 
imagen oficial, habilidades, estadísticas generales, y tipo.

* Con la libreria requests y su metodo get podemos optener toda la informacion de la API.
* Obtenemos la cantidad de pokemon en la API
'''
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0")
count = response.json()['count']-1

'''
* Organizamos la informacion.
'''

perfil = list()
for i in range(1,count):

    if i <= 905:
        response = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(i))
        jsonResponse = response.json()
    else:
        response = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(i+9095))
        jsonResponse = response.json()

    imagenOficial = jsonResponse['sprites']['front_default']
    
    habilidades = list()
    for objeto in jsonResponse['abilities']:
        habilidades.append(objeto['ability']['name'])

    estadisticasGenerales = list()
    for objeto in jsonResponse['stats']:
        estadisticasGenerales.append(objeto['stat']['name'] + ": " + str(objeto['base_stat']))

    tipo = list()
    for objeto in jsonResponse['types']:
        tipo.append(objeto['type']['name'])
    
    perfil.append((str(imagenOficial),','.join(habilidades),','.join(estadisticasGenerales),','.join(tipo)))
    print(str(i)+". "+str(jsonResponse['forms'][0]['name']) + " Ok")

'''
Realizar las operaciones de estructuración/modelamiento de datos pertinentes.

* La libreria mysql.connector nos permite comunicarnos con el motor de mysql.
* Se Procede a la creacion de la base de datos y tablas, todo lo referente a la estructura en mysql.
'''

mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="")
mydb.cursor().execute("CREATE DATABASE IF NOT EXISTS pokemon")
mydb.close()

mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="", database = "pokemon")
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS perfil (id INT AUTO_INCREMENT PRIMARY KEY, imagen VARCHAR(255), habilidades VARCHAR(255), estadisticas VARCHAR(255), tipo VARCHAR(255))")
mydb.close()

'''
Cargar la información en una Base de Datos (SQL).

* Se procede a subir toda la informacion recopiliada.
'''

mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="", database = "pokemon")
mycursor = mydb.cursor()
query = "INSERT INTO perfil (imagen, habilidades, estadisticas, tipo) VALUES (%s, %s, %s, %s)"
mycursor.executemany(query, perfil)
mydb.commit()
mydb.close()

'''
Autor: Edwar Alfredo Villamizar Rincon.
'''