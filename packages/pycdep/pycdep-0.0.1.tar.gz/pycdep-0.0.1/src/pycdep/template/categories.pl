% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.
%
% Author: stefaan.himpe@gmail.com
%
% Get it from http://sourceforge.net/projects/pycdep/

:-op(995, xfx, ===>).

strip_star_atom(A,P):-
    [B]=A, 
    strip_quote_from_atom(B,P).

write_list([]) :- nl.
write_list([[H1|T1]|T]):-
    nl,
    write_list(H1),
    write_list(T1),
    write_list(T).
write_list([H|T]):-
    write(H),
    write(' '),
    write_list(T).
write_list(L) :-
    write(L), 
    write(' ').

category([pattern(P), template(T)]) :-
    P ===> T.

synonym([hello], [hi]).
synonym([hey], [hi]).
synonym([howdy], [hi]).
synonym([hullo], [hi]).
synonym([hallo], [hi]).
synonym([hoi], [hi]).
synonym([goedemorgen], [hi]).
synonym([bonjour], [hi]).
synonym([yow], [hi]).
synonym([hai], [hi]).
synonym([mogge], [hi]).
synonym([joew], [hi]).
synonym([ave], [hi]).
synonym([ciao], [hi]).
[hi] ===> ['Hi there. Please formulate your query.'].

synonym([goodbye], [bye]).
synonym([quit], [bye]).
synonym([stop], [bye]).
synonym([halt], [bye]).
synonym([end], [bye]).
synonym([done], [bye]).
synonym([finished], [bye]).
synonym([gedaan], [bye]).
synonym([klaar], [bye]).
synonym([fini], [bye]).
synonym([finito], [bye]).
synonym([salut], [bye]).
synonym([exit], [bye]).
[bye] ===> ['Bye bye. Be sure to come back one day.', think(nl), think(halt)].

%[] ===> ['Bye bye. Be sure to come back one day.', think(nl), think(halt)].

synonym([are],[is]).
synonym([you],[it]).
[how, are, you, star(_)] ===> ['I\'m doing fine thanks. How about your formulate a query?'].

[the, star(A)] ===> [srai(A)].

synonym([to], []).
synonym([us], [me]).
[to, me, star(A)] ===> [srai(A)].

synonym([list],[show]).
synonym([give],[show]).
synonym(['I', want, to, see], [show]).
[show, star(A)] ===> [srai(A)].

synonym([which],[what]).
synonym([are],[]).
[what, are, star(A)] ===> [srai(A)].

[files] ===> [think(findall(X, (headerfile X;cppfile X), R)), R].

synonym([header,files], [headerfiles]).
synonym([headers], [headerfiles]).
[headerfiles] ===> [think(findall(X, headerfile X, R)), R].

synonym([cpp,files], [cppfiles]).
synonym([code,files],[cppfiles]).
synonym([c, files], [cppfiles]).
synonym([cfiles], [cppfiles]).
synonym([codefiles],[cppfiles]).
[cppfiles] ===> [think(findall(X, cppfile X, R)), R].

synonym([from],[in]).
synonym([inside], [in]).
synonym([located], [found]).
synonym([present], [found]).
synonym([found], []).
synonym([involving], [in]).
synonym([project], []).
[cppfiles, found, in, project, star(A)] ===> [think( (strip_star_atom(A,P),
                                                      findall(['project', P, 'has cpp file', X, '\n'], 
                                                      (cppfile X, X belongs to project P), R))), 
                                              R].

[headerfiles, found, in, project, star(A)] ===> [think( (strip_star_atom(A,P),
                                                         findall(['project', P, 'has header file', X, '\n'], 
                                                         (headerfile X, X belongs to project P), R))), 
                                                 R].

[projects] ===> [think(findall(P, project P, R)), 
                 R].

[violations] ===> [think(findall(['in project', P, 'file', X, 'should not include file', Y, '\n'] , 
                                 violation(P,X,Y), R)), 
                   R].

[violations, in, project, star(A)] ===> [think( (strip_star_atom(A,P),
                                                findall(['in project',P, 'file', X, 'should not include file', Y, '\n'], 
                                                        violation(P,X,Y), R))), 
                                         R].

synonym([files],[file]).
synonym([file], []).
synonym([will],[does]).
[files, does, file, star(A), include] ===> [think((strip_star_atom(A,X),
                                                   findall(['file', X, 'includes file', Y, 'via path', P, '\n'], 
                                                   X depends on Y via P, S))), 
                                            S].

[headerfiles, does, file, star(A), include] ===> [think((strip_star_atom(A,X),
                                                         findall(['file', X, 'includes header file', Y, 'via path', P, '\n'], 
                                                         (headerfile Y, X depends on Y via P), S))), 
                                                  S].

[cppfiles, does, file, star(A), include] ===> [think((strip_star_atom(A,X),
                                                      findall(['file', X, 'includes cpp file', Y, 'via path', P, '\n'], 
                                                      ( cppfile Y, X depends on Y via P), S))), 
                                               S].
   
[files, are, included, by, file, star(A)] ===> [srai([files, does, file, A, include])].

[headerfiles, are, never, included] ===> [srai([orphaned, headerfiles])].
synonym([no, one], [noone]).
synonym([none], [noone]).
synonym([nobody], [noone]).
synonym([nothing], [noone]).
[headerfiles, are, included, by, noone] ===> [srai([orphaned, headerfiles])].



[headerfiles, are, included, by, file, star(A)] ===> [srai([headerfiles, does, file, A, include])].

[cppfiles, are, included, by, file, star(A)] ===> [srai([cppfiles, does, file, A, include])].

[how, does, file, star(A), include, file, star(B)] ===> [think((strip_star_atom(A,X),
                                                                strip_star_atom(B,Y),
                                                                findall(['file', X, 'includes file', Y, 'via path', P, '\n'],
                                                                        X depends on Y via P, S))),
                                                         S].
                                                  
[how, is, file, star(A), included, by, file, star(B)] ===> [srai([how, does, file, B, include, file, A])].

[orphaned, headerfiles] ===> [think( findall(['file', X, 'is included by no-one', '\n'], (headerfile X, \+(_ includes X)), R) ), R].

                                                    
[star(A)] ===> ['I did not understand what you wanted when you asked\n', A, '\nPlease rephrase the question in a different way.\nTo stop, type stop (or bye, or quit, or ...).'].

