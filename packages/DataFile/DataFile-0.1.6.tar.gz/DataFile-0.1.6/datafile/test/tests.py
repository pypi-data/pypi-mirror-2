import sys
import unittest
import os
import numpy
from datafile.extractfile import PartialDictionnary , dataFile ,IndexationError


class TestPartialDictionnary(unittest.TestCase):
    def setUp(self):
        self.D = PartialDictionnary()


    def test_load(self):
        self.D.load("A B C","1 2 3")
        k = self.D.keys()
        k.sort()
        self.assertEqual(k,["A","B","C"])
        self.assertEqual(self.D["A"],[1])


    def test_loadSeparatorValues(self):
        self.D.load("A B C","1,2,3",separatorValues=",")
        k = self.D.keys()
        k.sort()
        self.assertEqual(k,["A","B","C"])
        self.assertEqual(self.D["A"],[1])

    def test_loadString(self):
        self.D.load("A B C","1 n 3")
        k = self.D.keys()
        k.sort()
        self.assertEqual(k,["A","B","C"])
        self.assertEqual(self.D["B"],["n"])

    def test_partialGuess(self):
        self.D.load("Aa Bb Cc","1 2 3")
        self.assertEqual(self.D["A"],[1])
        self.assertEqual(self.D["a"],[1])

    def test_errorValue(self):
        self.D.load("Aa Bb Cc","1 2 3")
        self.assertRaises(KeyError,self.D.__getitem__,"v")

    def test_error2Value(self):
        self.D.load("Aa Ba Cc","1 2 3")
        self.assertRaises(KeyError,self.D.__getitem__,"a")

    def test_NumKeys(self):
        self.assertRaises(NameError,self.D.__setitem__,11,"11")



class TestDataFile(unittest.TestCase):
    
    def setUp(self):

        self.name1 = os.path.abspath(os.path.split(sys.argv[0])[0])+os.path.sep+"testdocfile.txt"
        self.dataFile = dataFile(self.name1)


    def test_GuessReading(self):
        Data = dataFile(self.name1)
        k = Data.keys()
        k.sort()
        self.assertEqual(k,["Aad","Bbd","Cc","DE"])


    def test_AutoReading(self):
        Data = dataFile(self.name1,index="auto")
        k = Data.keys()
        k.sort()
        self.assertEqual(k,["0","1","2","3"])


    def test_Guessing(self):
        
        self.assertEqual(numpy.any(self.dataFile["Aad"]-self.dataFile["ad"]),False)

    def test_ErrorGuessing(self):

        self.assertRaises(KeyError,self.dataFile.__getitem__,"d")

    def test_index(self):

        self.assertEqual(numpy.any(self.dataFile["Bbd"]-numpy.array([2,4,8,16])),False )
        self.assertEqual(numpy.any(self.dataFile["Bbd",0]-numpy.array([2,4,8])),False )
        self.assertEqual(numpy.any(self.dataFile["Bbd",1]-numpy.array([16])), False)
        self.assertEqual(self.dataFile["DE"],['iu', 'oi', 'pp', 'nn'])
        self.assertEqual(self.dataFile["DE",1],['nn'])
        self.assertRaises(KeyError,self.dataFile.__getitem__,("Bdb",2))


    def test_indexation(self):

        Data = dataFile(self.name1,index="A B C D")
        k = Data.keys()
        k.sort()
        self.assertEqual(k,["A","B","C","D"]) 


        Data = dataFile(self.name1,index=["A","B","C","D"])
        k = Data.keys()
        k.sort()
        self.assertEqual(k,["A","B","C","D"])

    def test_ErrorIndexation(self):

        #dataFile(self.name1,["A","B","C","D"])
        self.assertRaises(IndexationError,dataFile,self.name1,index=["A","B","C","D","E"] )

        

if __name__ == '__main__':



    unittest.main()

    
    
