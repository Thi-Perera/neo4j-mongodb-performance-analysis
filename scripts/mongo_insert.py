from utils import connect_mongo
from csv import DictReader
#funziona (da modificare se vuoi usare insert.py)

# Funzione che converte gli interi di un dizionario appena letto da csv da str a int
def to_dict(csv: [dict]):
    for k, e in enumerate(csv):
        for f, i in e.items():
            if i.isdigit():
                e[f] = int(i)
    return csv


'''
- Crea la connessione col MongoDB e seleziona il database corretto.
- Se presente il flag debug == True effettua una pulizia del database.
- Per ogni entità crea, o apre se esiste già, un file di sola lettura dal quale vengono letti i dati in csv e 
convertiti in dizionario e vengono inseriti nel database.
'''


def insert_mongo(ip: str = "localhost", port: str = "27017", debug: bool = True):
    client = connect_mongo(ip, port)
    db = client.test
    if debug:
        client.drop_database('test')
        print("MONGODB: Drop del database effettuato.")
    del client

    with open("C:/Users/newth/Desktop/NoSqlScritto/progetto/neo4jdata/csv/25/person.csv") as personf:
        rows = to_dict(list(DictReader(personf)))
        db.person.create_index("PhoneNumber", unique=True)
        db.person.insert_many(rows)
        if debug:
            print("MONGODB: Persone inserite.")

    with open("C:/Users/newth/Desktop/NoSqlScritto/progetto/neo4jdata/csv/25/cell.csv") as cellf:
        rows = to_dict(list(DictReader(cellf)))
        db.cell.insert_many(rows)
        if debug:
            print("MONGODB: Celle inserite.")

    with open("C:/Users/newth/Desktop/NoSqlScritto/progetto/neo4jdata/csv/25/call.csv") as callf:
        rows = to_dict(list(DictReader(callf)))
        db.call.insert_many(rows)
        if debug:
            print("MONGODB: Chiamate inserite.")

    return

insert_mongo(ip="localhost", port="27017", debug=True)