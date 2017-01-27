import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.nio.CharBuffer;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Provide an interface to get information from an experiment
 * file. 
 * 
 * Use cases: getting specific files for graphing, getting experiment metadata, exporting individual files 
 */
public class ExperimentFileReader {
	private String path;
	private ArrayList<String> nodeNames;
	private int numberOfNodes;
	private final int MAX_NODE_NUM_LENGTH = 10;

	
	
	/**
	 * Creates ExperimentFile, file at path must follow correct format or IOException will be trown 
	 * 
	 * @param path absolute path to the experiment file
	 */
	ExperimentFileReader(String path) throws IOException
	{
		this.path = path;
		BufferedReader in = new BufferedReader(new FileReader(path));
		String experimentFileInfo = in.readLine();
		
		if(!isMetadataFormatCorrect(experimentFileInfo))
		{
			throw new IOException("Experiment files must start with an integer of length " + MAX_NODE_NUM_LENGTH + " or less then a space then one or more node names seperated by spaces then newline.");
		}
		numberOfNodes = extractNumOfNodes(experimentFileInfo);
		nodeNames = extractNodeNames(experimentFileInfo);
		
	}
	
	/**
	 * Given first line of experiment file determines of the correct file format is followed
	 * @param experimentInfo First line of file, no new line at end
	 * @return true if experimentInfo is formatted properly
	 */
	private boolean isMetadataFormatCorrect(String experimentInfo)
	{
		Pattern infoPattern = Pattern.compile("^\\d{1,10} {1}(?:\\w+ {1})*\\w+{1}$");
		Matcher infoMatcher = infoPattern.matcher(experimentInfo);
		return infoMatcher.matches();	
	}
	
	/**
	 * Given first line of experiment file returns the number of nodes in file
	 * @param experimentInfo First line of file, no new line at end
	 * @return number of nodes in file
	 */
	private int extractNumOfNodes(String experimentInfo)
	{
		Pattern dataPattern = Pattern.compile("^(\\d{1,10}) ");
		Matcher dataMatcher = dataPattern.matcher(experimentInfo);
		if(dataMatcher.find())
		{
			return Integer.parseInt( dataMatcher.group(1));
		}
		return -1;
	}
	
	/**
	 * Given first line of experiment file returns ArrayList<String> of node names
	 * @param experimentInfo First line of file, no new line at end
	 * @return ArrayList<String> of nodeNames in file
	 */
	static private ArrayList<String> extractNodeNames(String experimentInfo)
	{
		Pattern dataPattern = Pattern.compile(" {1}(\\w+)");
		Matcher dataMatcher = dataPattern.matcher(experimentInfo);
		ArrayList<String> nodeNames = new ArrayList();
		while(dataMatcher.find())
		{
			nodeNames.add(dataMatcher.group(1));
		}
		return nodeNames;
	}
	
	/**
	 * Takes string formatted: nodeName fileType length and returns logBinMetadata with info
	 * @param data line froma file formatted nodeName fileType length 
	 * @return
	 */
	static private LogBinMetadata extractBinAndLogMetadata(String data)
	{
		//TODO check file format
		//TODO what if fail
		String[] splitData = data.split("\\s");
		if(splitData.length >= 3 )
		{
			String nodeName = splitData[0];
			boolean isLogFile = splitData[1].equals( "log" );
			int fileLength = Integer.parseInt( splitData[2] );		
			return new LogBinMetadata(nodeName,isLogFile,fileLength);
			
		}
		return null;
	}
	
	/*
	 * 
	 */
	public static void findInFile(Reader r, FileLoction where)
	{
		
		
	}
	
	/**
	 * 
	 * Reads char by char into char buff until newline
	 * @param r reader 
	 * @param buff read line placed in buff starting from index 0, includes line data and newline
	 * @return length of data in char[]
	 * @throws IOException
	 */
	private static int readLine(Reader r, char[] buff) throws IOException //TODO: multiple newlines may cause issues
	{
		int i = 0;
		do//TODO: check char[] 
		{
			buff[i] = (char) r.read();
			i++;
		}while( !String.valueOf(buff[i-1]).matches("\\n"));
		return i;
	}

	/**
	 * Advances reader with experiment file open to the searched for location in the 
	 * file
	 * 
	 * @param r reader with file open
	 * @param nodeName name of node to search for files
	 * @param wantLogFile true to search for log file, false to search for bin file
	 * @throws IOException
	 */
	public static boolean findNodeFile(Reader r, String nodeName, boolean wantLogFile) throws IOException
	{
		char[] buff = new char[100];
		int length = readLine(r, buff);
		ArrayList a = extractNodeNames( String.copyValueOf(buff, 0, length-1) );
		
		//loop till the that is true then return successful
		//if never found return false
		length = readLine(r, buff);
		String logBinInfo  = String.copyValueOf(buff, 0, length);
		LogBinMetadata parsedData = extractBinAndLogMetadata(logBinInfo);		
		while (!parsedData.getName().equals(nodeName) || parsedData.isLogFile() != wantLogFile)
		{
			long j  = r.skip(parsedData.getFileLength());
			length = readLine(r, buff);
			logBinInfo  = String.copyValueOf(buff, 0, length);
			parsedData = extractBinAndLogMetadata(logBinInfo);
		}

		//check name and file type if not skip by chars
		return true;
	}
	
	/**
	 * Advances reader with experiment file open to the searched for location in the 
	 * file
	 * 
	 * @param r reader with file open
	 * @param nodeIndex index of node to search for files
	 * @param wantLogFile true to search for log file, false to search for bin file
	 * @throws IOException
	 */
	public static boolean findNodeFile(Reader r, int nodeIndex, boolean wantLogFile) throws IOException
	{
		char[] buff = new char[100];
		int length = readLine(r, buff);
		ArrayList a = extractNodeNames( String.copyValueOf(buff, 0, length-1) );
		
		//loop till the that is true then return successful
		//if never found return false
		length = readLine(r, buff);
		String logBinInfo  = String.copyValueOf(buff, 0, length);
		LogBinMetadata parsedData = extractBinAndLogMetadata(logBinInfo);	
		int i = 0;
		while (i != nodeIndex || parsedData.isLogFile() != wantLogFile)
		{
			long j  = r.skip(parsedData.getFileLength());
			length = readLine(r, buff);
			logBinInfo  = String.copyValueOf(buff, 0, length);
			parsedData = extractBinAndLogMetadata(logBinInfo);
			if(parsedData.isLogFile())
			{
				i++;
			}
		}

		//check name and file type if not skip by chars
		return true;
	}
	
	

	public String getPath() {
		return path;
	}
	public ArrayList<String> getNodeNames() {
		return nodeNames;
	}
	public int getNumberOfNodes() {
		return numberOfNodes;
	}
	
	
	/*
	 * Locations in experiment file that may be useful to advance to
	 */
	public enum FileLoction {
	    NODENAMES_BEGINING
	}
	
	
}


class LogBinMetadata
{
	private String name;
	private int fileLength;
	private boolean isLogFile;
	
	LogBinMetadata(String name, boolean isLogFile, int fileLength )
	{
		this.name = name;
		this.isLogFile = isLogFile;
		this.fileLength = fileLength;
	}
	
	public String getName() {
		return name;
	}

	public int getFileLength() {
		return fileLength;
	}

	public boolean isLogFile() {
		return isLogFile;
	}

	@Override
	public String toString() {
		return name + " " + fileLength + " " + isLogFile; 
	
	}

}



