#!/usr/bin/env python3
from collections import deque
import os
import os.path
import random
import string

def find_next(pairs, nextt, prev):
    for i in range(0, len(pairs)):
        if pairs[i][0] == nextt and i > prev:
            return i
    return -1

def printWay(pairs):
    pendientes = pairs[:]
    #print(pendientes)

    i = 0
    while True:
        if i >= len(pendientes):
            break
        e = pendientes[i]
        fromm = e[0]
        too = e[1]
        #print("from " + fromm)
        #print("too " + too)
        index = i
        while True:
            index = find_next(pendientes, too, index)
            if index == -1:
                print(fromm + ' => ' + too)
                break
            else:
                too = pendientes[index][1]
                #print("too " + too)
        i+=1



def random_renames(files):
    """
    Generate a list of randomised renames to shuffle a list of files.

    Example:
        random_renames(["a", "b", "c"])
    This might generate:
        ("a", "c"), ("b", "a"), ("c", "b")

    Where each tuple indicates first the original name, and then the new name
    of the file.
    """

    remaining_names = files[:]  # Note: copying the list because we will modify this one

    for orig in files:
        # Find a list of potential new names, which is all unused names, except
        # the current filename
        potential_names = [name for name in remaining_names if name != orig]
        # Pick one from that list and remove it from our pool of unused names
        newname = random.choice(potential_names)
        remaining_names.remove(newname)

        # Output this rename from the generator
        yield (orig, newname)


def main():
    pairs = []
    """
    Renames files in the 'shuffleme' directory in such a way as to shuffle all
    of them between their existing names.
    """
    # I just created a directory called "shuffleme" in CWD, replace this with
    # your full path if necessary
    path = 'Audios'

    # Get the existing files from that directory
    files = os.listdir(path)

    # Prefix all the names with the dir name
    files = [os.path.join(path, name) for name in files]

    # Generate our list of randomised renames from the directory list.  This is
    # a deque for reasons that might be clearer later on.  (A deque is like a
    # list but designed for fast adding/removing from either end)
    file_renames = deque(random_renames(files))

    while file_renames:  # While there are still files left to rename
        # Get our first intended rename
        oldname, newname = file_renames.popleft()

        # Avoid trying to rename files to the same name. This involves adding
        # random characters to the name until we hit on a name that doesn't
        # exist, then renaming to this compromise of a name, and then delaying
        # the rename to the real name.
        tempname = newname
        while os.path.exists(tempname):
            tempname += random.choice(string.ascii_letters)

        # If we did have to change names...
        if tempname != newname:
            # ... then remember to rename to the new name
            file_renames.append((tempname, newname))
            # Sanity check: we definitely *are* going to rename the original
            # user of this name away, right? If not, we're in for an infinite
            # loop.
            assert any(name == newname for name, _ in file_renames)

        # Perform the actual rename. Not renaming to newname (actual new name),
        # but tempname (same as newname unless that file exists, in which case
        # we already delayed a separate rename).
        pairs.append([oldname, tempname])
        print(oldname + " -> " + tempname)
        os.rename(oldname, tempname)
    
    print('\n')
    printWay(pairs)


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