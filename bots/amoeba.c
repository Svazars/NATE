#include <stdio.h>

int main() {

  unsigned int turns = 0;
  unsigned long long int money = 0;

  int matched = scanf("Exchange opened for %u days. Initial money = %llu", &turns, &money);
  if (matched != 2) {
  	printf("Unexpected exchange format, exiting.\n");
  	return -1;
  } else {
    printf("OK\n");
  }

  unsigned long long int p, m, s;

  for (int i = 0; i < turns; i++) {
        int result = scanf("%llu %llu %llu", &p, &m, &s);
        if (result == 0 || result == EOF) {
           printf("Failed to scan on day %d\n", i);
           return -1;
        }

  	printf("Buy 0\n"); // i am amoeba, i do nothing
  }

  return 0;
}
