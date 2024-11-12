import cv2
import numpy as np
import random
from time import sleep as wait

squareResolution = 40 # Résolution de la grille carrée
screenWidth = 900 # Largeur de l'écran
screenHeight = 900  # Hauteur de l'écran

backgroundColor = (0, 0, 0)
nodeColourOff = (200, 200, 200)
nodeColourOn = (255, 255, 255)
nodeRadius = int((screenWidth / squareResolution) / 8)
lineColour = (255, 255, 255)

nodeOffThreshold = 0.5
nodeOffMaximum = 1

resetDelay = 1
resetToggled = False

squares = np.zeros((squareResolution + 1, squareResolution + 1), dtype=int)


# Générer aléatoirement l'état des nœuds dans la grille de carrés
def generate_square_corners():
    global squares
    squares = np.random.choice([0, 1], size=(squareResolution + 1, squareResolution + 1),
                               p=[1 - nodeOffThreshold, nodeOffThreshold])



# Dessiner les cercles représentant les nœuds dans l'image
def draw_square_corners(image):
    for x in range(squareResolution + 1):
        for y in range(squareResolution + 1):
            color = nodeColourOff if squares[x][y] == 0 else nodeColourOn
            cv2.circle(image, (int(x * (screenWidth / squareResolution)), int(y * (screenHeight / squareResolution))),
                       nodeRadius, color, -1)



# Dessiner les lignes pour représenter les isolignes
def draw_line(image, start_coords, end_coords):
    cv2.line(image, start_coords, end_coords, lineColour, 1)


# Générer les isolignes selon l'état des nœuds dans la grille de carrés
def draw_isolines(image):
    for x in range(squareResolution):
        for y in range(squareResolution):
            case = get_case_from_corners(
                squares[x][y],
                squares[x + 1][y],
                squares[x + 1][y + 1],
                squares[x][y + 1]
            )
            xPos = int(x * (screenWidth / squareResolution))
            yPos = int(y * (screenHeight / squareResolution))

            edgeA = (xPos + int((screenWidth / squareResolution) * 0.5), yPos)
            edgeB = (xPos + int(screenWidth / squareResolution), yPos + int((screenHeight / squareResolution) * 0.5))
            edgeC = (xPos + int((screenWidth / squareResolution) * 0.5), yPos + int(screenHeight / squareResolution))
            edgeD = (xPos, yPos + int((screenHeight / squareResolution) * 0.5))

            # Dessiner les lignes pour chaque cas d'isoline
            if case in [1, 14]:
                draw_line(image, edgeC, edgeD)
            if case in [2, 13]:
                draw_line(image, edgeB, edgeC)
            if case in [3, 12]:
                draw_line(image, edgeB, edgeD)
            if case in [4, 11]:
                draw_line(image, edgeA, edgeB)
            if case == 5:
                draw_line(image, edgeA, edgeD)
                draw_line(image, edgeB, edgeC)
            if case in [6, 9]:
                draw_line(image, edgeA, edgeC)
            if case in [7, 8]:
                draw_line(image, edgeA, edgeD)
            if case == 10:
                draw_line(image, edgeA, edgeB)
                draw_line(image, edgeC, edgeD)

def get_case_from_corners(a, b, c, d):
    return (a * 8) + (b * 4) + (c * 2) + d

nodesToggled = True
def run():
    global nodesToggled  
    while True:
        generate_square_corners()
        canvas = np.zeros((screenHeight, screenWidth, 3), dtype=np.uint8)

        if nodesToggled:
            draw_square_corners(canvas)

        draw_isolines(canvas)
        cv2.imshow("Marching squares", canvas)

        if not resetToggled:
            break

        if cv2.waitKey(resetDelay * 1000) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    nodesToggled = True  # Définir l'état initial des nœuds à afficher
    while True:
        generate_square_corners()
        canvas = np.zeros((screenHeight, screenWidth, 3), dtype=np.uint8)

        if nodesToggled:
            draw_square_corners(canvas)

        draw_isolines(canvas)
        cv2.imshow("Marching squares", canvas)

        key = cv2.waitKey(resetDelay * 1000)  

        if key == ord('q') or key == 27:  
            break
        elif key == ord('t'): 
            nodesToggled = not nodesToggled

    cv2.destroyAllWindows()