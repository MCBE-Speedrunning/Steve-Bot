#ifndef __MATH_H_
#define __MATH_H_

/* Suppress unused parameter warnings */
#ifdef __GNUC__
#    define UNUSED(x) UNUSED_##x __attribute__((__unused__))
#else
#    define UNUSED(x) UNUSED_##x
#endif

/* Fallthrough pseudo-keyword macro */
#if __has_attribute(__fallthrough__)
#    define fallthrough __attribute__((__fallthrough__))
#else
#    define fallthrough                                                        \
        do {                                                                   \
        } while (0) /* fallthrough */
#endif

#define EXIT_FAILURE 1
#define EXIT_SUCCESS 0
#define FILE_NAME    "bc_input.bc"
#define TIMEOUT      5

/* Signal handlers */
void timeout_hander(int sig);
void child_handler(int sig);

#endif