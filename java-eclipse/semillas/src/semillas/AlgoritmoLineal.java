package semillas;
public class AlgoritmoLineal {
    public static void main(String[] args) {
        int x0=6;
	int x0i=x0;
	int a=13;
	int c=7;
	int m=8;
	int xi=-1;
	int i=0;
	double ri=0.0;
	do
	{
		xi=(a*x0+c)%m;
		ri=xi/(m-1.0);
		System.out.printf("%d xi=%d ri=%.5f\n",++i,xi,ri);
		x0=xi;
	}while(x0i!=x0);
    }
    
}
