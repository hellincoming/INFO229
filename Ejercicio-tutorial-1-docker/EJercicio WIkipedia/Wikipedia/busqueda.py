import wikipedia
import os
import pymongo
wikipedia.set_lang("es")
DATABASE='WikiFixed'
BUSQUEDA='busqueda'
RESULTADO='resultado'
myclient = pymongo.MongoClient(host=os.environ['MONGO_HOST'], port=int(os.environ['MONGO_PORT']))
db = myclient[DATABASE]
busqueda = db[BUSQUEDA]
resultados = db[RESULTADO]
print("Que desea buscar")
busc='rey misterio'
res=wikipedia.summary(busc , sentences = 10 , chars = 0 , auto_suggest = True , redirect = True )
print(res)
db.busqueda.insert_one({'busqueda':busc})
db.resultados.insert_one({'resultado':res})

