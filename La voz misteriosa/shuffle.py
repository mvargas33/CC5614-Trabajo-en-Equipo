#!/usr/bin/env python3
from collections import deque
import os
import os.path
import random
import string

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
        os.rename(oldname, tempname)


if __name__ == '__main__':
    main()

    # Add numeration
    path = 'Audios'
    for count, filename in enumerate(os.listdir(path)):
        original = os.path.join(path, filename)
        new = os.path.join(path, str(count) + ' ' + filename)
        os.rename(original, new) 