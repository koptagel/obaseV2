
import numpy as np
from scipy.sparse import *
import sqlite3
import scipy.io as sio

import SalesFunctions
import SalesMarginalFunctions
import DistanceFunctions
import MappingFunctions
import ProfileFunctions
import RecommendationFunctions
import DatabaseInfoFunctions

def getSimilarCustomers(db_name, customerIndex, criteria, ax1, ax2, TimePoints, TimePointsY, searchType, distanceType, numCustomers, minPercentage, profileId):
    
    dimensions = ["WeekIndex", "DowIndex", "HourIndex", "ItemG3Index", "WeblogMatrix", "WeblogGraph", "TimeSlots"]
    
    tempAx1 = -1
    tempAx2 = -1
    
    if ax1 == 6 or ax2 == 6:
        tempAx1 = ax1
        tempAx2 = ax2
        
        if ax1 == 6:
            ax1 = 2
        else:
            ax2 = 2
            
    if ax1 < ax2:
        desiredFields = [dimensions[ax1], dimensions[ax2]]
    elif ax1 > ax2:
        desiredFields = [dimensions[ax2], dimensions[ax1]]
    elif ax1 < 3:
        desiredFields = [dimensions[ax1], dimensions[ax1+1]]
    else:
        desiredFields = [dimensions[ax1-1], dimensions[ax1]]
    
    if tempAx1 != -1:
        ax1 = tempAx1
    if tempAx2 != -1:
        ax2 = tempAx2
    
        
    filename = 'database/MarginalSalesTensor_Customer%s%s.mat' % (desiredFields[0][:-5], desiredFields[1][:-5])
    #print("filename :%s" %filename)
    
    dataDict = sio.loadmat(filename)
    
    #originSales = dataDict[str(customerIndex)]
    #originSales = SalesFunctions.getCustomerSales(db_name, customerIndex, criteria, ax1, ax2, TimePoints, TimePointsY)  
    originSales = SalesMarginalFunctions.getCustomerSalesFromMarginalMats(dataDict, customerIndex, criteria, ax1, ax2, TimePoints, TimePointsY)  
    #print("shape: %d %d" % (originSales.shape[0],originSales.shape[1]))

    if searchType == 0:
        DATABASE_SHAPE = DatabaseInfoFunctions.getDatabaseShape(db_name)
        numAllCustomers = DATABASE_SHAPE[5]
        customerIndexList = np.arange(numAllCustomers)
    else:
        customerIndexList = []

        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        sqlQuery = "SELECT CustomerId FROM ProfileCustomers WHERE ProfileId = %d ORDER BY CustomerPercentage DESC" % profileId 
        c.execute(sqlQuery)

        for values in c:
            custId = values[0]
            customerIndexList.append(MappingFunctions.getCustomerIndex(db_name, custId))
        conn.close()
    
    
    if distanceType==0:
        metric = 'kl'
    elif distanceType==1:
        metric = 'is'
    elif distanceType==2:
        metric = 'hel'
    else:
        metric = 'euc'
        
    
    distances = np.zeros(len(customerIndexList))

    for i in range(len(customerIndexList)):        
        #customerSales = SalesFunctions.getCustomerSales(db_name, int(customerIndexList[i]), criteria, ax1, ax2, TimePoints, TimePointsY)    
        #customerSales = dataDict[str(customerIndexList[i])]
        customerSales = SalesMarginalFunctions.getCustomerSalesFromMarginalMats(dataDict, customerIndexList[i], criteria, ax1, ax2, TimePoints, TimePointsY)  
   
        distances[i] = DistanceFunctions.distance(originSales.toarray(), customerSales.toarray(), metric)
        
    indices = distances.argsort()
    sortedDistances = np.sort(distances)
    sortedDistances = - sortedDistances
    percentages = (100 * np.ones(len(customerIndexList))) - ( sortedDistances * 100 / np.min(sortedDistances) )
    
    customerIdList = []
    for i in range(len(customerIndexList)):
        custIdx = customerIndexList[indices[i]]
        customerIdList.append(MappingFunctions.getCustomerId(db_name, int(custIdx)))
    customerIdList = np.array(customerIdList)
    
    minDistance = -int(np.max(sortedDistances))
    maxDistance = -int(np.min(sortedDistances))
    
    count = 0
    customersData = []
    for i in range(len(customerIdList)):
        if count < numCustomers:
            if int(percentages[i])>= minPercentage:
                data2 = {}
                data2['percentage'] = int(percentages[i])
                data2['distances'] = - int(sortedDistances[i])
                data2['id'] = int(customerIdList[i])

                customersData.append(data2)
                count = count+1
                   
    return customersData, minDistance, maxDistance


def getGroupRecommendations(db_name, baseCount, criteria, recommenderType,numRecItems, shape1, customersData):
    if baseCount == 0 or baseCount > len(customersData):
        baseCount = len(customersData)

    allProducts = []
    for i in range(baseCount):
        custIndex = MappingFunctions.getCustomerIndex(db_name, customersData[i]["id"])
        recProducts = RecommendationFunctions.getRecommendationOfCustomer(db_name, custIndex, criteria, recommenderType, numRecItems, shape1)

        for j in range(len(recProducts)):
            allProducts.append(recProducts[j]["id"])
            
    recProducts = []
    percProducts = []

    for i in range(len(allProducts)):
        if allProducts[i] not in recProducts:
            recProducts.append(allProducts[i])
            percProducts.append(100/baseCount)
        else:
            index = recProducts.index(allProducts[i])
            percProducts[index] = percProducts[index] + 100/baseCount

    sortedIndices = np.array(percProducts).argsort()[::-1]


    productsData = []
    for i in range(len(sortedIndices)):
        data2 = {}
        data2['percentage'] = int(percProducts[sortedIndices[i]])
        data2['id'] = int(recProducts[sortedIndices[i]])

        productsData.append(data2)
    
    return productsData

def getSimilarCustomersWithProducts(db_name, customerIndex, criteria, ax1, ax2, TimePoints, TimePointsY, searchType, distanceType, numCustomers, minPercentage, profileId, numRecItems, recommenderType, shape1, baseCount):
    customersData, minDistance, maxDistance = getSimilarCustomers(db_name, customerIndex, criteria, ax1, ax2, TimePoints, TimePointsY, searchType, distanceType, numCustomers, minPercentage, profileId)
    
    productsData = getGroupRecommendations(db_name, baseCount, criteria, recommenderType,numRecItems, shape1, customersData)
    if searchType == 1:
        ProfileFunctions.updateProfileItems(db_name, profileId, productsData)
    
    return customersData, minDistance, maxDistance, productsData