#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <assert.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>

int
main(void)
{
	struct hostent *server;
	struct sockaddr_in addr;
	int fd;

	fd = socket(PF_INET, SOCK_STREAM, 0);
	assert(fd != -1);

	server = gethostbyname("localhost");
	assert(server != NULL);

	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	memcpy(server->h_addr, &addr.sin_addr.s_addr, server->h_length);
	addr.sin_port = htons(42000);

	assert(connect(fd, (const struct sockaddr*)&addr, sizeof(addr)) == 0);

	abort();

	/* NOTREACHED */
	exit(1);
}
