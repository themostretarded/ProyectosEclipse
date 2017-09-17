import java.awt.*;
import javax.swing.*;
public class saludo extends JFrame {
	private JTextField textField;
	public static void main(String[] args){
		saludo marco= new saludo();
		marco.setSize(300,200);
		marco.crearGUI();
		marco.setVisible(true);
	}
	private void crearGUI(){
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		Container window= getContentPane();
		window.setLayout(new FlowLayout());
		textField =new JTextField("hola");
		window.add(textField);
	}

}
