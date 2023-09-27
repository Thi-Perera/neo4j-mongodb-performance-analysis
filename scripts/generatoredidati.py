#!/bin/env python3

from faker import Faker
from random import randrange
from datetime import datetime
from argparse import ArgumentParser
from threading import Thread
from os import path, mkdir
import csv

parser = ArgumentParser(description="Select multiplyer for number of datas.")
parser.add_argument('-p', '--percentage',
                    dest="P",
                    required=True,
                    help='Specify the percentage.')
args = parser.parse_args()

''' VARIABILI '''
num_person = 20000 * int(args.P) // 100
num_call = 1000000 * int(args.P) // 100
num_cell = 16000 * int(args.P) // 100
start_date = [2020, 1, 1]
end_date = [2020, 2, 1]
range_call = 1200  # Durata massima in secondi

fake = Faker("it_IT")
person, cell, call = [], [], []

headers = [
    'FullName',
    'FirstName',
    'LastName',
    'CallingNbr',
    'CalledNbr',
    'StartDate',
    'EndDate',
    'Duration',
    'CellSite',
    'City',
    'State',
    'Address'
]

''' 
LISTA DI PERSONE 

- Inserisce in person gli headers necessari. 
- Genera per il numero di persone scelto una lista temporanea di nome e 
cognome, ne ricava il nome completo. 
- Genera un numero di telefono unico finché non rientra nello standard italiano, ossia 3xxxxxxxxx (10 cifre).
- Aggiunge la lista creata in person.
- Scrive su file.

'''


def gen_person(num_person):
    global person
    person = [['Number'] + headers[:3]]
    for _ in range(num_person):
        now = [
            fake.first_name_nonbinary(),
            fake.last_name_nonbinary()
        ]
        now.insert(0, now[0] + now[1])
        while True:
            pn = fake.unique.phone_number()
            if pn[0] == '3' and len(pn) == 10:
                now.insert(0, pn)
                break
        person.append(now)
    write('person', person)


''' 
LISTA DI CHIAMATE 

- Inserisce in call gli headers necessari.
- Sceglie un chiamante casuale.
- Sceglie un chiamato casuale finché non coincida con il chiamante.
- Genera una data di inizio chiamata in un intervallo definito in standard UNIX Epoch.
- Genera una durata.
- Ricava la data di fine chiamata.
- Scrive su file.

'''


def gen_call(num_call, num_person, start_date, end_date, range_call):
    global call
    call = [headers[3:9].copy()]
    for i in range(1, num_call + 1):
        call += [[person[randrange(1, num_person)][0]]]
        while True:
            end = person[randrange(1, num_person)][0]
            if end != call[i][0]:
                call[i] += [end]
                break
    # LISTA DATE
    for i in range(1, len(call[1:]) + 1):
        call[i].append(int(fake.unix_time(datetime(end_date[0], end_date[1], end_date[2]),
                                           datetime(start_date[0], start_date[1], start_date[2]))))
        delta = randrange(1, range_call)
        call[i].append(call[i][2] + delta)
        call[i].append(delta)
        call[i].append(cell[randrange(1, num_cell)][0])
    write("call", call)


'''
LISTA CELLE 

- Inserisce in cell gli headers necessari.
- Genera un nome di città, una via e la sigla dello Stato.
- Scrive su file.

'''


def gen_cell(num_cell):
    global cell
    cell = [headers[-4:]]
    for i in range(1, num_cell + 1):
        cell += [[fake.administrative_unit()]]
        cell[i].append(fake.current_country_code())
        cell[i].append(fake.street_name())
        cell[i].insert(0, i)
    write("cell", cell)


'''
SCRITTURA SU FILE
- Crea, o apre se esiste già, un file in sola scrittura nella directory ./csv/.
- Scrive su file csv la lista passata come parametro.

'''


def write(name, obj_list):
    with open('../csv/' + name + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(obj_list)


# Se non esiste la directory ./csv/ la crea
if not path.exists("../csv"):
    mkdir("../csv")

# Crea il thread di generazione delle celle telefoniche
thread = Thread(target=gen_cell, args=(num_cell,))

# Fa partire il thread e la generazione delle persone
thread.start()
gen_person(num_person)

# Attende la fine dei threads
thread.join()

# Genera le chiamate
gen_call(num_call, num_person, start_date, end_date, range_call)