# Code designed and written by: Almiqdad Elzein
# Andrew ID: aelzein
# file created: November 6th, 2016

# Modification history:
# Start           Finish
# 6/11  8:30am    6/11   11:20am
# 7/11  2:10pm    7/11   4:05pm
# 7/11  7:25pm    7/11   9:00pm
# 9/11  8:30pm    9/11   10:20pm
# 10/11 7:30am    10/11  10:00am
# 11/11 1:30pm    11/11  5:20pm
# 12/11 11:20am   12/11  1:30pm
# 13/11 6:30pm    13/11  9:20pm
# 15/11 5:20pm    15/11  6:00pm
# 18/11 8:20am    18/11  11:00am
# 21/11 7:00am    21/11  9:00am
# 22/11  7:10pm   22/11  9:30pm
# 23/11  12:00pm  23/11  3:00pm
# 23/11  6:00pm   23/11  9:00pm
# 25/11  2:20pm   25/11  4:00pm

###############################################################################
from ImageWriter import*
from Tkinter import*
from ImageTk import*
###############################################################################

# define the combinations of blackPixels corresponding to each digit
zero = [0.551,0.537,0.576,0.516]
one = [0.452,0.470,0.391,0.625]
two = [0.700,0.285,0.548,0.430]
three = [0.684,0.363,0.346,0.746]
four = [0.677,0.282,0.437,0.690]
five = [0.398,0.704,0.306,0.694]
six = [0.377,0.576,0.601,0.608]
seven = [0.800,0.353,0.407,0.353]
eight = [0.668,0.605,0.666,0.681]
nine = [0.571,0.600,0.378,0.653]
D = [0.526,0.615,0.607,0.527]

#define operations
addition = [0.421,0.346,0.426,0.501]
subtraction = [0.813,0.875,0.860,0.936]
multiplication = [0.583,0.473,0.512,0.647]
division = [0.632,0.087,0.622,0.111]




#this function checks wheather or not there is some black in a given column         
def blackInCol(pic,col):
    #get number of rows in the picture
    rows = getHeight(pic)
    #search through all pixels in the given column,if you find a black pixel,
    #return True        
    for r in range(rows):
        if getColor(pic,col,r)==[0,0,0]:
                return True
    #if you are done searching and there is no black pixel in that Column, return
    #False            
    return False


#This function returns the next column which has some black in it after a given
#column
def nextColWithBlack(pic,col):
    #get number of columns in the picture
    columns = getWidth(pic)
    #search every column starting from the given column, if you find a column with
    #some black, return that column
    for c in range(col,columns):
        if blackInCol(pic,c) == True:
            return c
    #Otherwise, return None
    return None
    



#this function finds the the next row with black in it after a given row and
#between 2 columns
def nextrowWithBlack(pic,startrow,startcol,endcol):
    #search the pixels of every row starting from the starting row    
    for r in range(startrow,getHeight(pic)):
        for c in range(startcol,endcol):
            #when you encounter the first black pixel, return the row that this pixel is
            #found in
             if getColor(pic,c,r)==[0,0,0]:
                return r
            
            


#this function returns the column of the first black pixel in a given
#row and inbetween 2 given columns
def firstBlackinrow(pic,row,startcol,endcol):
    #search through every pixel in the given row    
    for c in range(startcol,endcol):
        #when you encounter the first black pixel, return the column that this pixel is
        #found in                   
        if getColor(pic,c,row)==[0,0,0]:
                return c



#this function converts a colored image to a  black and White image
def convertBlackWhite(pic):
    #get number of rows    
    rows=getHeight(pic)
    #get number of columns    
    columns=getWidth(pic)
    #go through each pixel in the image and find its R.G.B values.
    #if the average of these values is greater than or equal to 100, convert
    #that pixel to white. Otherwse, convert it to black    
    for i in range(0,rows):
        for j in range(0,columns):
            c=getColor(pic,j,i)
            if sum(c)/3>=100:
                setColor(pic,j,i,[255,255,255])
                
            else:
                setColor(pic,j,i,[0,0,0])


#this function finds the start and end rows of the biggest blob inbetween 2
#columns
def horizontalSegmentation(pic,startcol,endcol):
    #get number of rows of the picture
    rows=getHeight(pic)
    #create a list of the sizes of all blobs
    BlobSizes=[]
    #craete a list with the start and endpoint of blobs
    BlobsStartEnd=[]
    #starting from row zero
    row=0
    #while there are still rows with black in the do the following:    
    while nextrowWithBlack(pic,row,startcol,endcol)!=None:
        #assign the next row that has black in it (which could also be the row am currently at) to the variable start         
        row=nextrowWithBlack(pic,row,startcol,endcol)
        #append the start of the blob to the list of starts and ends of blobs        
        BlobsStartEnd.append(row)
        #initiate a counter for the length of the blobs        
        lengthOfBlob=0
        #variable t for breaking second while loop    
        t=None        
        #while the value of row is greater than or equal to the number of rows in the picture:        
        while row<=rows and t!=-1:
            #if there are some black pixels in the current row,add one to the length of the blob            
            if firstBlackinrow(pic,row,startcol,endcol)!=None:
                 lengthOfBlob=lengthOfBlob+1
            #Otherwise,set t equal to -1, which breaks this loop                 
            else:
                t=-1    
            #move to the next row                
            row=row+1
        #add the size of the blob you just counted to the list that contains the sizes of all the blobs           
        BlobSizes.append(lengthOfBlob)
        #we should add the endpoint of the blob we just counted. This however will not
        #be the value of the variable row,but row-2. this is because the value of row
        #increases twice after we found the last row with black in it. it will
        #increase by one to reach the row that has NO black in it, and increase by 1
        #when we set the variable t to the value that'll break the loop
        BlobsStartEnd.append(row-2)
    #find the index of the largest blob size in the blobsizes list        
    BiggestBlobSize=max(BlobSizes)         
    index=BlobSizes.index(BiggestBlobSize)
    #if there is more than one blob,return that it's an equal sign
    if len(BlobSizes) == 2:
        return 'equal sign'
    #the start and end points of that blob are given by the formulas
    #startRow=2*index and EndRow=2*index+1
    return [BlobsStartEnd[2*index],BlobsStartEnd[2*index+1]] 


#this function returns the start and end columns of the first character whose
#starting column is after a given column
def verticalSegmentation(pic,col):
    #if there's no column with black in it after the given columns, return None
    if nextColWithBlack(pic,col) == None:
        return None
    #get number of columns in the picture
    columns=getWidth(pic)
    #initiate founstart as False    
    foundStart=False
    #initiate founEnd as False     
    foundEnd=False
    #initiate a variable that'll store the starting point of the character
    start=0
    #initiate a variable that'll store the ending point of the character
    end=0
    #initiate an indicator of wheather the width of the character is less than 5
    #pixels since if the width is less than 5, it's probably NOT a character
    lessThanFive=False
    #go from the given column to the last column. keep going as long as the start
    #column(the first column with some black in it) isn't found yet
    while lessThanFive==False:
        foundStart=False
        foundEnd=False
        while col<columns and foundStart==False:
            if blackInCol(pic,col)==False:
                col=col+1
            #when you find the first column with some black, mark it as the start and
            #set foundStart to True            
            else:
                foundStart=True
                start=col
#after we have found the starting column:
        #go from that starting column to the last column. keep going unless you find
        #a column with no black in it
        while col<columns and foundEnd==False:        
            if blackInCol(pic,col)==True:
                col=col+1
            #if you find a column that doesn't have black in it, the end column of the
            #digit will be the column before that column.Also, if the last column in the
            #picture is the end column, the function should return that last column            
            else:
                foundEnd=True
                end=col-1
        #if the width is graeter than 5 braek the first loop                
        if end-start>5:
            lessThanFive=True
    #return the start and end column of the digit                        
    return [start,end]


#this function returns the ratio of black pixels to total pixels of each
#of the 4 quadrant of the region bounded by 2 given rows and 2 given columns
def findpercentages(pic,startrow,endrow,startcol,endcol):
    #find the midpoint btween start and end column
    midCol=startcol+((endcol-startcol)/2)
    #find the midpoint btween start and end row
    midRow=startrow+((endrow-startrow)/2)
    #initiate a counter for the total number of pixels in a quadrant
    pixels=0
    #initiate a list that'll include the percentage in the 4 quadrants
    quadPercents=[0,0,0,0]
    #initiate a counter for the total number of black pixels in a quadrant
    blackPixels=0   
    #go through the first quadrant and count both the total number of
    #pixels and the number of black pixels
    for r in range(startrow,midRow):
        for c in range(startcol,midCol):
            #if the pixel is black,add one to both the pixel counter and the black
            #pixel counter
            if getColor(pic,c,r)==[0,0,0]:
                pixels=pixels+1
                blackPixels=blackPixels+1
            #if the pixel is white,add one to the pixel counter only
            elif getColor(pic,c,r)==[255,255,255]:
                pixels=pixels+1           
    #find the ratio of black pixels in the second quadrant        
    quadPercents[1]=1.0*blackPixels/pixels

    #reset pixels' and black pixels' count to zero
    pixels=0
    blackPixels=0     
    #go through the first quadrant and count both the total number of
    #pixels and the number of black pixels
    for r in range(startrow,midRow):
        for c in range(midCol,endcol):
            #if the pixel is black,add one to both the pixel counter and the black
            #pixel counter
            if getColor(pic,c,r)==[0,0,0]:
                pixels=pixels+1
                blackPixels=blackPixels+1
            #if the pixel is white,add one to the pixel counter only
            elif getColor(pic,c,r)==[255,255,255]:
                pixels=pixels+1
    #find the ratio of black pixels to total pixels in the first quadrant 
    quadPercents[0]=1.0*blackPixels/pixels


    #reset pixels' and black pixels' count to zero
    pixels=0
    blackPixels=0     
    #go through the third quadrant and count both the total number of
    #pixels and the number of black pixels
    for r in range(midRow,endrow):
        for c in range(startcol,midCol):
            #if the pixel is black,add one to both the pixel counter and the black
            #pixel counter
            if getColor(pic,c,r)==[0,0,0]:
                pixels=pixels+1
                blackPixels=blackPixels+1
            #if the pixel is white,add one to the pixel counter only
            elif getColor(pic,c,r)==[255,255,255]:
                pixels=pixels+1
    #find the percentage of black pixels in the third quadrant
    quadPercents[2]=1.0*blackPixels/pixels


    #reset pixels' and black pixels' count to zero
    pixels=0
    blackPixels=0     
    #go through the fourth quadrant and count both the total number of
    #pixels and the number of black pixels
    for r in range(midRow,endrow):
        for c in range(midCol,endcol):
            #if the pixel is black,add one to both the pixel counter and the black
            #pixel counter
            if getColor(pic,c,r)==[0,0,0]:
                pixels=pixels+1
                blackPixels=blackPixels+1
            #if the pixel is white,add one to the pixel counter only
            elif getColor(pic,c,r)==[255,255,255]:
                pixels=pixels+1
    #find the ratio of black pixels to total pixels in the fourth quadrant
    quadPercents[3]=1.0*blackPixels/pixels
    #return the list of the ratios of the 4 quadrants
    return quadPercents


#this function takes a list of black pixel percentages in each quadrant and
#returns the corresponding character
def decode(perc):
    
    #find the total difference between the input combination and each of the characters' percentage combination
    differencewithZero = [abs(1.0*perc[0]-zero[0])/4,abs(1.0*perc[1]-zero[1])/4,abs(1.0*perc[2]-zero[2])/4,abs(1.0*perc[3]-zero[3])/4]
    differencewithZero = sum(differencewithZero)
    
    differencewithOne = [abs(1.0*perc[0]-one[0])/4,abs(1.0*perc[1]-one[1])/4,abs(1.0*perc[2]-one[2])/4,abs(1.0*perc[3]-one[3])/4]
    differencewithOne = sum(differencewithOne)

    differencewithTwo = [abs(1.0*perc[0]-two[0])/4,abs(1.0*perc[1]-two[1])/4,abs(1.0*perc[2]-two[2])/4,abs(1.0*perc[3]-two[3])/4]
    differencewithTwo = sum(differencewithTwo)

    differencewithThree = [abs(1.0*perc[0]-three[0])/4,abs(1.0*perc[1]-three[1])/4,abs(1.0*perc[2]-three[2])/4,abs(1.0*perc[3]-three[3])/4]
    differencewithThree = sum(differencewithThree)

    differencewithFour = [abs(1.0*perc[0]-four[0])/4,abs(1.0*perc[1]-four[1])/4,abs(1.0*perc[2]-four[2])/4,abs(1.0*perc[3]-four[3])/4]
    differencewithFour = sum(differencewithFour)

    differencewithFive = [abs(1.0*perc[0]-five[0])/4,abs(1.0*perc[1]-five[1])/4,abs(1.0*perc[2]-five[2])/4,abs(1.0*perc[3]-five[3])/4]
    differencewithFive = sum(differencewithFive)

    differencewithSix = [abs(1.0*perc[0]-six[0])/4,abs(1.0*perc[1]-six[1])/4,abs(1.0*perc[2]-six[2])/4,abs(1.0*perc[3]-six[3])/4]
    differencewithSix = sum(differencewithSix)

    differencewithSeven = [abs(1.0*perc[0]-seven[0])/4,abs(1.0*perc[1]-seven[1])/4,abs(1.0*perc[2]-seven[2])/4,abs(1.0*perc[3]-seven[3])/4]
    differencewithSeven = sum(differencewithSeven)

    differencewithEight = [abs(1.0*perc[0]-eight[0])/4,abs(1.0*perc[1]-eight[1])/4,abs(1.0*perc[2]-eight[2])/4,abs(1.0*perc[3]-eight[3])/4]
    differencewithEight = sum(differencewithEight)

    differencewithNine = [abs(1.0*perc[0]-nine[0])/4,abs(1.0*perc[1]-nine[1])/4,abs(1.0*perc[2]-nine[2])/4,abs(1.0*perc[3]-nine[3])/4]
    differencewithNine = sum(differencewithNine)


    differencewithAdd = [abs(1.0*perc[0]-addition[0])/4,abs(1.0*perc[1]-addition[1])/4,abs(1.0*perc[2]-addition[2])/4,abs(1.0*perc[3]-addition[3])/4]
    differencewithAdd = sum(differencewithAdd)

    differencewithSub = [abs(1.0*perc[0]-subtraction[0])/4,abs(1.0*perc[1]-subtraction[1])/4,abs(1.0*perc[2]-subtraction[2])/4,abs(1.0*perc[3]-subtraction[3])/4]
    differencewithSub = sum(differencewithSub)

    differencewithMult = [abs(1.0*perc[0]-multiplication[0])/4,abs(1.0*perc[1]-multiplication[1])/4,abs(1.0*perc[2]-multiplication[2])/4,abs(1.0*perc[3]-multiplication[3])/4]
    differencewithMult = sum(differencewithMult)

    differencewithDiv = [abs(1.0*perc[0]-division[0])/4,abs(1.0*perc[1]-division[1])/4,abs(1.0*perc[2]-division[2])/4,abs(1.0*perc[3]-division[3])/4]
    differencewithDiv = sum(differencewithDiv)

    
    differencewithD = [abs(1.0*perc[0]-D[0])/4,abs(1.0*perc[1]-D[1])/4,abs(1.0*perc[2]-D[2])/4,abs(1.0*perc[3]-D[3])/4]
    differencewithD = sum(differencewithD)

    #put all differences in a list
    differences = [differencewithZero,differencewithOne,differencewithTwo,differencewithThree,differencewithFour,differencewithFive,differencewithSix,differencewithSeven,differencewithEight,differencewithNine,differencewithAdd,differencewithSub,differencewithMult,differencewithDiv,differencewithD]

    #find the minimum difference
    minDifference = min(differences)

    #return the character that most closely represents the input combination of black percentage combination
    if minDifference == differencewithZero:
        return '0'
    if minDifference == differencewithOne:
        return '1'
    if minDifference == differencewithTwo:
        return '2'
    if minDifference == differencewithThree:
        return '3'
    if minDifference == differencewithFour:
        return '4'
    if minDifference == differencewithFive:
        return '5'
    if minDifference == differencewithSix:
        return '6'
    if minDifference == differencewithSeven:
        return '7'
    if minDifference == differencewithEight:
        return '8'
    if minDifference == differencewithNine:
        return '9'

        
    if minDifference == differencewithAdd:
        return '+'
    if minDifference == differencewithSub:
        return '-'
    if minDifference == differencewithMult:
        return '*'
    if minDifference == differencewithDiv:
        return '/'
    if minDifference == differencewithD:
        return 'D'





#this function takes a picture with an equation in it and returns that equation
def getEquationstring(pic):
    #find number of columns in the pictures
    width = getWidth(pic)
    #initiate a string to contain the equation
    equation = ''
    #make image black and white
    convertBlackWhite(pic)
    #initiate a counter for the columns
    col =0
    #docode each sequence of black pixels in the picture and add it to
    #the equation string
    while col<width and verticalSegmentation(pic,col)!=None:
        #find the start and end columns of the character
        startcol = verticalSegmentation(pic,col)[0]
        endcol =  verticalSegmentation(pic,col)[1]
        #if you identify an equal sign, add it to the equation string
        if horizontalSegmentation(pic,startcol,endcol) == 'equal sign':
            equation = equation+'='
        else:
            #find the start and end rows of the character
            startRow = horizontalSegmentation(pic,startcol,endcol)[0]
            endRow = horizontalSegmentation(pic,startcol,endcol)[1]
            #find the combination of ratios of black pixels to total pixels in each quadrant
            perc = findpercentages(pic,startRow,endRow,startcol,endcol)
            #use the percentages to decode that character
            character = decode(perc)
            #add that character to the equation string
            equation = equation+character
        col = endcol+1
    #return the equation string
    return equation



#this function takes a string and flips it
def flip(string):
    #initialize a strig to contain flipped version of the argument
    flipped=''
    #go through each character, starting from the end and put in in
    #the result string
    for i in range(len(string)):
        flipped = flipped+string[len(string)-1-i]
    #return the result string
    return flipped
    
#This function finds the number after a specified index
def numAfter(index,string):
    #define possible digits
    digits = ['0','1','2','3','4','5','6','7','8','9','.','/','*']
    #initialize string to contain the resulting number
    number = ''
    #get the portion of the string am interested in 
    subString = string[index+1:]
    #go from the index to the end of the string
    for i in range(len(subString)):
        #if you find a digit, add it to number string
        if subString[i] in digits:
            number = number+subString[i]
        #if you find something that's not a digit, return whatever is in the number
        #string
        else:
            return number
    return number
    
    
#This function finds the number after a specified index
def numBefore(index,string):
    #define possible digits
    digits = ['0','1','2','3','4','5','6','7','8','9','.','/','*']
    #initialize string to contain the result
    number = ''
    #get the portion of the string am interested in 
    subString = string[:index]
    #go from the given index,backwords
    for i in range(len(subString)):
        #if you find a digit, add it to number string
        if subString[len(subString)-i-1] in digits:
            number = number+subString[len(subString)-i-1]
        #if you find something that's not a digit, return whatever is in the number string, flipped    
        else:
            return flip(number) 
    return flip(number)



#This function takes a string  that's an equation and solves the equation
def solveEquation(string):
    #define a list of all digits
    digits = ['0','1','2','3','4','5','6','7','8','9']
    #define a list of the possible operations in the string
    operations = ['+','-','=']
    #get the index of the equal sign
    equalIndex = string.index('=')
    #initiate a list of all D-terms
    Dterms = []
    #initialize a list of all integers
    integers = []
    #go through the left side of the equation
    for i in range(0,equalIndex):
        #if you're at index zero
        if i == 0:
            #if you have a '-' check what follows it
            if string[i] == '-':
                #if it's followed by a D, add '-D' to the Dtrems
                if string[i+1] == 'D':
                    Dterms.append('-D')
                #if it's followed by a number, check if there is a 'D' after that number
                elif string[i+1] in digits:
                    number = string[i+1]+numAfter(i+1,string)
                    evnumber = str(eval('1.0*'+string[i+1]+numAfter(i+1,string)))
                    #if there is, add the term to the Dterms with a '-' sign before it
                    if string[i+1+len(number)] == 'D':
                        Dterms.append('-'+evnumber+'D')
                    #otherwise, add the number to integers
                    elif string[i+1+len(number)] in operations:
                        number = string[i+1]+numAfter(i+1,string)
                        evnumber = str(eval('1.0*'+string[i+1]+numAfter(i+1,string)))
                        integers.append(evnumber)                
            #if you find a D, add 'D' to Dterms
            if string[i] == 'D':
                Dterms.append('D')
            #if you find a Digit check the full number
            if string[i] in digits:
                number = string[i]+numAfter(i,string)
                evnumber = str(eval('1.0*'+string[i]+numAfter(i,string)))
                #if the number is followed by an operation, add the number to integers
                if string[i+len(number)] in operations:
                    integers.append('-'+evnumber)
                #if the number is followed by a 'D', add it to Dterms
                elif string[i+len(number)] == 'D':
                    Dterms.append(evnumber+'D')
        #if you're are in an index that's not zero
        else:
            #if you have a plus or minus sign, check if the term after it is an integer or a D-term
            if string[i] == '+' or string[i] == '-':
                #if there is a 'D', add the D to the Dterms with the appropriete sign
                if string[i+1] == 'D':
                    if string[i] == '-':
                        Dterms.append('-D')
                    else:
                        Dterms.append('D')
                #if there is a digit, find the number and check if the number has a 'D' after it or a plus or minus
                if string[i+1] in digits:
                    number = string[i+1]+ numAfter(i+1,string)
                    evnumber = str(eval('1.0*'+string[i+1]+ numAfter(i+1,string)))
                    #if there is a 'D' after the number, add the term to the Dterms
                    if string[i+1+len(number)] == 'D':
                        if string[i] == '+':
                            Dterms.append(evnumber+'D')
                        else:
                            Dterms.append('-'+evnumber+'D')
                    #if there is an operation after the number,add the term to integers
                    if string[i+1+len(number)] in operations:
                        if string[i] == '+':
                            integers.append('-'+evnumber)
                        else:
                            integers.append(evnumber)
    #go through the right side of the equation
    for i in range(equalIndex+1,len(string)):
        #if you're at index right after the equal
        if i == equalIndex+1:
            #if you have a '-' check what follows it
            if string[i] == '-':
                #if it's followed by a D, add 'D' to the Dtrems
                if string[i+1] == 'D':
                    Dterms.append('D')
                #if it's followed by a number, check if there is a 'D' after that number
                elif string[i+1] in digits:
                    number = string[i+1]+numAfter(i+1,string)
                    evnumber = str(eval('1.0*'+string[i+1]+numAfter(i+1,string)))
                    #if there is, add the term to the Dterms
                    if string[i+1+len(number)] == 'D':
                        Dterms.append(evnumber+'D')
                    #otherwise, add the number to integers with a minus sign
                    elif string[i+1+len(number)] in operations:
                        number = string[i+1]+numAfter(i+1,string)
                        evnumber = str(eval('1.0*'+string[i+1]+numAfter(i+1,string)))
                        integers.append('-'+evnumber)                
            #if you find a D, add '-D' to Dterms
            if string[i] == 'D':
                Dterms.append('-D')
            #if you find a Digit check the full number
            if string[i] in digits:
                number = string[i]+numAfter(i,string)
                evnumber = str(eval('1.0*'+string[i]+numAfter(i,string)))
                #if the number is the last number in the string, add it to the integers
                if i+len(number)>(len(string)-1):
                    integers.append(str(eval('1.0*'+number)))
                else:
                    #if the number is followed by an operation, add the number to integers
                    if string[i+len(number)] in operations:
                        integers.append(evnumber)
                    #if the number is followed by a 'D', add it to Dterms
                    elif string[i+len(number)] == 'D':
                        Dterms.append('-'+evnumber+'D')
        #if you're are in an index that's not zero
        else:
            #if you have a plus or minus sign, check if the term after it is an integer or a D-term
            if string[i] == '+' or string[i] == '-':
                #if there is a 'D', add the D to the Dterms with the appropriete sign
                if string[i+1] == 'D':
                    if string[i] == '+':
                        Dterms.append('-D')
                    else:
                        Dterms.append('D')
                #if there is a digit, find the number and check if the number has a 'D' after it or a plus or minus
                if string[i+1] in digits:
                    number = string[i+1]+ numAfter(i+1,string)
                    evnumber = str(eval('1.0*'+string[i+1]+ numAfter(i+1,string)))
                    #if the number is the last thing in the string, add it to the integers list
                    if (i+1+len(number))>(len(string)-1):
                        if string[i] == '+':
                            integers.append(evnumber)
                        else:
                            integers.append('-'+evnumber)
                    else:
                        evnumber = str(eval('1.0*'+string[i+1]+ numAfter(i+1,string)))
                        #if there is a 'D' after the number, add the term to the Dterms
                        if string[i+1+len(number)] == 'D':
                            if string[i] == '-':
                                Dterms.append(evnumber+'D')
                            else:
                                Dterms.append('-'+evnumber+'D')
                        #if there is an operation after the number,add the term to integers
                        if string[i+1+len(number)] in operations:
                            if string[i] == '-':
                                integers.append('-'+evnumber)
                            else:
                                integers.append(evnumber)
    
        
                                 
    #initiate a sum for the integers and the D coefficients
    intsum = 0
    coffsum = 0
    #sum the integers and Dterms' coefficiennts
    for integer in integers:
        intsum = intsum+float(integer)
    for term in Dterms:
        if len(term[:term.index('D')]) == 0:
            coffsum = coffsum+1
        else:
            if term[:term.index('D')] == '-':
                coffsum = coffsum - 1
            else:
                number = float(term[:term.index('D')])
                coffsum = coffsum+number
    #if the sum of coefficients is zero, return 'no solution'
    if coffsum == 0:
        return 'No Solution'
    #divide the sum of integers by the sum of Dterms
    result = 1.0*intsum/coffsum
    #return the result
    return str(result)

#this function takes the name of an image file with an equation in it and
#returns the solution of that equation
def SolvePic(filename):
    #load the picture
    pic = loadPicture(filename)
    #show the picture
    showPicture(pic)
    #get the equation in the picture
    equation = getEquationstring(pic)
    #solve that equation
    result = solveEquation(equation)
    #return the result
    return result



#this function gets the filename of the target picture, solves the equation, and
#displays it to the user
def getAndSolve():
    #define some globals
    global filename
    global resultLabel 
    #get the filename from the filename entry
    equationFile = filename.get()
    filename.delete(0,END)
    #solve the equation
    solution = SolvePic(equationFile)
    #display the solution of the equation
    resultLabel.configure(text = 'Solution:'+'\n'+'\n'+'\n D ='+'   '+solution) 
    


    

    




#create a user-interface window
window = Tk()
window.geometry('660x700')
window.title('Equation Solver')


#create a canvas
c= Canvas(window,width = 660, height = 700,bg='grey')
c.pack()


#create an entry for the file name
filename = Entry(window)
filename.place(x=240,y=200)


#create a button that solves the equation that allows the program to solve the equation
solveButton = Button(window,text='Solve',font='Verdana 9 bold',fg='black',bg="white",command = getAndSolve)
solveButton.place(x=390,y=200)


#create some labels on the canvas
welcomeLabel = Label(window,text ='Enter a picture of an arithmatic equation with one unknow here, and it will be solved!,Make'+'\n'+' sure your unknown is " D"\n'+'\n'+'\n'+'enter the file name here:',font='Verdana 9 bold',fg='black',bg="grey")
welcomeLabel.place(x=0,y=120)


#create a label for the result
resultLabel = Label(window,text ='Solution:'+'\n'+'\n'+'\n D =',font='Verdana 9 bold',fg='black',bg="grey")
resultLabel.place(x=260,y=230)


window.mainloop()  
