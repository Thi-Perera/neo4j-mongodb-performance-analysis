#!/bin/env python3
from sys import exit
from mongo_insert import insert_mongo
from neo_insert import insert_neo
from threading import Thread
from argparse import ArgumentParser

# Crea un parser per la lettura dei flag all'esecuzione da riga di comando
parser = ArgumentParser(description="Inserts files into either MongoDB or Neo4j databases, or both of them.")
parser.add_argument('-d', '--debug',
                    action="store_true",
                    default=False,
                    help='Debugging, it deletes all collections in \'test\' database.')
parser.add_argument('-m', '--mongo',
                    action="store_true",
                    default=False,
                    help='Insert files only to MongoDB database.')
parser.add_argument('-n', '--neo',
                    action="store_true",
                    default=False,
                    help='Insert files only to Neo4j database.')
parser.add_argument('-a', '--all',
                    action="store_true",
                    default=False,
                    help='Insert files only to Neo4j database.')


args = parser.parse_args()
debug = args.debug

# Setta dei valori booleani per decidere in che database inserire i dati, in base ai flag del parser
mongo, neo = (args.mongo, args.neo) if not args.all else (args.all, args.all)

thread_mongo = None
# Se si vuole inserire su MongoDB...
if mongo:
    # ... ma non su Neo4j
    if not neo:
        # Viene invocata la realtiva funzione di inserimento
        insert_mongo(debug=debug)
    # ... e anche Neo4j
    else:
        # Viene creato e fatto eseguire un thread per l'inserimento su MongoDB
        thread_mongo = Thread(target=insert_mongo, kwargs={'debug': debug})
        thread_mongo.start()

# Se si vuole inserire su Neo4j...
if neo:
    # Viene invocata la relativa funzione di inserimento
    insert_neo(debug=debug)

# Si attende la fine del thread...
if thread_mongo is not None:
    thread_mongo.join()

# ... per poi stampare un messaggio di fine
print("Inserimenti finiti.")
exit(0)
