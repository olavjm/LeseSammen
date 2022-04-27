#High Fidelity

import psycopg2

studenter = {}
emner = {}
grupper = {}

bruker = ''

# Login med bruker fra studenter. Passord må matche.
def login():
    global bruker
    navn = str(input("Navn: "))
    passord = str(input("Passord: "))
    for key, value in studenter.items():
        if navn.upper() in key.upper() and passord == value[0]:
            bruker = key
            print("Velkommen", bruker)
            break
        

# Henter data fra databasen, og lagrer det i dictionaries.
def hentDatabase():
    global emner
    global studenter
    con = psycopg2.connect(host="localhost",database="LeseSammen", user="postgres", password="honning121")
    cursor = con.cursor()
    postgreSQL_select_Query = "select * from student"
    cursor.execute(postgreSQL_select_Query)
    student_records = cursor.fetchall()

    for row in student_records:
        studenter[row[0]] = (row[1], row[2])

    query = "select * from studentEmner"
    cursor.execute(query)
    emne_data = cursor.fetchall()

    for e in emne_data:
        emner[e[0]] = (e[1], e[2], e[3])

    cursor.close()
    con.close()

hentDatabase()


# Registrerer bruker og plaserer informasjonen i databasen
def registrerBruker():
    #Student
    con = psycopg2.connect(host="localhost",database="LeseSammen", user="postgres", password="honning121")
    cursor = con.cursor()
    nynavn = str(input("Navn:"))
    nypassord = str(input("Passord:"))
    nymail = str(input("Mail:"))
    cursor.execute("INSERT INTO student (navn, passord, mail) VALUES(%s, %s, %s)", (nynavn, nypassord, nymail))
    con.commit()
    
    #Emner
    emne1 = str(input("Emnekode 1:"))
    emne2 = str(input("Emnekode 2:"))
    emne3 = str(input("Emnekode 3:"))
    con = psycopg2.connect(host="localhost",database="LeseSammen", user="postgres", password="honning121")
    cursor = con.cursor()
    cursor.execute("INSERT INTO studentEmner (navn, emne1, emne2, emne3) VALUES(%s, %s, %s, %s)", (nynavn, emne1, emne2, emne3))
    con.commit()
    cursor.close()
    con.close()


# Oppretter en gruppe med valgt fag, inkludert inlogget person og 4 ledige plasser
def lagGruppe():
    global bruker
    global grupper
    con = psycopg2.connect(host="localhost",database="LeseSammen", user="postgres", password="honning121")
    cursor = con.cursor()
    postgreSQL_select_Query = "select * from grupper"
    cursor.execute(postgreSQL_select_Query)
    gruppe_records = cursor.fetchall()

    for row in gruppe_records:
        grupper[row[5]] = (row[0], row[1], row[2], row[3], row[4])

    fag = str(input("Emne:"))

    for emne in emner.items():
        if fag.upper() in emne[1]:
              fag = fag.upper()
              
    cursor.execute("INSERT INTO grupper (navn1, navn2, navn3, navn4, navn5, emnekode) VALUES(%s, %s, %s, %s, %s, %s)", (bruker, "NULL", "NULL", "NULL", "NULL", fag))
    con.commit()
            

    cursor.close()
    con.close()


# Finner en gruppe med ledig plass for valgt fag og plasserer deg i databasen for gruppen
def finnGruppe():
    global bruker
    global grupper
    con = psycopg2.connect(host="localhost",database="LeseSammen", user="postgres", password="honning121")
    cursor = con.cursor()
    postgreSQL_select_Query = "select * from grupper"
    cursor.execute(postgreSQL_select_Query)
    gruppe_records = cursor.fetchall()

    counter = 0
    fag = str(input("Emne:"))
    for row in gruppe_records:
        if fag.upper() in row and "NULL" in row:
            for col in row:
                if row[counter] == "NULL":
                    counter += 1
                    navn = "navn" + str(counter)
                    cursor.execute("UPDATE grupper SET "+navn+" = "+"'"+bruker+"'"+" WHERE emnekode = "+"'"+fag.upper()+"'"+"")
                    con.commit()
                    break
                else:
                    counter += 1
                    
    cursor.close()
    con.close()

    


