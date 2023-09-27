from utils import connect_neo
#funziona (da modificare se vuoi usare insert.py)

#mettere bool = False dopo aver finito il testing
def insert_neo(ip: str = "localhost", port: str = "7687", user: str = "neo4j", passwd: str = "neo4jnosqlproject",
               debug: bool = True):
    driver = connect_neo(ip, port, user, passwd)

    delete_query = "MATCH (n) DETACH DELETE n"
    insert_queries = [

        "LOAD CSV WITH HEADERS FROM 'file:///csv/75/person.csv' AS row \
         CREATE(n:person \
         {FullName: row.FullName, FirstName: row.FirstName, LastName: row.LastName, PhoneNumber: toInteger(row.PhoneNumber)})",

        "LOAD CSV WITH HEADERS FROM 'file:///csv/75/cell.csv' AS row \
         CREATE (n:cell {CellSite:toInteger(row.CellSite), State:row.State, City:row.City, Address:row.Address})",

        "LOAD CSV WITH HEADERS FROM 'file:///csv/75/call.csv' AS row \
         CREATE (n:call {CallingNbr:toInteger(row.CallingNbr), CalledNbr:toInteger(row.CalledNbr), \
         StartDate:toInteger(row.StartDate), EndDate:toInteger(row.EndDate), Duration:toInteger(row.Duration), \
         CellSite:toInteger(row.CellSite)})",

        "MATCH (p:person), (c:call) \
         WHERE p.PhoneNumber = c.CallingNbr \
         CREATE (p)-[r:is_calling]->(c)",

        "MATCH (p:person), (c:call) \
         WHERE p.PhoneNumber = c.CalledNbr \
         CREATE (c)-[r:is_called]->(p)",

        "MATCH (c1:call), (c2:cell) \
         WHERE c1.CellSite = c2.CellSite \
         MERGE (c1)-[r:is_done]->(c2)"

    ]

    debug_messages = [
        "NEO4J: Persone inserite",
        "NEO4J: Celle inserite",
        "NEO4J: Chiamate inserite",
        "NEO4J: Relazione is_calling creata",
        "NEO4J: Relazione is_called creata",
        "NEO4J: Relazione is_located creata"
    ]

    with driver.session() as db:
        try:
            # Se il flag debug == True effettua una pulizia del database
            if debug:
                db.run(delete_query)
                print("NEO4J: Drop del database effettuato.")

            # Esegue ogni query e se presente il flag debug == True stampa un messaggio
            for index in range(len(insert_queries)):
                db.run(insert_queries[index])
                if debug:
                    print(debug_messages[index])

            print("NEO4J: Inserimento completato con successo.")

        except Exception as e:
            # Se si verifica un'eccezione, stampa un messaggio di errore
            print(f"NEO4J: Errore durante l'inserimento: {str(e)}")
        finally:
            driver.close()

    return




# da togliere una volta visto che funziona
insert_neo(ip="localhost", port="7687", user="neo4j", passwd="neo4jnosqlproject", debug=True)