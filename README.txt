plateParser (ALPHA) README		Basel M. Al-Barghouthi     
11/12/14

Introduction:

plateParser takes plate reader data, in the form of a CSV file, and outputs a text file of the data for each plate. Currently, plateParser
only works for data in in the "list" export format. This can be specified in the plate reader before exporting the data. Also, because I 
have not encountered all data formats, it might not work if the main data is not in columns B or C, if the list header doesn't contain the word "Meas",
and if one of either "number of assay repeats" and "number of plate repeats" is not equal to 1. It will work, however, for single and multiplate formats
that are like the attached sample. Currently also only works with 96-well plates

plateParser is written in Python v.2.7 and R. You MUST have Python 2.7, Numpy(http://www.scipy.org/scipylib/download.html)
and R installed for this to work.

HOW TO USE:

1- Drag the file you wish to parse into the same directory as plateParser.py, plate_analysis_sh.R, and settings.txt. For instructional purposes, test_13.csv is included.

2- Settings.txt contains the indices of the BLANK plates, which will be averaged and subtracted as background. The indices are in the following
format: 1 = A1, 2 = A2, 13 = B1, etc... 
Please make sure you input all the appropriate indices before you run the script. Please make sure they are comma-separated with no 
spaces, tabs, or newline characters. ex.(1,2,3,4,67,88,56,77), but without the parentheses.

3- Open your terminal and navigate to the directory, then run the Python script. If the files are in the folder "plateParser" on your desktop, you would navigate to
it in the following manner (on Mac OSX):
		cd Desktop
		cd plateParser
		sudo python plateParser.py
		
sudo is required because, since plateParser will create folders on your machine, it needs admin access. If it prompts you for your password, please enter it.
plateParser will then ask you for the same of the file, without .csv. In this case, it would be "test_13" (without quotes).

plateParser will then ask for the length of the assay (time between plate reads). For this sample, please enter 2300.

Please disregard the terminal output. This will be removed in later versions.

plateParser should produce the following files:

results_test_13_1.txt
results_test_13_2.txt
results_test_13_3.txt
results_test_13_4.txt
results_test_13_5.txt

These contain raw data, where each "results" file contains the raw data for each plate.


tempMat.txt

This is a temporary file. Please disregard or delete.

The following folders should be produced:


results_test_13_1
results_test_13_2
results_test_13_3
results_test_13_4
results_test_13_5

Each folder represents data from a plate, and will contain a "FITS" text file with the slope values for each well, and a PDF file with graphs of every graphable well. 

