#!/usr/bin/env python3
from collections import deque
import os
import os.path
import random
import string

def myShuffle(path):
    moves = []

    files = os.listdir(path)
    files = [os.path.join(path, name) for name in files]

    if len(files) % 2 == 1:
        reserva = files.pop()

    while len(files) > 0:
        primero = files.pop(random.randint(0, len(files)-1))
        segundo = files.pop(random.randint(0, len(files)-1))
        os.rename(primero, primero + "QWERTY")
        os.rename(segundo, segundo + "QWERTY")
        os.rename(primero + "QWERTY", segundo)
        os.rename(segundo + "QWERTY", primero)
        moves.append([primero, segundo])
        print(primero + " <-> " + segundo)

    if reserva != None:
        os.rename(segundo, segundo + "QWERTY")
        os.rename(reserva, reserva + "QWERTY")
        os.rename(segundo + "QWERTY", reserva)
        os.rename(reserva + "QWERTY", segundo)
        moves.append([segundo, reserva])
        print(segundo + " <-> " + reserva)

    # print(moves)



if __name__ == '__main__':
    path = 'Audios'

    # Shuffle
    myShuffle(path) 
    
    # Add numeration
    for count, filename in enumerate(os.listdir(path)):
        original = os.path.join(path, filename)
        new = os.path.join(path, str(count) + ' ' + filename)
        os.rename(original, new) 