
import numpy as np
from scipy.sparse import *
import sqlite3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import DatabaseInfoFunctions

def getSalesMatrixOfCustomer(db_name, customerIndex, desiredFields, plotCriteria, shapes):
    # Marginalise Sales Tensor
    temp = ""
    for i in range(len(desiredFields)):
        temp = temp + ", %s" % desiredFields[i]
    temp = temp[1:]
    sqlQuery = "SELECT " + temp + ", SUM(Amount) FROM SalesTensor WHERE CustomerIndex=%d GROUP BY " %customerIndex + temp 

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(sqlQuery)

    # Store xAxis, yAxis and corresponding values of the sales matrix into lists; row, col and data.
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
        
    #row = np.array(row)
    #col = np.array(col)    
    
    salesMatrix = csr_matrix( (data,(row,col)), shape=(shapes[0],shapes[1]) )

    conn.close()
    
    return salesMatrix


def getSalesSlotMatrixOfCustomer(db_name, customerIndex, desiredFields, plotCriteria, shapes, TimePoints, TimePointsY):
    # Change Time Slot axis to Hour axis. Then, marginalise Sales Tensor. 
    temp = ""
    for i in range(len(desiredFields)):
        if desiredFields[i] == "TimeSlots":
            temp = temp + ", HourIndex" 
        else:
            temp = temp + ", %s" % desiredFields[i]
    temp = temp[1:]
    sqlQuery = "SELECT " + temp + ", SUM(Amount) FROM SalesTensor WHERE CustomerIndex=%d GROUP BY " %customerIndex + temp 

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(sqlQuery)

    # Store xAxis, yAxis and corresponding values of the sales matrix into lists; row, col and data.
    row = []
    col = []
    data = []
    for values in cur:
        if values[0] != -1 and values[1] != -1:
            row.append(values[0])
            col.append(values[1])
            data.append(values[2])
        
    row = np.array(row)
    col = np.array(col)    
    
    salesMatrix = csr_matrix( (data,(row,col)), shape=(shapes[0],shapes[1]) )

    conn.close()
    
    
    # Collapse the matrix to achieve time slots
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

def getSalesHistogramOfCustomer(db_name, customerIndex, desiredField, plotCriteria, shape1):
    # Marginalise Sales Tensor
    sqlQuery = "SELECT " + desiredField + ", SUM(Amount) FROM SalesTensor WHERE CustomerIndex=%d GROUP BY " %customerIndex + desiredField
    
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(sqlQuery)

    # Store xAxis, yAxis and corresponding values of the sales matrix into lists; row, col and data.
    row = []
    col = []
    data = []
    for values in cur:
        if values[0] != -1:
            row.append(0)
            col.append(values[0])
            data.append(values[1])
        
    if plotCriteria == 'binary':
        data = np.ones(len(row))
    else:
        data = np.array(data) 
        
    row = np.array(row)
    col = np.array(col)
    
    salesMatrix = csr_matrix( (data,(row,col)), shape=(1,shape1) )

    conn.close()
    
    return salesMatrix

def getCustomerSales(DB_NAME, customerIndex, criteria, ax1, ax2, TimePoints, TimePointsY):
    dimensions = ["WeekIndex", "DowIndex", "HourIndex", "ItemG3Index", "WeblogMatrix", "WeblogGraph", "TimeSlots"]
    labels = ["Week", "Day Of Week", "Hour", "Item Group", "Weblog Matrix", "Weblog Graph", "Time Slots"]
    #shapes = [81, 7, 24, 180, -1, -1, 24]
    DATABASE_SHAPE = DatabaseInfoFunctions.getDatabaseShape(DB_NAME)
    shapes = [DATABASE_SHAPE[0], DATABASE_SHAPE[1], DATABASE_SHAPE[2], DATABASE_SHAPE[4], -1, -1, DATABASE_SHAPE[2]] 
    
    desiredFields = [dimensions[ax1], dimensions[ax2]]
    desiredShapes = [shapes[ax1], shapes[ax2]]
    desiredLabels = [labels[ax1], labels[ax2]]   
    
    if criteria ==1:
        plotCriteria = 'sum'
    else:
        plotCriteria = 'binary'
    
    # Based on the given axis values, 
    if ax1 in [0,1,2,3] and ax2 in [0,1,2,3]:
        if ax1 != ax2:   
            salesMatrix = getSalesMatrixOfCustomer(DB_NAME, customerIndex, desiredFields, plotCriteria, desiredShapes)
        else: 
            salesMatrix = getSalesHistogramOfCustomer(DB_NAME, customerIndex, desiredFields[0], plotCriteria, desiredShapes[0])     
    elif ax1 == 6 or ax2 == 6:
        salesMatrix = getSalesSlotMatrixOfCustomer(DB_NAME, customerIndex, desiredFields, plotCriteria, desiredShapes, TimePoints, TimePointsY)
    
    return salesMatrix


def getCustomerSalesMap(DB_NAME, customerIndex, plotTitle, criteria, ax1, ax2, TimePoints, TimePointsY):
    salesMatrix = getCustomerSales(DB_NAME, customerIndex, criteria, ax1, ax2, TimePoints, TimePointsY)
    
    dimensions = ["WeekIndex", "DowIndex", "HourIndex", "ItemG3Index", "WeblogMatrix", "WeblogGraph", "TimeSlots"]
    labels = ["Week", "Day Of Week", "Hour", "Item Group", "Weblog Matrix", "Weblog Graph", "Time Slots"]
    
    desiredFields = [dimensions[ax1], dimensions[ax2]]
    desiredLabels = [labels[ax1], labels[ax2]]   
    
    
    fig = plt.figure(num=None, figsize=(6,8), dpi=80, facecolor='w', edgecolor='k')
    if ax1 != ax2:
        plt.imshow(salesMatrix.toarray().T, aspect='auto', interpolation='nearest', vmin=0)
        plt.ylabel(desiredLabels[1])
    else:
        plt.bar(np.arange(salesMatrix.shape[1]), salesMatrix.toarray()[0,:])
    
    plt.xlabel(desiredLabels[0])
    plt.title(plotTitle)
    plt.show()
        
        
def getSalesMatrix(db_name, criteria, shapes):
    #Criteria 0=count, 1=sum, 2=binary
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    if criteria == 0:
        c.execute("SELECT CustomerIndex, ItemG3Index, COUNT(ItemG3Index) FROM SalesTensor GROUP BY CustomerIndex, ItemG3Index")
    else:
        c.execute("SELECT CustomerIndex, ItemG3Index, SUM(Amount) FROM SalesTensor GROUP BY CustomerIndex, ItemG3Index")

    row = []
    col = []
    data = []

    for values in c:
        if values[1] != -1:
            row.append(values[0])
            col.append(values[1])
            data.append(values[2])

    row = np.array(row)
    col = np.array(col)    
    if criteria == 2:
        data = np.ones(len(row))

    salesMatrix = csr_matrix( (data,(row,col)), shape=(shapes[0],shapes[1]) )
    conn.close()

    return salesMatrix


def getSalesMatrixWithoutG3(db_name, criteria, shapes):
    #Criteria 0=count, 1=sum, 2=binary
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    if criteria == 0:
        c.execute("SELECT CustomerIndex, ItemIndex, COUNT(ItemIndex) FROM SalesTensor GROUP BY CustomerIndex, ItemIndex")
    else:
        c.execute("SELECT CustomerIndex, ItemIndex, SUM(Amount) FROM SalesTensor GROUP BY CustomerIndex, ItemIndex")

    row = []
    col = []
    data = []

    for values in c:
        if values[1] != -1:
            row.append(values[0])
            col.append(values[1])
            data.append(values[2])

    row = np.array(row)
    col = np.array(col)    
    if criteria == 2:
        data = np.ones(len(row))

    salesMatrix = csr_matrix( (data,(row,col)), shape=(shapes[0],shapes[1]) )
    conn.close()

    return salesMatrix


def getSalesEstimationG3OfCustomer(db_name, customerIndex, criteria, shape1):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    tableName = "SalesEstimationG3_%d" % criteria
    sqlQuery = "SELECT ItemG3Index, Amount FROM %s WHERE CustomerIndex=%d " % (tableName, customerIndex)
    cur.execute(sqlQuery)

    row = []
    col = []
    data = []

    for values in cur:
        row.append(0)
        col.append(values[0])
        data.append(values[1])

    row = np.array(row)
    col = np.array(col)

    salesMatrixEst = csr_matrix( (data,(row,col)), shape=(1,shape1) )

    conn.close()
    
    return salesMatrixEst


def getSalesEstimationOfCustomer(db_name, customerIndex, criteria, shape1):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    tableName = "SalesEstimation_%d" % criteria
    sqlQuery = "SELECT ItemIndex, Amount FROM %s WHERE CustomerIndex=%d " % (tableName, customerIndex)
    cur.execute(sqlQuery)

    row = []
    col = []
    data = []

    for values in cur:
        #print(values)
        row.append(0)
        col.append(values[0])
        data.append(values[1])

    row = np.array(row)
    col = np.array(col)

    salesMatrixEst = csr_matrix( (data,(row,col)), shape=(1,shape1) )

    conn.close()
    
    return salesMatrixEst