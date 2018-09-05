from Word_cgt import Word
from Letter_cgt import Letter


class Hom:
    def __init__(self, a_dict={}):
        # this is the constructor for a Homomorphism. This has been organized as a
        # dictionary in this language. It is the best data structure for telling me
        # "a" maps to "ab"
        self._dict = {}

        for key, item in a_dict:
            if not isinstance(key, Letter):
                raise Exception("not a letter, my dude")
            if not isinstance(item, Word):
                raise Exception("can't map to something that's not a word")

            self._dict[key] = item

        # training wheels are best for everyone
        self._paranoid = True

    def add_entry(self, a_letter, a_word):
        # this will add another entry to the dictionary or homomorphism that only accepts
        # a Letter going to a Word
        if self._paranoid:
            if not isinstance(a_letter, Letter):
                raise Exception("not a letter, friend. i only add letters")
            if not isinstance(a_word, Word):
                raise Exception("not a word, and i only work with words, pal")
            for key in self._dict.keys():
                if a_letter == key:
                    print("well, you're writing over another entry with " + a_letter.get_str()
                          + " but i guess that's ok, just be wary")

        self._dict.update({a_letter: a_word})

    def return_str_dict(self):
        # this will return a dictionary that is equivalent to the homomorphism but with
        # strings instead of Letter and Word objects
        str_dict = {}
        for key, items in self._dict.items():
            letter_string = key.get_str()
            word_string = items.return_word_str()
            str_dict[letter_string] = word_string
        return str_dict

    def call_entry(self, a_letter):
        # this returns the Word that corresponds to the Letter in the homomorphism.
        # If the Letter inputted is the inverse of the letter in the homomorphism, it will
        # output the inverse word. i.e. a => ab, A => BA
        if self._paranoid:
            if not isinstance(a_letter, Letter):
                raise Exception("I only can call Letters, bud")

        for key, a_word in self._dict.items():
            if a_letter == key:
                if a_letter.check_capital():
                    return a_word.return_inv_word()
                return a_word

    def check_keys(self, a_letter):
        # this checks to see if a Letter is one of the keys to the dictionary, or if
        # this homomorphism sends a certain character to a specific Word, or just itself
        if self._paranoid:
            if not isinstance(a_letter, Letter):
                raise Exception("not a letter, and i only do letters")
        for key in self._dict.keys():
            if a_letter == key:
                return True
        return False

    def return_word_application(self, a_word):
        # this takes a Word as its input and transforms it according to the rules of the
        # homomorphism. if a Letter exists in the word, but not in the homomorphism it sends
        # the letter to itself. This also returns a new word, so the original isn't changed
        hom_applied_word = Word()
        for i in range(a_word.return_word_len()):
            word_letter = a_word.return_word_letter(i)
            if self.check_keys(word_letter):
                hom_entry = self.call_entry(word_letter)
                for character in hom_entry.return_str_list():
                    letter = Letter(character)
                    hom_applied_word.add_letter(letter)
            else:
                hom_applied_word.add_letter(word_letter)

        return hom_applied_word
