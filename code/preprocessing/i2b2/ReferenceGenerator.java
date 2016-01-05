/**
 * Calculates gold standard sentence boundaries for i2b2 data.
 */
package i2b2;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

import org.apache.commons.io.FileUtils;

import au.com.bytecode.opencsv.CSVWriter;

public class ReferenceGenerator 
{
	public static void main(String args[])
	{
        if (args.length != 2)
        {
            System.out.println("Usage: ReferenceGenerator PLNDIR BNDSDIR\n");
            System.out.println("\tPLNDIR   path to plaintext i2b2 files");
            System.out.println("\tBNDSDIR  path to write sentence boundaries to");
        }
        else
        {
            String dataPath = args[0];
            String outPath = args[1];

            ReferenceGenerator refGen = new ReferenceGenerator();
            refGen.createReferenceOffsets(dataPath,outPath);
        }
	}

	private void createReferenceOffsets(String dataPath, String outFile) 
	{
		File dir = new File(dataPath);
		File[] allFiles = dir.listFiles();

		try 
		{
			for(File f : allFiles)
			{
				ArrayList<String[]> refs = processFile(f);
								
				CSVWriter writer = new CSVWriter(new FileWriter(outFile +  f.getName().replace(".txt", ".csv")));
				writer.writeAll(refs);
				writer.close();
			}			
		} 
		catch (IOException e) 
		{			
			e.printStackTrace();
		}

	}

	private ArrayList<String[]> processFile(File f) 
	{
		ArrayList<String[]> refs = new ArrayList<>();

		try
		{
			String allText = FileUtils.readFileToString(f);
			
			BufferedReader br = new BufferedReader(new FileReader(f));
			String nextLine;

			int start = 0;
			int end = 0;

			while((nextLine=br.readLine())!=null)
			{
				end = start + nextLine.length()+1;
				if(start==0 && end==0)
					continue;
				
				String[] record = new String[2];
				record[0] = "" + start;
				record[1] = "" + end;
				refs.add(record);
				start = start + nextLine.length()+1;
			}

			br.close();
		}
		catch(IOException ie)
		{
			System.err.println(ie.getMessage());
			ie.printStackTrace();
		}

		return refs;
	}
}
