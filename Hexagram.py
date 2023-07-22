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
# The I Ching uses a type of divination called cleromancy. Traditionally, yarrow sticks or coins are used in the
# sortition.
#
# TODO: Implement other methods/sources for truly random generated numbers.
# TODO: Print out hexagram name
# TODO: Print out relevant text from hexagrams.xml
# TODO: Finish hexagrams.xml
# TODO: Produce more visually appealing hexagrams.
# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
import secrets
import time
import RFExplorer
from RFExplorer import RFE_Common
import xml.etree.ElementTree as et


class Hexagram:

    BLANK = "[                       ]"
    DASHED = "[-----------------------]"

    def __init__(self, method="1"):
        self._hexagram = []
        self._rf_exp = None
        self._rf_exp_inst = None
        self._method = method

        if int(self._method) == 2:
            print("init rf explorer...")
            self._rf_exp = RFExplorer.RFECommunicator()

        self.set_trigrams()

    def set_trigrams(self):
        self._lower_trigram = Trigram(self._method, self._rf_exp)
        self._upper_trigram = Trigram(self._method, self._rf_exp)

        self._hexagram.append(self._lower_trigram)
        self._hexagram.append(self._upper_trigram)

    def flip_yaos(self):
        if self._method == 1:
            for i in self._hexagram:
                i.flip_coins()
        elif int(self._method) == 2:
            self._rf_exp = RFExplorer.RFECommunicator()
            self._rf_exp.GetConnectedPorts()
            if (self._rf_exp.ConnectPort("/dev/cu.SLAB_USBtoUART", 500000)):
                self._rf_exp.SendCommand("r")
                # Wait for unit to notify reset completed
                while (self._rf_exp.IsResetEvent):
                    pass
                time.sleep(8)

                self._rf_exp.SendCommand_RequestConfigData()
                while (self._rf_exp.ActiveModel == RFExplorer.RFE_Common.eModel.MODEL_NONE):
                    self._rf_exp.ProcessReceivedString(True)  # Process the received configuration
                for i in self._hexagram:
                    i.flip_coins(self._rf_exp)
            self._rf_exp.Close()  # Finish the thread and close port
            self._rf_exp = None

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

    def get_hex_name(self):
        pass


class Trigram:

    def __init__(self, method, rf_exp=None):
        self._trigram_yaos = []
        self._trigram_value = None
        self._trigram_name = None

        self._y0 = Yao(method, rf_exp)
        self._y1 = Yao(method, rf_exp)
        self._y2 = Yao(method, rf_exp)

        self._trigram_yaos.append(self._y0)
        self._trigram_yaos.append(self._y1)
        self._trigram_yaos.append(self._y2)

    def flip_coins(self, rf_exp=None):
        if rf_exp:
            for i in self._trigram_yaos:
                i.flip_coins(rf_exp)
        else:
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


    def __init__(self, method, rf_exp=None):
        self._c1 = Coin(method, rf_exp)
        self._c2 = Coin(method, rf_exp)
        self._c3 = Coin(method, rf_exp)

        self._yao = []
        self._yao.append(self._c1)
        self._yao.append(self._c2)
        self._yao.append(self._c3)

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

    def flip_coins(self, rf_exp=None):
        if rf_exp:
            for i in self._yao:
                i.flip(rf_exp)
            self._calc_name()
        else:
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

    def __init__(self, method, rf_exp=None):
        self._state = None
        self._method = method
        self._rf_exp = rf_exp

        self._calc_state = lambda x: [0, "[ 0 ]"] if x == 0 else [1, "[ 1 ]"]
        self.count = 0
        self._dot = "."

    def flip(self, rf_exp=None):
        _ = self._gen_state(rf_exp)
        print(self._dot*self.count)
        self.count += 1
        self._set_state(self._calc_state(_))

    def _gen_state(self, rf_exp):
        freq = []
        _ = self._method
        if int(self._method) == 2:
            input("Press and hold 'return/enter' while thinking of your question to proceed.")
            counter = 0
            while counter < 2:
                #Process all received data from device
                rf_exp.ProcessReceivedString(True)
                _ = self._sweep_rf(rf_exp)
                print(_)
                freq.append(_)
                counter += 1
                time.sleep(0.3)
            state = self._diff_freq(freq[0], freq[1])
        else:
            input("Press and hold 'return/enter' while thinking of your question to proceed.")
            state = secrets.randbelow(2)

        return state

    def _diff_freq(self, freq1, freq2):
        freq3 = abs(int(freq1) - int(freq2))

        state = 0 if int(freq3) % 2 == 0 else 1

        print("FREQ3: {} | STATE: {}".format(freq3, state))

        return state

    def _sweep_rf(self, objAnalyzer):
        nIndex = objAnalyzer.SweepData.Count - 1
        objSweepTemp = objAnalyzer.SweepData.GetData(nIndex)
        nStep = objSweepTemp.GetPeakDataPoint()
        freq = objSweepTemp.GetFrequencyMHZ(nStep)

        return freq

    def _set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state


class Parser:

    def __init__(self):
        self._parsed = et.parse(source="interpretation/hexagrams.xml")
        self.root = self._parsed.getroot()

    def _parse(self):
        pass


class HexModel:

    def __init__(self):
        self._name = None
        self._number = None
        self._description = None
        self._judgement = None
        self._image = None
        self._lines = None

    class Abstraction:

        def __init__(self, text, interpretation):
            self.text = text
            self.interpretation = interpretation

    class Judgement(Abstraction):

        def __init__(self, text, interpretation):
            super().__init__(text, interpretation)

    class Image(Abstraction):

        def __init__(self, text, interpretation):
            super().__init__(text, interpretation)

    class Lines:

        def __init__(self, lines: list):
            self.lines = lines


    class Line(Abstraction):

        def __init__(self, text, interpretation):
            super().__init__(text, interpretation)


class MethodManager:

    def __init__(self):
        self.method = None
        self._select_method()

    def _select_method(self):
        print("1. /dev/random")
        print("2. RF Explorer")
        inp = input("Select Method: ")
        _ = str(inp).isnumeric()
        if _:
            inp = int(inp)
            if (inp < 3 and inp > 0):
                self.method = inp
                print("Method: {} selected".format(self.method))
        else:
            raise KeyboardInterrupt


class Doorway:

    def __init__(self):
        try:
            self.methodManager = MethodManager()
            self.hex = Hexagram(self.methodManager.method)
            print("Think of an open ended question.")
            print("If the answer can be answered with a 'yes,' or a 'no' you are throwing wrong.")
            self.question = input("If you like, type your question out here, otherwise hold the question in your mind then press and hold enter: ")
            print("..........................")
        except:
            print("Please input a valid option.")
            self.__init__()

    def cast(self):
        self.hex.flip_yaos()
        print("Q:" + self.question)
        self.hex.print()


if __name__ == "__main__":
    _ = Doorway()
    _.cast()
