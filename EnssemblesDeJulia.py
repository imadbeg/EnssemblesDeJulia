import numpy as np
import cv2

x1, x2 = -2.1, 0.6
y1, y2 = -1.2, 1.2
image_x = 270
image_y = 240
iteration_max = 50
zoom_x = image_x / (x2 - x1)
zoom_y = image_y / (y2 - y1)

img = np.zeros((image_y, image_x, 3), np.uint8)

for x in range(image_x):
    for y in range(image_y):
        c_r = x / zoom_x + x1
        c_i = y / zoom_y + y1
        z_r, z_i = c_r, c_i
        j = 0
        while z_r*z_r + z_i*z_i < 4 and j < iteration_max:
            tmp = z_r
            z_r = z_r**2 - z_i**2 + c_r
            z_i = 2*z_i*tmp + c_i
            j += 1
        color_value = 255 - int(j * 255 / iteration_max)
        img[y, x] = (color_value, color_value, color_value)


cv2.imshow('Enssemble de Julia', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
