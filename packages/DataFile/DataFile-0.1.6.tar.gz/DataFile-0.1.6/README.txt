=========
Data File
=========

This package provides an easy way to open a datafile
by returning a "modified" dictionnary (see Guessing) of numpy arrays that corresponds
to the differents columns.If the column contains strings it will return an array of strings.

By default it will try to guess the indexation from the commentaries, and if failed will index it 
from 0 to n::


		 #!/usr/bin/env python
		 
		 from datafile.extractfile import dataFile

		 f = dataFile("./datafile/test/testdocfile.txt")
		 # the index will be guessed and if not found it will
		 # be indexed from 0 to n
		 
		 f = dataFile("./datafile/test/testdocfile.txt",index="auto")
		 #f will be indexed from 0 to n
		 		 
		 #f["0"] will return a numpy array of the first column.
		 #f["0",1] will return a numpy array of the index number 1 of the first column,
		 # if the column is divided in index (ensemble of points separated by one or more space)

		 f = dataFile("./datafile/test/testdocfile.txt" , "A B C D")
		 #f will be indexed on "A" "B" "C" (if three columns)
		 f = dataFile("./datafile/test/testdocfile.txt" , ["A", "B","C","D"]
		 #f will be indexed on "A" "B" "C"


Guessing
========

if the datafile contains in the commentaries a line like:
#Lx(nm) Ly(nm) D(A)
and the file at three column, it will index the three columns
with "Lx(nm)" "Ly(nm)" , "D(A)"::
		 
		 #!/usr/bin/env python
		 f = dataFile("./file")
		 f["Lx"]
		 f["x"]
		 #both are going to return the first column
		 f["nm"]
		 #will return a key error	 


Main usage
==========

I use it with ipython to plot datas and explore them.
Lauching ipython -pylab will launch a ipython with
matplotlib loaded.
After loading the file with dataFile you can plot the data
with only typping plot(f["A"],f["B"])


email : jeanmichel.arbona@gmail.com		 




