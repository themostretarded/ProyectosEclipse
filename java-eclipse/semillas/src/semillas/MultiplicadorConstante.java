package semillas;
public class MultiplicadorConstante {
    public static void main(String[] args) {
        int num=8;
	int D=4;
	int x0=9803;
	int constante=8550;
	int yi,xi;
	double ri;
	int i;
	for(i=0;i<num;i++)
	{
		yi=x0*constante;
		xi=cNumero(Integer.toString(yi),D);
		ri=cNumeroDe(Integer.toString(xi));
		System.out.printf("\nxi=%d\tri=%.5f",xi,ri);
		x0=xi;
	}
    }
 public static int cNumero(String auxiliar,int d)
 {
     String auxconver="";
     if(auxiliar.length()%2==0)
     {
	int distancia=(auxiliar.length()-d)/2;
	if(distancia>0)
	{
            auxconver=auxiliar.substring(distancia,auxiliar.length()-distancia);
	}
	else
	{
	    auxconver=auxiliar;
	}
     }
     else
     {
	String momentaneo="0";
	momentaneo=momentaneo+auxiliar;
	cNumero(momentaneo,d);
     }
    return Integer.parseInt(auxconver);
 }
 public static double cNumeroDe(String auxiliar)
 {
     return Double.parseDouble(("0."+auxiliar));
 }
}