import java.util.Scanner;
public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println ("Empezamos el programa");

        System.out.println ("Elija una temperatura:");

        String entradaTeclado = "";

        Scanner entradaEscaner = new Scanner (System.in); //Creación de un objeto Scanner

        entradaTeclado = entradaEscaner.nextLine (); //Invocamos un método sobre un objeto Scanner

        System.out.println ("La temperatura es: \"" + entradaTeclado +"\"");
		Thread hilo = new Procesos("Perdida");
		Thread hilo2 = new Procesos("LanzaGas");
		
		hilo.run();
		hilo2.run();

	}

}
