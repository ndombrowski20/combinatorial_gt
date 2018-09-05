from Word_cgt import Word
from WordTrie_cgt import WordTrie


class Cache:
    def __init__(self, key_list: list):
        # the purpose of cache is to take the yielded cosets of different
        # Words and store them in one place so as to not have to generate
        # the entire coset again. It does this by creating a dictionary of
        # Words to their Tries which store the cosets.

        self._dict = {}
        self._paranoid = True
        self._bool_dict = {}
        self._dict_list = {}

        if self._paranoid:
            for entry in key_list:
                if not isinstance(entry, Word):
                    raise Exception("all my keys are words, guy")

        for i in range(len(key_list)):
            a_word = key_list[i]
            a_word_trie = WordTrie()
            a_word_trie.add_word(a_word)
            self._dict[a_word] = a_word_trie
            self._bool_dict[a_word] = False
            self._dict_list[a_word] = [a_word]

    def create_coset(self, a_word):
        # this allows for a new coset (or Trie, as it is being stored here)
        # to be added to the Cache. it does so by checking if a Word is already
        # in the Cache. if not, then a new coset is added.
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("i only use words as keys, pal")
            for key in self._dict.keys():
                if key == a_word:
                    raise Exception("I'm not making you a coset, you already have one")

        a_word_trie = WordTrie()
        a_word_trie.add_word(a_word)
        self._dict[a_word] = a_word_trie
        self._bool_dict[a_word] = False
        self._dict_list[a_word] = [a_word]

    def add_to_coset(self, a_word, a_word_equiv):
        # this takes a Word and searches for it in the keys. If it is in the
        # keys then it will add the word equivalent to the trie that is
        # associated with it. It does this by searching the cache for the Word,
        # finding the trie, and adding the word to it.
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("i can only search for words")
            if not isinstance(a_word_equiv, Word):
                raise Exception("I'm only adding words to this Trie")
            check = False
            for key in self._dict.keys():
                if a_word == key:
                    check = True
                    break
            if not check:
                raise Exception("this word doesn't have a Trie yet")

        for key in self._dict.keys():
            if key == a_word:
                self._dict[key].add_word(a_word_equiv)
                self._dict_list[key].append(a_word_equiv)
                self._bool_dict[key] = False

    def check_complete(self, a_word):
        # this checks if a coset has been completed. It essentially forces the
        # user to mark a coset complete and if a Word's equivalent is added, the
        # complete check is put back to false to ensure that the user is consciously
        # adding an equivalent word to the Trie.
        for key in self._bool_dict.keys():
            if key == a_word:
                return self._bool_dict[key]

    def mark_coset_complete(self, a_word):
        # this is the method that allows the user to set a coset as complete
        for key in self._bool_dict.keys():
            if key == a_word:
                self._bool_dict[key] = True

    def check_key(self, a_word):
        # this can be used to check that a word is even in the cache before
        # things are called upon
        for key in self._dict.keys():
            if key == a_word:
                return True
        return False

    def get_coset_trie(self, a_word):
        # this calls forth the coset in case it ever needs to be referenced
        # or set to a variable which would be easier than typing the whole thing
        # out over and over again.
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("only words homes")
            check = False
            for key in self._dict.keys():
                if a_word == key:
                    check = True
                    break

            if not check:
                raise Exception("not in the keys, pal. add it and try again")

        return self._dict[a_word]

    def get_coset_list(self, a_word):
        # this is made to generate a list of all of the entries so that the entries
        # of the list can be yielded one at a time
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("words, bruv, words. how many times...")
        for key in self._dict_list.keys():
            if a_word == key:
                return self._dict_list[key]
