import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.commons.io.FileUtils;
import org.apache.commons.lang3.StringUtils;

import au.com.bytecode.opencsv.CSVWriter;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;

public class StanfordSegmenter 
{
	StanfordCoreNLP pipeline;
	
	public StanfordSegmenter()
	{
		Properties props = new Properties();
	    props.setProperty("annotators", "tokenize, ssplit");
	    pipeline = new StanfordCoreNLP(props);
	}

	public static void main(String[] args) 
	{
        String dataPath, outPath;
        if (args.length < 2) {
            System.out.println("Missing required arguments specifying input/output directories");
        } else {
            dataPath = args[0];
            outPath = args[1];
		
            StanfordSegmenter stanfordSeg = new StanfordSegmenter();
            stanfordSeg.segmentAll(dataPath,outPath);
        }
	}

	private void segmentAll(String dataPath, String outPath) 
	{
		File dir = new File(dataPath);
        File[] allFiles = dir.listFiles();

		try 
		{
			for(File f : allFiles)
			{
                if (!f.isDirectory()) {
				System.out.println("=== Processing file: " + f.getName() + " ===");
				ArrayList<String[]> refs = processFile(f);
								
				CSVWriter writer = new CSVWriter(new FileWriter(outPath + f.getName().replace(".txt", ".csv")));
				writer.writeAll(refs);
				writer.close();
                }
			}			
		} 
		catch (IOException e) 
		{			
			e.printStackTrace();
		}	
	}

	private ArrayList<String[]> processFile(File f) throws IOException 
	{		
		String allText = FileUtils.readFileToString(f);
		Annotation document = new Annotation(allText);
		pipeline.annotate(document);
		
		List<CoreMap>sentences = document.get(SentencesAnnotation.class);
		
		List<String> sentenceList = new ArrayList<>();		
		
		for (CoreMap sentence : sentences) 
		{		   
		   String sentenceString = Sentence.listToOriginalTextString(sentence.get(TokensAnnotation.class));
		   sentenceList.add(sentenceString);
		}

		//----
		int sum = 0;
		int i=0;
		for(String sent : sentenceList)
		{
			if(i!=0)
				sent = StringUtils.stripStart(sent, null);
			
			sum+=sent.length();
			i++;
		}
		
		//-----
		
		int start = 0;
		int end = 0;
		
		ArrayList<String[]> responses = new ArrayList<>();
		
		int j=0;
		for(String sent : sentenceList)
		{
			if(j!=0)
				sent = StringUtils.stripStart(sent, null);
						
			end = start + sent.length();
			String[] record = new String[2];
			record[0] = "" + start;
			record[1] = "" + end;
			
			//System.out.println("Start: " + start + " End: " + end);
			
			String extract = allText.substring(start, end);
			if(!extract.equals(sent))
			{
				System.err.println("Mismatch");
				System.err.println("== Extract:" + extract);
				System.err.println("== Segment:" + sent);
				System.exit(1);
			}
			
			responses.add(record);
			start = start + sent.length();
			j++;
		}
		
		return responses;
	}

}
