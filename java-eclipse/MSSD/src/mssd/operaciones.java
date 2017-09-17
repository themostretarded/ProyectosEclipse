/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package mssd;

import java.util.Random;

/**
 *
 * @author Rei
 */
public class operaciones {
    public double productosmedios(int d,int semilla,int x,int n)
	{
            double num = 0;
	String temporal;
	String  cadenatemporal = "";
		int y0,y,xi,x0,x1;
		float ri;
		int contador=0;
		x0=semilla;
		x1=x;
	for(int i=0;i<n;i++)
	{
		y0=x0*x1;
	//	System.out.println(y0);
		String enteroString = Integer.toString(y0);
	
		for(int j=0;j<enteroString.length();j++)
		{
			contador=contador+1;		
		}
		if(contador%2!=0)
		{
			StringBuffer sb = new StringBuffer(enteroString);
			sb.insert(0,"0");
			contador=contador+1;			
			enteroString=sb.toString();			
			//System.out.println("yo= "+enteroString+  " con numero de digitos = "+contador);
			//System.out.print("NUMERO DE DIGITOS A TOMAR  =  de  "+enteroString.length()/d+"  a  "    );
		//	System.out.println((enteroString.length()/d)+d);
			for(int z=(enteroString.length()/d);z<((enteroString.length()/d)+d);z++)
			{
				char a_char=enteroString.charAt(z);
				//System.out.println(a_char);
				
					StringBuilder sbtemp = new StringBuilder();
					sbtemp.append(a_char);	
					temporal = sbtemp.toString();
					cadenatemporal = cadenatemporal+temporal;
			}
		}
		else
		{		
			StringBuffer sb = new StringBuffer(enteroString);
			enteroString=sb.toString();
			//System.out.println("yo= "+enteroString+  " con numero de digitos = "+contador);
			//System.out.print("NUMERO DE DIGITOS A TOMAR  =  de  "+enteroString.length()/d+"  a  "    );
			//System.out.println((enteroString.length()/d)+d);
			for(int z=(enteroString.length()/d);z<((enteroString.length()/d)+d);z++)
			{
				char a_char=enteroString.charAt(z);
				//System.out.println(a_char);
				
					StringBuilder sbtemp = new StringBuilder();
					sbtemp.append(a_char);	
					temporal = sbtemp.toString();
					cadenatemporal = cadenatemporal+temporal;
		
			}	
		}
		xi=Integer.parseInt(cadenatemporal);	
		StringBuffer sb = new StringBuffer(cadenatemporal);
		sb.insert(0,"0.");
		cadenatemporal=sb.toString();	
		ri=Float.parseFloat(cadenatemporal);
		cadenatemporal="";
		contador=0;
		//System.out.println(xi);
		//System.out.println("r"+i+"= "+ri);
		x0=x1;
		x1=xi;
                num=ri;
	}
        
	return num;
	}	

    double productosmedios(int i, Random rand, Random rand2, int i0) {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
	
}
