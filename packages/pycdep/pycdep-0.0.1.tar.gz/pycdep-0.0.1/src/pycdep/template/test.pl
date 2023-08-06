
%operator definitions
:- op(990, fy, project).
:- op(990, fy, to).
:- op(990, xfy, belongs).
:- op(970, xfx, includes).
:- op(800, fy, from).
:- op(800, fy, include).
:- op(800, xfy, cannot).
:- op(650, fy, on).
:- op(650, xfy, depends).
:- op(990, fy, headerfile).
:- op(990, fy, cppfile).
:- op(670, yfx, via).
:- op(800, xfx, costs).
:- dynamic (includes)/2.
:- dynamic 
     recursive_cost/2.


%useful queries
%
%basic stuff:
%    . in a query, a variable name starting with a capital will be filled in by prolog
%    . \+ can be used to say "not"
%    . you can use an underscore _ to indicate that you are not interested in solutions for a given variable
%
%examples:
%find out which header files exist
%headerfile X.
%
%find out which cppfiles exist
%cppfile X.
%
%find out which files are directly included by 'a.h'
%'a.h' includes X.
%
%find out which files are included by 'a.h' (recursively)
%'a.h' depends on X.
%
%find out which header files are included by noone
%\+ is a prolog way of writing "not"
%findall(F, (headerfile F, \+(_ includes F)), R).
%
%find out if someone includes cpp files
%findall(F2, (cppfile F, F2 includes F), R).
%
%find out which files are recompiled by changing 'a.h'
%X depends on 'a.h'.
%
%find out which files directly include 'a.h'
%X includes 'a.h'.
%
%find out which header files aren't included by anyone
%(i.e. find headerfiles F, for which no path arrives in F)
%\+ is a prolog way of writing "not"
%headerfile F, \+path(_,F,_).
%
%find out which hierarchy violations are present
%violation(Project, Sourcefile, Includefile).
%
%find out which hierarchy violations are present in project 'p1'
%violation('p1', S, D).
%
%find out which hierarchy violations are present involving file 'mmi/mmi2.h'
%(so both violations caused by files included by mmi2.h, and violations caused by files including mmi2.h)
%violation(P, 'mmi/mmi2.h', D); violation(P, S, 'mmi/mmi2.h')
%
%find all violations and wrap them in a Result list
%findall( ['in project', P, 'file', S, 'should not include file', D], violation(P,S,D), Result).
%
%get a list of all projects
%projects(P).
%
%count all violations in project 'bga'
%count_violations('bga', NoOfViolations).
%
%count all violations over all projects
%count_violations(_, NoOfViolations)
%
%get a list of all files
%files(F).
%
%get a list of all header files
%findall(F, headerfile F, Result).
%
%get a list of all cpp files
%findall(F, cppfile F, Result).
%
%get a list of all header files defined in project 'bga'
%findall(F, (headerfile F, F belongs to project 'bga'), R).
%
%get a sorted set of all header files involved in a violation with project 'ocv'
%findall(F, (headerfile F, (violation('ocv', _, F); violation('ocv', F, _))), IntermediateResult), list_to_set(IntermediateResult, R2), sort(R2, Result).
%
%get a list of all violations where 'mmi/mmi2.h' is included over all projects
%findall(S, violation(_, S, 'mmi/mmi2.h'), IntermediateResult), list_to_set(IntermediateResult, R2), sort(R2, FinalResult).
%
%get a list of all violations where 'mmi/mmi2.h' is included in project 'bga'
%findall(F, violation('bga', F, 'mmi/mmi2.h'), IR), list_to_set(IR, IR2), sort(IR2, FR).
%
%how many lines of code must be reparsed if i touch 'comp/comp_ext.h' ?
%recompile_after_touching_file_cost('comp/comp_ext.h', Loc).
%
%how many of lines of code must be reparsed to fully rebuild the complete application ?
%this takes some thinking: 
%- the compiler only compiles cpp files, one by one.
%- for each cpp file, it will run the preprocessor on it
%- then compile the result
%conclusion: find all cpp files, and sum the cost of the cpp-file+all files it eventually includes
%findall(F, cppfile F, R), recompile_list_of_cppfiles_cost(R, C).
%
%how many lines of code must be reparsed after cleaning only project 'ocv' ?
%findall(F, (cppfile F, F belongs to project 'ocv'), R), recompile_list_of_cppfiles_cost(R, Cost).
%
%how many statements were counted in 'env/env_error.h'?
%'env/env_error.h' costs X.
%
%list all files with a length > 2000?
%findall(F, (F belongs to project _, F costs C, C>2000), R).
%
%make your own favorite query here

X depends on Y :-
    path(X, Y, _).

X depends on Y via P :-
    path(X, Y, P).

violation(Project, X, Y) :-
    X includes Y, 
    X belongs to project Project,
    Y belongs to project Py,
    Project cannot include from Py.

%count_violations(Project, L) L contains all violations of project Project including something which it shouldn't
count_violations(Project, L) :-
    findall( [Project,Src,Dest], violation(Project, Src, Dest), Result), 
    list_to_set(Result, Result2),
    length(Result2, L).

%projects(P) returns a list of all projects known to dependency analyzer
projects(P) :-
    findall(S, _ belongs to project S, P).

%files(F) returns a list of all files known to dependency analyzer
files(F) :-
    findall(S, S belongs to project _, F).

%a predicate to find out if there's an include path P from file A to file B
path(A,B,Path) :-
    travel(A,B,[A],Q),
    reverse(Q,Path).

travel(A,B,P,[B|P]) :-
    A includes B.
travel(A,B,Visited,Path) :-
    A includes C,
    C \== B,
    \+member(C,Visited),
    travel(C,B,[C|Visited],Path).

%the following takes a list of files, looks up the associated cost and returns the total cost over the complete list
sum_cost(List,Cost) :-
   sum_cost_helper(List, 0, Cost).
sum_cost_helper([], Acc, Acc).
sum_cost_helper([H|T], Acc, FinalResult) :-
   ( 
      H costs C1, 
      Intermediate is C1 + Acc,
      sum_cost_helper(T, Intermediate, FinalResult)
   ), !
      ;
   (
      \+(H costs C1), !,
      write('No cost found for file '), 
      write(H), 
      nl
   ).


%the following takes a single file, finds out which files depend on that file, then sums the cost over all those files
%for a cpp file:
%    * massive speed-up by assuming that cppfiles are not included by other files
%    * in that case, touching a cpp file only requires recompiling the cpp file
%for a header file:
%    * find all cpp files that eventually include this header file
%    * then compile each of those separately, i.e. sum their cost with the cost of the files they include
recompile_after_touching_file_cost(F, C) :-
    (
        cppfile F, !,
        F costs C
    )
;
    (
        findall(Y, (cppfile Y, Y depends on F), R),
        list_to_set(R, R1), %%remove duplicates (same include file can be reachable via multiple paths from a given cpp file)
        recompile_list_of_cppfiles_cost(R1, C)
    ).

file_plus_includefiles_cost(F, C) :-
    findall(Incl, F depends on Incl, IR),
    list_to_set(IR, Set), %%remove duplicates (same include file include via different paths); this also happens during real compilation: duplicate include files are filtered out by #ifdef 
    sum_cost(Set, IncludeFileCost),
    F costs FileItselfCost,
    C is FileItselfCost + IncludeFileCost.

%given a file, check which files it includes, and sum their costs
cached_file_plus_includefiles_cost(F, C) :-
    (recursive_cost(F,C), !)
    ;
    (file_plus_includefiles_cost(F,C),
    assert(recursive_cost(F,C))).

%the following takes a list of files; 
%for each file in the list, 
%  find the files  included by that file, 
%  and return the total cost over all files
%(i.e. principle of separate compilation)
recompile_list_of_cppfiles_cost(List, Cost) :-
   recompile_list_of_cppfiles_cost_helper(List, 0, Cost).
recompile_list_of_cppfiles_cost_helper([], Acc, Acc).
recompile_list_of_cppfiles_cost_helper([H|T], Acc, FinalResult) :-
     file_plus_includefiles_cost(H, IntermediateCost),
     IntermediateAcc is IntermediateCost + Acc,
     recompile_list_of_cppfiles_cost_helper(T, IntermediateAcc, FinalResult).

what_if_f1_includes_f2_extra_cost_for_rebuild_all(F1, F2, C1, C2, C) :-
    findall(F, cppfile F, R), 
    recompile_list_of_cppfiles_cost(R, C1),
%   write('cost without inclusion: '), write(C1), nl,
    assert(F1 includes F2),
    findall(G, cppfile G, L),
    recompile_list_of_cppfiles_cost(L, C2),
%   write('cost with inclusion: '), write(C2), nl,
    retract(F1 includes F2),
    C is C2 - C1.
%   write('difference: '), write(C), nl.

what_if_f1_includes_f2_cost_for_rebuild(F1, F2, C) :-
    assert(F1 includes F2),
    recompile_after_touching_file_cost(F1, C),
    retract(F1 includes F2).

%minimize set of include files
%by removing include files which are implied by another include file in the 
%list
%sometimes multiple solutions are possible, but we only look for one.
first_implied_by_list(First, List) :-
    member(El, List),
    El depends on First, !.

remove_implied_includes(List, Result) :-
    remove_redundant_helper(List, IntermediateResult),
    reverse(IntermediateResult, RevResult), 
    remove_redundant_helper(RevResult, IntermediateResult2),
    reverse(IntermediateResult2, Result).

remove_redundant_helper([], []).
remove_redundant_helper([Head | Tail], Result) :-
    first_implied_by_list(Head, Tail), !,
    remove_redundant_helper(Tail, Result).
remove_redundant_helper([Head | Tail], [Head | Result]) :-
    remove_redundant_helper(Tail, Result).

% 
minimize_includes(File,OriginalIncludes,MinimizedIncludes,ToBeRemoved) :-
    findall(I, File includes I, OriginalIncludes),
    length(OriginalIncludes, L1),
    remove_implied_includes(OriginalIncludes, MinimizedIncludes),
    length(MinimizedIncludes, L2),
    L1 \== L2,
    subtract(OriginalIncludes,MinimizedIncludes,ToBeRemoved).

%some helpers to pretty-print prolog answers
spaces(0) :- !.
spaces(N) :- write(' '), N1 is N-1, spaces(N1).

pp(S) :- pp(S, 0).
pp([H|T], I) :- !, J is I+3, pp(H,J), ppx(T, J), nl.
pp(X, I) :- spaces(I), write(X), nl.

ppx([],_).
ppx([H|T], I) :- pp(H, I), ppx(T, I).

%experimental stuff to generate html
:- use_module(library(http/html_write)).

%bulletedlist will generate nested a html bulleted list
bulletedlist(L, ul(Html)) :-
    !,
    bulletedlist_items(L, Html).

bulletedlist_items([H|T], [Head | Rest] ) :-
    is_list(H), !,
    bulletedlist(H,Head),
    bulletedlist_items(T, Rest).
bulletedlist_items([H|T], [li(H) | Rest] ) :-
    bulletedlist_items(T, Rest).
bulletedlist_items([],[]).

%bulletedlist2 - adds "because" and "includes"
bulletedlist2(L, CurrentDepth, FirstLevelSuffix, SecondLevelSuffix, ul(Html)) :-
    bulletedlist2_items(L, CurrentDepth, FirstLevelSuffix, SecondLevelSuffix, Html).
bulletedlist2_items([H|T], CurrentDepth, FirstLevelSuffix, SecondLevelSuffix, [Head | Rest] ) :-
    is_list(H), !,
    NewDepth is CurrentDepth + 1,
    bulletedlist2(H, NewDepth, FirstLevelSuffix, SecondLevelSuffix, Head),
    bulletedlist2_items(T, CurrentDepth, FirstLevelSuffix, SecondLevelSuffix, Rest).
bulletedlist2_items([H|T], CurrentDepth, FirstLevelSuffix, SecondLevelSuffix, [li(H2) | Rest] ) :-
    CurrentDepth = 1, 
    concat_atom([H, ' ', FirstLevelSuffix], H2),
    bulletedlist2_items(T, CurrentDepth, FirstLevelSuffix, SecondLevelSuffix, Rest).
bulletedlist2_items([H|T], CurrentDepth, FirstLevelSuffix, SecondLevelSuffix, [li(H) | Rest] ) :-
    CurrentDepth = 2,
    T = [], !, 
    bulletedlist2_items(T, CurrentDepth, FirstLevelSuffix, SecondLevelSuffix, Rest).
bulletedlist2_items([H|T], CurrentDepth, FirstLevelSuffix, SecondLevelSuffix, [li(H2) | Rest] ) :-
    CurrentDepth = 2,
    concat_atom([H, ' ', SecondLevelSuffix], H2),
    bulletedlist2_items(T, CurrentDepth, FirstLevelSuffix, SecondLevelSuffix, Rest).

bulletedlist2_items([],_,_,_,[]).

%define here which queries will be visible in the WEB frontend
%fow now, all queries are expected to take 2 files as input
webapp_queries(query1, 'Which *other* *header* files are recompiled if I change File 1? And WHY?').
webapp_queries(query2, 'Which *other* files are recompiled if I change File 1? And WHY?').
webapp_queries(query3, 'Which *other* files are recompiled if I change File 1?').
webapp_queries(query4, 'File1 (recursively) includes what?').
webapp_queries(query5, 'Who (eventually) includes File1?').
webapp_queries(query6, 'How does File 1 include File 2?').
webapp_queries(query7, 'EXPENSIVE: How many lines of code have to be reparsed if I touch File1 (without adding new includes)').
webapp_queries(query8, 'EXPENSIVE: Suppose File1 included File2. How many lines of code have to be parsed extra for full rebuild of MMI?').
webapp_queries(query9, 'What include files can be safely removed from File1 (warning: do not remove precompiled header files!)?').

query1(File1, _) :-
      findall([X,P], (headerfile X, X depends on File1 via P), R), 
      bulletedlist2(R, 0, because, includes, Html),
      phrase(html(Html), Tokens),
      print_html(Tokens),      
      halt.

query2(File1, _) :-
      findall([X, P], X depends on File1 via P, R), 
      bulletedlist2(R, 0, because, includes, Html),
      phrase(html(Html), Tokens),
      print_html(Tokens),      
      halt.

query3(File1, _) :-
      setof(X, X includes File1, R), 
      bulletedlist(R, Html), 
      phrase(html(Html), Tokens),
      print_html(Tokens),      
      halt.

query4(File1, _) :-
      setof(X, File1 depends on X, R), 
      bulletedlist(R, Html),
      phrase(html(Html), Tokens),
      print_html(Tokens),      
      halt.

query5(File1, _) :-
      setof(X, X depends on File1, R), 
      bulletedlist(R,Html),
      phrase(html(Html), Tokens),
      print_html(Tokens),
      halt.

query6(File1, File2) :-
      findall([File1, P], File1 depends on File2 via P, R), 
      concat_atom(['depends on ', File2, ' via'], Suffix),
      bulletedlist2(R, 0, Suffix, 'which includes', Html),
      phrase(html(Html), Tokens),
      print_html(Tokens),
      halt.

query7(File1, _) :-
      recompile_after_touching_file_cost(File1, Loc),
      concat_atom(['If you touch file ', File1, ' without adding new includes, at least '], Msg1),
      phrase(html(p([Msg1, b(Loc), ' lines of code have to be reparsed.'])), Tokens),
      print_html(Tokens),
      halt.

query8(File1, File2) :-
      what_if_f1_includes_f2_extra_cost_for_rebuild_all(File1, File2, C1, C2, Diff),
      concat_atom(['Lines of code to be parsed before adding #include "', File2, '" in ', File1], Msg1),
      concat_atom(['Lines of code to be parsed after adding #include "', File2, '" in ', File1], Msg2),
      Msg3 = 'Difference',
      Result = [ Msg1, [C1], Msg2, [C2], Msg3, [Diff] ],
      bulletedlist(Result, Html),
      phrase(html(Html), Tokens),
      print_html(Tokens),
      halt.

query9(File1, _) :-
      minimize_includes(File1, Original, Minimal, ToBeRemoved),
      Result = [ 'Current includes: ', Original, 'Minimal includes', Minimal, 'To be removed: ', ToBeRemoved ],
      bulletedlist(Result, Html),
      phrase(html(Html), Tokens),
      print_html(Tokens),
      halt.
   
query10(_) :-
      findall(C, ((cppfile SRC; headerfile SRC), 
                  setof(IncludeFile, SRC depends on IncludeFile, SortedResult),  %%find all recursive dependencies, sort and remove duplicates
                  setof(IncludeFile1, SRC includes IncludeFile1, SortedResult1), %%find all directly included files, sort and remove duplicates
                  sum_cost(SortedResult, C),                                     %%sum their costs
                  SRC costs OwnCost,                                             %%find the cost of the cpp file itself
                  TotalCost is C + OwnCost,                                      %%total cost = own cost + include file costs
                  write(SRC), write(' directly includes '), write(SortedResult1), 
                  write(' which recursively causes a total of '), write(TotalCost), write(' statements to be parsed.'), nl), _),
     %% and now for the expensive part of this query
      findall(_, (cppfile CPP2,
                   setof(H2, (CPP2 depends on H2), SortedResult2),
                   write(CPP2), 
                   write(' eventually includes header files '), 
                   write(SortedResult2), 
                   write('.'), 
                   nl), _),
      halt.

write_includes(X,Y) :-
    write(' '), 
    write('"'),
    write(X), 
    write('"'),
    write(' -> '), 
    write('"'),
    write(Y), 
    write('"'),
    write(' [color="black"]; \n'). 

write_arcs([]).
write_arcs([H|T]) :-
    write_arc(H),
    write_arcs(T).

write_arc(A) :-
    A = [X, Y],
    write_includes(X,Y).    

to_graphviz(ListOfArcs) :-
    write('digraph Dependencies {\n'),
    write(' concentrate=true;\n'), 
    write_arcs(ListOfArcs),
    write('}').

to_graphviz(Filename, ListOfArcs) :-
    telling(Old),
    tell(Filename),
    to_graphviz(ListOfArcs),
    told,
    tell(Old),
    halt.

% facts extracted from MMI
% file types
headerfile 'pycdep/sandbox/a.h'.
headerfile 'sandbox/lib/d.h'.
cppfile 'pycdep/sandbox/a.cpp'.
headerfile 'sandbox/lib/c.h'.
headerfile 'sandbox/lib/b.h'.
headerfile 'sandbox/lib/orphan.h'.


% projects
project 'pycdep/sandbox'.
project 'sandbox/lib'.


% project relations
'pycdep/sandbox/a.h' belongs to project 'pycdep/sandbox'.
'sandbox/lib/d.h' belongs to project 'sandbox/lib'.
'pycdep/sandbox/a.cpp' belongs to project 'pycdep/sandbox'.
'sandbox/lib/c.h' belongs to project 'sandbox/lib'.
'sandbox/lib/b.h' belongs to project 'sandbox/lib'.
'sandbox/lib/orphan.h' belongs to project 'sandbox/lib'.


% include relations
'sandbox/lib/c.h' includes 'sandbox/lib/d.h'.
'pycdep/sandbox/a.cpp' includes 'pycdep/sandbox/a.h'.
'sandbox/lib/c.h' includes 'pycdep/sandbox/a.h'.
'sandbox/lib/d.h' includes 'sandbox/lib/c.h'.
'pycdep/sandbox/a.cpp' includes 'sandbox/lib/b.h'.
'pycdep/sandbox/a.cpp' includes 'sandbox/lib/c.h'.


% hierarchy definition
'sandbox/lib' cannot include from 'pycdep/sandbox'.

% lines of code cost
'pycdep/sandbox/a.h' costs 0.
'sandbox/lib/d.h' costs 0.
'pycdep/sandbox/a.cpp' costs 0.
'sandbox/lib/c.h' costs 0.
'sandbox/lib/b.h' costs 0.
'sandbox/lib/orphan.h' costs 0.


:- use_module(library(plunit)).
:- begin_tests(intuitivequeries).

ans1(['project','pycdep/sandbox','has header file','pycdep/sandbox/a.h','\n']).
ans2(['file','pycdep/sandbox/a.cpp','includes header file','pycdep/sandbox/a.h','via path','pycdep/sandbox/a.cpp','pycdep/sandbox/a.h','\n',
      'file','pycdep/sandbox/a.cpp','includes header file','pycdep/sandbox/a.h','via path','pycdep/sandbox/a.cpp','sandbox/lib/c.h','pycdep/sandbox/a.h','\n',
      'file','pycdep/sandbox/a.cpp','includes header file','sandbox/lib/d.h','via path','pycdep/sandbox/a.cpp','sandbox/lib/c.h','sandbox/lib/d.h','\n',
      'file','pycdep/sandbox/a.cpp','includes header file','sandbox/lib/c.h','via path','pycdep/sandbox/a.cpp','sandbox/lib/c.h','\n',
      'file','pycdep/sandbox/a.cpp','includes header file','sandbox/lib/b.h','via path','pycdep/sandbox/a.cpp','sandbox/lib/b.h','\n']).
ans3(['file','pycdep/sandbox/a.cpp','includes file','pycdep/sandbox/a.h','via path','pycdep/sandbox/a.cpp','pycdep/sandbox/a.h','\n',
      'file','pycdep/sandbox/a.cpp','includes file','sandbox/lib/b.h','via path','pycdep/sandbox/a.cpp','sandbox/lib/b.h','\n',
      'file','pycdep/sandbox/a.cpp','includes file','sandbox/lib/c.h','via path','pycdep/sandbox/a.cpp','sandbox/lib/c.h','\n',
      'file','pycdep/sandbox/a.cpp','includes file','sandbox/lib/d.h','via path','pycdep/sandbox/a.cpp','sandbox/lib/c.h','sandbox/lib/d.h','\n',
      'file','pycdep/sandbox/a.cpp','includes file','pycdep/sandbox/a.h','via path','pycdep/sandbox/a.cpp','sandbox/lib/c.h','pycdep/sandbox/a.h','\n',
      'file','pycdep/sandbox/a.cpp','includes file','sandbox/lib/c.h','via path','pycdep/sandbox/a.cpp','sandbox/lib/c.h','sandbox/lib/d.h','sandbox/lib/c.h','\n']).
ans4(['file','pycdep/sandbox/a.cpp','includes file','sandbox/lib/d.h','via path','pycdep/sandbox/a.cpp','sandbox/lib/c.h','sandbox/lib/d.h','\n']).
ans5(['pycdep/sandbox','sandbox/lib']).
ans6(['in project','sandbox/lib','file','sandbox/lib/c.h','should not include file','pycdep/sandbox/a.h','\n']).
ans7(['file','sandbox/lib/orphan.h','is included by no-one','\n']).

test(strip_star_atom) :-
    strip_star_atom(['\'Test\''], 'Test').

test(tokenise1) :-
    tokenise(['this is a', 'simple case'], [this, is, a, simple, case]).
test(tokenise2) :-
    tokenise(['thIs IS a \'NOT SO SIMPLE\' case ???'], [this, is, a, '\'NOT SO SIMPLE\'', case]).

test(q1) :-
    find_and_reply([hi], [], ['Hi there. Please formulate your query.']), !.
test(q1_synonym) :-
    find_and_reply([hello], [], ['Hi there. Please formulate your query.']), !.

% test a subset of all possible queries related to asking header files in a project
test(q3_1) :-
    find_and_reply([headerfiles, in, '\'pycdep/sandbox\''], [], X),
    ans1(A), A=X,
    !.
test(q3_2) :-
    find_and_reply([headerfiles, in, project, '\'pycdep/sandbox\''], [], X), 
    ans1(A), A=X,
    !.
test(q3_3) :-
    find_and_reply([headers, in, '\'pycdep/sandbox\''], [], X), 
    ans1(A), A=X,
    !.
test(q3_4) :-
    find_and_reply([header, files, in, '\'pycdep/sandbox\''], [], X), 
    ans1(A), A=X,
    !.
test(q3_5) :-
    find_and_reply([show, header, files, in, '\'pycdep/sandbox\''], [], X), 
    ans1(A), A=X,
    !.
test(q3_6) :-
    find_and_reply([show, us, the, header, files, in, '\'pycdep/sandbox\''], [], _), 
    ans1(A), A=X,
    !.
test(q3_7) :-
    find_and_reply([show, the, header, files, in, '\'pycdep/sandbox\''], [], _), 
    ans1(A), A=X,
    !.
test(q3_8) :-
    find_and_reply([which, are, the, header, files, in, '\'pycdep/sandbox\''], [], X), 
    ans1(A), A=X,
    !.
test(q3_9) :-
    find_and_reply([what, are, the, headers, in, project, '\'pycdep/sandbox\''], [], X), 
    ans1(A), A=X,
    !.
test(q3_10) :-
    find_and_reply([what, are, the, headers, located, inside, project, '\'pycdep/sandbox\''], [], X), 
    ans1(A), A=X,
    !.
test(q3_11) :-
    find_and_reply([what, are, the, headerfiles, located, inside, '\'pycdep/sandbox\''], [], X), 
    ans1(A), A=X,
    !.
test(q3_12) :-
    find_and_reply([show, to, me, the, headerfiles, found, in, '\'pycdep/sandbox\''], [], X), 
    ans1(A), A=X,
    !.
test(q3_13) :-
    find_and_reply([show, which, headerfiles, are, included, by, '\'pycdep/sandbox/a.cpp\''], [], X),
    ans2(A), A=X,
    !.
test(q3_14) :-
    find_and_reply([which, cppfiles, are, included, by, file, '\'pycdep/sandbox/a.cpp\''], [], X),
    X = [[]],
    !.
test(q3_15) :-
    find_and_reply([which, files, does, '\'pycdep/sandbox/a.cpp\'', include],[],X), 
    ans3(A), A=X,
    !.
test(q3_16) :-
    find_and_reply([which, files, are, included, by, file, '\'pycdep/sandbox/a.cpp\''],[],X), 
    ans3(A), A=X,
    !.
test(q3_17) :-
    find_and_reply([how, does, '\'pycdep/sandbox/a.cpp\'', include, file, '\'sandbox/lib/d.h\''],[],X), 
    ans4(A), A=X,
    !.
test(q3_18) :-
    find_and_reply([how, is, file, '\'sandbox/lib/d.h\'', included, by, file, '\'pycdep/sandbox/a.cpp\''],[],X),
    ans4(A), A=X,
    !.

test(q4_1):-
    find_and_reply([projects],[],X),
    ans5(A), A=X,
    !.

test(q5_1):-
    find_and_reply([violations, in, '\'sandbox/lib\''], [], X),
    ans6(A), A=X,
    !.

test(q6_1):-
    find_and_reply([orphaned, headerfiles], [], X),
    ans7(A), A=X,
    !.
test(q6_2):-
    find_and_reply([headerfiles, are, never, included], [], X),
    ans7(A), A=X,
    !.
test(q6_3):-
    find_and_reply([which, headerfiles, are, never, included], [], X),
    ans7(A), A=X,
    !.
 test(q6_3):-
    find_and_reply([which, headerfiles, are, included, by, noone], [], X),
    ans7(A), A=X,
    !.


:- end_tests(intuitivequeries).
