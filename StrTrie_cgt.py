class StringTrie:

    # this was the base logic used to construct the WordTrie class.
    # It is included simply for the purpose of demonstrating the logic
    # with another data type to ensure that the method for its construction
    # is sound.

    def __init__(self):
        self.root = dict()

    def add_str(self, a_str):
        entry = self.root
        for char in a_str:
            entry = entry.setdefault(char, {})
        entry.setdefault("__")

    def print_trie(self):
        entry = self.root
        for items in entry:
            print(entry)
            entry = entry[items]

    def search_trie(self, a_str):
        entry = self.root
        for char in a_str:
            if char not in entry:
                return False
            entry = entry[char]
        if "__" in entry:
            return True
        return False

    def add_str_list(self, word_list: list):
        for entry in word_list:
            self.add_str(entry)
