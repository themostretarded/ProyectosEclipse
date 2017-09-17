package semillas;
public class SecuenciallMultiplicativo {
    public static void main(String[] args) {
        int x0=17;
	int x0i=x0;
	int a=21;
	int m=32;
	int xi=-1;
	int i=0;
	double  ri=0.0;
	do
	{
		xi=(a*x0)%m;
		ri=xi/(m-1.0);
		System.out.printf("%d xi=%d\tri=%.5f\n",++i,xi,ri);
		x0=xi;
	}while(x0i!=x0);
    }
}
