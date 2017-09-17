package semillas;
public class ProductosMedios {
    public static void main(String[] args) {
        int num=8;
	int D=4;
	int x0=7550;
	int xi=8550;
	int y0=x0*xi;
	int i=0;
	int yi_1;
	int xi_1=cNumero(Integer.toString(y0),D);
        double ri=cNumeroDec(Integer.toString(xi_1));
	System.out.printf("\nxi=%d\tri=%.5f",xi_1,ri);
	double ri_1;
	x0=xi;
	xi=xi_1;
	for(i=0;i<num-1;i++)
	{
		yi_1=x0*xi;
		xi_1=cNumero(Integer.toString(yi_1),D);
		ri_1=cNumeroDec(Integer.toString(xi_1));
		System.out.printf("\nxi=%d\tri=%.5f",xi_1,ri_1);
		x0=xi;
		xi=xi_1;
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
	String paso="0";
	paso=paso+auxiliar;
	return cNumero(paso,d);
     }
    return Integer.parseInt(auxconver);
 }
 public static double cNumeroDec(String auxiliar)
 {
     return Double.parseDouble(("0."+auxiliar));
 }
}