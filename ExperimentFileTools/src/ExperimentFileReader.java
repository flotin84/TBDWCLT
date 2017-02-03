import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.nio.CharBuffer;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Provides an interface to get information from experiment
 * files. 
 * 
 * Instancing an ExperimentFileReader object provides methods of getting metadata from an experiment file.
 * 
 * Static methods advance an existing Reader,i.e BufferReader FileReader , that has an experiment file
 * open to the correct location to read from a specific log/bin file.
 * 
 * Use cases: getting specific files for graphing, getting metadata for DB , getting experiment metadata, exporting individual files 
 */
public class ExperimentFileReader {//TODO only work with long not int
	private String path;
	private ArrayList<String> nodeNames;
	private int numberOfNodes;
	private final int MAX_NODE_NUM_LENGTH = 10;

	
	
	/**
	 * Creates ExperimentFileReader, file at path must follow correct Experiment file format 
	 * or IOException will be thrown. When created all experiment metadata is read from the file and
	 * placed in accessible fields. 
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
	//	nodeNames = extractNodeNames(experimentFileInfo);
		
	}
	
	/**
	 * Given first line of experiment file determines of the correct file format is followed
	 * @param experimentInfo First line of file, no new line at end
	 * @return true if experimentInfo is formatted properly
	 */
	private static boolean isMetadataFormatCorrect(String experimentInfo)
	{
		Pattern infoPattern = Pattern.compile("^EXPTBD \\d{8}$");
		Matcher infoMatcher = infoPattern.matcher(experimentInfo);
		return infoMatcher.matches();	
	}
	
	/**
	 * Checks that nodeFileInfo matches (nodeName log/bin fileLength) format. This check
	 * allows for trailing whitespace characters but no leading ones.
	 * <p>Valid Example:node_1 log 9938 
	 * @param nodeFileInfo Log/bin file metadata line.
	 * @throws IOException Thrown if nodeFileInfo does not match file format.
	 */
	private static void verifyNodeMetadataFormat(String nodeFileInfo) throws IOException
	{
		Pattern infoPattern = Pattern.compile("^(\\d+) (\\w+) (\\w+) (\\d+)\\s*$");
		String  exceptionMessage = "Incorrect node metadata format: ";
		Matcher infoMatcher = infoPattern.matcher(nodeFileInfo);
		if(infoMatcher.matches())
		{
			System.out.println(infoMatcher.group(1));
			System.out.println(infoMatcher.group(2));
			System.out.println(infoMatcher.group(3));
			System.out.println(infoMatcher.group(4));
			if(infoMatcher.group(2).equals("log") || infoMatcher.group(2).equals("bin"))
			{
				if(infoMatcher.group(3).equals("master") || infoMatcher.group(3).equals("slave_"))
				{
					return;
				}
				else
				{
					exceptionMessage += "Expected " + infoMatcher.group(3) + " to equal master or slave_";
				}
			}
			else
			{
				exceptionMessage += "Expected " + infoMatcher.group(2) + " to equal log or bin.";
			}
			
			
		}else
		{
			exceptionMessage += "Expected " + nodeFileInfo + "to match nodeNum log/bin nodeType fileLength.";
		}
		
		throw new IOException(exceptionMessage);
	}
	
	/**
	 * Given first line of experiment file returns the number of nodes in file
	 * @param experimentInfo First line of file, no new line at end
	 * @return number of nodes in file
	 */
	private static int extractNumOfNodes(String experimentInfo)
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
	/*static private ArrayList<String> extractNodeNames(String experimentInfo)
	{
		Pattern dataPattern = Pattern.compile(" {1}(\\w+)");
		Matcher dataMatcher = dataPattern.matcher(experimentInfo);
		ArrayList<String> nodeNames = new ArrayList();
		while(dataMatcher.find())
		{
			nodeNames.add(dataMatcher.group(1));
		}
		return nodeNames;
	}*/
	
	/**
	 * Takes string formatted: nodeName fileType length and returns logBinMetadata with info
	 * @param data line froma file formatted nodeName fileType length 
	 * @return
	 * @throws IOException Thrown if node metadata format is incorrect.
	 */
	static private LogBinMetadata extractNodeMetadata(String data) throws IOException
	{
		verifyNodeMetadataFormat(data);
		//TODO what if fail
		String[] splitData = data.split("\\s");
		if(splitData.length >= 3 )
		{
			int nodeIndex = Integer.parseInt( splitData[0] );
			boolean isLogFile = splitData[1].equals( "log" );
			String nodeType = splitData[2];
			int fileLength = Integer.parseInt( splitData[3] );		
			return new LogBinMetadata(nodeIndex,isLogFile,nodeType,fileLength);
			
		}
		return null;
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
	 * Advances reader currently at the beginning of an experiment file to a specific location in the 
	 * file. The reader will be placed at the beginning of the desired log/bin file with
	 * the matching nodeName. 
	 * 
	 * @param r Reader at beginning of experiment file.
	 * @param nodeName Name of node as stored in the experiment file.
	 * @param wantLogFile True to search for log file, false to search for bin file.
	 * @throws IOException Thrown if file doesn't follow experiment file format, or reader experiences IO issues.
	 * @return True if reader is successfully advanced to log/bin file.
	 */
	/*public static boolean findNodeFile(Reader r, String nodeName, boolean wantLogFile) throws IOException
	{//TODO check for proper file format
		char[] buff = new char[100];
		int length = readLine(r, buff);
		ArrayList a = extractNodeNames( String.copyValueOf(buff, 0, length-1) );
		
		//loop till the that is true then return successful
		//if never found return false
		length = readLine(r, buff);
		String logBinInfo  = String.copyValueOf(buff, 0, length);
		LogBinMetadata parsedData = extractNodeMetadata(logBinInfo);		
		while (!parsedData.getName().equals(nodeName) || parsedData.isLogFile() != wantLogFile)
		{
			long j  = r.skip(parsedData.getFileLength());
			length = readLine(r, buff);
			logBinInfo  = String.copyValueOf(buff, 0, length);
			parsedData = extractNodeMetadata(logBinInfo);
		}
		//check name and file type if not skip by chars
		return true;//TODO make return meaningful
	}*/
	
	/**
	 * Advances a reader currently at the beginning of an experiment file to a specific 
	 * location in the file. The reader will be placed at the beginning of the log/bin file with
	 * the matching index.
	 * 
	 * @param r Reader at beginning of experiment file.
	 * @param nodeIndex index of node to search for files, index starts at 0.
	 * @param wantLogFile True to search for log file, false to search for bin file.
	 * @throws IOException Thrown if file doesn't follow experiment file format, or reader experiences IO issues.
	 * @return True if reader is successfully advanced to log/bin file.
	 */
	public static boolean findNodeFile(Reader r, int nodeIndex, boolean wantLogFile) throws IOException
	{
		char[] buff = new char[100];
		int length = readLine(r, buff);
		isMetadataFormatCorrect(String.copyValueOf(buff, 0, length));//Look to doing this more dynamically
		r.skip(2000/2);//2000 bytes / 2 bytes for UTF-16
		length = readLine(r, buff);
		
		String logBinInfo  = String.copyValueOf(buff, 0, length);
		System.out.print(String.copyValueOf(buff, 0, length));
		LogBinMetadata parsedData = extractNodeMetadata(logBinInfo);	
		int i = 0;
		while (parsedData.getNodeIndex() != nodeIndex || parsedData.isLogFile() != wantLogFile)
		{
			long j  = r.skip(parsedData.getFileLength());
			length = readLine(r, buff);
			logBinInfo  = String.copyValueOf(buff, 0, length);
			System.out.print(String.copyValueOf(buff, 0, length));
			parsedData = extractNodeMetadata(logBinInfo);
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
	/*public enum FileLoction {
	    NODENAMES_BEGINING
	}
	*/
	
}


class LogBinMetadata
{
	private int nodeIndex;
	private int fileLength;
	private boolean isLogFile;
	private String nodeType;
	
	LogBinMetadata(int nodeIndex, boolean isLogFile,String nodeType, int fileLength )
	{
		this.nodeIndex = nodeIndex;
		this.isLogFile = isLogFile;
		this.nodeType = nodeType;//TODO check for correct types
		this.fileLength = fileLength;
	}
	
	public int getNodeIndex() {
		return nodeIndex;
	}

	public String getNodeType() {
		return nodeType;
	}
	
	public int getFileLength() {
		return fileLength;
	}

	public boolean isLogFile() {
		return isLogFile;
	}

	@Override
	public String toString() {
		return nodeType + ", file length = " + fileLength + ", index = "+ nodeIndex + ", Is log file? " + isLogFile; 
	
	}

}





