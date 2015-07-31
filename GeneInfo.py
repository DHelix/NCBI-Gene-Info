# Author: Dan Jin
# Version: 1.0
# Date: Nov. 08, 2013
# Function:
#	-Read a .txt file or csv file; or read a .xls file and convert it to a .csv file. 
#	-Automatically find gene's ID, full name, chromosome localization and function description based on gene symbol, and also include the web page link to that gene.
#	-Write the searching result into a new .txt file.
# Note: The first row (header) of "Homo_sapiens.gene_info.txt" used in this script was manually modified.
# Usage: python GeneInfo.py [inputFileName] [OutputFileName]


# import library
#import os
import sys
import csv
import re
import urllib


# Import Homo_sapiens.gene_info.txt
print "Importing Homo_sapiens.gene_info.txt..."
# read csv file
NCBIGeneInfo = list(csv.reader(open("Homo_sapiens.gene_info.txt",'rU'),delimiter='\t'))
print "Done importing Homo_sapiens.gene_info.txt\n"
#print basic info about the list: the number of records and the length of each record
#print "\nthe length of list: %d\n" %((len(NCBIGeneInfo))-1)
#print "the number of element in each record: %d\n" %(len(NCBIGeneInfo[0]))
#print the header
#print(NCBIGeneInfo[0])

# Get the number of column
for i in range(len(NCBIGeneInfo[0])):
	if NCBIGeneInfo[0][i]=='GeneID':
		GeneID=i
	if NCBIGeneInfo[0][i]=='Symbol':
		Symbol=i
	if NCBIGeneInfo[0][i]=='Synonyms':
		Synonym=i
	if NCBIGeneInfo[0][i]=='map_location':
		MapLoc=i
	if NCBIGeneInfo[0][i]=='description':
		Description=i


#inFileNameRaw="Gene List.txt"
		
# Ask for input and output file names.
if len(sys.argv[1:]) == 2:
	[inFileNameRaw,outFileName]=sys.argv[1:3]
elif len(sys.argv[1:]) == 1:
	inFileNameRaw = sys.argv[1]
	outFileName = 'Result.txt'
else:
	print "Need input and output file names."
	inFileNameRaw = str(raw_input("Please enter file names for reading from:"))
	if inFileNameRaw == '':	
		inFileNameRaw = "Gene List.txt"
	outFileName = str(raw_input("Please enter file names for writing into:"))
	if outFileName == '':
		outFileName = "Result.txt"
print "Opening", inFileNameRaw
		
		

# IF input file is a .txt file
# Check if input file is a .txt file
fileFormat=re.compile('[Tt][Xx][Tt]$')
if (re.search(fileFormat,inFileNameRaw)!=None):
	# read txt file
	inFile=list(csv.reader(open(inFileNameRaw,'rU'),delimiter='\n'))

# IF input file is a .csv or .xls file
# Check input file's format. if it is not a csv file, convert it to csv file using xls2csv function
fileFormatXls=re.compile('[Xx][Ll][Ss]$')
if (re.search(fileFormatXls,inFileNameRaw)!=None):
	inFileName=inFileNameRaw[:-4]+'.csv' # generate new input file name with .csv
	xls2csv.xls2csv(inFileNameRaw,inFileName) # Convert file to csv
	print "Done converting %s to %s!\n" %(inFileNameRaw,inFileName)
else:
	inFileName=inFileNameRaw

# read csv file
inFile=list(csv.reader(open(inFileName,'rU'),delimiter=','))
# print basic info about the list: the number of records and the length of each record
print "\nThe length of list: %d\n" %(len(inFile))


textFile = open(outFileName, "w")
print ("Start to write into "+outFileName+"\n")	

# Abstract each gene symbol from input file, get its GeneID, Synonyms, map location and description from "Homo_sapiens.gene_info.txt"
# Open online record by using: view-source:www.ncbi.nlm.nih.gov/gene/XXX (XXX = NCBI Gene ID). Find and copy its summary.
for sym in inFile:
	# inFile is a list! Have to convert each element to a string before comparing it with NCBIGeneInfo table. 
	symString=''.join(sym)
	# Search in NCBIGeneInfo table to find the corresponding record
	y=0
	for line in NCBIGeneInfo:
		if line[Symbol] == symString:
			y=1
			symGeneID=line[GeneID]
			symSynonym=line[Synonym]
			symMapLoc=line[MapLoc]
			symDescription=line[Description]
			
			print("Gene ID: " + symGeneID)
			print("Gene Symbol: " + symString)
			print("Full Name: " + symDescription)
			print("Synonyms: " + symSynonym)
			print("Chromosome Location: " + symMapLoc)
			
			textFile.write("Gene ID: " + symGeneID + "\n")
			textFile.write("Gene Symbol: " + symString + "\n")
			textFile.write("Full Name: " + symDescription + "\n")
			textFile.write("Synonyms: " + symSynonym + "\n")
			textFile.write("Chromosome Location: " + symMapLoc + "\n")
			
			# Get summary from NCBI website
			NCBIurl='http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id='+str(symGeneID)+'&retmode=xml'
			fbhandle = urllib.urlopen(NCBIurl)
			for line in fbhandle.readlines():
				if '<Item Name="Summary" Type="String">' in line:
					Summary=line.strip('\t')
					Summary=((re.compile('<Item Name="Summary" Type="String">(.*?)</Item>')).search(Summary)).group(1)
					print '\nSummary:', Summary
					textFile.write('\nSummary:'+Summary + "\n")
                        
			# print the NCBI url of the gene
			url='http://www.ncbi.nlm.nih.gov/gene/'+str(symGeneID)
			print("\nFor more info about this gene, please click here:\n" + url)
			textFile.write("\nFor more info about this gene, please see here:\n" + url + "\n")
			
			print("\n--------------------------------------\n")
			textFile.write("\n--------------------------------------\n\n")
			
	if y==0:
		    print 'No record found in "Homo_sapiens.gene_info.txt"\n'

textFile.close()
print ("All records were written in "+outFileName+"\n")
print "Program is done!"
