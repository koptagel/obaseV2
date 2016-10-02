
import numpy as np
from scipy.sparse import *
import sqlite3

import MappingFunctions
import NmfFunctions
import SalesFunctions

def generateCustomerProfile(db_name, profileId, profileDs, productList, minPercentage, numCustomers, criteria, shapes):
    
    # Load SalesMatrix in the shape NumCustomers x NumItemsGroup3
    salesMatrix = SalesFunctions.getSalesMatrix(db_name, criteria, shapes)
 
    # Find valid and invalid items 
    validItems = []
    invalidItems = []

    for i in range(len(productList)):
        itemIndex = MappingFunctions.getItemG3IndexWithItemId(db_name, productList[i])
        if itemIndex != -99 or itemIndex != -1:
            validItems.append(itemIndex)
        else:
            data = {}
            data['id'] = int(productList[i])
            invalidItems.append(data) 
            
    # Apply Nmf with Fix Basis
    rank = 1
    maxIter = 2
    
    Z2 = np.zeros((rank,shapes[1]))
    Z2[0,validItems] = 1

    _, _, _, _, customerIndices, customerPercentages = NmfFunctions.nmfFixBasis(salesMatrix.toarray(), Z2, maxIter, rank)
    
    # Apply limitations
    count = 0
    customerData = []
    for i in range(len(customerIndices)):
        if count < numCustomers:
            if int(customerPercentages[i])>= minPercentage:
                data2 = {}
                data2['percentage'] = int(customerPercentages[i])
                data2['id'] = MappingFunctions.getCustomerId(db_name, int(customerIndices[i]))

                customerData.append(data2)
                count = count+1
        else:
            break
            
    # Update database
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    tableName = "ProfileMapping"

    sqlQuery = "DELETE FROM %s WHERE ProfileId=%d" % (tableName, profileId)
    cur.execute(sqlQuery)
    sqlQuery = "INSERT INTO %s VALUES (%d, \"%s\")" % (tableName, profileId, profileDs)
    cur.execute(sqlQuery)


    tableName = "ProfileCustomers"

    sqlQuery = "DELETE FROM %s WHERE ProfileId=%d" % (tableName, profileId)
    cur.execute(sqlQuery)
    for i in range(len(customerData)):
        sqlQuery = "INSERT INTO %s VALUES (%d, %d, %d)" % (tableName, profileId, customerData[i]["id"], customerData[i]["percentage"])
        cur.execute(sqlQuery)

    conn.commit()
    conn.close()
            
    return customerData, invalidItems


def updateProfileItems(db_name, profileId, productsData):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    tableName = "ProfileItems"

    sqlQuery = "DELETE FROM %s WHERE ProfileId=%d" % (tableName, profileId)
    cur.execute(sqlQuery)
    for i in range(len(productsData)):
        sqlQuery = "INSERT INTO %s VALUES (%d, %d, %d)" % (tableName, profileId, productsData[i]["id"], productsData[i]["percentage"])
        cur.execute(sqlQuery)

    conn.commit()
    conn.close()