import numpy as np

disks = []
for x in range(3):
    perm = list(range(26))
    while any([perm[i] == i for i in range(26)]):
        perm = np.random.permutation(26)
    disks.append(perm)

reverser_raw = np.random.permutation(26)
reverser_mapped = np.stack((reverser_raw, np.roll(reverser_raw, 26 // 2)))
reverser_list = reverser_mapped.tolist()
reverser = [x[1] for x in sorted(zip(reverser_list[0], reverser_list[1]))]
reverser_np = np.array(reverser)
disks_np = np.array(disks)

with open("disks.npy", "wb") as f:
    np.save(f, disks_np)
    np.save(f, reverser_np)

with open("disks.npy", "rb") as f:
    d = np.load(f)
    r = np.load(f)
print(d)
print("\n")
print(r)