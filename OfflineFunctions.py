
import numpy as np
from scipy.sparse import *
from sklearn.decomposition import NMF
import sqlite3
import scipy.io as sio

import SalesFunctions
import MappingFunctions
import DatabaseInfoFunctions

def generateRecommendationsG3(db_name, criteria):
    DATABASE_SHAPE = DatabaseInfoFunctions.getDatabaseShape(db_name)
    shapes = [DATABASE_SHAPE[5], DATABASE_SHAPE[4]] 

    # criteria 0 count, 1 sum, 2 binary
    salesMatrix = SalesFunctions.getSalesMatrix(db_name, criteria, shapes)
    
    model = NMF(n_components=20, init='nndsvd', random_state=2)
    W = model.fit_transform(salesMatrix) 
    H = model.components_
    salesMatrixEst = np.dot(W,H)
    
    return salesMatrixEst

def updateSalesEstimationG3Table(db_name, criteria, salesMatrixEst):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    tableName = "SalesEstimationG3_%d" % criteria 

    sqlQuery = "DROP TABLE IF EXISTS %s" % tableName
    cur.execute(sqlQuery)

    sqlQuery = "CREATE TABLE %s (CustomerIndex INT, ItemG3Index INT, Amount REAL)" % tableName
    cur.execute(sqlQuery)

    for i in range(salesMatrixEst.shape[0]):
        for j in range(salesMatrixEst.shape[1]):
            sqlQuery = "INSERT INTO %s VALUES (%d, %d, %.2f)" % (tableName, i, j, salesMatrixEst[i,j])
            cur.execute(sqlQuery)

    conn.commit()
    conn.close()
    
def updateRecommendationsG3(db_name, criteria):
    salesMatrixEst = generateRecommendationsG3(db_name, criteria)
    updateSalesEstimationG3Table(db_name, criteria, salesMatrixEst)
    
    
def generateRecommendations(db_name, criteria):
    DATABASE_SHAPE = DatabaseInfoFunctions.getDatabaseShape(db_name)
    shapes = [DATABASE_SHAPE[5], DATABASE_SHAPE[3]] 
    
    # criteria 0 count, 1 sum, 2 binary
    salesMatrix = SalesFunctions.getSalesMatrixWithoutG3(db_name, criteria, shapes)
    
    model = NMF(n_components=20, init='nndsvd', random_state=2)
    W = model.fit_transform(salesMatrix) 
    H = model.components_
    salesMatrixEst = np.dot(W,H)
    
    return salesMatrixEst

def updateSalesEstimationTable(db_name, criteria, salesMatrixEst):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    tableName = "SalesEstimation_%d" % criteria 

    sqlQuery = "DROP TABLE IF EXISTS %s" % tableName
    cur.execute(sqlQuery)

    sqlQuery = "CREATE TABLE %s (CustomerIndex INT, ItemIndex INT, Amount REAL)" % tableName
    cur.execute(sqlQuery)

    for i in range(salesMatrixEst.shape[0]):
        for j in range(salesMatrixEst.shape[1]):
            sqlQuery = "INSERT INTO %s VALUES (%d, %d, %.2f)" % (tableName, i, j, salesMatrixEst[i,j])
            cur.execute(sqlQuery)

    conn.commit()
    conn.close()
    
    
def updateSalesEstimationTableWithThreshold(db_name, criteria, salesMatrixEst, threshold):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    tableName = "SalesEstimation_%d" % criteria 

    sqlQuery = "DROP TABLE IF EXISTS %s" % tableName
    cur.execute(sqlQuery)

    sqlQuery = "CREATE TABLE %s (CustomerIndex INT, ItemIndex INT, Amount REAL)" % tableName
    cur.execute(sqlQuery)

    for i in range(salesMatrixEst.shape[0]):
        for j in range(salesMatrixEst.shape[1]):
            if salesMatrixEst[i,j] >= threshold:
                sqlQuery = "INSERT INTO %s VALUES (%d, %d, %.2f)" % (tableName, i, j, salesMatrixEst[i,j])
                cur.execute(sqlQuery)

    conn.commit()
    conn.close()
    
def updateRecommendations(db_name, criteria):
    salesMatrixEst = generateRecommendations(db_name, criteria)
    updateSalesEstimationTable(db_name, criteria, salesMatrixEst)
    
def updateRecommendationsWithThreshold(db_name, criteria, threshold):
    salesMatrixEst = generateRecommendations(db_name, criteria)
    updateSalesEstimationTableWithThreshold(db_name, criteria, salesMatrixEst, threshold)
    
    
def updateMarginalSalesTensor(db_name, desiredFields):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    tableName = "MarginalSalesTensor_%s%s%s" % (desiredFields[0][:-5], desiredFields[1][:-5], desiredFields[2][:-5])

    sqlQuery = "DROP TABLE IF EXISTS %s" % tableName
    cur.execute(sqlQuery)

    sqlQuery = "CREATE TABLE %s (%s INT, %s INT, %s INT, Amount REAL)" % (tableName, desiredFields[0], desiredFields[1], desiredFields[2])
    cur.execute(sqlQuery)

    temp = "%s, %s, %s" % (desiredFields[0], desiredFields[1], desiredFields[2])
    sqlQuery = "SELECT " + temp + ", SUM(Amount) FROM SalesTensor GROUP BY " + temp 
    cur.execute(sqlQuery)

    col0 = []
    col1 = []
    col2 = []
    data = []

    for values in cur:
        col0.append(values[0])
        col1.append(values[1])
        col2.append(values[2])
        data.append(values[3])

    for i in range(len(data)):
        sqlQuery = "INSERT INTO %s VALUES (%d, %d, %d, %.2f)" % (tableName, col0[i], col1[i], col2[i], data[i])
        cur.execute(sqlQuery)  

    conn.commit()
    conn.close()
    
def updateAllMarginalSalesTensors(db_name):
    desiredFields = ["CustomerIndex", "WeekIndex", "DowIndex"]
    updateMarginalSalesTensor(db_name, desiredFields)

    desiredFields = ["CustomerIndex", "WeekIndex", "HourIndex"]
    updateMarginalSalesTensor(db_name, desiredFields)

    #desiredFields = ["CustomerIndex", "WeekIndex", "ItemIndex"]
    #updateMarginalSalesTensor(db_name, desiredFields)

    desiredFields = ["CustomerIndex", "WeekIndex", "ItemG3Index"]
    updateMarginalSalesTensor(db_name, desiredFields)

    desiredFields = ["CustomerIndex", "DowIndex", "HourIndex"]
    updateMarginalSalesTensor(db_name, desiredFields)

    desiredFields = ["CustomerIndex", "DowIndex", "ItemG3Index"]
    updateMarginalSalesTensor(db_name, desiredFields)

    desiredFields = ["CustomerIndex", "HourIndex", "ItemG3Index"]
    updateMarginalSalesTensor(db_name, desiredFields)
    
    
def updateMarginalSalesTensorMat(db_name, desiredFields, desiredShapes, numCustomers):
    dataDict = {}
    for idx in range(numCustomers): 
        customerIndex = idx
        salesMatrix = SalesFunctions.getSalesMatrixOfCustomer(db_name, customerIndex, desiredFields, "sum", desiredShapes)

        dataDict.update({str(idx):salesMatrix})

    filename = 'database/MarginalSalesTensor_Customer%s%s.mat' % (desiredFields[0][:-5], desiredFields[1][:-5]) 
    sio.savemat(filename, dataDict)
    

def updateAllMarginalSalesTensorMat(db_name):
    dimensions = ["WeekIndex", "DowIndex", "HourIndex", "ItemG3Index"]
    DATABASE_SHAPE = DatabaseInfoFunctions.getDatabaseShape(db_name)
    shapes = [DATABASE_SHAPE[0], DATABASE_SHAPE[1], DATABASE_SHAPE[2], DATABASE_SHAPE[4]] 

    desiredFields = ["WeekIndex", "DowIndex"]
    desiredShapes = [DATABASE_SHAPE[0], DATABASE_SHAPE[1]]
    updateMarginalSalesTensorMat(db_name, desiredFields, desiredShapes, DATABASE_SHAPE[5])

    desiredFields = ["WeekIndex", "HourIndex"]
    desiredShapes = [DATABASE_SHAPE[0], DATABASE_SHAPE[2]]
    updateMarginalSalesTensorMat(db_name, desiredFields, desiredShapes, DATABASE_SHAPE[5])
    
    desiredFields = ["WeekIndex", "ItemG3Index"]
    desiredShapes = [DATABASE_SHAPE[0], DATABASE_SHAPE[4]]
    updateMarginalSalesTensorMat(db_name, desiredFields, desiredShapes, DATABASE_SHAPE[5])
    
    desiredFields = ["DowIndex", "HourIndex"]
    desiredShapes = [DATABASE_SHAPE[1], DATABASE_SHAPE[2]]
    updateMarginalSalesTensorMat(db_name, desiredFields, desiredShapes, DATABASE_SHAPE[5])
    
    desiredFields = ["DowIndex", "ItemG3Index"]
    desiredShapes = [DATABASE_SHAPE[1], DATABASE_SHAPE[4]]
    updateMarginalSalesTensorMat(db_name, desiredFields, desiredShapes, DATABASE_SHAPE[5])
    
    desiredFields = ["HourIndex", "ItemG3Index"]
    desiredShapes = [DATABASE_SHAPE[2], DATABASE_SHAPE[4]]
    updateMarginalSalesTensorMat(db_name, desiredFields, desiredShapes, DATABASE_SHAPE[5])
    