import numpy as np
from PIL import Image
from numpy import asarray
#move your image file to the python project
image = Image.open('maze4.png') #change the 'maze4.png' to name of your maze image
image_as_array=asarray(image)

spaces = [1 if (pixel == [0, 0, 0, 0]).all() else 0 for pixel in image_as_array]

# print(image_as_array)
# print(spaces)

places_can_go = []

for i in range(20):
    for j in range(20):
        if (image_as_array[i][j] == np.array([0, 0, 0, 0])).all():
            places_can_go.append([i, j])
print(places_can_go)

locations=np.array(places_can_go)

locations = np.transpose(locations)

np.save('data/location20x20_maze4.npy', locations)

#create two new files: one for locations and one for adjacency matrix, then replace all the file links in the run sim code and create adj mat code accordingly