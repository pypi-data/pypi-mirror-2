Reblok
======

[Reblok](http://devedge.bour.cc/wiki/Reblok) build an Abstract Syntax Tree (AST) back from python bytecode.


###Requirements:
* [byteplay](http://pypi.python.org/pypi/byteplay)

###Compatility:
*	python 2.[5-7]

* Has not been tested with python3,
*	Should work with [pypy](http://pypy.org), although some specific opcodes are not handled (see
	[Pypy special opcodes](http://codespeak.net/pypy/dist/pypy/doc/interpreter-optimizations.html#special-bytecodes)).

###Installation
	easy_install reblok

or

	wget http://devedge.bour.cc/resources/reblok/src/reblok.latest.tar.gz
	tar xvf reblok.latest.tar.gz
	cd reblok-* && ./setup.py install

Documentation
-------------

You can found reblok opcodes documentation at [http://devedge.bour.cc/resources/reblok/doc/sources/ast.html](http://devedge.bour.cc/resources/reblok/doc/sources/ast.html)

Example
-------

	>>> from reblok import Parser
	>>> add = lambda x: x + 1
	>>> ast = Parser().walk(add)
	>>> print ast
	['function', '<lambda>', [['ret', ('add', ('var', 'x', 'local'), ('const', 1))]], [('x', '<undef>')], None, None, [], {}]


About
-----

*Reblok* is licensed under GNU GPL v3.
It is developped by Guillaume Bour <guillaume@bour.cc>
