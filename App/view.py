"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
import time
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar cronológicamente los artistas")
    print("3- Listar cronológicamente las adquisiciones")
    print("4- Clasificar las obras de un artista por técnica")
    print("5- Clasificar las obras por la nacionalidad de sus creadores")
    print("6- Transportar obras de un departamento")
    print("7- Las n obras más antiguas para un medio específico")
    print("8- Número de obras de una nacionalidad")
    print("0- Salir")

def isDead(Date):
    if Date == "0":
        retorno = "Sigue con vida (o no se sabe la fecha de su muerte)."
    else:
        retorno = Date
    return retorno

def printSortedArtists(ord_artists, sample=3):
    size = lt.size(ord_artists)

    if size == 0:
        print("\nNo se encontraron obras adquiridas dentro del rango ingresado.\n")

    elif size > sample:
        print("\nEl número de artistas que nacieron entre esos años es de ", size ," artistas.")

        print("\nLas primeras ", sample, " obras ordenadas son:")
        counted1=1
        i = 1
        while counted1 <= sample and i <= size:
            artist = lt.getElement(ord_artists, i)
            print('\nNombre: ' + artist['DisplayName'] + ', Año de nacimiento: ' + artist['BeginDate'] + ', Año de fallecimiento: ' + isDead(artist['EndDate']) + ', Nacionalidad: ' + artist['Nationality'] + ", Género: " + artist["Gender"])
            counted1 += 1
            i += 1

        print("\nLas últimas ", sample, " obras ordenadas son:")
        counted2=1
        j=size
        finalArtists = lt.newList(datastructure="SINGLE_LINKED")
        while counted2 <= sample and 1 <= j <= size:
            artist = lt.getElement(ord_artists, j)
            lt.addFirst(finalArtists, artist)
            counted2 += 1
            j -= 1
        for k in range(1,4):
            artist = lt.getElement(finalArtists, k)
            print('\nNombre: ' + artist['DisplayName'] + ', Año de nacimiento: ' + artist['BeginDate'] + ', Año de fallecimiento: ' + isDead(artist['EndDate']) + ', Nacionalidad: ' + artist['Nationality'] + ", Género: " + artist["Gender"])


def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()


def loadData(catalog, size):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog, size)

def lastArtists(catalog):

    return controller.lastArtists(catalog)

def lastArtworks(catalog):
    
    return controller.lastArtworks(catalog)

def getArtistsName(catalog, constituentID):
    
    return controller.getArtistsName(catalog, constituentID)

def printSortResults(ord_artworks, sample=10):
    size = lt.size(ord_artworks)
    if size > sample:
        print("Las primeras ", sample, " obras ordenadas son: ")
        i = 1
        while i <= sample:
            artworks = lt.getElement(ord_artworks, i)
            print("Titulo: " + artworks["Title"] + " Dimensiones : " + 
            artworks["Dimensions"] + " Fecha de adquisición : " + artworks["DateAcquired"])
            i += 1

def printFirstFive(listA):
    i = 1
    while i <= 5:
        elementA = lt.getElement(listA, i)
        constituentID = elementA["ConstituentID"]
        artistName = getArtistsName(catalog, constituentID)
        print("Título: ", elementA["Title"], ", Artista(s): ", artistName, ", Fecha: ", elementA["Date"], ", Medio: ", elementA["Medium"], ", Dimensiones: "
        , elementA["Dimensions"], ", Clasificación: ", elementA["Classification"], ", Costo: ",  elementA["elementCost"])
        i += 1

def printFirstandLast(listA):
    i = 1
    h = 1
    while i <= 3:
        elementA = lt.getElement(listA, i)
        constituentID = elementA["ConstituentID"]
        artistName = getArtistsName(catalog, constituentID)
        print("Título: ", elementA["Title"], ", Artista(s): ", artistName, ", Fecha: ", elementA["Date"], ", Medio: ", elementA["Medium"], ", Dimensiones: "
        , elementA["Dimensions"])
        i += 1

    while h <= 3:
        elementA = lt.getElement(listA, i)
        constituentID = elementA["ConstituentID"]
        artistName = getArtistsName(catalog, constituentID)
        print("Título: ", elementA["Title"], ", Artista(s): ", artistName, ", Fecha: ", elementA["Date"], ", Medio: ", elementA["Medium"], ", Dimensiones: "
        , elementA["Dimensions"])
        h += 1


def printLoadResult(catalog):
    print('Artistas cargados: ', lt.size(catalog['artists']))
    print('Obras cargadas: ', lt.size(catalog['artworks']))

    print("\nPrimeros tres artistas cargados: ")
    for n in range(1,4):
        actualArtist = lt.getElement(catalog["artists"], n)
        print(actualArtist["DisplayName"])
        
    print("Últimos tres artistas cargados: ")
    for n in range(lt.size(catalog["artists"])-2, lt.size(catalog["artists"])+1):
        actualArtist = lt.getElement(catalog["artists"], n)
        print(actualArtist["DisplayName"])


    print("\nPrimeras tres obras cargadas: ")
    for n in range(1,4):
        actualArtist = lt.getElement(catalog["artworks"], n)
        print(actualArtist["Title"])
        
    print("Últimas tres obras cargadas:")
    for n in range(lt.size(catalog["artworks"])-2, lt.size(catalog["artworks"])+1):
        actualArtist = lt.getElement(catalog["artworks"], n)
        print(actualArtist["Title"])

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        size = int(input(
"""Ingrese el tamaño de la muestra:
1. Small
2. 5%
3. 10%
4. 20%
5. 30%
6. 50%
7. 80%
8. Large\n"""
        ))

        print("Cargando información de los archivos ....")

        start_time = time.process_time()

        catalog = initCatalog()
        loadData(catalog, size)
        lastArtists_ = lastArtists(catalog)
        lastArtworks_ = lastArtworks(catalog)
        printLoadResult(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("\nLa carga de los datos tardó ", elapsed_time_mseg, " milisegundos.")

    elif int(inputs[0]) == 2:
        year0 = input("Ingrese el año inicial\n")
        year1 = input("Ingrese el año final\n")
        
        start_time = time.process_time()
        sortedArtists = controller.sortByBirth(catalog, year0, year1)
        printSortedArtists(sortedArtists)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000

        print("\nLa operación tardó ", elapsed_time_mseg, " milisegundos.")

    elif int(inputs[0]) == 3:
        date0 = input("Ingrese la fecha desde la cual filtrar (en forma AAAA-MM-DD): ")
        date1 = input("Ingrese la fecha hasta la cual filtrar (en forma AAAA-MM-DD): ")
        start_time = time.process_time()
        filtredArtworks = controller.filterByDate(catalog, date0, date1)
        result = controller.sortArtworksByAcquiredDate(filtredArtworks)
        elapsed_time_mseg = (stop_time - start_time)*1000

        print("\nLa operación tardó ", elapsed_time_mseg, " milisegundos.")
        print("\nEl número total de obras en el rango cronológico es de ", lt.size(result))
        printFirstandLast(result)
    
    elif int(inputs[0]) == 4:
        ArtistName = input("Indique el nombre del artista a consultar: ")
        result = controller.filterTechnicArtists(catalog, ArtistName)
        dictT = result[4]
        listT = dictT[result[2]]
        print(ArtistName, " tiene un total de ", str(result[0]), " obras dentro del museo.")
        print("Existe un total de ", str(result[1]), " de medios utilizados en sus obras.")
        print("El medio más utilizado fue: ", str(result[2]), " con ", str(result[3]), " piezas. ")
        print("El listado de obras de dicha técnica es: ")
        i = 1
        while i <= lt.size(listT):
            element = lt.getElement(listT, i)
            print("Título: ", element["Title"], ", Fecha: ", element["Date"], ", Medio: ", element["Medium"], ", Dimensiones: "
            , element["Dimensions"])
            i += 1
        
    elif int(inputs[0]) == 5:
        start_time = time.process_time()
        topTen = controller.topTenNats(catalog)
        print("TOP 10")
        h = lt.size(topTen)
        r = 1
        while lt.size(topTen) >= h >= 1:
            actualPair = lt.getElement(topTen, h)
            nationality = actualPair["key"]
            number = lt.size(actualPair["value"])
            print(r, ". ", nationality, ": ", number)
            h -= 1
            r += 1
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("\nLa operación tardó ", elapsed_time_mseg, " mseg.")
        

    elif int(inputs[0]) == 6:
        department = input("Indique el nombre del departamento a consultar: ")
        result = controller.transportArtworks(catalog, department)
        listA = result[3]
        listC = result[4]
        print("El total de obras para transportar de ", department, " es de: ", result[0])
        print("El costo estimado en USD es de: ", str(result[1]))
        print("EL peso estimado en Kg es de: ", str(result[2]))
        print("Los 5 items más antiguos para transportar son: ")
        printFirstFive(listA)
        print("-------------------------------------------------")
        print("Los 5 items más costosos para transportar son: ")
        printFirstFive(listC)
        
    elif int(inputs[0]) == 7:
        medium = input("Indique el medio específico a consultar: ")
        nArtworks = int(input("Indique el número de obras a consultar: "))
        listm = controller.findArtworksMedium(catalog, medium, nArtworks)
        i = 1
        while i <= lt.size(listm):
            element = lt.getElement(listm, i)
            print("Título: ", element["Title"], ", Fecha: ", element["Date"], ", Medio: ", element["Medium"], ", Dimensiones: "
            , element["Dimensions"])
            i += 1

    elif int(inputs[0]) == 8:
        nationality = input("Ingrese la nacionalidad a consultar: ")
        
        listNat = controller.findArtworksNationalities(catalog, nationality)
        numArtworks = lt.size(listNat)

        print("El número total de obras de la nacionalidad ", nationality, " es de ", numArtworks)

    else:
        sys.exit(0)
sys.exit(0)
