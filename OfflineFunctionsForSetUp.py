
import OfflineFunctions

def main():
    db_name = "database/ObaseDb.db"
    
    # Generate Marginal Sales Tensors and Save Them Into .mat Files
    #print("Marginal Tensors - Start")
    #OfflineFunctions.updateAllMarginalSalesTensorMat(db_name)
    #print("Marginal Tensors - End")
    
    # Generate Recommendations According to ItemGroup3 Purchases
    print("Recommendations Group3 - Start")
    criteriaList = [1,2]
    for i in range(len(criteriaList)):
        OfflineFunctions.updateRecommendationsG3(db_name, criteriaList[i])
    print("Recommendations Group3 - End")
       
    # Generate Recommendations According to Item Purchases
    print("Recommendations - Start")
    criteriaList = [1,2]
    thresholdList = [0.1,0.01]
    for i in range(len(criteriaList)):
        OfflineFunctions.updateRecommendationsWithThreshold(db_name, criteriaList[i], thresholdList[i])     
    print("Recommendations - End")

if __name__ == "__main__": main()