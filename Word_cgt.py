from Letter_cgt import Letter

class Word:
    def __init__(self, a_list=[]):
        # a Word is an object which consists of a list of Letters
        # whenever I am referring to an object which is of the class
        # Word in comments I'll capitalize the first letter. when
        # I am referencing variables, if I expect it to be a word I will
        # label it as a_word to differentiate from a_str or a_list
        # when a new word is created I will call it that or something more
        # specific to its importance. i.e. inv_word = inverse word

        for entry in a_list:
            if not isinstance(entry, Letter):
                raise Exception("I only add letters")

        self._list = a_list

        # yep, the training wheels are everywhere
        self._paranoid = True

    def return_word_str(self):
        # returns the Word's list of Letters as just a string
        word_str = ""
        for entry in self._list:
            word_str = word_str + entry.get_str()
        return word_str

    def return_str_list(self):
        # returns the Word's list of Letters as a list of strings
        word_list = []
        for entry in self._list:
            word_list.append(entry.get_str())
        return word_list

    def return_letter_list(self):
        word_list = []
        for entry in self._list:
            word_list.append(entry)
        return word_list

    def __eq__(self, other):
        # this allows two Words to be compared to see if they are the same
        # string. Ordinarily, the class stores both as separate data instances
        # so this just allows them to be tested if they represent the same data
        self_str = self.return_word_str()
        othr_str = other.return_word_str()
        return self_str.__eq__(othr_str)

    def __hash__(self):
        # this returns the word as a hashable object as instances of classes
        # are not ordinarily hashable objects
        self_str = self.return_word_str()
        return self_str.__hash__()

    def __str__(self):
        # this allows the word to be printed when the print function is called,
        # which makes testing if the results are accurate easier
        self_str = self.return_word_str()
        return self_str.__str__()

    def add_word(self, a_word):
        # this takes a Word and adds a second Word to the end of it
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("I only add words")
        self._list.extend(a_word._list)

    def add_str(self, a_str):
        # this takes a Word and converts each character into a Letter before adding
        # it to the Word's list of Letters
        if self._paranoid:
            if not isinstance(a_str, str):
                raise Exception("This isn't a string")
        for character in a_str:
            letter = Letter(character)
            self._list.append(letter)

    def add_letter(self, a_letter):
        # this takes a Word and adds a Letter to the list of Letters
        if self._paranoid:
            if not isinstance(a_letter, Letter):
                raise Exception("who are you trying to fool, not a letter")
        self._list.append(a_letter)

    def return_word_len(self):
        # this returns an integer which is the length of the Word, or number of
        # entries in the Word's list
        length_int = len(self._list)
        if self._paranoid:
            if not isinstance(length_int, int):
                raise Exception("what did you do? why is len not returning a number")
        return length_int

    def return_inv_word(self):
        # this returns an inverse Word, which would be changing all
        # cases to the inverse and reversing the list. I.e. aBAb's inverse is BabA
        inv_word = Word([])
        for a_letter in self._list:
            inv_word._list.append(a_letter.return_inv_letter())
        inv_word._list.reverse()
        return inv_word

    def return_word_letter(self, i):
        # this returns the 'i'th letter in the Word
        if self._paranoid:
            if not isinstance(i, int):
                raise Exception("how am i supposed to count when you're not giving me numbers")
        word_letter = self._list[i]
        return word_letter

    def return_reverse(self):
        # this returns a Word who's order has been reversed, but the tenses not changed
        # this becomes useful when adding Words that reduce to the empty word, but can't
        # just be run through the return_inv_word ie. aA = Aa
        reverse_word = Word([])
        reverse_word.add_word(self)
        reverse_word._list.reverse()
        return reverse_word

    def set_reduced(self):
        # this takes a Word and sets it to its reduced form, or eliminates all
        # instances of a Letter being next to its inverse by eliminating both the
        # Letter and the inverse. i.e. AbbaABa eventually eliminates to Aba
        if self.return_word_len() <= 0:
            return self
        for i in range(self.return_word_len() - 1):
            a_letter = self._list[i]
            next_letter = self._list[i + 1]
            if a_letter.check_cancels(next_letter):
                del self._list[i + 1]
                del self._list[i]
                return self.set_reduced()
        return self

    def return_word_multiplication(self, a_word):
        # this takes two Words and adds them together and then reduces the combination
        # of the two Words. it also does so without altering either Word so those pieces
        # of data still exist
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("not a word, homes")

        multiplied_word = Word()
        multiplied_word.add_word(self)
        multiplied_word.add_word(a_word)

        multiplied_word.set_reduced()
        return multiplied_word

    def check_identity(self):
        # when we move on to Groups, we don't reduce, but instead we allow Words
        # such as aA in order to construct properly the non reduced Words of the
        # Free Group. This checks if it is an instance of one of those reducible
        # Words.
        # we use a test Word as we don't want to reduce the actual Word

        test_word = Word([])
        test_word.add_word(self)
        test_word.set_reduced()
        if test_word.return_word_len() == 0:
            return True
        return False
