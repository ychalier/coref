
grammar = [
    ('s', ['n', 'vp']),
    ('n', 'Tom'),
    ('v', 'walks'),
    ('vp', ['v', 'jj']),
    ('jj', 'fast')
]
"""
sentence = "Tom walks fast".split(" ")
non_terminals = [rule[0] for rule in grammar]
#TODO: remove duplicates
n = len(sentence)
r = len(non_terminals)
P = [] # couples of words,
for i in range(n):
    P.append([])
    for j in range(n):
        P[i].append([])
        for k in range(r):
            P[i][j].append(False)
for s in range(n):
    for v in range(r):
        if sentence[s] == grammar[v][1]:
            P[0][s][v] = True
for l in range(2, n + 1):  # length of span
    for s in range(n - l + 1):  # start of span
        for p in range(l - 1):  # partition of span
            for rule in [r for r in grammar if type(r[1]) == type([])]:
                a = non_terminals.index(rule[0])
                b = non_terminals.index(rule[1][0])
                c = non_terminals.index(rule[1][1])
                # rule a --> b, c
                # b is s
                # c is s+p
                # print(l, s, p, a, b, c)
                if P[p][s][b] and P[l-p-2][s+p+1][c]:
                    print(non_terminals[a])
                    P[l-1][s][a] = True

print(P[-1][0][0])
"""

terminals = {
    "the": "DET",
    "dog": "N",
    "walks": "V",
    "fast": "JJ"
}

non_terminals = {
    "S": ["NP", "VP"]
}

sentence = "the dog walks fast".split(" ")
edges = []


index = 0
while True:
    nt = terminals[sentence[index]]
    edges.append(([nt], []))
    # check last edge
