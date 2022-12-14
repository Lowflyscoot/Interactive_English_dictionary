from random import choice


class EDictionary:
    def __init__(self):
        self.stop_words = ["стоп", "выход", "stop", "exit"]

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

    def start_training(self):
        print("start training session!")
        training_list = list(self.words.items())
        while True:
            e_word, (r_words, examples) = choice(training_list)
            print(e_word)
            while True:
                received_word = input()
                if received_word in self.stop_words:
                    print("Training stopped")
                    return
                if received_word in r_words:
                    print(f"Nice °͜°\n{choice(examples)}")
                    break
                elif received_word == "помощь":
                    print(f"True answer is {', '.join(r_words)}\n{choice(examples)}\nPrint again")
                    continue
                else:
                    print("It is mistake, try again")
                    continue

    def add_words(self):
        print("adding new words in dictionary, do divide russian words and examples with ','")
        while True:
            input_tuple = []
            for num in range(0, 3):
                received_data = input()
                if num > 0:
                    received_data = received_data.split(",")
                if received_data in self.stop_words:
                    print("adding stopped")
                    return
                input_tuple.append(received_data)
            new_e_word, (new_r_words), (new_examples) = input_tuple

            if new_e_word in self.words.keys():
                for word in new_r_words:
                    if not word in self.words[new_e_word][0]:
                        self.words[new_e_word][0].append(word)
                for example in new_examples:
                    if not (example+"\n") in self.words[new_e_word][1]:
                        self.words[new_e_word][1].append(example)
            else:
                self.words.update({new_e_word: (new_r_words, new_examples)})
            print("successful add")

    def show_dictionary_eng(self):
        output = list(self.words.keys())
        output.sort()
        for word in output:
            print(f"{word: <20} -> {str(self.words[word][0])}")
        print("\nend of dictionary\n")
        return

    def show_dictionary_rus(self):
        output_dict = {}
        for e_word, (r_words, examples) in self.words.items():
            for word in r_words:
                output_dict.update({word: e_word})
        output = list(output_dict.keys())
        output.sort()
        for word in output:
            print(f"{word: <20} -> {str(output_dict[word])}")
        print("\nend of dictionary\n")
        return


class Menu:
    def __init__(self, description):
        self.stop_words = ["стоп", "выход", "stop", "exit"]
        self.parent = None
        self.description = description
        self.elements = []

    def add_element(self, obj):
        self.elements.append(obj)
        obj.parent = self

    def __call__(self):
        while True:
            print(self.description)
            if self.parent is not None:
                print("0: return to previous menu")
            for i, element in enumerate(self.elements, start=1):
                print(f"{i}: {element.description}")

            received_text = input()
            if received_text in self.stop_words: return
            try:
                select = int(received_text)-1
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
        main_menu = Menu("main menu")
        printing_dictionary_menu = Menu("view dictionary")

        training_action = Action("training", edict.start_training)
        add_action = Action("add new words to dictionary", edict.add_words)
        show_eng_action = Action("english", edict.show_dictionary_eng)
        show_rus_action = Action("russian", edict.show_dictionary_rus)

        main_menu.add_element(training_action)
        main_menu.add_element(add_action)
        main_menu.add_element(printing_dictionary_menu)

        printing_dictionary_menu.add_element(show_eng_action)
        printing_dictionary_menu.add_element(show_rus_action)

        try:
            main_menu()
        except KeyboardInterrupt:
            print("Exit")
