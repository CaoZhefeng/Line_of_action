import random

exm_turn = 100000
counter = 0
for i in range(exm_turn):
	x = random.uniform(-1, 1)
	y = random.uniform(-1, 1)
	if x ** 2 + y ** 2 < 1:
		counter = counter + 1
print("pi:{0}".format((4 * counter / exm_turn)))
