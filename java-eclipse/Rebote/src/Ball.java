import java.awt.*;
import javax.swing.*;
public class Ball extends Thread {
	private JPanel panel;
	private int x = 7, xChange = 7;
	private int y = 0, yChange = 2;
	private final int diameter = 10;
	private final int width = 100, height = 100;
	boolean keepGoing;
	public Ball(JPanel thePanel) {
		panel = thePanel;
	}
	public void run() {
		keepGoing = true;
		while (keepGoing) {
			move();
			bounce();
			draw();
			delay();
			delete();
		}
	}
	private void move() {
		x = x + xChange;
		y = y + yChange;
	}
	private void bounce() {
		if (x <= 0 || x >= width) {
			xChange = -xChange;
		}
		if (y <= 0 || y >= height) {
			yChange = -yChange;
		}
	}
	private void delay() {
		try {
			Thread.sleep(50);
		}
		catch (InterruptedException e) {
			return;
		}
	}
	private void draw() {
		Graphics paper = panel.getGraphics();
		paper.setColor(Color.red);
		paper.fillOval(x, y, diameter, diameter);
	}
	private void delete() {
		Graphics paper = panel.getGraphics();
		paper.setColor(Color.white);
		paper.fillOval (x, y, diameter, diameter);
	}
	public void pleaseStop() {
		keepGoing = false;
	}
}
