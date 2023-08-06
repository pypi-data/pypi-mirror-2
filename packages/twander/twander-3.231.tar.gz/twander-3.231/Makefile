# FreeBSD Ports Makefile For 'twander'
# $Id: Makefile,v 1.33 2005/02/02 23:37:21 tundra Exp $


all: # Just need to create the compiled image
	@python -OOOO -c"import py_compile;py_compile.compile('twander.py')"

install:
	${BSD_INSTALL_SCRIPT} ./twander.py   ${PREFIX}/bin
	${BSD_INSTALL_SCRIPT} ./twander.pyo  ${PREFIX}/bin
	${BSD_INSTALL_MAN}    ./twander.1.gz ${PREFIX}/man/man1

