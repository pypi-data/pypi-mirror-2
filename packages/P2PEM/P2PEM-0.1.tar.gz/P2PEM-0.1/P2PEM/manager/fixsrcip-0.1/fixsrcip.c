/* $Id: fixsrcip.c 43 2004-11-22 20:57:29Z lennart $ */

/***
  This file is part of fixsrcip.

  fixsrcip is free software; you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published
  by the Free Software Foundation; either version 2 of the License,
  or (at your option) any later version.

  fixsrcip is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with fixsrcip; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
  USA.
***/

#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <dlfcn.h>
#include <stdlib.h>

static void do_bind(int fd) {
    char *address;
    struct sockaddr_storage _local;
    struct sockaddr_in *local = (struct sockaddr_in*) &_local;
    socklen_t s_local = sizeof(_local);

    if (!(address = getenv("FIXSRCIP")))
        return;

    if (getsockname(fd, (struct sockaddr *) &_local, &s_local) < 0 || s_local != sizeof(struct sockaddr_in))
        return;

    if (local->sin_family == AF_INET && local->sin_addr.s_addr == INADDR_ANY) {

        if (!inet_aton(address, &local->sin_addr))
            return;

        bind(fd, (struct sockaddr*)  local, sizeof(struct sockaddr_in));
    }
}

int connect(int fd, const struct sockaddr* sa, socklen_t l) {
    int (*real_connect)(int, const struct sockaddr*, socklen_t);
    
    do_bind(fd);
    real_connect = dlsym(RTLD_NEXT, "connect");
    return real_connect(fd, sa, l);
}

ssize_t sendto(int fd, const void *buf, size_t l, int flags, const struct sockaddr *sa, socklen_t sal) {
    int (*real_sendto)(int, const void *, size_t, int, const struct sockaddr *, socklen_t);

    do_bind(fd);
    real_sendto = dlsym(RTLD_NEXT, "sendto");
    return real_sendto(fd, buf, l, flags, sa, sal);
}

ssize_t sendmsg(int fd, const struct msghdr *msg, int flags) {
    int (*real_sendmsg)(int, const struct msghdr *, int);

    do_bind(fd);
    real_sendmsg = dlsym(RTLD_NEXT, "sendmsg");
    return real_sendmsg(fd, msg, flags);
}
