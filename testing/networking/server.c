#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <assert.h>
#include <err.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int
main(void)
{
	char buf[1024], cli_addr_buf[1024];
	struct sockaddr_in addr, cli_addr;
	socklen_t cli_len;
	int cli_sock, fd;

	fd = socket(PF_INET, SOCK_STREAM, 0);
	assert(fd != -1);

	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = INADDR_ANY;
	addr.sin_port = htons(42000);

	assert(bind(fd, (const struct sockaddr*)&addr, sizeof(addr)) == 0);

	cli_len = sizeof(cli_addr);

	listen(fd, 1);

	for (;;) {
		cli_sock = accept(fd, (struct sockaddr*)&cli_addr, &cli_len);
		if (inet_ntop(AF_INET, &cli_addr.sin_addr.s_addr,
		    cli_addr_buf, cli_len) != NULL) {
			if (read(cli_sock, buf, sizeof(buf)) == -1)
				warn("read failed");
			else
				printf("host=%s/port=%d said: %s\n",
				    cli_addr_buf, ntohs(cli_addr.sin_port),
				    buf);
		}
		sleep(10);
		close(cli_sock);
	}

	/* NOTREACHED */
	exit(0);
}
