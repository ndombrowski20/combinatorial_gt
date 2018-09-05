from WordTrie_cgt import WordTrie
from Word_cgt import Word
from Letter_cgt import Letter
import time, os


class Group:
    def __init__(self, generator_list, relator_list, upper_limit):

        construction_start = time.time()

        # here is the construction of the class Group. Each Group must have
        # a list of generators and a list of relators. Unlike the other classes
        # I didn't design methods to add generators or relators after the initial
        # construction of the class. As the name specifies, this version of Group
        # uses iterable functions (generators) to yield a value. This frees up
        # space as an entire list need not be created if the first values suffices.
        # The generators must all be Letters and the relators Words.
        self._generator_list = []
        self._relator_list = []
        self._relator_len_list = []
        self._relator_len_max = 0
        self._relator_len_min = 0

        # this feels like putting training wheels on a 747 but maybe that's what
        # 747s need. after all, crashing a 747 is worse than crashing a bike
        self._paranoid = True

        for entry in generator_list:
            if not isinstance(entry, Letter):
                raise Exception("not a letter")
            self._generator_list.append(entry)
            if entry.return_inv_letter() not in self._generator_list:
                self._generator_list.append(entry.return_inv_letter())

        for entry in relator_list:
            if not isinstance(entry, Word):
                raise Exception("not a word")
            for i in range(entry.return_word_len()):
                if entry.return_word_letter(i) not in self._generator_list:
                    raise Exception("i'm not working with relators that "
                                    "don't send to my generators, sorry pal")
            self._relator_list.append(entry)
            self._relator_len_list.append(entry.return_word_len())

        for entry in self._relator_list:
            if entry.return_inv_word() not in self._relator_list:
                self._relator_list.append(entry.return_inv_word())
            if entry.return_reverse() not in self._relator_list:
                self._relator_list.append(entry.return_reverse())

        # Instead of doing cache stuff here, I'm going to create a trie here that
        # will be the normal closure of the relators.
        self._upper_limit = upper_limit
        self._ncor = WordTrie()
        identity = Word([])
        for entry in self.yield_coset_new(identity, self._upper_limit):
            self._ncor.add_word(entry)

        # print("construction time: % s seconds \n" % (round(time.time() - construction_start, 3)))
        # print(process.memory_info().rss / 10 ** 6)

    def yield_coset_new(self, a_word, max_length):
        # this function creates a generator that will spit out the next item
        # which is equivalent to the inputted word. It accomplishes this by
        # inserting the relators in every possible position in the Word, and
        # yields that word. Once it goes through all positions and relators,
        # it goes through the previously yielded Words and runs on them.
        # it stores them in a list local to the function. It was the only way
        # to prevent duplicates from coming up
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("I'm gonna lose it. words only")
            if not isinstance(max_length, int):
                raise Exception("we're working with math and you can't tell "
                                "me an integer to work with?")

        def _insert_relators(a_str, a_rule):
            # as the variable names suggest, this only takes strings as inputs.
            # Because this requires cutting up and gluing together objects, it's
            # easier to work with mutable objects than the Words or Letters
            for i in range(len(a_str)):
                if i == 0:
                    new_str = a_rule + a_str
                    yield new_str
                else:
                    head_a_str = a_str[:i]
                    tail_a_str = a_str[i:]
                    new_str = head_a_str + a_rule + tail_a_str
                    yield new_str
            new_str = a_str + a_rule
            yield new_str

        def _iterate_with_words(product_trie, word_rule_list, list_to_expand,
                                fresh_list, max_length_here):
            # As you can tell by how it is called below, this will be called until.
            # the list to expand is empty. What this means is that this process will
            # iterate until nothing is added for a full cycle through everything in the
            # fresh list. I got rid of the coset list because nothing was being done
            # with that information. This will take more memory than if I wasn't storing
            # them at all but we still need to protect against duplicates. The trie also
            # makes searching for things in it faster.
            fresh_list.clear()
            for a_fresh_word in list_to_expand:
                for a_rule in word_rule_list:
                    if not a_fresh_word.return_word_len() + a_rule.return_word_len() > max_length_here:
                        a_str = a_fresh_word.return_word_str()
                        a_rule_str = a_rule.return_word_str()
                        for new_string in _insert_relators(a_str, a_rule_str):
                            new_word = Word([])
                            new_word.add_str(new_string)
                            if not product_trie.search_trie(new_word):
                                product_trie.add_word(new_word)
                                fresh_list.append(new_word)
                                yield new_word
            list_to_expand.clear()
            list_to_expand.extend(fresh_list)

        # this takes the coset of the word and adds itself as well as the
        # list for expansion and expands it. then whenever the expansion
        # list has entries to expand, the program will run and the iterable
        # will continue to run

        coset_trie = WordTrie()
        coset_trie.add_word(a_word)
        expand_me = [a_word]
        yield a_word

        while expand_me:
            newly_added = []
            coset_producer = _iterate_with_words(coset_trie, self._relator_list,
                                                 expand_me, newly_added, max_length)
            for member in coset_producer:
                yield member

    def yield_coset_of_len(self, a_word, the_len):
        # this calls the yield coset method but only outputs them if the length is equal to
        # the length specified. so if I wanted only the members with length 3 it will output
        # only them
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("not a word, homes")
            if the_len > self._upper_limit:
                raise Exception("sorry i don't yield words with lengths greater than"
                                "my upper limit")

        total_coset = self.yield_coset_new(a_word, the_len)
        for member in total_coset:
            if member.return_word_len() == the_len:
                yield member

    def yield_non_reduced_words(self, max_len):
        # the purpose of this method is to create a iterable that will hand the
        # program the members of the set of the non reduced words on the generators
        # one at a time. This saves the space of having to generate the entire list
        # similarly to how the yield coset was aimed at not creating and saving the entire
        # list of Words

        if self._paranoid:
            if max_len > self._upper_limit:
                raise Exception("sorry i don't make words with lengths greater than"
                                "my upper limit")

        def _add_generators(letter_list, product_list, new_list):
            # this takes the generators, and the list of Words which are already non-reduced
            # members, and adds the generators to the members of that list, yielding them
            # one at a time.
            new_product_list = []
            for letter in letter_list:
                for old_word in new_list:
                    non_reduced_word = Word([])
                    non_reduced_word.add_word(old_word)
                    non_reduced_word.add_letter(letter)
                    if non_reduced_word not in product_list:
                        if non_reduced_word not in new_product_list:
                            new_product_list.append(non_reduced_word)
                            yield non_reduced_word
            product_list.extend(new_product_list)
            new_list.clear()
            new_list.extend(new_product_list)

        # this then takes an empty list and runs the _add_generators. So the first iteration
        # will return the generators, and the next will return their combinations, and so on

        identity = Word([])
        non_reduced_word_list = [identity]
        fresh_list = [identity]
        for i in range(max_len):
            nrw_iterable = _add_generators(self._generator_list, non_reduced_word_list, fresh_list)
            for j in nrw_iterable:
                yield j

    def test_equals(self, word1, word2, num):
        # this takes two Words and tests if they are equals. it does so by combining a Word
        # (word1 in this case) with the second Word's inverse. The logic of this being that
        # if A = B then A*B^-1 = I where I is the identity. However, some words require more
        # than just that, so we create a iterator for the coset of this new word and test each
        # entry against a Word yielded from the normal closure of the relators. We obtain this
        # normal closure of the relators by creating a coset for the identity.
        # also i set num like that for fun, and it'll help with figuring out how long the words
        # have to be to get them to properly reduce

        if self._paranoid:
            if not isinstance(word1, Word):
                raise Exception("only words; the first one is not one")
            if not isinstance(word2, Word):
                raise Exception("still only working with words")
            if not isinstance(num, int):
                raise Exception("see earlier comment about not knowing integers")
            if num > self._upper_limit:
                raise Exception("sorry i don't search for words with lengths greater than"
                                "my upper limit")

        word1_word2inv = Word([])
        word1_word2inv.add_word(word1)
        word1_word2inv.add_word(word2.return_inv_word())
        # print(word1.return_word_str() + " == " + word2.return_word_str() + "?")

        coset_w1w2inv = self.yield_coset_new(word1_word2inv, num)

        for w1w2inv_equiv in coset_w1w2inv:
            # ncor is normal closure of the relators, with the length of the equivalent to w1w2inv
            # being tested against the ncor being the maximum length
            if self._ncor.search_trie(w1w2inv_equiv):
                # print('equal')
                return True
        # print("not equal")
        return False

    def yield_elems_of_quotient(self, len_of_non_reduced, num_of_test_equals):
        # this method yields from the group each element of the quotient. it does so
        # by creating an iterable which yields the next member of the set of non reduced
        # Words on the Free group and tests if they are equal to members of the elements
        # of the quotient. if they aren't they then are yielded forward.
        if self._paranoid:
            if len_of_non_reduced > self._upper_limit:
                raise Exception("sorry no words with lengths greater than my upper limit")
            if num_of_test_equals > self._upper_limit:
                raise Exception("sorry no words with lengths greater than my upper limit")

        total = 0
        for t in range(len_of_non_reduced + 1):
            total = total + 4**t

        # overall_start_time = time.time()
        identity = Word([])
        elem_of_quotient = [identity]

        freegroup_nonreduced = self.yield_non_reduced_words(len_of_non_reduced)
        i = 0
        for a_word in freegroup_nonreduced:
            # print("I'm " + a_word.return_word_str())
            admitted = True
            # start_time = time.time()

            for existing_elem in elem_of_quotient:
                # print("I'm being tested against " + existing_elem.return_word_str())
                if self.test_equals(a_word, existing_elem, num_of_test_equals):
                    # print("didn't make it \n")
                    admitted = False
                    break

            # print("this took %s seconds \n" % (round(time.time() - start_time, 3)))
            i = i+1
            # print(str(i) + " of " + str(total - 1) + " completed")

            if admitted:
                # print("made it \n")
                elem_of_quotient.append(a_word)
                # print("memory used so far (in MB): ")
                # print(process.memory_info().rss / 10 ** 6)
                yield a_word

        # print("Overall time: %s seconds" % (round(time.time() - overall_start_time, 3)))
        # print("There are " + str(len(elem_of_quotient)) + " entries")
        # print("memory use:")
        # print(process.memory_info().rss / 10 ** 6)

    def list_generators(self):
        # this returns all of the generators in a list. This is done so that when the
        # Letters need to be added in graph form, it doesn't assume which letters to append.
        a_list = []
        for entry in self._generator_list:
            a_list.append(entry)
        return a_list

    def list_non_inv_generators(self):
        a_list = []
        for entry in self._generator_list:
            if not entry.check_capital():
                a_list.append(entry)

        return a_list

    def list_relator_strings(self):
        relator_list = []
        for entry in self._relator_list:
            relator_list.append(entry.return_word_str())
        return relator_list

    def list_generator_strings(self):
        generator_list = []
        for entry in self.list_non_inv_generators():
            generator_list.append(entry.get_str())
        return generator_list
