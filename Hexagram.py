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
# The readings rely on the Jungian concept of synchronicity. Meaning from the thrown hexagram is best derived from the
# person who threw it. This person's interpretation of the hexagram would be the most true interpretation. The outputted
# text most applicable to the question and all possible answers to that question from that person's perspective should
# be taken as the reading. This method of interpreting the thrown hexagram should offset the bias (cultural or
# otherwise) produced during the process of translating the original text, as well as offset any meaning lost during
# translation.
#
#
# TODO: Implement other methods/sources for truly random generated numbers.
# TODO: Produce more visually appealing hexagrams.
# TODO: Add interpretation for transformed hexagram.
# TODO: Only print out the transformed hexagram when necessary.
# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
import secrets
import time
import RFExplorer
from RFExplorer import RFE_Common
import xml.etree.ElementTree as et
from openai import OpenAI


class Hexagram:

    BLANK = "[                       ]"
    DASHED = "[-----------------------]"
    HEX_CHART = {'[1, 1]': 1, '[1, 4]': 33, '[1, 6]': 44, '[1, 5]': 12, '[1, 8]': 10, '[1, 7]': 13, '[1, 3]': 6, '[1, 2]': 25,
                 '[4, 1]': 26, '[4, 4]': 52, '[4, 6]': 18, '[4, 5]': 23, '[4, 8]': 41, '[4, 7]': 22, '[4, 3]': 4, '[4, 2]': 27,
                 '[6, 1]': 9, '[6, 4]': 53, '[6, 6]': 57, '[6, 5]': 20, '[6, 8]': 61, '[6, 7]': 37, '[6, 3]': 59, '[6, 2]': 42,
                 '[5, 1]': 11, '[5, 4]': 15, '[5, 6]': 46, '[5, 5]': 2, '[5, 8]': 19, '[5, 7]': 36, '[5, 3]': 7, '[5, 2]': 24,
                 '[8, 1]': 43, '[8, 4]': 31, '[8, 6]': 28, '[8, 5]': 45, '[8, 8]': 58, '[8, 7]': 49, '[8, 3]': 47, '[8, 2]': 17,
                 '[7, 1]': 14, '[7, 4]': 56, '[7, 6]': 50, '[7, 5]': 35, '[7, 8]': 20, '[7, 7]': 30, '[7, 3]': 64, '[7, 2]': 21,
                 '[3, 1]': 5, '[3, 4]': 39, '[3, 6]': 48, '[3, 5]': 8, '[3, 8]': 60, '[3, 7]': 63, '[3, 3]': 29, '[3, 2]': 3,
                 '[2, 1]': 34, '[2, 4]': 62, '[2, 6]': 32, '[2, 5]': 16, '[2, 8]': 54, '[2, 7]': 55, '[2, 3]': 40, '[2, 2]': 51}

    def __init__(self, method="1"):
        self._hexagram = []
        self._rf_exp = None
        self._rf_exp_inst = None
        self._method = method
        self._hex_model = None
        if int(self._method) == 2:
            print("init rf explorer...")
            self._rf_exp = RFExplorer.RFECommunicator()
        self.set_trigrams()

    def set_trigrams(self):
        self._lower_trigram = Trigram(self._method, self._rf_exp)
        self._upper_trigram = Trigram(self._method, self._rf_exp)

        self._hexagram.append(self._lower_trigram)
        self._hexagram.append(self._upper_trigram)

    def get_hex_num(self):
        return self._hex_model.number

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
        parser = Parser()
        hex = parser.get_hexagram(self.HEX_CHART[str([self._hexagram[0].trigram_value, self._hexagram[1].trigram_value])])
        self._hex_model = HexModel(**hex)
        print(self.DASHED)
        print(self.BLANK + " | " + self._hex_model.name + " | ")
        self._print_primary()
        print(self.BLANK + " | " + self._hex_model.name + " | ")
        print(self.DASHED)
        print("\n")
        transformed = self._print_meaning().copy()
        if len(transformed) > 0:
            print(self.DASHED)
            print(self.BLANK + " | " + self._hex_model.name + " | ")
            self._print_transformed()
            print(self.BLANK + " | " + self._hex_model.name + " | ")
            print(self.DASHED)
        return transformed.copy()

    def _print_primary(self):
        for i in self._hexagram:
            i.print_primary()

    def _print_transformed(self):
        for i in self._hexagram:
            i.print_transformed()

    def _print_meaning(self, hex_number=None):
        if hex_number:
            self._print_transformed_meaning()
        else:
            return self._print_primary_meaning().copy()

    def _print_primary_meaning(self):
        print("Hex Number: " + str(self._hex_model.number))
        print("Description: " + self._hex_model.description)
        print("Judgement: " + self._hex_model.judgement[0])
        print("J Interpretation: " + self._hex_model.judgement[1])
        print("Image: " + self._hex_model.image[0])
        print("I Interpretation: " + self._hex_model.image[1])
        return self._print_changing_lines().copy()

    def _print_transformed_meaning(self):
        print("Hex Number: " + str(self._hex_model.number))
        print("Description: " + self._hex_model.description)
        print("Judgement: " + self._hex_model.judgement[0])
        print("J Interpretation: " + self._hex_model.judgement[1])
        print("Image: " + self._hex_model.image[0])
        print("I Interpretation: " + self._hex_model.image[1])

    def _print_changing_lines(self):
        counter = 1
        transformed = []
        self._hexagram.reverse()
        for tri in self._hexagram:
            for yao in tri._trigram_yaos:
                if yao.yao_name_young_old[4] == 1:
                    print("Line {}".format(counter) + self._hex_model.lines[counter][0])
                    print("Line {} Interpretation: ".format(counter) + self._hex_model.lines[counter][1])
                    transformed.append(counter)
                counter += 1
        self._hexagram.reverse()
        return transformed.copy()

class HexModel:

    def __init__(self, name, number, desc, judge, img, lines):
        self.name = name
        self.number = number
        self._transformed_number = number
        self.description = desc
        self.judgement = judge
        self.image = img
        self.lines = lines

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

    class Line(Abstraction):

        def __init__(self, text, interpretation, state):
            super().__init__(text, interpretation)
            self._changed_state = state

    class Lines:

        def __init__(self, lines: list):
            self.lines = lines


class Trigram:

    TRIGRAM_CHART = {'[1, 1, 1]': 1, '[0, 0, 1]': 2, '[0, 1, 0]': 3, '[1, 0, 0]': 4, '[0, 0, 0]': 5, '[1, 1, 0]': 6,
                     '[1, 0, 1]': 7, '[0, 1, 1]': 8}

    def __init__(self, method, rf_exp=None):
        self._trigram_yaos = []
        self.trigram_value = None
        self.trigram_name = None

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
        self._trigram_yaos.reverse()
        for i in self._trigram_yaos:
            j = i.print_primary()
            print(j[2][2] + " | " + j[2][1])
        self._trigram_yaos.reverse()

    def print_transformed(self):
        self._trigram_yaos.reverse()
        for i in self._trigram_yaos:
            j = i.print_transformed()
            print(j[1][0] + " | " + j[1][1])
        self._trigram_yaos.reverse()

    def _calc_trigram(self):
        bits = []
        self._trigram_yaos.reverse()
        for i in self._trigram_yaos:
            bits.append(i.yao_name_young_old[3])
        self._trigram_yaos.reverse()
        self.trigram_value = self.TRIGRAM_CHART[str(bits)]

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
        self.yao_name_young_old = None
        self._yao_name_transformed = None

        self._YINYANG = lambda x: ["[0X0]", "Yin"] if x == 1 or x == 3 else ["[000]", "Yang"]

        self._YINYANG_YOUNGOLD = {0: ["{000}", "Changing Yang   ", self.SH_YANG_CHANGING, 1, 1],
                                  1: ["[0X0]", "Unchanging Yin  ", self.AT_YIN_UNCHANGE, 0, 0],
                                  2: ["[000]", "Unchanging Yang ", self.AT_YANG_UNCHANGE, 1, 0],
                                  3: ["{0X0}", "Changing Yin    ", self.SH_YIN_CHANGING, 0, 1]}

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
        self.yao_name_young_old = self._YINYANG_YOUNGOLD[_sum]
        self._yao_name_transformed = self._TRANSFORMED[_sum]
        self._sum = _sum

    def _sum_coins(self):
        _sum = 0
        # _second_sum = 0

        for i in self._yao:
            if i.get_state():
                _sum = i.get_state()[0] + _sum
                # _second_sum = i.get_state()[1] + _sum

        return _sum

    def print_primary(self):
        _ = self.yao_name_young_old
        return [self._sum, self._yao_name_yinyang, self.yao_name_young_old]

    def print_transformed(self) :
        return [self._sum, self._yao_name_transformed, self.yao_name_young_old]


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
        self._root = self._parsed.getroot()
        self._hexes = self._root.findall("hexagram")

    def get_hexagram(self, hex_num):
        for i in self._hexes:
            _ = i.get('number')
            if int(_) == int(hex_num):
                name = i.get('name')
                desc = i.find("description").text
                judge = i.find("judgement")
                image = i.find("image")
                lines = i.find("lines")

                judge_t = judge.find("text").text
                judge_i = judge.find("interpretation").text

                image_t = image.find("text").text
                image_i = image.find("interpretation").text

                l_one = lines.find("one")
                l_two = lines.find("two")
                l_three = lines.find("three")
                l_four = lines.find("four")
                l_five = lines.find("five")
                l_six = lines.find("six")

                l_one_t = l_one.find("text").text
                l_one_d = l_one.find("meaning").text
                l_two_t = l_two.find("text").text
                l_two_d = l_two.find("meaning").text
                l_three_t = l_three.find("text").text
                l_three_d = l_three.find("meaning").text
                l_four_t = l_four.find("text").text
                l_four_d = l_four.find("meaning").text
                l_five_t = l_five.find("text").text
                l_five_d = l_five.find("meaning").text
                l_six_t = l_six.find("text").text
                l_six_d = l_six.find("meaning").text

                kwargs = {"name": name, "number": hex_num, "desc": desc, "judge": [judge_t, judge_i],
                          "img": [image_t, image_i], "lines": {1: [l_one_t, l_one_d], 2: [l_two_t, l_two_d],
                                                               3: [l_three_t, l_three_d], 4: [l_four_t, l_four_d],
                                                               5: [l_five_t, l_five_d], 6: [l_six_t, l_six_d]}}

                return kwargs


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
            print("If the question can be answered with a 'yes,' or a 'no' you are throwing wrong.")
            self.question = input("Type your question out here and hold the question in your mind, then press and hold enter/return key \n" +\
                                  "If you don't have a question, clear your mind, then press and hold the enter/return key:")
            print("..........................")
        except:
            print("Please input a valid option.")
            # self.__init__()

    def cast(self):
        self.hex.flip_yaos()
        print("Q:" + self.question)
        lines = self.hex.print()
        self.ai_interpretation(lines)

    def ai_interpretation(self, lines):
        try:
            client = OpenAI()
            if len(self.question) == 0:
                string = "Please interpret the following hexagram as a general read for the current state of the querent's state of mind:\
                                 hexagram:{}".format(self.hex.get_hex_num())
            else:
                if len(lines) > 0:
                    string = "Please interpret the following question in the context of this hexagram:\
                         question:{} \
                         hexagram:{} \
                         Please also interpret within the context of lines {}".format(self.question, self.hex.get_hex_num(), lines)
                else:
                    string = "Please interpret the following question in the context of this hexagram:\
                         question:{} \
                         hexagram:{}".format(self.question, self.hex.get_hex_num())
            completion = client.chat.completions.create(
                # model="gpt-3.5-turbo",
                model="gpt-4",
                messages=[
                    # {"role": "system",
                    #  "content": "You are a fortune-teller, an oracle, and a mystic. You specialize in the i ching"},
                    # {"role": "user", "content": string}
                    {"role": "user", "content": string}
                ]
            )
            message = completion.choices[0].message.content.split("\n")

            for i in message:
                print(i)
        except:
            print("No ai")


if __name__ == "__main__":
    _ = Doorway()
    _.cast()
