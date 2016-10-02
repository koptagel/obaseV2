
# Import required libraries
import requests
import numpy as np
import scipy.io as sio
from scipy.sparse import *

def generateCustomerMapping(filename,outfilename,fieldnames):
    
    # Read CustomerIndex - CustomerId pairs from file and store them in two lists; index and data.
    index = []
    data = []
    with open(filename) as inFile:
        for row, entry in enumerate(inFile, 0):
            index.append(int(row))
            data.append(int(entry))
    
    index = np.array(index)
    data = np.array(data)
            
    # Write CustomerIndex - CustomerId pairs to a txt file. 
    with open(outfilename, 'w') as outFile:
        #for i in range(len(fieldnames)):
        #    outFile.write('%s\t' % fieldnames[i])
        #outFile.write('\n')
        
        for i in range(len(index)):
            outFile.write('%d\t %d\n' % (index[i],data[i]))
            
            
def generateItemMapping(filename,filenameDs,outfilename,fieldnames):
    index = []
    itemId = []
    itemDs = []
    itemIdG3 = []
    itemDsG3 = []
    
    # Read ItemIndex - ItemId and ItemIndex - ItemDs pairs from files and store them in lists; index, itemId and ItemDs.
    with open(filename) as inFile:
        for row, entry in enumerate(inFile, 0):
            index.append(int(row))
            itemId.append(int(entry))
    
    with open(filenameDs) as inFile:
        for row, entry in enumerate(inFile, 0):
            itemDs.append(entry)

    index = np.array(index)
    itemId = np.array(itemId)
    
    # For each item, get UrunGrup3 information from api and store IdUrunGrup3 and DsUrunGrup3 values in lists; itemIdG3 and itemDsG3.
    num = 0
    num2 = 0
    for i in range(len(itemId)):
        r = requests.get('http://212.57.2.68:93/api/database/urun?$select=IdUrunGrup3&$filter=IdUrun+eq+%d' % itemId[i])
        tempId = r.json()
        
        if len(tempId) == 0 or tempId[0]['IdUrunGrup3'] is None:
            tempId = -1
            tempDs = 'Invalid Item'
            num = num+1
        else:
            tempId = int(tempId[0]['IdUrunGrup3'])

            r = requests.get('http://212.57.2.68:93/api/database/urungrup3?$select=DsUrunGrup3&$filter=IdUrunGrup3+eq+%d' % tempId)
            tempDs = r.json()

            if len(tempDs) == 0 or tempDs[0]['DsUrunGrup3'] is None:
                tempDs = 'Invalid Item'
                num2 = num2 + 1
            else:
                tempDs = tempDs[0]['DsUrunGrup3']
                
        itemIdG3.append(int(tempId))
        itemDsG3.append(tempDs)
        
    print('Number of Invalid Items: %d %d' %(num,num2))
    
    indexG3 = []
    visited = []

    for i in range(len(index)):
        temp = itemIdG3[i]
        
        if int(temp) == -1:
            indexG3.append(-1)
        else:
            if temp not in visited:
                visited.append(temp)

            idx = visited.index(temp)
            indexG3.append(idx)

    # Write ItemIndex, ItemId, ItemG3Index, ItemG3Id, ItemG3Ds and ItemDs values into file.
    with open(outfilename, 'w', encoding='utf-8') as outFile:
        #for i in range(len(fieldnames)):
        #    outFile.write('%s\t' % fieldnames[i])
        #outFile.write('\n')

        for i in range(len(index)):
            outFile.write('%d\t %d\t %d\t %d\t %s\t %s' % (index[i],itemId[i],indexG3[i],itemIdG3[i],itemDsG3[i],itemDs[i]))
            
            
def generateSalesTensor(filename,mappingfilename,outfilename,fieldnames):
    weekIndex = []
    dowIndex = []
    hourIndex = []
    itemIndex = []
    itemG3Index = []
    customerIndex = []
    amount = []

    itemMap = []
    with open(mappingfilename) as inFile2:
        for line2 in inFile2:
            values2 = line2.split('\t')
            itemMap.append(values2[2])    

    #itemMap = itemMap[1:]

    # Store sales records into corresponding lists.
    with open(filename) as inFile:
        for line in inFile:
            values = line.split('\t')

            weekIndex.append(values[0])
            dowIndex.append(values[1])
            hourIndex.append(values[2])
            itemIndex.append(values[3])

            itemG3Index.append(itemMap[int(values[3])])

            customerIndex.append(values[4])
            amount.append(values[5])

    # Write sales tensor into file. 
    with open(outfilename, 'w', encoding='utf-8') as outFile:
            #for i in range(len(fieldnames)):
            #    outFile.write('%s\t' % fieldnames[i])
            #outFile.write('\n')

            for i in range(len(weekIndex)):
                outFile.write('%s\t %s\t %s\t %s\t %s\t %s\t %s' % (weekIndex[i],dowIndex[i],hourIndex[i],itemIndex[i],itemG3Index[i],customerIndex[i],amount[i]))