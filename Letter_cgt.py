class Letter:
    def __init__(self, _symbol, _exponent=0):
        # this is the construction of the class of Letter which is
        # essentially the cornerstone of all of this as homomorphisms,
        # Words, and Groups will all be made up in some way of Letters.
        # _symbol explains what the character will be and exponent will
        # denote if it is the inverse or not (here represented with
        # capitalization).
        # If I'm referencing the class Letter the L will be capitalized.

        # sets the Letter's
        if len(_symbol) != 1:
            raise Exception("I only take letters with length one")
        self._symbol = _symbol.lower()

        # decides the Letter's exponent or case
        if _symbol == _symbol.upper():
            exponent_check = -1
        else:
            exponent_check = 1
        if _exponent == 0:
            _exponent = exponent_check
        if abs(_exponent) != 1:
            raise Exception("only -1/1 for exponent")

        self._exponent = _exponent

        # these are my training wheels
        self._paranoid = True

    def get_str(self):
        # this returns the Letter as a string i.e. a or A
        if self._exponent == 1:
            self_str = self._symbol
        else:
            self_str = self._symbol.upper()
        return self_str

    def __eq__(self, other):
        # this lets me test if two Letter objects are representing
        # the same thing
        if self._paranoid:
            if not isinstance(other, Letter):
                raise Exception("comparing apples and oranges here pal")

        self_str = self.get_str()
        othr_str = other.get_str()
        return self_str.__eq__(othr_str)

    def __hash__(self):
        # this turns the Letter into a hashable datatype by returning the
        # string version
        self_str = self.get_str()
        return self_str.__hash__()

    def __str__(self):
        # this allows the letter to be called by the print function and return
        # the actual string representation rather than the Letter object
        self_str = self.get_str()
        return self_str

    def check_cancels(self, a_letter):
        # if a Letter cancels with another, they have to have the same symbol, but
        # opposite exponents. This checks that and returns true or false
        if self._paranoid:
            if not isinstance(a_letter, Letter):
                raise Exception("a letter can't cancel with "
                                "something that's not a letter")

        if self._symbol == a_letter._symbol:
            return self._exponent != a_letter._exponent
        return False

    def check_capital(self):
        # this checks if the Letter is an inverse or not and returns true or false
        return self._exponent == -1

    def return_inv_letter(self):
        # this returns a Letter's inverse without changing the Letter itself.
        inv_letter = Letter(self._symbol, self._exponent * -1)
        return inv_letter
