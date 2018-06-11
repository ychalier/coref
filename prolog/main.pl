/*---------------------------------------------------------------*/
/* Telecom Paristech - J-L. Dessalles 2018                       */
/* Symbolic Natural Language Processing            					     */
/*            http://teaching.dessalles.fr/SNLP                  */
/*---------------------------------------------------------------*/



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Main file of procedural semantics           %
% - loads other modules                       %
% - runs parsing                              %
% - operate semantic linking                  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



:- consult('util.pl').		% loading utility predicates
								% these predicates include 'get_line', 'att' and 'print_tree'

:- consult('grammar.pl').	% loading grammar and lexicon

:- consult('world.pl').		% loading world knowledge



% Main goal - starts the DCG parser
go :-		go(s, 'Sentence').	% no argument, sentence by default
go(Cat)	 :- go(Cat, 'Phrase').
go(Cat, Msg) :-		% analyse category 'Cat' phrase (eg. s, dp, np)
	nl, write(Msg), write(' > '),
	get_line(Phrase),
	Phrase \== [''],
	!,
	dcg_parse(Cat, Phrase).	% start DCG parser
go(_, _).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% parsing                                     %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
dcg_parse(Cat, L) :-		% Cat is the phrase type to be recognized (default: s)

	%%%%%%%%%%%%%%% running DCG parser  %%%%%%%%%%%%%%
	Phrase =.. [Cat, FS, Pred, Tree, L, []],	% adding arguments to Phrase
	Phrase,		% executing DCG, for instance 	s(FS,Pred,Tree,L,[]),
	nl, write('Syntactically correct'),nl,

	parse_reference(Tree),

	%%%%%%%%%%%%%%% Printing results	%%%%%%%%%%%%%%
	write(FS), nl,
	print_tree(Tree),	 % comment if tree display is annoying
	execute(Pred),	%%%%%%% uncomment to trigger top execution
	writeln(Pred),
	write('this sentence makes sense'),nl,
	get_single_char(	C), member(C, [27]), !, nl,  % type 'Esc' to skip alternatives
	go.
dcg_parse(_) :-
	go.

parse_reference(Tree) :-
	Tree =.. [Terminal],
	!,
	write(Terminal).
parse_reference(Tree) :-
	Tree =.. [Head|SubTree],
	write(Head), write(" "),
	parse_reference_node(SubTree).

parse_reference_node([]).
parse_reference_node([Node]) :-
	!,
	parse_reference(Node).
parse_reference_node([H|Node]) :-
	parse_reference(H),
	parse_reference_node(Node).




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% semantic linking                            %
% ----------------                            %
% two connected phrases must share a variable %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% link(_, A, B, A) :- !, writeln(B).	% comment this clause to unveil the next clause

% semantic linking
link(NroArg, Pred1, Pred2, Pred1) :-
	write('linking '), write(Pred1), write(' with '), writeln(Pred2),
	Pred1 =.. [_ | Args1],		% converts predicate into list to extracts arguments.  p(a,b,c) =.. [p,a,b,c]
	nth1(NroArg, Args1, A),		% selects the nth argument
	Pred2 =.. P_Arg2,			% converts predicate into list
	select_arg(P_Arg2, A),	% unifies A with an argument in Pred2
	execute(Pred2).


select_arg([P], P) :- !.			% no arguments, this is a constant (e.g. proper noun)
select_arg([_|ArgL], A)	:-
	member(A, ArgL).				% only first argument considered


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 'execute(P)' tries to run predicate P
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

execute(A) :- atom(A), !.	% constants are not executed (e.g. proper noun)
execute(P) :-
	% write('executing '), writeln(P),
	P =.. [Pred | Args],	% separating predicate from arguments
	length(Args, Arity),	% Arity = number of arguments
	dynamic(Pred/Arity),	% declare the predicate as dynamic (useful in SWI-Prolog)
	P,	%%%%%%%%%%  Execution
	write(' ...> '), writeln(P),	% P may have changed after execution
	true.
