import java.awt.*;
import java.awt.event.*;

import javax.swing.*;
public class EjemploDibujo extends JFrame implements ActionListener {
	private JButton button;
	private JPanel panel;
	public static void main(String[]args){
		EjemploDibujo marco=new EjemploDibujo();
		marco.setSize(400,300);
		marco.crearGUI();
		marco.setVisible(true);
	}
	private void crearGUI(){
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		Container ventana = getContentPane();
		ventana.setLayout(new FlowLayout());
		panel =new JPanel();
		panel.setPreferredSize(new Dimension(300,200));
		panel.setBackground(Color.white);
		ventana.add(panel);
		button=new JButton("haz clic");
		ventana.add(button);
		button.addActionListener(this);		
	}
	public void actionPerformed(ActionEvent event){
	Graphics papel = panel.getGraphics();
	papel.drawLine(0,0,100,100);
	}
}
