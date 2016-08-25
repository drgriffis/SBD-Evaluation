import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;

import au.com.bytecode.opencsv.CSVReader;

public class SegmentationEvaluator 
{
	public static void main(String args[])
	{
        String reference, response, reference_suffix, response_suffix;
        if (args.length < 3) {
            System.out.println("Missing required arguments specifying reference/prediction directories and file suffixes");
        } else {
            reference = args[0];
            response = args[1];
            reference_suffix = args[2];
            response_suffix = args[3];
            SegmentationEvaluator segEval = new SegmentationEvaluator();
            segEval.evaluate(reference, response, reference_suffix, response_suffix);
        }
	}

	private void evaluate(String reference, String response, String reference_suffix, String response_suffix) 
	{
		double TP = 0.0;
		double FP = 0.0;
		double FN = 0.0;
		
		File[] refFiles = new File(reference).listFiles();
		for(File f : refFiles)
		{
			double tp = 0;
			double fp = 0;
			double fn = 0;
			
			HashSet<String>referencePairs = new HashSet<String>(readBoundaries(f.getAbsolutePath(),false));
			HashSet<String>responsePairs = new HashSet<String>(readBoundaries(response + f.getName().replace(reference_suffix, response_suffix),false));
			
			HashSet<String> copyResponse = new HashSet<String>(responsePairs);			
			copyResponse.retainAll(referencePairs);
			
			tp += copyResponse.size();
			fp += (responsePairs.size() - tp);
			
			HashSet<String> copyReference2 = new HashSet<String>(referencePairs);
			copyReference2.removeAll(responsePairs);
			fn += copyReference2.size();		
			
			TP += tp;
			FP += fp;
			FN += fn;
		}
		
		double precision = TP/(TP+FP);
		double recall = TP/(TP+FN);
		double fscore = ((recall+precision)==0)?0:2*precision*recall/(precision+recall);
		
		System.out.println("Precision: " + precision);
		System.out.println("Recall: " + recall);
		System.out.println("F-Score: " + fscore);
	}

	public ArrayList<String> readBoundaries(String f,boolean add)
	{
		ArrayList<String>pairs = new ArrayList<String>();
		
		try
		{
			CSVReader reader = new CSVReader(new FileReader(f));
			String[] nextLine;
			
			int count = 1;
			while((nextLine=reader.readNext())!=null)
			{
				if(add)
				{
					int end = Integer.parseInt(nextLine[1]);
					end += 1;
					nextLine[1] = "" + end; 
					
//					if(count>=3)
//					{
//						int start = Integer.parseInt(nextLine[0]);
//						start += (count-2);
//						nextLine[0] = "" + start;
//					}
				}
				
				pairs.add(nextLine[0] + "#" + nextLine[1]);
				count++;
			}
			
			reader.close();
		}
		catch(IOException ie)
		{
			System.err.println(ie.getMessage());
		}
		return pairs;
	}
}
