import numpy as np
import cv2

x1, x2 = -2.1, 0.6
y1, y2 = -1.2, 1.2
zoom = 100
iteration_max = 50
image_x = int((x2 - x1) * zoom)
image_y = int((y2 - y1) * zoom)

img = np.zeros((image_y, image_x, 3), np.uint8)

for x in range(image_x):
    for y in range(image_y):
        c_r = x / zoom + x1
        c_i = y / zoom + y1
        z_r, z_i = 0, 0
        j = 0
        while z_r**2 + z_i**2 < 4 and j < iteration_max:
            tmp = z_r
            z_r = z_r**2 - z_i**2 + c_r
            z_i = 2*z_i*tmp + c_i
            j += 1
        if j == iteration_max:
            color = (0, 0, 0) 
        else:
            color = (0, 0, j * 255 // iteration_max)
        img[y, x] = color

cv2.imshow('Fractale de Mendelbort', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
