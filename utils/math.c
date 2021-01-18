/*
 * This is a simple program that calls BC and terminates it if it takes longer
 * than five seconds to complete. There is no real reason for this to be done
 * in C instead of Python, however there are some key advantages:
 *
 *  - Mango gets to play with C making him happy
 *  - C is compiled instead of interpreted so this is technically more efficient
 *    - Ok mayyyybe is slower because it uses a seperate process?
 *  - It makes us look smarter?
 */
#define _POSIX_SOURCE
#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

#include "math.h"

bool timeout = false, child_done = false;

void timeout_hander(int UNUSED(sig))
{
    timeout = true;
}

void child_handler(int UNUSED(sig))
{
    child_done = true;
}

int main(void)
{
    pid_t pid = fork();
    switch (pid) {
    case 0:
        execl("/bin/bc", "", "-q", "bc_funcs/lib.bc", "bc_funcs/init.bc",
              FILE_NAME, "bc_funcs/exit.bc", NULL);
        fallthrough;
    case -1:
        perror("calc");
        return EXIT_FAILURE;
    default:
        /* Setup signal handlers after fork so the child doesnt inherit them */
        signal(SIGALRM, timeout_hander);
        signal(SIGCHLD, child_handler);
        alarm(TIMEOUT);
        pause();

        /*
         * Wait for either the child process to terminate, or for 5 seconds to
         * have passed
         */
        if (timeout) {
            puts("Error: 5 second timeout reached");
            kill(pid, 9);
        }

        break;
    }

    return EXIT_SUCCESS;
}