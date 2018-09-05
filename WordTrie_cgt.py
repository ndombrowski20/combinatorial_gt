from Word_cgt import Word


class WordTrie:
    def __init__(self):
        # a Trie (which is like an attempt not a plant) is a data
        # structure that lets me store things in a series of dictionaries
        # that can then be searched. For my purposes, it serves as an easily
        # searchable list (although it's not really that) which will be used
        # to store cosets of different Words

        self.root = dict()
        self._paranoid = True

    def add_word(self, word):
        # seeing as the Trie doesn't allow for any Words to be saved to it in
        # its creation, all Words must be added to it after the fact. add_Word
        # allows for one Word to be added at a time, there are other methods for
        # adding lists of Words, but considering we're using iterables, it seemed
        # like a good idea to include one that just adds a single Word
        entry = self.root
        if self._paranoid:
            if not isinstance(word, Word):
                raise Exception("Not a word")
        word_list = word.return_letter_list()
        for letter in word_list:
            entry = entry.setdefault(letter, {})
        entry.setdefault("__")

    def search_trie(self, word):
        # this allows the user to search the Trie and establish whether
        # an entry exists. This has a good function either for seeing if something
        # is equal to any entry in the Trie OR if an entry already exists.
        if self._paranoid:
            if not isinstance(word, Word):
                raise Exception("I can only search for WORDS in my Trie of WORDS")
        entry = self.root
        for letter in word.return_letter_list():
            if letter not in entry:
                return False
            entry = entry[letter]
        if "__" in entry:
            return True
        return False

    def add_word_list(self, word_list: list):
        # this allows for a list of words to be added to a Trie at once
        # rather than calling add_Word half a hundred times.
        if self._paranoid:
            if not isinstance(word_list, list):
                raise Exception("this has to be a list")
            for entry in word_list:
                if not isinstance(entry, Word):
                    raise Exception("and it has to be a list of WORDS")

        for word in word_list:
            self.add_word(word)
