
import sqlite3

### Functions of CustomerMapping table
def getCustomerIndex(db_name, customerId):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute("SELECT CustomerIndex FROM CustomerMapping WHERE CustomerId=?", (customerId,))
    result = cur.fetchone()
    if result is None:
        print("Invalid Customer Id")
        customerIndex = -99
    else:
        customerIndex = result[0]
        
    conn.close()
    return customerIndex

def getCustomerId(db_name, customerIndex):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute("SELECT CustomerId FROM CustomerMapping WHERE CustomerIndex=?", (customerIndex,))
    result = cur.fetchone()
    if result is None:
        print("Invalid Customer Index")
        customerId = -99
    else:
        customerId = result[0]
        
    conn.close()
    return customerId


### Functions of ItemMapping table
def getItemIndexWithItemId(db_name, itemId):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute("SELECT ItemIndex FROM ItemMapping WHERE ItemId=?", (itemId,))
    result = cur.fetchone()
    if result is None:
        print("Invalid Item Id")
        itemIndex = -99
    else:
        itemIndex = result[0]
        
    conn.close()
    return itemIndex

def getItemIdWithItemIndex(db_name, itemIndex):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute("SELECT ItemId FROM ItemMapping WHERE ItemIndex=?", (itemIndex,))
    result = cur.fetchone()
    if result is None:
        print("Invalid Item Index")
        itemId = -99
    else:
        itemId = result[0]
        
    conn.close()
    return itemId

def getItemG3IndexWithItemId(db_name, itemId):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute("SELECT ItemG3Index FROM ItemMapping WHERE ItemId=?", (itemId,))
    result = cur.fetchone()
    if result is None:
        print("Invalid Item Id")
        itemG3Index = -99
    else:
        itemG3Index = result[0]
        
    conn.close()
    return itemG3Index

def getItemG3IdWithItemIndex(db_name, itemIndex):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute("SELECT ItemG3Id FROM ItemMapping WHERE ItemIndex=?", (itemIndex,))
    result = cur.fetchone()
    if result is None:
        print("Invalid Item Index")
        itemG3Id = -99
    else:
        itemG3Id = result[0]
        
    conn.close()
    return itemG3Id


def getItemG3IndexWithItemIndex(db_name, itemIndex):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute("SELECT ItemG3Index FROM ItemMapping WHERE ItemIndex=?", (itemIndex,))
    result = cur.fetchone()
    if result is None:
        print("Invalid Item Index")
        itemG3Index = -99
    else:
        itemG3Index = result[0]
        
    conn.close()
    return itemG3Index


def getItemG3IdWithItemG3Index(db_name, itemG3Index):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute("SELECT ItemG3Id FROM ItemMapping WHERE ItemG3Index=?", (itemG3Index,))
    result = cur.fetchone()
    if result is None:
        print("Invalid Item Index")
        itemG3Id = -99
    else:
        itemG3Id = result[0]
        
    conn.close()
    return itemG3Id