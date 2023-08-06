Pycdep in a nutshell
====================
You've installed pycdep and obviously now you want to use it.
The way pycdep works is as follows:

#. You invoke pycdep, specifying some command line options. As a result, you get a prolog program.
#. You load the prolog program in swi-prolog (other prologs are untested) and you can formulate queries to get information about and visualization of the dependencies in your software.

Example
=======
Run the following command
::
  python pycdep.py --sandbox mysandbox -R /path/to/code --common-root-folder code --strip-common-root-folder

This will run pycdep.py. The **--sandbox** option causes pycdep to use folder mysandbox as a sandbox folder, i.e. a folder where intermediary files (should they be needed) will be saved. Also, if you don't specify a path to a log file, the log file will end up in the sandbox folder. The **-R** option adds /path/to/code as a directory that has to be recursively scanned and processed. The **--common-root-folder** option specifies that path names in the output will be truncated so that they start with the folder specified as --common-root-folder. 
The **--strip-common-root-folder**  causes the common root folder to be stripped from the pathnames.

To clarify the meaning of the --common-root-folder and --strip-common-root-folder options, here's an example. Suppose you have the following file structure
::
  /path/to/code/a.cpp
  /path/to/code/a.h
  /path/to/code/lib/b.cpp
  /path/to/code/lib/b.h

If you specify --common-root-folder code, the path names in the resulting prolog and graphviz files will be truncated as follows
::
  code/a.cpp
  code/a.h
  code/lib/b.cpp
  code/lib/b.h
If you additionally specify --strip-common-root-folder, the path names in the resulting prolog and graphviz files will be truncated as follows
::
  a.cpp
  a.h
  lib/b.cpp
  lib/b.h

Running the resulting prolog file
=================================
Load the generated prolog program in swi-prolog (type the following on the command line/shell)
::
  swipl -f dependencies.pl

You arrive in an interactive prompt, and now you can already perform prolog queries. The generated prolog file contains many examples of predefined queries. A useful one is the full_report query. It will write all kinds of interesting facts about your source code in a text report
::
  ?- full_report(_).

Use its source. Here's an example prolog query that finds all the files that include file 'lib/b.h'
::
  ?- findall(F, F depends on 'lib/b.h', Result), write(Result).

Here's how to dump all the include dependencies in a .dot file for visualization using graphviz (inside prolog)
::
  ?- findall([F1,F2], F1 includes F2, Result), to_graphviz('test.dot', Result).

(see the documentation inside the generated prolog file to see more examples). 

To generate a .png from the .dot file, you can do (on a command line)
::
  dot -Tpng test.dot -o test.png

Using the natural language frontend [experimental]
==================================================
If you are not too keen on learning prolog to get information about the system, you can try out the very experimental natural language front-end. To be able to use this front-end you need to load two additional prolog files: intuitivequery.pl and categories.pl. The file intuitivequery.pl implements an interpreter for a dialect of a superset of a subset of the artificial-intelligence markup language (AIML). The categories.pl defines the natural language queries using an AIML-like syntax. Unlike AIML, the syntax used in categories.pl is not XML based, which makes it less cumbersome to edit.

Here's how to load the generated prolog file together with the natural language interface, and to start up the natural language input loop
::
  swipl -g "[dependencies, intuitivequery, categories], loop."

You can now type queries like
::
  ?- Show me the header files in project 'lib' ?
  ?- Which header files are included by noone ?

Please see categories.pl, and tests.pl for some inspiration about possible queries.

Command line options
====================
To get an overview of the command line options, type
::
  python pycdep.py --help

As a result you get
::
  usage: pycdep.py [-h] [-s SANDBOX] [-l LOGFILE] [-V VERBOSITY] [-r REPORTNAME]
                 [-v] [-p PREFIXLENGTH] [-i] [-I INCLUDEDIR]
                 [-R RECURSIVEINCLUDEDIR] [-X EXCLUDEDIR]
                 [-Y RECURSIVEEXCLUDEDIR] [-C CPPSUFFIX] [-H HEADERSUFFIX]
                 [-S SEPARATOR] [-P PROLOGDATABASENAME]
                 [-d HIERARCHYDEFINITION] [-f COMMONROOTFOLDER] [-c]

The available command line options are
::
  -h, --help            show this help message and exit
  -s SANDBOX, --sandbox SANDBOX
                        generates intermediate files in the SANDBOX folder (if
                        any)
  -l LOGFILE, --logfile LOGFILE
                        choose how to name the logfile
  -V VERBOSITY, --verbosity VERBOSITY
                        choose log level (50 = CRITICAL, 40 = ERRROR, 30 =
                        WARNING, 20 = INFO, 10 = DEBUG, 0 = NOT SET)
  -r REPORTNAME, --report-name REPORTNAME
                        generates a report with name REPORTNAME
  -v, --version         show version and quit
  -p PREFIXLENGTH, --prefix-length PREFIXLENGTH
                        max no of path prefixes to keep (to avoid duplicate
                        names)
  -i, --case-insensitive
                        consider file names to be case insensitive (win32)
  -I INCLUDEDIR, --include-dir INCLUDEDIR
                        add a directory to examine non-recursively
  -R RECURSIVEINCLUDEDIR, --recursive-include-dir RECURSIVEINCLUDEDIR
                        add a directory to examine recursively
  -X EXCLUDEDIR, --exclude-dir EXCLUDEDIR
                        exclude a directory from analysis
  -Y RECURSIVEEXCLUDEDIR, --recursive-exclude-dir RECURSIVEEXCLUDEDIR
                        exclude a directory and all its subdirectories from
                        analysis
  -C CPPSUFFIX, --cppfile-suffix CPPSUFFIX
                        define file extension of c/c++ files (default: cpp)
  -H HEADERSUFFIX, --headerfile-suffix HEADERSUFFIX
                        define file extension of header files (default: h)
  -S SEPARATOR, --path-separator SEPARATOR
                        define an additional path separator (default: '/')
  -P PROLOGDATABASENAME, --prolog-name PROLOGDATABASENAME
                        define the name of the prolog database that will be
                        saved
  -d HIERARCHYDEFINITION, --hierarchy-definition HIERARCHYDEFINITION
                        location of hierarchy.txt (include constraint
                        specificiation)
  -f COMMONROOTFOLDER, --common-root-folder COMMONROOTFOLDER
                        when displaying a file path, always start from the
                        common root folder if possible
  -c, --strip-common-root-folder
                        when displaying a file path starting from a common
                        root folder, include the common root folder from the
                        displayed path


