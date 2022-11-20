from random import choice


class EDictionary:
    def __enter__(self):
        self.words = {}
        with open("dict.txt", mode="r", encoding="utf-8") as memory_file:
            for row in memory_file:
                if row:
                    e_word, r_words, examples = row.split("/")
                    self.words.update({e_word: (r_words.split(","), examples.split(","))})
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open("dict.txt", mode="w", encoding="utf-8") as memory_file:
            for e_word, (r_words, examples) in self.words.items():
                r_words_stripped = map(str.strip, r_words)
                examples_stripped = map(str.strip, examples)
                memory_file.write(e_word+"/"+",".join(r_words_stripped)+"/"+",".join(examples_stripped)+"\n")

    def training_start(self):
        print("start training session!")
        training_list = list(self.words.items())
        while True:
            e_word, (r_words, examples) = choice(training_list)
            print(e_word)
            while True:
                received_word = input()
                if received_word == "stop":
                    print("Training stopped")
                    return
                if received_word in r_words:
                    print(f"Nice °͜°\n{choice(examples)}")
                    break
                elif received_word == "help":
                    print(f"True answer is {', '.join(r_words)}\n{choice(examples)}\nPrint again")
                    continue
                else:
                    print("It is mistake, try again")
                    continue


class Menu:
    def __init__(self, description):
        self.parent = None
        self.description = description
        self.elements = []

    def add_element(self, obj):
        self.elements.append(obj)
        obj.parent = self

    def __call__(self):
        while True:
            print(self.description)
            print("0: return to previous menu")
            for i, element in enumerate(self.elements, start=1):
                print(f"{i}: {element.description}")

            try:
                select = int(input())-1
            except ValueError:
                print("incorrect input")
                continue
            if select > len(self.elements):
                print("incorrect input")
                continue
            elif select < 0 and self.parent is not None:
                break
            self.elements[select]()


class Action:
    def __init__(self, description, function):
        self.parent = None
        self.description = description
        self.function = function

    def __call__(self):
        self.function()


if __name__ == "__main__":
    with EDictionary() as edict:
        main_menu = Menu("This is main menu")
        printing_dictionary_menu = Menu("view dictionary")
        training_action = Action("training", edict.training_start)
        printing_dictionary_menu.add_element(training_action)
        main_menu.add_element(printing_dictionary_menu)
        main_menu.add_element(training_action)
        main_menu()
