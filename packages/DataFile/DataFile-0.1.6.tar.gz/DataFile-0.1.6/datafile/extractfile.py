"""
ToDo:
dataFile:
  * Include separator search for guess
"""

import numpy
import types


class IndexationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class PartialDictionnary(dict):
    def __init__(self):
        #dict.__init__(self)
        """
        Dictionnary can return value for partial index

        """

    def load(self,index="",line="",separatorValues=""):
        self.loadIndex(index)
        self.loadValue(line,separatorValues)
        
    def loadIndex(self,index="",sep=None):
        self.index = index.split(sep)
        
        for points in self.index:

            self[points]= [ ]
            

        

    def loadValue(self,line="",separator=""):


        
        if separator == "":
            for i,points in enumerate(self.index):

                try:
                    self[points].append(float(line.split()[i]))
                except:
                    self[points].append(line.split()[i])
        else:
            for i,points in enumerate(self.index):
                try:
                    self[points].append(float(line.split(separator)[i]))
                except:
                    self[points].append(line.split(separator)[i])


    def numpys(self):

        for data in self.keys():
            if isinstance(self[data][0] ,types.StringType):
                pass
            else:
                self[data] = numpy.array(self[data],dtype=float)

    def keys(self):

        return self.index

    

    def __getitem__(self,a):


        if self.has_key(a):

            return dict.__getitem__(self,a)

        else:

            lf = [ k for k in self.keys() if a in k ]

            if len(lf) == 1:
                return dict.__getitem__(self,lf[0])
            elif len(lf) == 0:
                #Normal error value
                return dict.__getitem__(self,a)

            elif len(lf)>=2:
                

                r = """ """
                for l in lf:
                    r += """ "%s" """%l
                raise KeyError("""%s , possibles values: %s """ %(a,r) )

    def __setitem__(self,a,b):

        if isinstance(a,types.IntType):
            raise NameError("Digit keys not allowed")
        else:
            dict.__setitem__(self,a,b)

    

class dataFile(PartialDictionnary):
    def __init__(self,filename,index="guess",separator=None,quiet=False):
        PartialDictionnary.__init__(self)
        """
        Try to generate a smart dictionnary given a data file 
        index= "guess": will try to see if it can guess the different type
                of data of the file from the commentaries.
                if failed it will go to index = "auto"
                "auto": the index will be generated according the number of column on
                the file.
                ["IndexA","indexB",...], will index the file according to the list given
                object. 

        Example: 
        #Lx(nano) Ly(nano)
         1 2
         4 5
         8 4

         4 5
        
        A = dataFile(file)
        A["Lx"] , A["Lx(nano)"] , A["x"] will print the first column
        A["nano"] will return an error
        A["Lx",0] will return the first part of the column
                  a part is a group of points separated by one line or more
        A = dataFile(file,index="auto") will index with "0" and "1"        
        A = dataFile(file,index=["First","second"]) will index with "First" and "second"

        Remarque:
        guess will see if it found on the commentary(line beginnig with #)
        a line with the same number of word than the number of column
        it will read the commentary from the line closer to the data until the top
        of the file

        
        >>> Li = dataFile( "/home/jarbona/tmpAFM/PCE20_10005HeightRetrace.data",Origami)
        >>> len(Li.datas[0])
        22
        >>> Li.datas[0][0].keys()
        ['Angle', 'MappingEfficiency', 'Number', 'Surface', 'MeanHeight', 'MiniHeight', 'MaxiHeight', 'Lx', 'Ly']
        >>> Ll = dataFile( "/home/jarbona/tmpAFM/PCE20_10005HeightRetrace.data",index="guess")
        Guessed index : "N" "Lx(nm)" "Ly(nm)" "S(nm*nm)" "MeanHeight(nm)" "MiniHeight(nm)" "MaxiHeigth(nm)" "MappingEffieciency" "Angle" 
        """


        self.filename = filename
        self.index = index
        self.separator = separator
        self.quiet = quiet

        self.getDatas(filename=self.filename)
        self.treatDatas(index=self.index,separator=self.separator)
        self.numpys()

    def getDatas(self,filename):
        """
        separate the filename in rawdatas and metadatas
        get the lines of the sets in self.set
        """


        self.metadatas = {}
        self.rawdatas = {}

        with open(filename,'r') as data:

            self.set = [0]
            
            self.metadatas[0]=[]
            self.rawdatas[0]=[]

            setConsecutif = True
            indexSet = 0

            n = 0
            for line in data:

                
                if line[0] =="#":
                    self.metadatas[indexSet].append(line[1:])

                else:
                    if line.split() != []:
                        setConsecutif = False
                        self.rawdatas[indexSet].append(line)
                        n += 1
                    else:
                        if setConsecutif == False:
                            
                            self.set.append(n)
                            indexSet += 1
                            setConsecutif = True
                            
                            self.metadatas[ indexSet ] = []
                            self.rawdatas[ indexSet ] = []




        self.set.append(n)
        #TODO: clean the set


    def treatDatas(self,index,separator):


        self.index = ""

        
        n = len(self.rawdatas[0][0].split(separator))

        #Check that all lines have the sam number of points
        for set in self.rawdatas.keys():
            
            for l in self.rawdatas[set]:

                if n != len(l.split(separator)):

                    raise NameError("All lines don't have the same number of points")

        

        if index != "auto" and index != "guess":

            
            if  isinstance(index,types.ListType):
                                
                if n != len(index):
                    raise IndexationError("The index has a different length than the number of columns")
                
                self.index = " ".join(index)
                self.loadIndex(self.index)
                                        
            elif isinstance(index,types.StringType):
                
                if n != len(l.split(separator)):
                    raise IndexationError("The index has a different length than the number of columns")
                self.index = index
                self.loadIndex(self.index)
                

        
        if index == "guess"  and self.metadatas != {}:

            #Try to find in metadata a possible index in letters:
            
            

            self.metadatas[0].reverse()

            for sep in [";",",",None]:
                for l in self.metadatas[0]:


                    if len(l.split(sep)) == n:
                        #Indexion according to the array
                        self.index = l[:-1]

                        if sep is ";" or sep is ",":
                            #remove the withe spaces at the beginig or at the end
                            liste = l.split(sep)
                            L = [ " ".join(el.split()) for el in liste]

                            self.index = sep.join(L)
                        
                        self.loadIndex(self.index,sep)
                        if not self.quiet:
                            print "Guessed index : %s "%str(self.keys())
                        break


                if self.index != "":
                    break

            self.metadatas[0].reverse()





        if index == "auto" or self.index == "":

            l = ["%i"%i for i in range(n)]
            self.index = " ".join(l)
            self.loadIndex(self.index)

            if not self.quiet:
                print "Auto index : %s"%str(self.keys())




        if self.index != "": 
            for set in self.rawdatas.keys():
                for l in self.rawdatas[set]:
                    self.loadValue(l,separator=separator)


           
    def __getitem__(self,a):


        if isinstance(a,types.StringType):

            return PartialDictionnary.__getitem__(self,a)

        if isinstance(a,types.TupleType):
            
            if isinstance(a[0],types.StringType) is False or isinstance(a[1],types.IntType) is False :
                raise KeyError( "Usage: \"key\",index") 
            
            
            if a[1] <= len(self.set)-2:
                return PartialDictionnary.__getitem__(self,a[0])[ self.set[ a[1] ]: self.set[ a[1] + 1] ]

            else:
                raise  KeyError( "The index %i, is not valid" % a[1])
        
    


    
    
