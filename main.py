import numpy as np

from enigma import Enigma

if __name__ == '__main__':
    with open("disks.npy", "rb") as f:
        disks = np.load(f)
        reverser = np.load(f)

    enigma = Enigma(disks, reverser, [15, 21, 3], [[0, 15, 7], [0]])

    encoded = enigma.encode("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(encoded)
    decoded = enigma.encode(encoded)
    print(decoded)
