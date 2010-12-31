/* this file is in the public domain */

#include <stdio.h>

#include "static.h"
#include "dynamic.h"

int main(int argc, char **argv) {
	printf("Hello, %c, %d, %ld, %c, %d, %ld\n", a(), b(), c(), d(), e(), f());
	return 0;
}

