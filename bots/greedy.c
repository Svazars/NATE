#include <stdio.h>
#include <stdbool.h>

typedef unsigned long long int uint64;

int main() {

  unsigned int turns = 0;
  uint64 money = 0;

  int matched = scanf("Exchange opened for %u days. Initial money = %llu", &turns, &money);
  if (matched != 2) {
  	printf("Unexpected exchange format, exiting.\n");
  	return -1;
  } else {
    printf("OK\n");
  }

  double averagePrice = 0.0;
  uint64 p = 0, m = 0, s = 0;

  for (int i = 0; i < turns; i++) {
  	int result = scanf("%llu %llu %llu", &p, &m, &s);
    if (result == 0 || result == EOF) {
        printf("Failed to scan on day %d\n", i);
        return -1;
    }

    if (i == (turns - 1)) {
      // last turn, sell everything
      printf("Sell %llu", s);
      continue;
    }
    
    uint64 maySpendInRound = m / 2;
    bool shouldBuy = false;

    if (s == 0) {
      // lets buy something
      shouldBuy = true;
    } else if (p <= averagePrice) {
      // current price is more profitable than our average stock price. Lets buy more cheap stocks!
      shouldBuy = true;
    } else {
      // Sell everything
      shouldBuy = false;
    }

    if (shouldBuy) {
      uint64 amount = maySpendInRound / p;
      printf("Buy %llu\n", amount);
      averagePrice  = ((averagePrice * s) + (amount * p)) / (s + amount);
    } else {
      printf("Sell %llu\n", s);
      averagePrice = 0.0;
    }
  }

  return 0;
}
