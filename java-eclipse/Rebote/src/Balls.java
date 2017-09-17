import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
public class Balls extends JFrame implements ActionListener {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private JButton go1, go2, stop1, stop2;
	private JPanel panel1, panel2;
	private Ball ball1, ball2;
	public static void main(String[] args) {
		Balls frame = new Balls();
		frame.setSize(500,150);
		frame.createGUI();
		frame.setVisible(true);
	}
	private void createGUI() {
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		Container window = getContentPane();
		window.setLayout(new FlowLayout());
		go1 = new JButton("go 1");
		window.add(go1);
		go1.addActionListener(this);
		stop1 = new JButton("stop 1");
		window.add(stop1);
		stop1.addActionListener(this);
		panel1 = new JPanel();
		panel1.setPreferredSize(new Dimension(100, 100));
		panel1.setBackground(Color.white);
		window.add(panel1);
		panel2 = new JPanel();
		panel2.setPreferredSize(new Dimension(100, 100));
		panel2.setBackground(Color.white);
		window.add(panel2);
		go2 = new JButton("go 2");
		window.add(go2);
		go2.addActionListener(this);
		stop2 = new JButton("stop 2");
		window.add(stop2);
		stop2.addActionListener(this);
	}
	public void actionPerformed(ActionEvent event) {
		if (event.getSource() == go1) {
			ball1 = new Ball(panel1);
			ball1.start();
		}
		if (event.getSource() == go2) {
			ball2 = new Ball(panel2);
			ball2.start();
		}
		if (event.getSource() == stop1) {
			ball1.pleaseStop();
		}
		if (event.getSource() == stop2) {
			ball2.pleaseStop();
		}
	}
}

