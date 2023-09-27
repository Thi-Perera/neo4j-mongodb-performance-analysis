#!/bin/env python3
#funziona 

from pymongo import MongoClient
from neo4j import GraphDatabase
from argparse import ArgumentParser
from time import time


# Restituisce il timestamp, o un intervallo di tempo se dato un valore di partenza
def timestamp(start: float = 0) -> float:
    return time() - start


# Crea la connessione con MongoDB sul database 'test' e restituisce l'oggetto MongoClient
def connect_mongo(ip: str = "localhost", port: str = "27017"):
    conn_str = "mongodb://" + ip + ":" + port + "/test?retryWrites=true&w=majority"
    return MongoClient(conn_str, serverSelectionTimeoutMS=5000)


# Crea la connessione con Neo4j sul database di default e restituisce l'oggetto GraphDatabase.driver
def connect_neo(ip: str = "localhost", port: str = "7687", user: str = "neo4j", passwd: str = "neo4jnosqlproject"):
    uri = "neo4j://" + ip + ":" + port
    return GraphDatabase.driver(uri, auth=(user, passwd))


# Crea un ArgumentParser per l'esecuzione da riga di comando per alcuni flag comuni ad alcuni scripts
def parse():
    parser = ArgumentParser(description="Executes some queries to Neo4j.")
    parser.add_argument('-t', '--time',
                        action="store_true",
                        default=False,
                        help='Prints execution time.')
    parser.add_argument('-n',
                        dest="N",
                        required=True,
                        help='Specify which query to execute [1-4].')
    parser.add_argument('-c', '--cache',
                        action="store_true",
                        default=False,
                        help='Clear cache')
    parser.add_argument('-p', '--perc',
                        dest="P",
                        default="",
                        help='Percentage')

    return parser.parse_args()
