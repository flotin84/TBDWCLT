import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

//Static methods that get file by path
//or
//instance experiment file then member calls

/**
 * Provide an interface to get information from an experiment
 * file. 
 */
public class ExperimentFile {
	private String path;
	private ArrayList<String> nodeNames;
	private int numberOfNodes;
	private final int MAX_NODE_NUM_LENGTH = 10;
	
	/**
	 * Creates ExperimentFile, file at path must follow correct format or IOException will be trown 
	 * 
	 * @param path absolute path to the experiment file
	 */
	ExperimentFile(String path) throws IOException
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
	private ArrayList<String> extractNodeNames(String experimentInfo)
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

	public String getPath() {
		return path;
	}
	public ArrayList<String> getNodeNames() {
		return nodeNames;
	}
	public int getNumberOfNodes() {
		return numberOfNodes;
	}
	
}


