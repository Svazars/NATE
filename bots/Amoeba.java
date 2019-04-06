import java.util.Scanner;

public class Amoeba {

  private static long skipUntilLong(Scanner scanner) {
    while(true) {
      if (scanner.hasNextLong()) {
        return scanner.nextLong();
      }

      scanner.next();
    }
  }
  public static void main(String[] arg) {  
    final Scanner scanner = new Scanner(System.in);
    final long turns = skipUntilLong(scanner);
    final long money = skipUntilLong(scanner);

    System.out.println("OK");  
  
    for (int i = 0; i < turns; i++) {
        long p = skipUntilLong(scanner);
        long m = skipUntilLong(scanner);
        long s = skipUntilLong(scanner);
        System.out.println("Buy 0"); // i am amoeba, i do nothing
    }
  }
  
}
