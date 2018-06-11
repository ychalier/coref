def read_grammar(filename):
    grammar = {}
    symbols = []
    file = open(filename, 'r')
    for line in file.readlines():
        rule = line.replace('\n', '').split(' --> ')
        derivation = rule[1].split(', ')
        if rule[0] not in grammar.keys():
            grammar[rule[0]] = []
        for symbol in [rule[0]] + derivation:
            if symbol not in symbols:
                symbols.append(symbol)
        grammar[rule[0]].append(derivation)
    file.close()
    terminals = [s for s in symbols if s not in grammar.keys()]
    return grammar, terminals


def read_lexicon(filename):
    lexicon = {}
    file = open(filename, 'r')
    for line in file.readlines():
        line_split = line.replace('\n', '').split(' --> ')
        words_str = line_split[1].split(', ')
        words = {}
        for word in words_str:
            features = {}
            if '[' in word:
                features_list =\
                    word[word.index('[') + 1:word.index(']')].split(';')
                for f in features_list:
                    feature_split = f.split(':')
                    features[feature_split[0]] = feature_split[1]
                words[word[:word.index('[')]] = features
            else:
                words[word] = features
        lexicon[line_split[0]] = words
    file.close()
    return lexicon


class Parser:

    def __init__(self, filename_grammar, filename_lexicon):
        self.grammar, self.terminals = read_grammar(filename_grammar)
        self.lexicon = read_lexicon(filename_lexicon)
        self.rules = []
        for category in self.grammar:
            for output in self.grammar[category]:
                self.rules.append((category, output))
        self.dictionnary = {}
        for category in self.lexicon.keys():
            for entry, features in self.lexicon[category].items():
                self.dictionnary[entry] = (category, features)

    def parse(self, sentence):
        print("\nParsing:\n\t", sentence, "\n")
        words = sentence.split(' ')
        tree = self.parse_aux(words, 's', 0, len(words) - 1)[1]
        tree.draw()
        print("")
        return tree

    def parse_aux(self, sentence, target, start, end, verbose=False):
        """
            tags: list of tags representing the sentence to parse
            target: the targetted grammatical category
            start: start position of parsing
            end: end position of parsing (None if unknown)
        """

        if verbose:
            print("Parsing target {0} at position {1}".format(target, start))

        if start >= len(sentence):
            return -1, None

        if target in self.terminals:
            category = self.dictionnary[sentence[start]][0]
            if target == category:
                if verbose:
                    print("\tSuccessfully parsed {0}".format(target))
                return (start + 1,\
                        Node(category, [], value=sentence[start], index=start))

        for category, pattern in [r for r in self.rules if r[0] == target]:
            if verbose:
                print("Trying with rule {0} --> {1}".format(category, pattern))
            next_start = start
            childs = []
            for i, requirement in enumerate(pattern):
                next_end = None
                if i == len(pattern) - 1:
                    next_end = end
                next_start, sub_tree =\
                    self.parse_aux(sentence, requirement, next_start, next_end)
                childs.append(sub_tree)
                if next_start == -1:
                    break
            if next_start != -1 and (end is None or next_start == end + 1):
                if verbose:
                    print("\tSuccessfully parsed {0}".format(target))
                return next_start, Node(category, childs)
            elif verbose:
                print("Trying another rule for", target,\
                    "({0}, {1})".format(next_start, end))

        if verbose:
            print("Could not parse {0}".format(target))
        return -1, None

    def features_match(self, master, slave):
        features_master = self.dictionnary[master][1]
        features_slave = self.dictionnary[slave][1]
        for feature in features_master.keys():
            if feature in features_slave.keys():
                if features_master[feature] != features_slave[feature]:
                    return False
        return True

    def link(self, sentence, tree, pronoun_index):
        """
            Links a pronoun to a noun.
        """
        pronoun = sentence[pronoun_index]
        for i, word in enumerate(sentence):
            if (self.dictionnary[word][0] == 'n'
                and self.features_match(pronoun, word)
                and not tree.find(pronoun_index).c_commands(tree.find(i))):
                return i

    def solve_coreference(self, sentence):
        tree = self.parse(sentence)
        sentence = sentence.split(' ')
        references = []
        for i, word in enumerate(sentence):
            if self.dictionnary[word][0] == 'pn':
                references.append((i, self.link(sentence, tree, i)))
        annotated_sentence = sentence[:]
        for id, indexes in enumerate(references):
            for index in indexes:
                if index is not None:
                    annotated_sentence[index] += "_{0}".format(id)
        print(" ".join(annotated_sentence))
        return references


class Node:

    def __init__(self, category, childs, value=None, parent=None, index=None):
        self.category = category
        self.childs = childs
        self.value = value
        self.parent = parent
        self.index = index
        for child in self.childs:
            child.parent = self

    def __str__(self):
        string = self.category + "("
        if len(self.childs) == 0:
            string += self.value
        for i, child in enumerate(self.childs):
            string += str(child)
            if i < len(self.childs) - 1:
                string += ", "
        return string + ")"

    def draw(self, indent=''):
        if len(self.childs) > 0:
            print(indent, '|_', self.category)
            for child in self.childs:
                child.draw(indent + '  ')
        else:
            print(indent, '|_', self.category, ':', self.value)

    def dominates(self, other):
        """
            Returns True if 'self' dominates 'other'
        """
        if len(self.childs) == 0:
            return False
        for child in self.childs:
            if child == other or child.dominates(other):
                return True
        return False

    def c_commands(self, other):
        """
            Returns True if 'self' c-commands 'other'
        """
        if self.dominates(other) or other.dominates(self):
            return False
        parent = self.parent
        while parent is not None:
            if len(parent.childs) > 1 and parent.dominates(self):
                return parent.dominates(other)
            parent = parent.parent
        return False

    def find(self, index):
        """
            Returns the node of the tree corresponding to a given index.
            None if nothing is found.
        """
        if self.index == index:
            return self
        for child in self.childs:
            answer = child.find(index)
            if answer is not None:
                return answer


parser = Parser('en.gram', 'en.lexic')
# print(parser.grammar)
# print(parser.lexicon)
# print(parser.dictionnary)

parser.solve_coreference("the boy likes his sister and protects her")
parser.solve_coreference("he said that John was_coming")
parser.solve_coreference("his sister said that John was_coming")
