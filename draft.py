import stat_parser


def print_tree(tree):
    """
        Recursively builds a string with a fancy representation of the syntax
        tree. Example for 'The dog is nice.':

        s
          |__np
          |    |__dt: the
          |    |__nn: dog
          |__vp
          |    |__vbz: is
          |    |__adjp
          |    |    |__jj: nice
          |__.: .

    """

    if len(tree) == 2 and type(tree[1]) == type(''):
        return "{0}: {1}".format(tree[0], tree[1])
    string = tree[0] + "\n"
    for sub_element in tree[1:]:
        string += "  |__"
        for line in print_tree(sub_element).split('\n'):
            if tree[0] in ["NP", "DPP"]:
                string += line + "\n  |"
            else:
                string += line + "\n   "
        string = string[:-3]
    if string[-1] == '\n':
        return string[:-1]
    return string

DEBUG = True

parser = stat_parser.Parser()
parser.pcfg = stat_parser.pcfg.PCFG()
parser.pcfg.load_model("test.model")
sentence = "the cousin talks to her sister about her aunt"
tree = parser.parse(sentence)

print(print_tree(tree))

if __name__ == '__main__' and not DEBUG:
    parser = Parser()
    print("Enter a sentence to parse. Leave blank to quit.")
    while True:
        sentence = input("? ")
        if len(sentence) == 0:
            break
        parsing_tree = parser.parse(sentence)
        print_tree(parsing_tree)
