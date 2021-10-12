import numpy as np
import random
import sys
import json
np.set_printoptions(threshold=sys.maxsize)

CST_PLAIN = 0
CST_FOREST = 1
CST_MOUNTAIN = 2
CST_LAKE = 3
CST_BEACH = 4
CST_TEMPORARY_BEACH = 5

def generateMap():

    mapLength = 56
    mapHeight = 32

    # generation de la map 56 * 32 avec uniquement des plaines
    map = np.full((mapLength, mapHeight), CST_PLAIN)

    # On applique l'algo de propagation pour, dans l'ordre, les forêts, les montagnes et les lacs
    center = [random.randint(0, mapLength - 1), random.randint(0, mapHeight - 1)]
    map = generatePatch(map, center, CST_FOREST)

    center = [random.randint(0, mapLength - 1), random.randint(0, mapHeight - 1)]
    map = generatePatch(map, center, CST_FOREST)

    center = [random.randint(0, mapLength - 1), random.randint(0, mapHeight - 1)]
    map = generatePatch(map, center, CST_MOUNTAIN)

    center = [random.randint(0, mapLength - 1), random.randint(0, mapHeight - 1)]
    map = generatePatch(map, center, CST_LAKE)

    # On termine par rajouter les plages
    map = generateBeaches(map, 3)

    map = np.transpose(map)
    mapList = map.tolist()
    return json.dumps(mapList)


def generatePatch(map, center, terrain):
    # Liste des cellules à traiter pour la propagation
    listCellToProcess = []

    # On place le centre
    map[center[0]][center[1]] = terrain

    # On propage le terrain
    listCellToProcess.append(center)
    map = propageTerrainFromCell(map, center, terrain,random.uniform(0.8, 1), listCellToProcess)

    # On retourne la map ainsi modifiée
    return map


def propageTerrainFromCell(map, cell, terrain, baseProba, listCellToProcess):

    # On enlève la cellule en cours des cellules à traiter
    listCellToProcess.remove(cell)

    # Propagation cellule à gauche
    currentCell = [cell[0], cell[1] - 1]
    # On vérifie que la cellule à changer n'est pas déjà transformée et qu'elle est bien dans les limites de la carte
    if (currentCell != terrain and currentCell[1] >= 0):
        probaPropagation = random.random()
        if probaPropagation < baseProba:
            listCellToProcess.append(currentCell)
            map[currentCell[0]][currentCell[1]] = terrain
            propageTerrainFromCell(map, currentCell, terrain, baseProba - random.uniform(0.05, 0.07), listCellToProcess)

    # Propagation cellule à droite
    currentCell = [cell[0], cell[1] + 1]
    # On vérifie que la cellule à changer n'est pas déjà transformée et qu'elle est bien dans les limites de la carte
    if (currentCell != terrain and currentCell[1] < len(map[0])):
        probaPropagation = random.random()
        if probaPropagation < baseProba:
            listCellToProcess.append(currentCell)
            map[currentCell[0]][currentCell[1]] = terrain
            propageTerrainFromCell(map, currentCell, terrain, baseProba - random.uniform(0.05, 0.07), listCellToProcess)

    # Propagation cellule en haut
    currentCell = [cell[0] - 1, cell[1]]
    # On vérifie que la cellule à changer n'est pas déjà transformée et qu'elle est bien dans les limites de la carte
    if (currentCell != terrain and currentCell[0] >= 0):
        probaPropagation = random.random()
        if probaPropagation < baseProba:
            listCellToProcess.append(currentCell)
            map[currentCell[0]][currentCell[1]] = terrain
            propageTerrainFromCell(map, currentCell, terrain, baseProba - random.uniform(0.05, 0.07), listCellToProcess)

    # Propagation cellule en bas
    currentCell = [cell[0] + 1, cell[1]]
    # On vérifie que la cellule à changer n'est pas déjà transformée et qu'elle est bien dans les limites de la carte
    if (currentCell != terrain and currentCell[0] < len(map)):
        probaPropagation = random.random()
        if probaPropagation < baseProba:
            listCellToProcess.append(currentCell)
            map[currentCell[0]][currentCell[1]] = terrain
            propageTerrainFromCell(map, currentCell, terrain, baseProba - random.uniform(0.01, 0.07), listCellToProcess)

    return map


def generateBeaches(map, rangePlage):

    # On parcourt la carte, pour chaque case d'eau on remplace ses voisins qui ne sont pas le l'eau par une plage
    for i in range(rangePlage):
        for h in range(len(map)):
            for l in range(len(map[0])):
                if map[h][l] == CST_LAKE or map[h][l] == CST_BEACH:
                    map = replaceNeighboursByTemporaryBeach(map, h, l)
        map = replaceTemporaryBeach(map)

    return map


def replaceNeighboursByTemporaryBeach(map, h, l):

    # Cellule de gauche
    if l-1 >= 0 and map[h][l-1] != CST_LAKE and map[h][l-1] != CST_BEACH:
        map[h][l-1] = CST_TEMPORARY_BEACH

    # Cellule de droite
    if l+1 < len(map[0]) and map[h][l+1] != CST_LAKE and map[h][l+1] != CST_BEACH:
        map[h][l+1] = CST_TEMPORARY_BEACH

    # Cellule du haut
    if h-1 >= 0 and map[h-1][l] != CST_LAKE and map[h-1][l] != CST_BEACH:
        map[h-1][l] = CST_TEMPORARY_BEACH

    # Cellule du bas
    if h+1 < len(map) and map[h+1][l] != CST_LAKE and map[h+1][l] != CST_BEACH:
        map[h+1][l] = CST_TEMPORARY_BEACH

    return map


def replaceTemporaryBeach(map):
    for h in range(len(map)):
        for l in range(len(map[0])):
            if map[h][l] == CST_TEMPORARY_BEACH:
                map[h][l] = CST_BEACH
    return map
