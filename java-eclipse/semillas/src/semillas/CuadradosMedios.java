package semillas;
public class CuadradosMedios {
    public static void main(String[] args) {
        	int num=8;
	int D=4;
	int x0=8550;
	int y0=(int)Math.pow(x0,2);
        System.out.println(y0);
	int xi=cNumero(Integer.toString(y0),D);
	double ri=conNumeroDe(Integer.toString(xi));
	System.out.printf("\nxi=%d\tri=%.5f",xi,ri);
	int i=0;
	int yi_1=0;
	int xi_1=0;
	double ri_1=0.0;
        
	for(i=0;i<num-1;i++)
	{
		yi_1=(int)Math.pow(xi,2);
		xi_1=cNumero(Integer.toString(yi_1),D);
		ri_1=conNumeroDe(Integer.toString(xi_1));
		System.out.printf("\nxi=%d\tri=%.5f",xi_1,ri_1);
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
	String momentaneo="0";
	momentaneo=momentaneo+auxiliar;
	return cNumero(momentaneo,d);
     }
    return Integer.parseInt(auxconver);
 }
 public static double conNumeroDe(String auxiliar)
 {
     return Double.parseDouble(("0."+auxiliar));
 }
}