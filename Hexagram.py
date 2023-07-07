# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# This file, 'Hexagram.py,' was created by Alexandrae Duran on 2/25/23 at 12:37 AM for the 'iching' project.
#
# Description: This class defines a hexagram. A hexagram is made of two trigrams, the lower and upper. A trigram
# is made of three lines, with a single line called a "Yao." Depending on the hexagram, the lines can be encoded in
# either 2 bits or 4 bits. The order of the hexagram is from bottom to top. Starting at the lower trigram, the meaning
# of line 1 is often about beginnings, line 2 can embody the inner world and whether we are reacting like a victim or
# owning our condition. Line 3 shows the response when our thoughts meet with manifestation. Going into the upper
# hexagram line 4, this line can be the manifestation itself. Line 5 is often the highest expression of the lesson
# taught by each hexagram, and line 6 often refers to how the energy of a particular Hexagram becomes exhausted or ends.
# The text in the hexagram.xml consists of interpretations of the I Ching by Richard Wilhelm.
#
# The I Ching uses a type of divination called cleromancy. Traditionally, coins are used in the sortition.
#
# TODO: Implement other methods/sources for truly random generated numbers.
# TODO: Print out hexagram name
# TODO: Print out relevant text from hexagrams.xml
# TODO: Finish hexagrams.xml
# TODO: Produce more visually appealing hexagrams.
# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

import secrets


class Hexagram:

    BLANK = "[                       ]"
    DASHED = "[-----------------------]"

    def __init__(self):
        self._hexagram = []

        self._lower_trigram = Trigram()
        self._upper_trigram = Trigram()

        self._hexagram.append(self._lower_trigram)
        self._hexagram.append(self._upper_trigram)

    def flip_yaos(self):
        self._clear()
        for i in self._hexagram:
            i.flip_coins()

    def print(self):
        print(self.DASHED)
        print(self.BLANK + " | " + "HEX_NAME" + " | ")
        self._print_primary()
        print(self.BLANK + " | " + "HEX_NAME" + " | ")
        print(self.DASHED)
        print("\n")
        print(self.DASHED)
        print(self.BLANK + " | " + "HEX_NAME" + " | ")
        self._print_transformed()
        print(self.BLANK + " | " + "HEX_NAME" + " | ")
        print(self.DASHED)


    def _print_primary(self):
        hex_name = self.get_hex_name()
        self._hexagram.reverse()
        for i in self._hexagram:
            i.print_primary()
        self._hexagram.reverse()

    def _print_transformed(self):
        hex_name = self.get_hex_name()
        self._hexagram.reverse()

        for i in self._hexagram:
            i.print_transformed()
        self._hexagram.reverse()

    def _clear(self):
        self._hexagram = None
        self._lower_trigram = None
        self._upper_trigram = None

        self.__init__()


    def get_hex_name(self):
        pass


class Trigram:

    def __init__(self):
        self._trigram_yaos = []
        self._trigram_value = None
        self._trigram_name = None

        self._e0 = Yao()
        self._e1 = Yao()
        self._e2 = Yao()

        self._trigram_yaos.append(self._e0)
        self._trigram_yaos.append(self._e1)
        self._trigram_yaos.append(self._e2)

    def flip_coins(self):
        for i in self._trigram_yaos:
            i.flip_coins()
        self._calc_trigram()

    def print_primary(self):
        _ = []
        self._trigram_yaos.reverse()
        for i in self._trigram_yaos:
            j = i.print_primary()
            print(j[2][2] + " | " + j[2][1])
        self._trigram_yaos.reverse()

    def print_transformed(self):
        _ = []
        self._trigram_yaos.reverse()
        for i in self._trigram_yaos:
            j = i.print_transformed()
            print(j[1][0] + " | " + j[1][1])
        self._trigram_yaos.reverse()

    def _calc_trigram(self):
        for i in self._trigram_yaos:
            pass


class Yao:

    AT_YANG_UNCHANGE = "[@@@@@@@@@@@@@@@@@@@@@@@]"
    AT_YIN_UNCHANGE = "[@@@@@@@@       @@@@@@@@]"
    SH_YANG_CHANGING = "[#######################]"
    SH_YIN_CHANGING = "[########       ########]"
    TRANSFORMED_YANG = "[&&&&&&&&       &&&&&&&&]"
    TRANSFORMED_YIN = "[&&&&&&&&&&&&&&&&&&&&&&&]"



    def __init__(self):
        self._coin_1 = Coin()
        self._coin_2 = Coin()
        self._coin_3 = Coin()

        self._yao = []
        self._yao.append(self._coin_1)
        self._yao.append(self._coin_2)
        self._yao.append(self._coin_3)

        self._sum = None

        self._yao_name_yinyang = None
        self._yao_name_young_old = None
        self._yao_name_transformed = None

        self._YINYANG = lambda x: ["[0X0]", "Yin"] if x == 1 or x == 3 else ["[000]", "Yang"]

        self._YINYANG_YOUNGOLD = {0: ["{000}", "Changing Yang   ", self.SH_YANG_CHANGING, 0],
                                  1: ["[0X0]", "Unchanging Yin  ", self.AT_YIN_UNCHANGE, 1],
                                  2: ["[000]", "Unchanging Yang ", self.AT_YANG_UNCHANGE, 0],
                                  3: ["{0X0}", "Changing Yin    ", self.SH_YIN_CHANGING, 1]}
        self._TRANSFORMED = {0: [self.TRANSFORMED_YANG, "Transformed Yang"],
                                  1: [self.AT_YIN_UNCHANGE, "Unchanging Yin"],
                                  2: [self.AT_YANG_UNCHANGE, "Unchanged Yang"],
                                  3: [self.TRANSFORMED_YIN, "Transformed Yin"]}

    def flip_coins(self):
        for i in self._yao:
            i.flip()
        self._calc_name()

    def _calc_name(self):
        _sum = self._sum_coins()

        self._yao_name_yinyang = self._YINYANG(_sum)
        self._yao_name_young_old = self._YINYANG_YOUNGOLD[_sum]
        self._yao_name_transformed = self._TRANSFORMED[_sum]
        self._sum = _sum

    def _sum_coins(self):
        _sum = 0

        for i in self._yao:
            if i.get_state():
                _sum = i.get_state()[0] + _sum

        return _sum

    def print_primary(self):
        _ = self._yao_name_young_old
        return [self._sum, self._yao_name_yinyang, self._yao_name_young_old]

    def print_transformed(self) :
        return [self._sum, self._yao_name_transformed, self._yao_name_young_old]


class Coin:

    def __init__(self):
        self._state = None
        self._rand_below = 2
        self._calc_state = lambda x: [0, "[ 0 ]"] if x == 0 else [1, "[ 1 ]"]
        self.count = 0
        self.dot = "."

    def flip(self):
        input("Press and hold 'return/enter' while thinking of your question to proceed.")
        _ = self._gen_state()
        print(self.dot*self.count)
        self.count += 1
        self._set_state(self._calc_state(_))

    def _gen_state(self):
        return secrets.randbelow(self._rand_below)

    def _set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state


class Doorway:

    def __init__(self):
        self.hex = Hexagram()
        print("Think of an open ended question.")
        print("If the answer can be answered with a 'yes,' or a 'no' you are throwing wrong.")
        self.question = input("If you like, type your question out here, otherwise hold the question in your mind then press and hold enter: ")
        print("..........................")

    def cast(self):
        self.hex.flip_yaos()
        print("Q:" + self.question)
        self.hex.print()


if __name__ == "__main__":
    _ = Doorway()
    _.cast()
