import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Set;

import org.apache.commons.io.FileUtils;

import com.aliasi.chunk.Chunk;
import com.aliasi.chunk.Chunking;
import com.aliasi.sentences.MedlineSentenceModel;
import com.aliasi.sentences.IndoEuropeanSentenceModel;
import com.aliasi.sentences.SentenceChunker;
import com.aliasi.sentences.SentenceModel;
import com.aliasi.tokenizer.IndoEuropeanTokenizerFactory;
import com.aliasi.tokenizer.TokenizerFactory;

import au.com.bytecode.opencsv.CSVWriter;

public class LingPipeSegmenter 
{
	static final TokenizerFactory TOKENIZER_FACTORY = IndoEuropeanTokenizerFactory.INSTANCE;
	static SentenceModel SENTENCE_MODEL;
	static SentenceChunker SENTENCE_CHUNKER;

	public static void main(String[] args) 
	{
        String dataPath, outPath, model;
        if (args.length < 3) {
            System.out.println("Missing required arguments specifying input/output directories and model");
        } else {
            dataPath = args[0];
            outPath = args[1];
            model = args[2];

            if (model.equals("me")) {
                SENTENCE_MODEL = new MedlineSentenceModel();
            } else if (model.equals("ie")) {
                SENTENCE_MODEL = new IndoEuropeanSentenceModel();
            }
            SENTENCE_CHUNKER = new SentenceChunker(TOKENIZER_FACTORY, SENTENCE_MODEL);

            LingPipeSegmenter lpSegmenter = new LingPipeSegmenter();
            lpSegmenter.segmentAll(dataPath,outPath);
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
                if (f.isFile()) {
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

		Chunking chunking = SENTENCE_CHUNKER.chunk(allText.toCharArray(),0,allText.length());
		Set<Chunk> sentences = chunking.chunkSet();
		if (sentences.size() < 1) 
		{
			System.out.println("No sentence chunks found.");
			//System.exit(1);
		}
		
		String slice = chunking.charSequence().toString();
		
		int sum = 0;
		ArrayList<String[]> responses = new ArrayList<>();
		for (Iterator<Chunk> it = sentences.iterator(); it.hasNext(); ) 
		{
			Chunk sentence = it.next();
			int start = sentence.start();
			int end = sentence.end();
			String sent = slice.substring(start,end);
			
			String extract = allText.substring(start, end);
			if(!extract.equals(sent))
			{
				System.err.println("Mismatch");
				System.err.println("Response: " + sent);
				System.err.println("Extract : " + extract);
				System.exit(1);
			}
			
			String[] record = new String[2];
			record[0] = "" + start;
			record[1] = "" + end;
			responses.add(record);
			sum += sent.length();			
		}
		
		//System.out.println("Lingpipe sum = " + sum);
		//System.out.println("String length = " + allText.length());

		return responses;
	}

}
