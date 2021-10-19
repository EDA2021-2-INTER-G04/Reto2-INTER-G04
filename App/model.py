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
               "birth": None,
               "dateAcquired": None,
               "department": None,
               "artistName": None}

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

    catalog["dateAcquired"] = mp.newMap(initialSize, maptype="CHAINING", loadfactor=4.0, comparefunction=cmpMaps)

    catalog["department"] = mp.newMap(10, maptype="PROBING", loadfactor=0.5, comparefunction=cmpMaps)

    catalog["artistName"] = mp.newMap(numArtists, maptype="CHAINING", loadfactor=4.0, comparefunction=cmpMaps)

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
    
    dateAcquired = artwork["DateAcquired"]
    isPresentdA = mp.contains(catalog["dateAcquired"], dateAcquired)
    if isPresentdA == True:
        listdA = mp.get(catalog["dateAcquired"], dateAcquired)["value"]
        lt.addLast(listdA, artwork)
        mp.put(catalog["dateAcquired"], dateAcquired, listdA)
    else:
        listdA = lt.newList('ARRAY_LIST')
        lt.addLast(listdA, artwork)
        mp.put(catalog["dateAcquired"], dateAcquired, listdA)


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

    artworkDepartment = artwork["Department"]
    isPresent = mp.contains(catalog["department"], artworkDepartment)
    if isPresent:
        listd = mp.get(catalog["department"], artworkDepartment)["value"]
        lt.addLast(listd, artwork)
        mp.put(catalog["department"], artworkDepartment, listd)
    else:
        listd = lt.newList('ARRAY_LIST')
        lt.addLast(listd, artwork)
        mp.put(catalog["department"], artworkDepartment, listd)


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
    
    artistName = artist["DisplayName"]
    isPresent = mp.contains(catalog["artistName"], artistName)
    if isPresent:
        listA = mp.get(catalog["artistName"], artistName)["value"]
        lt.addLast(listA, artist)
        mp.put(catalog["artistName"], artistName, listA)
    else:
        listA = lt.newList('ARRAY_LIST')
        lt.addLast(listA, artist)
        mp.put(catalog["artistName"], artistName, listA)
    

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

    """Convierte una fecha dada a datetime para comparación"""

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

def cmpByDate(pair1, pair2):
    date1 = pair1["key"]
    date2 = pair2["key"]

    return strDateToInt(date1) < strDateToInt(date2)

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

def cmpArterokByDateAcquired(date1, date2):

    """Compara las fechas de adquisición para ordenarlas ascendentemente"""

    if date1 == "" or date2 == "":
        return -1
    else:
        Date1 = strDateToInt(date1)
        Date2 = strDateToInt(date2)

    if (Date1 == Date2):
        return 0
    elif (Date1 > Date2):
        return 1
    else:
        return -1

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

def filterByDate(artworks, date0, date1): 
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

def filterTechnicArtists(catalog, ArtistName):

    ListArtist = mp.keySet(catalog["artistName"])
    found = False
    k=1
    while found == False and k <= lt.size(ListArtist):
        actualArtist = lt.getElement(ListArtist, k)
        actualKey = mp.get(catalog["artistName"], actualArtist)["key"]
        if actualKey.lower() == ArtistName.lower():
            filterListArtist = mp.get(catalog["artistName"], actualKey)["value"]
            element0 = lt.getElement(filterListArtist, 1)
            artistID = element0["ConstituentID"]
            found = True
        k += 1
    
    dataArtwork = catalog["artworks"]
    mediumList = lt.newList()
    newmedium = {}

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
    departmentsList = mp.keySet(catalog["department"])
    found = False
    k=1
    while found == False and k <= lt.size(departmentsList):
        actualDep = lt.getElement(departmentsList, k)
        actualKey = mp.get(catalog["department"], actualDep)["key"]
        if actualKey.lower() == department.lower():
            filterListDept = mp.get(catalog["department"], actualKey)["value"]
            mes.sort(filterListDept, cmpArterokByDate)
            found = True
        k += 1
    
    listCost = lt.newList(datastructure="ARRAY_LIST")
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
        else:
            kg = float(weight)
            totalWeight += kg

        if height != "" and width != "":
            if lenght != "":
                m3 = ((float(height)/100) * (float(width)/100) * (float(lenght)/100)) * 72
            else:
                m2 = ((float(height)/100) * (float(width)/100)) * 72
                m3 = 0
        else:
            m2 = 0
        
        sumx = kg + m2 + m3
        elementCost = 0
        if sumx != 0:
            elementCost = max(kg, m2, m3)
        else:
            elementCost = 48
        totalCost += elementCost
        element["elementCost"] = round(elementCost,2)
        lt.addLast(listCost, element)
        i += 1

    sizeFilterListDept = lt.size(filterListDept)
    listByCost = mes.sort(listCost, cmpArterokByCost)

    return sizeFilterListDept, round(totalCost,2), round(totalWeight,2), filterListDept, listByCost

def sortArtworksByDate(catalog, size):
    sub_list = lt.subList(catalog['artworks'], 1, lt.size(catalog['artworks']))
    sub_list = sub_list.copy()
    sorted_list = mes.sort(sub_list, cmpArterokByDate)

    return sorted_list

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

def sortArtworksByAcquiredDate(catalog, date0, date1): 

    orderedDateA = lt.newList(datastructure="ARRAY_LIST")
    datesA = mp.keySet(catalog["dateAcquired"])
    for i in range(1, lt.size(datesA)+1):
        actualKey = lt.getElement(datesA, i)
        actualPair = mp.get(catalog["dateAcquired"],actualKey)
        if actualKey != None and actualKey != "":
            if strDateToInt(date0) <= strDateToInt(actualKey) <= strDateToInt(date1):
                lt.addLast(orderedDateA, actualPair)
    
    mes.sort(orderedDateA, cmpByDate)

    return orderedDateA
