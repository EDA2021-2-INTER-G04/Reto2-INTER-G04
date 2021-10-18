"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time 
import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as mes
from DISClib.Algorithms.Sorting import quicksort as quis
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'artworks': None,
               'artists': None,
               "medium" : None,
               "nationality": None,
               "birth": None}

    catalog['artworks'] = lt.newList()
    catalog['artists'] = lt.newList("ARRAY_LIST")

    """
    Este indice crea un map cuya llave es el medio de la obra
    """
    initialSize = lt.size(catalog["artworks"])
    catalog["medium"] = mp.newMap(initialSize,
                                    maptype="CHAINING",
                                    loadfactor=4.0,
                                    comparefunction=cmpMaps)

    numArtists = lt.size(catalog["artists"])
    
    catalog["nationality"] = mp.newMap(numArtists, maptype="PROBING", loadfactor=0.4, comparefunction=cmpMaps)

    catalog["birth"] = mp.newMap(numArtists, maptype="PROBING", loadfactor=0.5, comparefunction=cmpMaps)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    lt.addLast(catalog['artworks'], artwork)

    medium = artwork["Medium"]
    isPresent = mp.contains(catalog["medium"], medium)
    if isPresent == True:
        listm = mp.get(catalog["medium"], medium)["value"]
        lt.addLast(listm, artwork)
        mp.put(catalog["medium"], medium, listm)
    else:
        listm = lt.newList('ARRAY_LIST')
        lt.addLast(listm, artwork)
        mp.put(catalog["medium"], medium, listm)


    listArtists = findArtist(artwork["ConstituentID"], catalog["artists"])
    artworkNationalities = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpStrings)

    for i in range(1, lt.size(listArtists)+1):
        artist = lt.getElement(listArtists, i)
        nationality = artist["Nationality"]
        if nationality != "" and nationality != None:
            if lt.isPresent(artworkNationalities, nationality) == 0:
                lt.addLast(artworkNationalities, nationality)
    
    for h in range(1, lt.size(artworkNationalities)+1):
        nationality = lt.getElement(artworkNationalities, h)
        isPresent = mp.contains(catalog["nationality"], nationality)
        if isPresent:
            listNat = mp.get(catalog["nationality"], nationality)["value"]
            lt.addLast(listNat, artwork)
            mp.put(catalog["nationality"], nationality, listNat)
        else:
            listNat = lt.newList("ARRAY_LIST")
            lt.addLast(listNat, artwork)
            mp.put(catalog["nationality"], nationality, listNat)

def addArtist(catalog, artist):
    lt.addLast(catalog['artists'], artist)

    birthYear = artist["BeginDate"]

    if birthYear != "0":
        isPresent = mp.contains(catalog["birth"], birthYear)
        if isPresent:
            listYears = mp.get(catalog["birth"], birthYear)["value"]
            lt.addLast(listYears, artist)
            mp.put(catalog["birth"], birthYear, listYears)
        else:
            listYears = lt.newList('ARRAY_LIST')
            lt.addLast(listYears, artist)
            mp.put(catalog["birth"], birthYear, listYears)
    
# Funciones para creacion de datos

def newArtist(name):
    
    artist = {'name': ""}
    artist['name'] = name
    
    return artist

def newArtwork(name):
    
    artwork = {'artwork': ""}
    artwork['artwork'] = name
    
    return artwork

# Funciones de consulta
def topTenNats(natMap):
    orderedNats = lt.newList(datastructure="ARRAY_LIST")
    nationalities = mp.keySet(natMap)
    for i in range(1, lt.size(nationalities)+1):
        actualKey = lt.getElement(nationalities, i)
        actualPair = mp.get(natMap,actualKey)
        lt.addLast(orderedNats, actualPair)
    
    mes.sort(orderedNats, cmpByValueSize)
    topTen = lt.subList(orderedNats, lt.size(orderedNats)-9, 10)

    return topTen

def lastArtists(catalog):
    
    artists = ""
    size = lt.size(catalog["artists"])
    for artist in range(0,3):
        artists += str((lt.getElement(catalog["artists"], size - artist)))

    return artists

def lastArtworks(catalog):
    
    artworks = ""
    size = lt.size(catalog["artworks"])
    for artwork in range(0,3):
        artworks += str((lt.getElement(catalog["artworks"], size - artwork)))

    return artworks

def firstAndlastArtworks(catalog, filterlist):
    
    artworks = lt.newList()
    size = lt.size(filterlist)
    for artwork in range(0,3):
        element = (lt.getElement(filterlist, artwork))
        element["Artista(s)"] = getArtistsName(catalog, element["ConstituentID"])
        lt.addLast(artworks, element)

    for artwork in range(0,3):
        element = (lt.getElement(filterlist, size - artwork))
        element["Artista(s)"] = getArtistsName(catalog, element["ConstituentID"])
        lt.addLast(artworks, element)

    return artworks

def listChronoArtists(catalog, initialYear, finalYear):
    DataArtists = catalog["artists"]
    sorted(DataArtists, key=lambda Date: Date["BeginDate"])
    finalList = lt.newList()

    for artist in range(0, lt.size(DataArtists)):
        element = DataArtists.getElement(artist)
        if element["BeginDate"] >= initialYear or element["BeginDate"] <= finalYear:
            finalList.addFirst(element)
    
    TotalSize = finalList.size()
    firstThree = finalList[:3]
    LastOneThree = finalList[-3:]
    returnList = [firstThree]
    returnList.append(LastOneThree)

    return TotalSize, returnList

def strDateToInt(Date):

    """Convierte una fecha dada a int para comparación"""

    if Date != "":
        DateF = Date.split("-")
        Date1F = []
        for element in DateF:
            Date1F.append(int(element))
        
        Date_ = datetime.datetime(Date1F[0], Date1F[1], Date1F[2])
        
        return Date_
    return None

#Funciones de ordenamiento
def cmpByValueSize(pair1, pair2):
    list1 = pair1["value"]
    list2 = pair2["value"]

    return lt.size(list1) < lt.size(list2)

def cmpArtistByBeginDate(artist1, artist2): 
    """
    Devuelve verdadero si la "BeginDate" del artista 1 es menor que la del artista 2.
    Args: artist1: información del primer artista que incluye su valor "BeginDate"
    artwork2: información del segundo artista que incluye su valor "BeginDate
    """
    
    return int(artist1["BeginDate"]) < int(artist2["BeginDate"])

def cmpStrings(string1, string2):
    if string1 == string2:
        return True
    else:
        return False

def cmpArterokByDateAcquired(artwork1, artwork2):

    """Compara las fechas de adquisición para ordenarlas ascendentemente"""

    Result = True

    if artwork1["DateAcquired"] == "" or artwork2["DateAcquired"] == "":
        return False
    
    else:
        Date1 = strDateToInt(artwork1['DateAcquired'])
        Date2 = strDateToInt(artwork2['DateAcquired'])

    return Date1 < Date2

def sortArtworks(catalog, size, sortingtype):
    sub_list = lt.subList(catalog['artworks'], 1, size)
    sub_list = sub_list.copy()
    start_time = time.process_time()
    if sortingtype == 1:
        sorted_list = sa.sort(sub_list, cmpArterokByDateAcquired)
    elif sortingtype == 2:
        sorted_list = ins.sort(sub_list, cmpArterokByDateAcquired)
    elif sortingtype == 3:
        sorted_list = mes.sort(sub_list, cmpArterokByDateAcquired)
    elif sortingtype == 4:
        sorted_list = quis.sort(sub_list, cmpArterokByDateAcquired)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000

    return elapsed_time_mseg, sorted_list

def cmpArterokByDate(artwork1, artwork2):
    
    Result = True

    if artwork1["Date"] == "" or artwork2["Date"] == "":
        return False
    
    else:
        Date1 =  artwork1['Date']
        Date2 = artwork2['Date']

    return Date1 < Date2

def cmpMaps(keyname, value):
    authentry = me.getKey(value)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def filterByDate(artworks, date0, date1): #O(n)
    filtredList = lt.newList(datastructure="ARRAY_LIST")
    for i in range(1, lt.size(artworks)+1):
        actualArtwork = lt.getElement(artworks, i)
        if date0 <= actualArtwork["DateAcquired"] <= date1:
            lt.addLast(filtredList, actualArtwork)

    return filtredList

def sortMediumsByDate(listm):
    
    sorted_list = mes.sort(listm, cmpArterokByDate)

    return sorted_list

def cmpArterokByCost(artwork1, artwork2):
    
    if artwork1['elementCost'] == None or artwork2['elementCost'] == None:
        print(artwork1)
    Cost1 =  artwork1['elementCost']
    Cost2 = artwork2['elementCost']

    return Cost1 > Cost2

def getArtistsName(catalog, constituentID):
    
    listconstituentID = constituentID[1:len(constituentID) - 1].split(", ")
    listconstituentIDn = lt.newList()
    for element in listconstituentID:
        lt.addLast(listconstituentIDn, element)
    i = 0
    j = 0
    artistNames = ""
    artistList = catalog["artists"]
    while i < lt.size(listconstituentIDn):
        element = lt.getElement(listconstituentIDn, i)
        if element == "-1":
            return "Anónimo"
        while j < lt.size(artistList):
            artist = lt.getElement(artistList, j)
            if element == artist["ConstituentID"]:
                artistNames += artist["DisplayName"] + " , "
                break
            j += 1
        i += 1
    
    return artistNames

def sortArtworksByAcquiredDate(filtredArtworks): #O(n log(n))
    start_time = time.process_time()

    sorted_list = mes.sort(filtredArtworks, cmpArterokByDateAcquired) 

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def filterTechnicArtists(catalog, ArtistName):

    filterListArtist = lt.newList()
    mediumList = lt.newList()
    newmedium = {}
    i = 0
    dataArtist = catalog["artists"]
    dataArtwork = catalog["artworks"]
    while i < lt.size(dataArtist):
        element = lt.getElement(dataArtist, i)
        artist = element["DisplayName"]
        if artist.lower() == ArtistName.lower():
            artistID = element["ConstituentID"]
            lt.addLast(filterListArtist, element)
        i = i + 1
    
    i = 0
    while i < lt.size(dataArtwork):
        element = lt.getElement(dataArtwork, i)
        artworkID = element["ConstituentID"] 
        if artistID in artworkID:
            medium = element["Medium"]
            if medium in newmedium:
                artworkmed = newmedium[medium]
                lt.addLast(artworkmed, element)
                newmedium[medium] = artworkmed
            else:
                artworkmed = lt.newList()
                lt.addLast(artworkmed, element)
                newmedium[medium] = artworkmed
                lt.addLast(mediumList, element)
        i = i + 1

    totalArtworks = 0
    mostTimes = 0
    for medium in newmedium:
        actual = lt.size(newmedium[medium])
        totalArtworks += actual
        if actual > mostTimes:
            mostTimes = actual
            granMedium = medium

    totalMediums = lt.size(mediumList)

    return totalArtworks, totalMediums, granMedium, mostTimes, newmedium

def transportArtworks(catalog, department):

    result = sortArtworksByDate(catalog, lt.size(catalog["artworks"]))
    listCost = lt.newList()

    filterListDept = lt.newList()
    i=0
    while i < lt.size(result[1]):
        element = lt.getElement(result[1],i)
        departmenti = element['Department']
        if departmenti.lower() == department.lower():
            lt.addLast(filterListDept,element)
        i = i + 1

    totalCost = 0
    totalWeight = 0
    i=0
    while i <= lt.size(filterListDept):
        element = lt.getElement(filterListDept,i)
        weight = element['Weight (kg)']
        height = element["Height (cm)"]
        lenght = element["Length (cm)"]
        width = element["Width (cm)"]
        if weight == "":
            kg = 0
            if height != "" and width != "":
                if lenght != "":
                    m3 = (float(height) * float(width) * float(lenght)) * 72
                else:
                    m2 = (float(height) * float(width)) * 72
                    m3 = 0
            else:
                m2 = 0
        else:
            kg = float(weight)
            totalWeight += kg
        sumx = kg + m2 + m3
        elementCost = 0
        if sumx != 0:
            elementCost = max(kg, m2, m3)
        else:
            elementCost = 48
        totalCost += elementCost
        element["elementCost"] = elementCost
        lt.addLast(listCost, element)
        i = i + 1

    sizeFilterListDept = lt.size(filterListDept)
    listByCost = mes.sort(listCost, cmpArterokByCost)

    return sizeFilterListDept, totalCost, totalWeight, filterListDept, listByCost

def sortArtworksByDate(catalog, size):
    sub_list = lt.subList(catalog['artworks'], 1, lt.size(catalog['artworks']))
    sub_list = sub_list.copy()
    start_time = time.process_time()
    sorted_list = mes.sort(sub_list, cmpArterokByDate)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000

    return elapsed_time_mseg, sorted_list

def findArtworksMedium(catalog, medium, nArtworks):

    listm = mp.get(catalog["medium"], medium)["value"]
    result = sortMediumsByDate(listm)
    if nArtworks > lt.size(result):
        return result
    else:
        sub_listn = lt.subList(result, 1, nArtworks)
        return sub_listn

def findArtist(ID: str, fullArtists):
    artistID = ID.replace("[","")
    artistID = artistID.replace("]","")

    IDs = artistID.split(", ")
    numArtists = len(IDs)

    artists = lt.newList(datastructure="ARRAY_LIST")

    n = 1
    numFounded = 0
    while (numFounded < numArtists) and (n <= lt.size(fullArtists)):
        actualArtist = lt.getElement(fullArtists, n)
        if actualArtist["ConstituentID"] in IDs:
            numFounded += 1
            lt.addLast(artists, actualArtist)
        n += 1
    
    return artists

def sortByBirth(catalog, year0, year1): 
    keyList = mp.keySet(catalog["birth"])
    filtredArtists = lt.newList(datastructure="ARRAY_LIST")
    
    for w in range(1, lt.size(keyList)+1):
        actualKey = lt.getElement(keyList, w)
        if int(year0) <= int(actualKey) <= int(year1):
            actualYearList = mp.get(catalog["birth"],actualKey)["value"]
            for k in range(1, lt.size(actualYearList)+1):
                actualArtist = lt.getElement(actualYearList, k)
                lt.addLast(filtredArtists, actualArtist)

    mes.sort(filtredArtists, cmpArtistByBeginDate)
 
    return filtredArtists

def findArtworksNationalities(catalog, nationality):
    listNat = mp.get(catalog["nationality"], nationality)["value"]

    return listNat