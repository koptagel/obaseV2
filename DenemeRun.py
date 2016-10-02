import numpy as np
import sqlite3

def func1(db_name, customerIndex):
    print("func1 starts") 
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    tableName = "asdDeneme"
    sqlQuery = "CREATE TABLE %s (CustomerIndex INT, ItemG3Index INT, Amount REAL)" % tableName
    c.execute(sqlQuery)
    
    sqlQuery = "SELECT ItemG3Index, SUM(Amount) FROM SalesTensor WHERE CustomerIndex=%d GROUP BY ItemG3Index " % customerIndex
    c.execute(sqlQuery)

    for values in c:
        print(values)

    conn.close()
    
def main():
    print("main starts")
    
    customerIndex = 10
    db_name = "database/ObaseDb"
    
    func1(db_name, customerIndex)
    
if __name__ == "__main__": main()