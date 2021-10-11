# app.py
from flask import Flask, request, jsonify
import numpy as np
import random
import matplotlib.pyplot as plt

app = Flask(__name__)

CST_PLAIN = 0
CST_FOREST = 1
CST_MOUNTAIN = 2
CST_LAKE = 3
CST_BEACH = 4


@app.get("/generate")
def generateMap():
    mapLength = 56
    mapHeight = 32

    #generation de la map 56 * 32 avec uniquement des plaines
    map = np.full((mapLength, mapHeight), CST_PLAIN)

    #On applique l'algo de propagation pour, dans l'ordre, les forêts, les montagnes et les lacs
    center = [random.randint(0, mapLength -1 ), random.randint(0, mapHeight - 1)]
    map = generatePatch(map, center, CST_FOREST)

    center = [random.randint(0, mapLength -1 ), random.randint(0, mapHeight - 1)]
    map = generatePatch(map, center, CST_FOREST)

    center = [random.randint(0, mapLength -1 ), random.randint(0, mapHeight - 1)]
    map = generatePatch(map, center, CST_MOUNTAIN)

    center = [random.randint(0, mapLength -1 ), random.randint(0, mapHeight - 1)]
    map = generatePatch(map, center, CST_MOUNTAIN)

    center = [random.randint(0, mapLength -1 ), random.randint(0, mapHeight - 1)]
    map = generatePatch(map, center, CST_LAKE)

    center = [random.randint(0, mapLength -1 ), random.randint(0, mapHeight - 1)]
    map = generatePatch(map, center, CST_LAKE)

    #On termine par rajouter les plagesù
    map = generateBeaches(map)

    plt.matshow(map)
    plt.show()

def generatePatch(map, center, terrain):
    #Liste des cellules à traiter pour la propagation
    listCellToProcess = []

    #On génère une taille aléatoire pour le patch de terrain
    width = random.randint(5, 15)
    height = random.randint(5,15)

    # On place le centre
    map[center[0]][center[1]] = terrain

    #On propage le terrain
    listCellToProcess.append(center)
    map = propageTerrainFromCell(map, center, terrain, 1, listCellToProcess)


    #On retourne la map ainsi modifiée
    return map

def propageTerrainFromCell(map, cell, terrain, baseProba, listCellToProcess):
        #Reduction de proba entre les cellules
        probaReduce = 0.07

        #On enlève la cellule en cours des cellules à traiter
        listCellToProcess.remove(cell)

        #Propagation cellule à gauche
        currentCell = [cell[0],cell[1] - 1]
        #On vérifie que la cellule à changer n'est pas déjà transformée et qu'elle est bien dans les limites de la carte
        if (currentCell != terrain and currentCell[1] >= 0 ):
            probaPropagation = random.random()
            if probaPropagation < baseProba :
                listCellToProcess.append(currentCell)
                map[currentCell[0]][currentCell[1]] = terrain
                propageTerrainFromCell(map, currentCell, terrain, baseProba - probaReduce, listCellToProcess)

        #Propagation cellule à droite
        currentCell = [cell[0],cell[1] + 1]
        #On vérifie que la cellule à changer n'est pas déjà transformée et qu'elle est bien dans les limites de la carte
        if (currentCell != terrain and currentCell[1] < len(map[0])):
            probaPropagation = random.random()
            if probaPropagation < baseProba :
                listCellToProcess.append(currentCell)
                map[currentCell[0]][currentCell[1]] = terrain
                propageTerrainFromCell(map, currentCell, terrain, baseProba - probaReduce, listCellToProcess)

        #Propagation cellule en haut
        currentCell = [cell[0] - 1,cell[1]]
        #On vérifie que la cellule à changer n'est pas déjà transformée et qu'elle est bien dans les limites de la carte
        if (currentCell != terrain and currentCell[0] >= 0):
            probaPropagation = random.random()
            if probaPropagation < baseProba :
                listCellToProcess.append(currentCell)
                map[currentCell[0]][currentCell[1]] = terrain
                propageTerrainFromCell(map, currentCell, terrain, baseProba - probaReduce, listCellToProcess)

        #Propagation cellule en bas
        currentCell = [cell[0] + 1,cell[1]]
        #On vérifie que la cellule à changer n'est pas déjà transformée et qu'elle est bien dans les limites de la carte
        if (currentCell != terrain and currentCell[0] < len(map)):
            probaPropagation = random.random()
            if probaPropagation < baseProba :
                listCellToProcess.append(currentCell)
                map[currentCell[0]][currentCell[1]] = terrain
                propageTerrainFromCell(map, currentCell, terrain, baseProba - probaReduce, listCellToProcess)

        return map

def generateBeaches(map):
    #On parcourt la carte, pour chaque case d'eau on remplace ses voisins qui ne sont pas le l'eau par une plage
    for h in range(len(map)):
        for l in range(len(map[0])):
            if map[h][l] == CST_LAKE:
                map = replaceNeighboursByBeach(map, h, l)
    return map

def replaceNeighboursByBeach(map, h, l):
    #Cellule de gauche
    currentCell = [h, l-1]
    if(currentCell[1] >= 0 and map[currentCell[0]][currentCell[1]] != CST_LAKE and map[currentCell[0]][currentCell[1]] != CST_BEACH):
        map[currentCell[0]][currentCell[1]] = CST_BEACH

    #Cellule de droite
    currentCell = [h, l + 1]
    if (currentCell[1] < len(map[0]) and map[currentCell[0]][currentCell[1]] != CST_LAKE and map[currentCell[0]][
        currentCell[1]] != CST_BEACH):
        map[currentCell[0]][currentCell[1]] = CST_BEACH

    #Cellule du haut
    currentCell = [h - 1, l]
    if (currentCell[0] >= 0 and map[currentCell[0]][currentCell[1]] != CST_LAKE and map[currentCell[0]][
        currentCell[1]] != CST_BEACH):
        map[currentCell[0]][currentCell[1]] = CST_BEACH

    #Cellule du bas
    currentCell = [h + 1, l]
    if (currentCell[0] < len(map) and map[currentCell[0]][currentCell[1]] != CST_LAKE and map[currentCell[0]][
        currentCell[1]] != CST_BEACH):
        map[currentCell[0]][currentCell[1]] = CST_BEACH

    return map


generateMap()

