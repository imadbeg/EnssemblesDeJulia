import numpy as np
import cv2
import math

# la taille de l'image et la profondeur de récursion
IMG_SIZE = 512
ORDER = 2

def draw_koch_segment(img, a, b, n):
    if n == 0:
        cv2.line(img, a, b, (255, 255, 255), 1)
    else:
        xa, ya = a
        xb, yb = b
        xc = int(xa + (xb - xa) / 3)
        yc = int(ya + (yb - ya) / 3)
        xd = int(xa + 2 * (xb - xa) / 3)
        yd = int(ya + 2 * (yb - ya) / 3)

        # le sommet du triangle 
        xe = int((xc + xd) / 2 - (math.sqrt(3) / 6) * (yd - yc))
        ye = int((yc + yd) / 2 + (math.sqrt(3) / 6) * (xd - xc))

        #  Appeles récursifs pour les quatre petits segments
        draw_koch_segment(img, a, (xc, yc), n-1)
        draw_koch_segment(img, (xc, yc), (xe, ye), n-1)
        draw_koch_segment(img, (xe, ye), (xd, yd), n-1)
        draw_koch_segment(img, (xd, yd), b, n-1)

# Image de base
img_triangle = np.zeros((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8)
img_koch = np.zeros((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8)

# les trois sommets du triangle initial
vertex_a = (IMG_SIZE // 2, IMG_SIZE // 8)
vertex_b = (IMG_SIZE // 8, IMG_SIZE * 7 // 8)
vertex_c = (IMG_SIZE * 7 // 8, IMG_SIZE * 7 // 8)

#  Dessiner le triangle de base sur son image
cv2.line(img_triangle, vertex_a, vertex_b, (255, 255, 255), 1)
cv2.line(img_triangle, vertex_b, vertex_c, (255, 255, 255), 1)
cv2.line(img_triangle, vertex_c, vertex_a, (255, 255, 255), 1)

draw_koch_segment(img_koch, vertex_a, vertex_b, ORDER)
draw_koch_segment(img_koch, vertex_b, vertex_c, ORDER)
draw_koch_segment(img_koch, vertex_c, vertex_a, ORDER)

cv2.imshow('Triangle de base', img_triangle)
cv2.imshow('Flocon de Koch', img_koch)

cv2.waitKey(0)
cv2.destroyAllWindows()
