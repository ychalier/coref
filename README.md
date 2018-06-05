# coref
A symbolic approach to coreference resolution.

## definitions and vocab

**Coreference** occurs when two or more expressions refers to the same **referent**. Usually, one expression is in a full form (the **antecedent**) and the other one in a abbreviated form (a **proform**).

In computational linguistics, coreference resolution is a well-studied problem in discourse. To derive the correct interpretation of a text, or even to estimate the relative importance of various mentioned subjects, pronouns and other referring expressions must be connected to the right individuals. Algorithms intended to resolve coreferences commonly look first for the nearest preceding individual that is compatible with the referring expression. Algorithms for resolving coreference tend to have accuracy in the 75% range. As with many linguistic tasks, there is a tradeoff between precision and recall.

**Simple constraints**

 - gender
 - number (singular / plural / third)


**Advanced constraints: syntaxic strucutre**: the idea here is to try a simplified version of the **c-command**.

The **c-command** is a relationship between the nodes of grammatical parse trees. The definition of **c-command** is based partly on the relationship of dominance: *Node N1 dominates node N2 if N1 is above N2 in the tree and one can trace a path from N1 to N2 moving only downwards in the tree (never upwards)*.

A *c-commands* B iff:

 - A does not dominate B
 - B does not dominate A
 - The first (i.e. the lowest) branching node that dominates A also dominates B.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/C-command.png/220px-C-command.png)

Here A c-commands B, C, D, E, F, and G. M does not c-commands anybody.

**It was hypothesized that one restriction between pronouns and antecedent is that the pronoun cannot appear in a position where it _c-commands_ its antecedent.**

## work plan

Probably in Python.

First, a small script to get started that checks the closest antecedent and computes gender/number comparisons to solve coreference.

Then, a more advanced script that first generates the syntax tree of a sentence to then solve more complex coreference issues.

## possible libraries

 - [pyStatParser](https://github.com/emilmont/pyStatParser), that uses CKY algorithm
 - [spaCy](https://spacy.io)
 
