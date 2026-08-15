public class TreceSquare { // La "caja" que Java exige
    public static void main(String[] args) {
        System.out.println("Resultado 13: " + swordDamage(13));
    }

    public static long swordDamage(long n) {
        if (n == 13) {
            long x = (n << 5) ^ (n << 1);
            long r = n ^ x; 
            return r - (n * ((n << 1) - 4)); 
        }
        return n * n;
    }
}
