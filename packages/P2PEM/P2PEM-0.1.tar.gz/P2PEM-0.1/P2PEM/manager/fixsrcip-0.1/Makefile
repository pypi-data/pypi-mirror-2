# $Id: Makefile 43 2004-11-22 20:57:29Z lennart $

VERSION=0.1
TARFILE=fixsrcip-$(VERSION).tar.gz
DISTDIR=fixsrcip-$(VERSION)/
DISTFILES=Makefile fixsrcip.c fixsrcip README LICENSE

fixsrcip.so: fixsrcip.c Makefile
	gcc -Wall -W -O2 -D_GNU_SOURCE -fPIC -shared -o $@ $< -ldl
	strip $@

dist: $(TARFILE)

$(TARFILE):
	rm -rf $(DISTDIR)
	mkdir $(DISTDIR)
	cp $(DISTFILES) $(DISTDIR)
	rm -f $(TARFILE)
	tar czf $(TARFILE) $(DISTDIR)
	rm -rf $(DISTDIR)

clean:
	rm -f fixsrcip.so *.tar.gz
	rm -rf fixsrcip-$(VERSION)

.PHONY: clean dist
