#!/bin/env python3
#funziona

from utils import connect_mongo, parse, timestamp
from datetime import datetime
from time import mktime
from statistics import stdev
from sys import exit


# Pulizia di cache ma non funziona
def clear_cache(client=connect_mongo()):
    client.test.command(
        {"planCacheClear": "call"},
        {"planCacheClear": "cell"},
        {"planCacheClear": "person"}
    )
    return


# Esegue la query passata come parametro e se presente flag t == True stampa il tempo di esecuzione, altrimenti 0
def exec_query(query: list, client=connect_mongo(), t: bool = True) -> float:
    start = timestamp()
    client.test.call.aggregate(query)

    return timestamp(start) if t else 0


if __name__ == "__main__":
    # Effettua il parsing dei parametri da riga di comando
    args = parse()

    # Ricava alcuni valori o flag dai parametri da riga di comando
    num = int(args.N)
    perc = args.P + "_" if args.P != "" else ""

    # Dichiara la data iniziale e finale da ricercare in UNIX Epoch e la durata della chiamata in secondi
    start_search = int(mktime(datetime(2020, 1, 27).timetuple()))
    end_search = int(mktime(datetime(2020, 1, 29).timetuple()))
    dur_search = 900

    # Lista delle queries
    queries = [
        [
            {"$match": {"StartDate": {"$gte": start_search,
                                      "$lt": end_search}}}
        ],

        [
            {"$match": {"StartDate": {"$gte": start_search,
                                      "$lt": end_search}}},
            {"$lookup": {"from": "people",
                         "localField": "CallingNbr",
                         "foreignField": "Number",
                         "as": "Calling"}}
        ],

        [
            {"$match": {"StartDate": {"$gte": start_search,
                                      "$lt": end_search}}},
            {"$lookup": {"from": "people",
                         "localField": "CallingNbr",
                         "foreignField": "Number",
                         "as": "Calling"}},
            {"$lookup": {"from": "cells",
                         "localField": "CellSite",
                         "foreignField": "CellSite",
                         "as": "Cell"}}
        ],

        [
            {"$match": {"StartDate": {"$gte": start_search,
                                      "$lt": end_search},
                        "Duration": {"$gte": dur_search}}},
            {"$lookup": {"from": "people",
                         "localField": "CallingNbr",
                         "foreignField": "Number",
                         "as": "Calling"}},
            {"$lookup": {"from": "cells",
                         "localField": "CellSite",
                         "foreignField": "CellSite",
                         "as": "Cell"}}
        ]
    ]

    if 0 < num < 5:
        # Prima pulizia preventiva della cache
        clear_cache()

        '''
        - Crea, o apre se esiste già, un file di sola scrittura.
        - Effettua la query la prima volta e scrive su file il tempo della prima esecuzione.
        - Effettua la query altre 30 volte e scrive su file tutte le 30 misurazioni.
        - Calcola la media e la deviazione standard dei dati misurati e li scrive su file.
        '''
        with open("C:/Users/newth/Desktop/NoSqlScritto/progetto/risultatiprovaperneo/mongo_result_" + perc + str(num) + ".csv", "w") as f:
            f.write("First," + str(exec_query(queries[num - 1], t=args.time)) + "\n")
            tmp = []
            for i in range(30):
                tmp += [exec_query(queries[num - 1], t=args.time)]
                f.write("," + str(tmp[i]) + "\n")
            f.write("Mean," + str(sum(tmp) / 30) + "\n")
            f.write("Std. Dev.," + str(stdev(tmp)) + "\n")
    else:
        print("Wrong query number. Only from 1 to 4.")
    exit(0)
