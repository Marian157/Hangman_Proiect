import csv
from collections import Counter

def cheie(x):
    return str(len(x))

vocabular={}
def f(key, value):
    if key in vocabular:
        vocabular[key].append(value)
    else:
        vocabular[key] = [value]

with open('../data/cuvinte_spz.csv', 'r', newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        v=row[0]
        f(cheie(v), v)

incercari=0
sec_incercari=[]
total_incercari=0

def verificare(l):
    lista_de_indexi=[]
    for i in range(len(cuvant_corect)):
        if cuvant_corect[i]==l:
            lista_de_indexi.append(i)
    return lista_de_indexi

def incearca_litere(c):
    global total_incercari
    global sec_incercari
    sec_incercari=[]
    global incercari
    incercari=0
    lista = vocabular[cheie(c)]
    listal=[]
    litere_utilizate = []
    litere_incercate = []
    for i in range(len(c)):
        if c[i] != "*" and c[i] not in litere_utilizate:
            litere_utilizate.append(i)
    while lista:
        for e in range(len(lista)):
            listal.append(lista[e])
            for j in litere_incercate:
                if j in lista[e]:
                    listal.pop()
                    continue
            for i in litere_utilizate:
                if lista[e][i]!=c[i]:
                    listal.pop()
                    break
        lista=listal
        listal = []
        litere = ''.join(lista)
        if litere==c:
            break
        for i in litere_utilizate:
            litere=litere.replace(c[i],"")
        if litere:
            incercari+=1
            l=Counter(litere).most_common(1)[0][0]
            sec_incercari.append(l)
            if verificare(l):
                for index in verificare(l):
                    c=c[:index]+l+c[index + 1:]
                    litere_utilizate.append(index)
            else:
                litere_incercate.append(l)
    total_incercari+=incercari
    return c

with open('../data/cuvinte_test.csv', 'r', newline='', encoding="utf-8") as csvin:
    fieldnames = ["game_id","pattern_initial", "cuvant_tinta"]
    nec = csv.DictReader(csvin, fieldnames=fieldnames)
    with open('../results/out_spz.csv', 'w', newline='', encoding="utf-8") as csvout:
        field = ['game_id', 'total_incercari', 'cuvant_gasit', 'status', 'secventa_incercari']
        cuvwriter = csv.DictWriter(csvout, fieldnames=field)
        cuvwriter.writeheader()
        for row in nec:
            cuvant_corect=row['cuvant_tinta'].lower()
            c=row['pattern_initial'].lower()
            c=incearca_litere(c)
            if '*' not in c:
                status="OK"
            else:
                status="FAIL"
            cuvwriter.writerow({'game_id': row['game_id'], 'total_incercari': incercari, 'cuvant_gasit': c, 'status': status, 'secventa_incercari': ' '.join(sec_incercari)})
print(total_incercari)