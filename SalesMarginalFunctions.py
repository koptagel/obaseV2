
import numpy as np
from scipy.sparse import *
import sqlite3
import matplotlib.pyplot as plt

import DatabaseInfoFunctions

def getSalesMatrixOfCustomerFromMarginals(db_name, customerIndex, desiredFields, plotCriteria, shapes):

    tableName = "MarginalSalesTensor_Customer%s%s" % (desiredFields[0][:-5], desiredFields[1][:-5])
    
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    sqlQuery = "SELECT %s, %s, Amount FROM %s WHERE CustomerIndex=%d" % (desiredFields[0], desiredFields[1], tableName, customerIndex)
    cur.execute(sqlQuery)

    row = []
    col = []
    data = []
    for values in cur:
        if values[0] != -1 and values[1] != -1:
            row.append(values[0])
            col.append(values[1])
            data.append(values[2])
    
    if plotCriteria == 'binary':
        data = np.ones(len(row))
    else:
        data = np.array(data) 
        
    salesMatrix = csr_matrix( (data,(row,col)), shape=(shapes[0],shapes[1]) )

    conn.close()
    
    return salesMatrix


def getCustomerSalesFromMarginals(DB_NAME, customerIndex, criteria, ax1, ax2, TimePoints, TimePointsY):
    dimensions = ["WeekIndex", "DowIndex", "HourIndex", "ItemG3Index", "WeblogMatrix", "WeblogGraph", "TimeSlots"]
    labels = ["Week", "Day Of Week", "Hour", "Item Group", "Weblog Matrix", "Weblog Graph", "Time Slots"]
    
    DATABASE_SHAPE = DatabaseInfoFunctions.getDatabaseShape(DB_NAME)
    shapes = [DATABASE_SHAPE[0], DATABASE_SHAPE[1], DATABASE_SHAPE[2], DATABASE_SHAPE[4], -1, -1, DATABASE_SHAPE[2]] 
    
    desiredFields = [dimensions[ax1], dimensions[ax2]]
    desiredShapes = [shapes[ax1], shapes[ax2]]
    desiredLabels = [labels[ax1], labels[ax2]]   
    
    if criteria ==1:
        plotCriteria = 'sum'
    else:
        plotCriteria = 'binary'
    
    if ax1 in [0,1,2,3] and ax2 in [0,1,2,3]:
        if ax1 != ax2:   
            salesMatrix = getSalesMatrixOfCustomerFromMarginals(DB_NAME, customerIndex, desiredFields, plotCriteria, desiredShapes)
        else: 
            salesMatrix = getSalesHistogramOfCustomer(DB_NAME, customerIndex, desiredFields[0], plotCriteria, desiredShapes[0])     
    elif ax1 == 6 or ax2 == 6:
        salesMatrix = getSalesSlotMatrixOfCustomer(DB_NAME, customerIndex, desiredFields, plotCriteria, desiredShapes, TimePoints, TimePointsY)
    
    return salesMatrix

def getSalesMatrixOfCustomerFromMarginalMats(dataDict, customerIndex, plotCriteria):
    salesMatrix = dataDict[str(customerIndex)]
    
    if plotCriteria == 'binary':
        salesMatrix[salesMatrix>0]=1
    
    return salesMatrix

def getSalesHistogramOfCustomerFromMarginalMats(dataDict, customerIndex, ax1, plotCriteria):
    tempMatrix = dataDict[str(customerIndex)].toarray()
    
    if ax1 < 3:
        salesMatrix = np.sum(tempMatrix, axis=1)
    else:
        salesMatrix = np.sum(tempMatrix, axis=0)
        
    if plotCriteria == 'binary':
        salesMatrix[salesMatrix>0]=1
    
    return csr_matrix(salesMatrix)

def getSalesSlotMatrixOfCustomerFromMarginalMats(dataDict, customerIndex, ax1, ax2, plotCriteria, TimePoints, TimePointsY):
    salesMatrix = dataDict[str(customerIndex)]
    
    isChanged = False

    salesMatrix = salesMatrix.toarray()

    if salesMatrix.shape[0] == 24:
        salesMatrix = salesMatrix.T
        isChanged = True

    newMatrix = np.zeros((salesMatrix.shape[0],1))

    for i in range(len(TimePoints)):
        ranges = salesMatrix[:,TimePoints[i]:TimePointsY[i]]
        sumRanges = np.sum(ranges,axis=1,keepdims=True)
        newMatrix = np.hstack((newMatrix,sumRanges))

    if isChanged:
        newMatrix = newMatrix.T
        newMatrix = newMatrix[1:,:]  
    else:
        newMatrix = newMatrix[:,1:]
        
    if plotCriteria == 'binary':
        newMatrix[np.where(newMatrix>0)]=1
    
    return csr_matrix(newMatrix)


def getCustomerSalesFromMarginalMats(dataDict, customerIndex, criteria, ax1,ax2, TimePoints, TimePointsY):
    if criteria ==1:
        plotCriteria = 'sum'
    else:
        plotCriteria = 'binary'
    
    # Select corresponding method according to the given axes 
    if ax1 in [0,1,2,3] and ax2 in [0,1,2,3]:
        if ax1 != ax2:   
            salesMatrix = getSalesMatrixOfCustomerFromMarginalMats(dataDict, customerIndex, plotCriteria)
        else: 
            salesMatrix = getSalesHistogramOfCustomerFromMarginalMats(dataDict, customerIndex, ax1, plotCriteria)     
    elif ax1 == 6 or ax2 == 6:
        salesMatrix = getSalesSlotMatrixOfCustomerFromMarginalMats(dataDict, customerIndex, ax1, ax2, plotCriteria, TimePoints, TimePointsY)
    
    return salesMatrix