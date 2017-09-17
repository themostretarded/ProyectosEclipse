import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
public class Nombre extends JFrame
implements ActionListener {
/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
private JButton button;
public static void main(String[] args) {
Nombre frame = new Nombre();
frame.setSize(400, 300);
frame.createGUI();
frame.setVisible(true);
}
private void createGUI() {
setDefaultCloseOperation(EXIT_ON_CLOSE);
Container window = getContentPane();
window.setLayout(new FlowLayout() );
button = new JButton("Ahi voy");
window.add(button);
button.addActionListener(this);
}
public void actionPerformed(ActionEvent event) {

String Nombre;
Nombre = JOptionPane.showInputDialog("Dime tu nombre:");

JOptionPane.showMessageDialog(null, "tu nombre es: " + Nombre);
}
}
