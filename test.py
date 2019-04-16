# from Gameing import Game
# from Board import Board
#
# b=Board()
# game1=Game(b)
# game1.start()

"""
4_15
3.写获胜条件
4.按步骤输出运行时间
"""

# a = {(1, 2), (2, 4), (5, 6), (7, 8)}
# value, pos, move= max((move, -position-move*2, position) for (position, move) in a)
# print(value, pos, move)
import numpy as np
a=[1,2,3,1,1,1,1,0,0]
arr=np.array(a)
p=np.where(arr==0)
print(p)