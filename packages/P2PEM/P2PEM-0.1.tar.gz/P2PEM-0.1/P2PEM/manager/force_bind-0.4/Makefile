# duilder header starts #
export PRJ := force_bind
export VER := 0.5
export REV := 1
export DESTDIR

export I_ETC := $(DESTDIR)/etc
export I_BIN := $(DESTDIR)/bin
export I_SBIN := $(DESTDIR)/usr/sbin
export I_USR_BIN := $(DESTDIR)/usr/bin
export I_USR_SBIN := $(DESTDIR)/usr/sbin
export I_USR_INCLUDE := $(DESTDIR)/usr/include
export I_USR_INC := $(DESTDIR)/usr/include
export I_USR_SHARE_DOC := $(DESTDIR)/usr/share/doc/force_bind-0.5
export I_USR_LIB := $(DESTDIR)/usr/lib
export I_LIB := $(DESTDIR)/usr/lib
export I_VAR := $(DESTDIR)/var
export I_VAR_LOG := $(DESTDIR)/var/log/force_bind

# DB stuff
export DB_SUPPORT := 0
# PG
export PG_FOUND := 0
export PG_INC := 
export PG_LIB := 
# MySQL
export MYSQL_FOUND := 0
export MYSQL_INC := 
export MYSQL_LIB := 

# duilder header ends #

export CC := gcc
export INCS +=
export LIBS +=
export CFLAGS += -ggdb3 -Wall -Wextra -Wno-long-long -pipe
export CFLAGSSO = $(CFLAGS) -ldl -lc -shared -rdynamic -fpic

.PHONY: all
all:	force_bind.so test_bind

force_bind.so:	force_bind.c
	$(CC) $(CFLAGSSO) -Wl,-soname,force_bind.so -o $@ force_bind.c

test_bind:	test_bind.c
	$(CC) $(CFLAGS) $< -o $@

.PHONY: clean
clean:
	@rm -f force_bind.so.* test_bind *.a *.o *.so* $(PRJ)-*.rpm $(PRJ)-*-*-*.tgz $(PRJ)-*.tar.gz

install:	all
	@mkdir -p $(I_USR_LIB)
	cp -vd force_bind.so $(I_USR_LIB)

# duilder tail starts #

# This is to allow exporting only the git tree
dist_git:
	@./duilder git "$(PRJ)" "/data/www/umbrella/kernel/us/force_bind" "0" "/data/www/umbrella/kernel/us/force_bind" "1"

.PHONY: dist
dist: clean
	@./duilder git "$(PRJ)" "/data/www/umbrella/kernel/us/force_bind" "0" "1" ""
	@./duilder tar "$(PRJ)" "$(VER)" "/data/www/umbrella/kernel/us/force_bind" ""
	@./duilder srpm "$(PRJ)" "$(VER)" "/data/www/umbrella/kernel/us/force_bind" "1" "../dinorepo/fedora/SRPMS" "/usr/local/bin/submit_package"
	@./duilder docs "$(PRJ)" "$(VER)" "/data/www/umbrella/kernel/us/force_bind"
	@./duilder final "$(PRJ)" "$(VER)" "/usr/local/bin/duilder_release"
	@rm -f "$(PRJ)-$(VER).tar.gz"

