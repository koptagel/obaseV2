
import numpy as np
from scipy.sparse import *
import sqlite3

import SalesFunctions
import MappingFunctions

def getRecommendationG3OfCustomer(db_name, customerIndex, criteria, recommenderType, numRecItems, shape1):
    if criteria == 2:
        plotCriteria = "binary"
    else:
        plotCriteria = "sum"

    salesMatrix = SalesFunctions.getSalesHistogramOfCustomer(db_name, customerIndex, "ItemG3Index", plotCriteria, shape1)
    salesMatrixEst = SalesFunctions.getSalesEstimationG3OfCustomer(db_name, customerIndex, criteria, shape1)
    
    
    if recommenderType == "mix":
        recItemIndices = np.argsort(salesMatrixEst.toarray())[0,:][::-1][0:numRecItems]
    else:

        boughtItems = np.where(salesMatrix.toarray()>0)[1]
        recAllItemIndices = np.argsort(salesMatrixEst.toarray())[0,:][::-1]

        recItemIndices = []

        if recommenderType == "discover":
            count = 0
            for i in range(len(recAllItemIndices)):
                if count < numRecItems and recAllItemIndices[i] not in boughtItems:
                    recItemIndices.append(recAllItemIndices[i])
                    count = count+1
                elif count == numRecItems:
                    break;

        elif recommenderType == "habit":
            count = 0
            for i in range(len(recAllItemIndices)):
                if count < numRecItems and recAllItemIndices[i] in boughtItems:
                    recItemIndices.append(recAllItemIndices[i])
                    count = count+1
                elif count == numRecItems:
                    break;

        else:
            count = 0
            for i in range(len(recAllItemIndices)):
                itemIndex = recAllItemIndices[i]
                if salesMatrixEst[0,itemIndex] >salesMatrix[0,itemIndex]:
                    recItemIndices.append(recAllItemIndices[i])
                    count = count+1
                elif count == numRecItems:
                    break;
                    
                    
    recProductData = []
    for i in range(len(recItemIndices)):
        data2 = {}
        data2['id'] = MappingFunctions.getItemG3IdWithItemG3Index(db_name, int(recItemIndices[i]))
        recProductData.append(data2)
        
    return recProductData


def getRecommendationOfCustomer(db_name, customerIndex, criteria, recommenderType, numRecItems, shape1):
    if criteria == 2:
        plotCriteria = "binary"
    else:
        plotCriteria = "sum"

    salesMatrix = SalesFunctions.getSalesHistogramOfCustomer(db_name, customerIndex, "ItemIndex", plotCriteria, shape1)
    salesMatrixEst = SalesFunctions.getSalesEstimationOfCustomer(db_name, customerIndex, criteria, shape1)
    
    
    if recommenderType == "mix":
        recItemIndices = np.argsort(salesMatrixEst.toarray())[0,:][::-1][0:numRecItems]
    else:

        boughtItems = np.where(salesMatrix.toarray()>0)[1]
        recAllItemIndices = np.argsort(salesMatrixEst.toarray())[0,:][::-1]

        recItemIndices = []

        if recommenderType == "discover":
            count = 0
            for i in range(len(recAllItemIndices)):
                if count < numRecItems and recAllItemIndices[i] not in boughtItems:
                    recItemIndices.append(recAllItemIndices[i])
                    count = count+1
                elif count == numRecItems:
                    break;

        elif recommenderType == "habit":
            count = 0
            for i in range(len(recAllItemIndices)):
                if count < numRecItems and recAllItemIndices[i] in boughtItems:
                    recItemIndices.append(recAllItemIndices[i])
                    count = count+1
                elif count == numRecItems:
                    break;

        else:
            count = 0
            for i in range(len(recAllItemIndices)):
                itemIndex = recAllItemIndices[i]
                if salesMatrixEst[0,itemIndex] >salesMatrix[0,itemIndex]:
                    recItemIndices.append(recAllItemIndices[i])
                    count = count+1
                elif count == numRecItems:
                    break;
                    
                    
    recProductData = []
    for i in range(len(recItemIndices)):
        data2 = {}
        data2['id'] = MappingFunctions.getItemIdWithItemIndex(db_name, int(recItemIndices[i]))
        recProductData.append(data2)
        
    return recProductData