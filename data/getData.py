import json
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper('https://query.wikidata.org/sparql')
sparql.setReturnFormat(JSON)

sparql.setQuery( """
        SELECT DISTINCT
            ?itemLabel
            ?sintomasLabel
        WHERE 
        {
            ?item wdt:P31 wd:Q112193867
            ; wdt:P780 ?sintomas
             SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
        }
        ORDER BY ?itemLabel
        """)

data = {}
try:
    ret = sparql.queryAndConvert()

    for r in ret["results"]["bindings"]:
        if not r['itemLabel']['value'] in data:
            data[r['itemLabel']['value']] = []
        data[r['itemLabel']['value']].append(r['sintomasLabel']['value'])

except Exception as e:
    print(e)

# Exportar datos

with open("data.json", "w") as outfile:
    json.dump(data, outfile)