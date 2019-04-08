import numpy as np

a = np.array([[1, 0],[2,4]])
indices = np.where(a == 0)
for coords in list(zip(indices[0], indices[1])):
	print(coords[0], coords[1])

