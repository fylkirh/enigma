import copy

import numpy as np

ROTOR_SIZE = 26
ORD_OFFSET = 97
NUM_ROTORS = 3


class EnigmaException(Exception):
    pass


def _invert_rotors(rotors):
    bare_range = np.array(range(ROTOR_SIZE))
    rotors_inv = []
    for i in range(NUM_ROTORS):
        rotor_mapped = np.stack((rotors[i], bare_range))
        rotor_list = rotor_mapped.tolist()
        rotor = [x[1] for x in sorted(zip(rotor_list[0], rotor_list[1]))]
        rotors_inv.append(rotor)
    return np.array(rotors_inv)


class Enigma:
    def __init__(self, rotors, reflector, init_positions, rotation_positions):
        if rotors.shape != (NUM_ROTORS, ROTOR_SIZE):
            raise EnigmaException("Invalid rotor array size")
        self.rotors = rotors
        # generate an inverse indexing of rotors for a backward passthrough
        self.rotors_inv = _invert_rotors(rotors)
        if len(reflector) != ROTOR_SIZE:
            raise EnigmaException("Invalid reflector size")
        self.reflector = reflector
        if len(init_positions) != NUM_ROTORS:
            raise EnigmaException("Invalid init positions array size")
        self.init_positions = copy.deepcopy(init_positions)
        self.positions = init_positions
        if len(rotation_positions) != NUM_ROTORS - 1:
            raise EnigmaException("Invalid rotation positions array size")
        self.rotation_positions = rotation_positions
        self.rotated = [False] * NUM_ROTORS

    def _reset(self):
        self.positions = copy.deepcopy(self.init_positions)
        self.rotated = [False] * NUM_ROTORS

    def encode(self, string):
        self._reset()
        res = ""
        for char in string.lower():
            char_num = ord(char) - ORD_OFFSET
            for i in range(NUM_ROTORS):
                # rotor rotations
                if i == 0:
                    self.positions[i] = (self.positions[i] + 1) % ROTOR_SIZE
                    self.rotated[i] = True
                else:
                    if self.rotated[i - 1] and not self.rotated[i] and any(
                            [self.positions[i - 1] == (self.positions[i] + rotation_position) % ROTOR_SIZE for
                             rotation_position in self.rotation_positions[i - 1]]):
                        self.positions[i] = (self.positions[i] + 1) % ROTOR_SIZE
                        self.rotated[i] = True
                        self.rotated[i - 1] = False
                    else:
                        self.rotated[i] = False
                # character translation through one rotor
                char_num = (self.rotors[i][(char_num - self.positions[i]) % ROTOR_SIZE] + self.positions[i]) % ROTOR_SIZE
            # translate character through the reflector
            char_num = self.reflector[char_num]
            for i in reversed(range(NUM_ROTORS)):
                char_num = (self.rotors_inv[i][(char_num - self.positions[i]) % ROTOR_SIZE] + self.positions[
                    i]) % ROTOR_SIZE
            res += chr(char_num + ORD_OFFSET)
        return res
