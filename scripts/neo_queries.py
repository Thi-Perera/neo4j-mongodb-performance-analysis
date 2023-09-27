#!/bin/env python3
#funziona

from utils import connect_neo, parse, timestamp
from time import time
from statistics import stdev
from sys import exit


# Pulizia di cache e funziona
def clear_cache():
    exec_query("CALL db.clearQueryCaches()")
    return


# Esegue la query passata come parametro e se presente flag t == True stampa il tempo di esecuzione, altrimenti 0
def exec_query(query: str, client=connect_neo(), t: bool = True) -> float:
    start = timestamp()
    with client.session() as db:
        db.run(query)

    return timestamp(start) if t else 0


if __name__ == "__main__":
    # Effettua il parsing dei parametri da riga di comando
    args = parse()

    # Ricava alcuni valori o flag dai parametri da riga di comando
    num = int(args.N)
    perc = args.P + "_" if args.P != "" else ""

    # Lista queries
    queries = [
       "MATCH (c:call)  \
        WHERE c.StartDate >= 1580083200 \
            AND c.StartDate < 1672473600   \
        RETURN c",

       "MATCH (p1:person)-[r1:is_calling]->(c:call)  \
        WHERE c.StartDate >= 1580083200 \
            AND c.StartDate < 1672473600   \
        RETURN p1, r1, c",

       "MATCH (p1:person)-[r1:is_calling]->(c:call)-[r2:is_done]->(ce:cell) \
        WHERE c.StartDate >= 1580083200 \
            AND c.StartDate < 1672473600   \
        RETURN p1, r1, c, r2, ce",

       "MATCH (p1:person)-[r1:is_calling]->(c:call)-[r2:is_done]->(ce:cell) \
        WHERE c.StartDate >= 1580083200 \
            AND c.StartDate < 1672473600 \
            AND c.Duration > 900   \
        RETURN p1, r1, c, r2, ce"
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
        with open('C:/Users/newth/Desktop/NoSqlScritto/progetto/risultatiprovaperneo/neo_result_' + perc + str(num) + '.csv', 'w') as f:
            f.write("First," + str(exec_query(queries[num - 1], t=args.time)) + "\n")
            tmp = []
            for i in range(30):
                tmp += [exec_query(queries[num - 1], t=args.time)]
                f.write("," + str(tmp[i]) + '\n')
            f.write("Mean," + str(sum(tmp)/30) + "\n")
            f.write("Std. Dev.," + str(stdev(tmp)) + "\n")
    else:
        print("Wrong query number. Only from 1 to 4.")
    exit(0)
