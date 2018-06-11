/*---------------------------------------------------------------*/
/* Telecom Paristech - J-L. Dessalles 2018                       */
/* Symbolic Natural Language Processing                 */
/*            http://teaching.dessalles.fr/SNLP                   */
/*---------------------------------------------------------------*/




girl('Ann').
boy('John').
nice('Ann').
dream(_, _).
child('John').
child('Pat').
room('my_room').
daughter('Ann', 'Lisa').
sister('Ann').

animate(X) :- girl(X).
animate(X) :- boy(X).
talk(X, Y, _):- animate(X), animate(Y).
