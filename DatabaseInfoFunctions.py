
import sqlite3

def getDatabaseShape(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT MAX(WeekIndex), MAX(DowIndex), MAX(HourIndex), MAX(ItemIndex), MAX(ItemG3Index), MAX(CustomerIndex) FROM SalesTensor")

    for values in c:
        NUM_ALL_WEEKS = values[0] + 1
        NUM_ALL_DOWS = values[1] + 1
        NUM_ALL_HOURS = values[2] + 1
        NUM_ALL_ITEMS = values[3] + 1
        NUM_ALL_ITEMSG3 = values[4] + 1
        NUM_ALL_CUSTOMERS = values[5] + 1

    databaseShape = [NUM_ALL_WEEKS, NUM_ALL_DOWS, NUM_ALL_HOURS, NUM_ALL_ITEMS, NUM_ALL_ITEMSG3, NUM_ALL_CUSTOMERS]
    
    conn.close()

    return databaseShape