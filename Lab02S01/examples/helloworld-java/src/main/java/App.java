public class App {
    public static void main(String[] args) {
        Greeter g = new Greeter();
        System.out.println(g.greet("Mundo"));
    }
}

class Greeter {
    public String greet(String name) {
        return "Olá, " + name + "!";
    }
}
