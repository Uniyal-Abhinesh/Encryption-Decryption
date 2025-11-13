/* Compatibility shim for __isoc23_strtol */
#define _GNU_SOURCE
#include <stdlib.h>
#include <string.h>

/* Provide compatibility wrapper if needed */
#ifdef __cplusplus
extern "C" {
#endif

long __isoc23_strtol(const char *nptr, char **endptr, int base) {
    return strtol(nptr, endptr, base);
}

#ifdef __cplusplus
}
#endif

