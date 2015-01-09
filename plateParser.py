import os
import math
#import itertools
import numpy
#import xlwt
import csv
numpy.set_printoptions(threshold='nan')
from collections import OrderedDict
import subprocess
plate = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","B11","B12",
"C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","C11","C12","D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","D11","D12","E1","E2","E3","E4","E5",
"E6","E7","E8","E9","E10","E11","E12","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","G1","G2","G3","G4","G5","G6","G7","G8","G9","G10","G11","G12","H1",
"H2","H3","H4","H5","H6","H7","H8","H9","H10","H11","H12"]


###
###CHANGE DISCREPANCY BETWEEN NUMPLATES AND NUMPLATES 2
###FIGURE OUT WHAT TO DO IF BOTH PLATE REPEATS AND ASSAY REPEATS == 1 OR ONE OF THEM != 1
###


#name of output file
#out= str(os.environ["out"])
#print out
#out=out+".txt"
numPlates = 0
outFile = open("tempMat.txt","w")

#name of results file
#inf = str(os.environ["in"])
#inf = inf+".csv"

#inf = "test_13_10_3_14.csv"
#inf2 = "test_13_10_3_14"
inf2 = raw_input("please enter the file name, WITHOUT the .csv. Ex. results_1_3: \n")
inf = inf2 + ".csv"
book = open(inf,"r")

time = raw_input("Please enter the time per assay in seconds:\n")
time = int(time)
time = time/60.000


i = csv.reader(book, lineterminator = "\n")

def assayRepeats():
	book.seek(0)
	for row in i:
		try:
			#return row[0]
			if "Number of assay repeats" in row[0]:
					return row[4]
				
			else:
				continue
		except IndexError:
			pass
	book.seek(0)

def plateRepeats():
	book.seek(0)
	for row in i:
		try:
			#return row[0]
			if "Number of plate repeats" in row[0]:
					return row[4]
				
			else:
				continue
		except IndexError:
			pass
	book.seek(0)
#numReads = int(os.environ["numReads"])
numReads = int(assayRepeats())
numPlates2 = int(plateRepeats())
column = 1
first = 1
last = 1
#a = 0
a = []
b = []
def firstLine():
	book.seek(0)
	global column
	global a
	counter = 1
	global first
	
	for row in i:
		
		#print row
		
		
		if "Well" in row:
				#print x
			counter += 1
			
			first = counter
			a.append(counter)	
			column = [row.index(j) for j in row if "Meas" in j]	
			column = int(column[0])
				
		else:
		
			counter += 1
		#	except IndexError:
			#	first+=1
			
			#	pass
	#print first
	#print a
	print a
	return a

##WONT WORK IF ONLY 1 RUN, SINCE ONLY 1 "WELL", CANT TELL LAST LINE
#####################
def lastLine():	
	global last
	global b

	book.seek(0)
	for row in i:
		try:
			if "H12" in row[0]:

			#print last
				b.append(last)
				last +=1
				

			else:
			
				last += 1

		except IndexError:
			last += 1
			pass
	book.seek(0)
	#if points != 1:
	
	x = (numReads * points * numPlates2)
	init = x-1
	step = x
	b = b[init::step]
	return b
	##else:
	
	##	x = (numPlates)
	##	init = x-1
	##	step = x
	##	b = b[init::step]
	##	#c = []
	##	#c.append(b[-1])
	##	#print c
	##	return b
	
###########################################
##def lastLine():	
##	global last
##	global b

##	book.seek(0)
##	for row in i:
##		try:
##			if "H12" in row[0]:
##
##			#print last
##				b.append(last)
##				last +=1
##				
##
##			else:
##			
##				last += 1
##
##		except IndexError:
##			last += 1
##			pass
##	book.seek(0)
##	x = (numReads * points)
##	init = x-1
##	step = x
##	b = b[init::step]
##	return b

def numPoints():
	y = 1
	x = 1

	book.seek(0)
	for row in i:
		try:
			#return row[0]
			if "Number of horizontal points" in row[0]:
				x =  int(row[4])
			else:

				continue
				
		except IndexError:
			pass
	book.seek(0)
	for row in i:
		try:
			#return row[0]
			if "Number of vertical points" in row[0]:
				y =  int(row[4])
			else:
				
				continue
		except IndexError:
			pass
	book.seek(0)
	return x*y

points = int(numPoints())	






numPlates = len(a)
startlineArray = firstLine()
endlineArray = lastLine()
row = book.readlines()
def mainParser(first,last,numpoints,assays,outfile):
	global row
	value_list = []
	average_list= []
	a=[]
	global plate
	#range of rows with relevant data
	for x in xrange(first-1,last):
		#print first, last
		
	#add the second value of each row (data) to a list
		value_list.append(float(row[x].split(",")[column]))
	
	#takes every n (number of data points for a well for each read), appends them to a list, making a list of lists
	for x in xrange(0, len(value_list),points):
		a.append(value_list[x:x+points])

	arr = numpy.array(a)
	#print arr
	#averages every 25
	average_list = numpy.mean(arr,axis=1)
	average_array = numpy.array(average_list).reshape(assays,96)
	#print average_list
	#assays is the number of times each plate is read (how many time points)
	#convert back to list
	average_array_p = average_array.tolist()
	#first list is names of wells
	average_array_p.insert(0,plate)
	d = OrderedDict()
	for i in average_array_p[0]:
		d[i] = None
		#print d
		#q is list of key names
	q = []
	q = d.keys()
	#for each list in average_array_p, add them to a dictionary
	for i in average_array_p[1:]:
		for j in xrange(0,len(i)):
			if d[q[j]] == None:
		
				d[q[j]] = [i[j]]
			else:
				d[q[j]].append(i[j])
	for keys in d.keys():
		line = str(d[keys])
		line=line.replace("[","")
		line =line.replace("]","")
		outfile.write(line)
		outfile.write("\n")
	outfile.close()
	
	
	
#def create_directory(file):
#	os.getcwd()
#	d = os.path.dirname(file)
#	if not os.path.exists(d):
#		os.makedirs(d)
	
for x in xrange (0,len(startlineArray)):

	outfileName = "results_%s_%s.txt" % (inf2, x+1)
	#outFile_directory = "/results/%s" %(outfileName)
	#create_directory(outFile_directory)
	outfile = open(outfileName, "w")
	#print startlineArray[x], endlineArray[x], points, numReads,outfile
	if numReads !=1:
		mainParser(startlineArray[x], endlineArray[x], points, numReads,outfile)
		subprocess.call("Rscript plate_analysis_sh.R %s %i %i" %(outfileName, numReads, time), shell = True)
	else:
		mainParser(startlineArray[x], endlineArray[x], points, numPlates2,outfile)
		subprocess.call("Rscript plate_analysis_sh.R %s %i %i" %(outfileName, numPlates2, time), shell = True)
	print "created %s" % (outfileName)
	
	
book.close()