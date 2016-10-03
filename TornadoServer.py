
### Library And Function Imports 
import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.escape import json_encode

import os
import json
import numpy as np
import scipy.io as sio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import HtmlPages
import SalesFunctions
import MappingFunctions
import ProfileFunctions
import WeblogFunctions
import SimilarityFunctions
import RecommendationFunctions
import DatabaseInfoFunctions

### Global Variable Declarations
HOST = 'localhost'
PORT = 8086

DIRNAME = os.path.dirname(os.path.realpath('__file__'))
TEMPLATE_DIRNAME = "" + DIRNAME + "/startbootstrap-business-casual-gh-pages"
STATIC_PATH = os.path.join(DIRNAME, '.')

DB_NAME = "database/ObaseDb.db"
DATABASE_SHAPE = DatabaseInfoFunctions.getDatabaseShape(DB_NAME) # NUM_WEEKS, NUM_DOWS, NUM_HOURS, NUM_ITEMS, NUM_ITEMSG3, NUM_CUSTOMERS


### Classes

### Landing Page Of The Server
class MainPage(tornado.web.RequestHandler):
    def get(self):
        self.post()
        
    def post(self):
        htmlContent = HtmlPages.getHtmlContent(HOST, PORT)
        self.write(htmlContent)


class CustomerSalesMap(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        # Get the input parameters
        temp = self.get_argument('jsonData')
        inputData = json.loads(temp)
        
        customerId = int(inputData['id'])
        customerIndex = MappingFunctions.getCustomerIndex(DB_NAME, customerId)
        
        criteria = inputData['type']
        ax1 = int(inputData['xAxis'])
        ax2 = int(inputData['yAxis'])
        
        # Check base cases
        if customerIndex == -99:
            self.write("Invalid Customer Id")
        elif criteria not in [1,2]:
            self.write("Invalid Type. Type must be 1 or 2.")
        elif ax1 not in [0,1,2,3,4,5,6]:
            self.write("Invalid Axis Value. Axis value must be 0,1,2,3,4,5 or 6.")
        elif ax2 not in [0,1,2,3,4,5,6]:
            self.write("Invalid Axis Value. Axis value must be 0,1,2,3,4,5 or 6.")    
        elif ax1 == 6 and ax2 == 6:
            self.write("Invalid Axis Value. Both of the axis values cannot be 6.")
        
        # If the given axes are web-related
        elif ax1 in [4,5] or ax2 in [4,5]:
            if ax1 != ax2:
                self.write("Invalid Axis Value. To plot weblog activities, both axes must have same value.")

            elif ax1 == 4:
                distances = WeblogFunctions.webBrowseMatrix(customerId)

                if np.sum(distances) == 0:
                    self.write("Invalid Customer Id. This customer does not have weblog data.")
                else:
                    WeblogFunctions.plotWeblogMatrix(customerId,distances)

                imageUrl = (HOST+":%s/files/%d_webmatrix.png" % (PORT,customerId))
                info = json.dumps({"image_url": imageUrl})
                self.write("%s" % info)

            else:
                distances = WeblogFunctions.webBrowseMatrix(customerId)

                if np.sum(distances) == 0:
                    self.write("Invalid Customer Id. This customer does not have weblog data.")
                else:
                    WeblogFunctions.webBrowseGraph(customerId,distances)

                imageUrl = (HOST+":%s/files/%d_webgraph.png" % (PORT,customerId))
                info = json.dumps({"image_url": imageUrl})
                self.write("%s" % info)
       
        else:  
            TimePoints = []
            TimePointsY = []
            if ax1 == 6 or ax2 == 6:
                slots = inputData['slots']
                for i in range(len(slots)):
                    TimePoints.append(int(slots[i]["x"]))
                    TimePointsY.append(int(slots[i]["y"]))

            plt.figure
            plotTitle = "Sales of Customer %d" % customerId

            SalesFunctions.getCustomerSalesMap(DB_NAME, customerIndex, plotTitle, criteria, ax1, ax2, TimePoints, TimePointsY)

            plt.savefig('./files/%d_%d_%d_%d.png' % (customerId,ax1,ax2,criteria))
            imageUrl = ("/files/%d_%d_%d_%d.png" % (customerId,ax1,ax2,criteria))

            info = json.dumps({"image_url": imageUrl})
            self.write("%s" % info)


class CustomersOfProfile(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        # Get the input parameters
        temp = self.get_argument('jsonData')
        inputData = json.loads(temp)
        
        numCustomers = inputData['Count']
        minPercentage = inputData['MinPercentage']
        criteria = inputData['Type']
        
        profileId = inputData['ProfileId']
        profileDs = inputData['ProfileDs']
        products = inputData['Products']
    
        # Check base cases
        if numCustomers<1:
            self.write("Invalid count. Count must be more than 0.")
        elif minPercentage>100:
            self.write("Invalid percentage. Minimum percentage must less than or equal to 100.")
        elif criteria not in [0,1,2]:
            self.write("Invalid Type. Type must be 1,2 or 3.")
        else:
            
            productList = []
            for i in range(len(products)):
                productList.append(int(products[i]['id']))
            
            if len(productList) == 0:
                self.write("Invalid Product List.")
            
            # Generate customer profile 
            else:
                shapes = [DATABASE_SHAPE[5], DATABASE_SHAPE[4]]
                customerData, invalidItems = ProfileFunctions.generateCustomerProfile(DB_NAME, profileId, profileDs, productList, minPercentage, numCustomers, criteria, shapes)

                if len(invalidItems) > 0:
                    json_data = json.dumps({"Customers": customerData, "InvalidItems": invalidItems})
                else:    
                    json_data = json.dumps({"Customers": customerData})

                self.write(json_data) 
    
    
class CustomerWeblogPlots(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        # Get the input parameters
        temp = self.get_argument('jsonData')
        inputData = json.loads(temp)
        
        customerId = int(inputData['id'])
        
        distances = WeblogFunctions.webBrowseMatrix(customerId)
        
        # Check the base case
        if np.sum(distances) == 0:
            self.write("Invalid Customer Id. This customer does not have weblog data.")
        else:
            WeblogFunctions.plotWeblogMatrix(customerId,distances)
            WeblogFunctions.webBrowseGraph(customerId,distances)

            matrixUrl = (HOST+":%s/files/%d_webmatrix.png" % (PORT,customerId))
            graphUrl = (HOST+":%s/files/%d_webgraph.png" % (PORT,customerId))

            info = json.dumps({"image_url": matrixUrl, "image_url_graph": graphUrl})
            self.write("%s" % info)

 
class similarCustomers(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        # Get the input parameters
        temp = self.get_argument('jsonData')
        inputData = json.loads(temp)

        customerId = int(inputData['id'])
        customerIndex = MappingFunctions.getCustomerIndex(DB_NAME, customerId)
        
        numCustomers = inputData['Count']
        minPercentage = inputData['MinPercentage']
        
        criteria = inputData['type']
        ax1 = int(inputData['xAxis'])
        ax2 = int(inputData['yAxis'])
        
        distanceType = inputData['distanceType']
        searchType = inputData['searchType']
        
        numRecItems = inputData['productCount']
        baseCount = inputData['baseCount']
        recommenderType = inputData['recommenderType']
        
        # Check base cases
        if customerIndex == -99:
            self.write("Invalid Customer Id")
        elif numCustomers<1:
            self.write("Invalid count. Count must be more than 0.")
        elif minPercentage>100:
            self.write("Invalid percentage. Minimum percentage must less than or equal to 100.")
        elif criteria not in [0,1,2]:
            self.write("Invalid Type. Type must be 1 or 2.")
        elif ax1 not in [0,1,2,3,4,5,6]:
            self.write("Invalid Axis Value. Axis value must be 0,1,2,3,4,5 or 6.")
        elif ax2 not in [0,1,2,3,4,5,6]:
            self.write("Invalid Axis Value. Axis value must be 0,1,2,3,4,5 or 6.")
        elif ax1 in [4,5] or ax2 in [4,5]:
            if ax1 != ax2:
                self.write("Invalid Axis Value. To use weblog activities, axis values must be same.")
        elif ax1 == 6 and ax2 == 6:
            self.write("Invalid Axis Value. Both of the axis values cannot be 6.")
        elif distanceType not in [0,1,2,3]:
            self.write("Invalid Distance Type. Distance type must be 0,1,2 or 3.")
        elif searchType not in [0,1]:
            self.write("Invalid Search Type. Search type must be 0 or 1.")
        else:
            TimePoints = []
            TimePointsY = []
            if ax1 == 6 or ax2 == 6:
                slots = inputData['slots']
                TimePoints = []
                TimePointsY = []
                for i in range(len(slots)):
                    TimePoints.append(int(slots[i]["x"]))
                    TimePointsY.append(int(slots[i]["y"]))
  
            if searchType ==1:
                profileId = inputData['ProfileId']
            else:
                profileId = 0
            
            # Get similar customers
            shape1 = DATABASE_SHAPE[3]
            customersData, minDistance, maxDistance, productsData = SimilarityFunctions.getSimilarCustomersWithProducts(DB_NAME,customerIndex, criteria, ax1, ax2, TimePoints, TimePointsY, searchType, distanceType, numCustomers, minPercentage, profileId, numRecItems, recommenderType, shape1, baseCount)
    
            json_data = json.dumps({"Customers": customersData, "Products": productsData, "MinDistance":minDistance, "MaxDistance": maxDistance})
            self.write(json_data)  
        
        
class RecommendProducts(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        # Get the input parameters
        temp = self.get_argument('jsonData')
        inputData = json.loads(temp)
        
        customerId = int(inputData['id'])
        numRecItems = int(inputData['Count'])
        recommenderType = inputData['type']
        criteria = inputData['criteria']
        
        customerIndex = MappingFunctions.getCustomerIndex(DB_NAME, customerId)
        # Check base cases
        if customerIndex == -99:
            self.write("Invalid Customer Id")
        elif recommenderType not in ["mix", "discover", "habit", "difference"]:
            self.write("Invalid Recommender Type. Type value must be mix, discover, habit or difference.")
        elif criteria not in [1,2]:
            self.write("Invalid Criteria Value. It must be 1 (sum) or 2 (binary).")
        elif numRecItems <= 0:
            self.write("Invalid Count. Count must be bigger than 0.")
        # Get recommendations
        else:
            shape1 = DATABASE_SHAPE[4]
            recommendedProducts = RecommendationFunctions.getRecommendationG3OfCustomer(DB_NAME, customerIndex, criteria, recommenderType, numRecItems, shape1)
            
            json_data = json.dumps({"Products": recommendedProducts})
            self.write(json_data) 
        
        
class RecommendProducts2(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        
    def get(self, *args):
        self.post(*args)
        
    def post(self, *args):
        # Get the input parameters
        temp = self.get_argument('jsonData')
        inputData = json.loads(temp)
        
        customerId = int(inputData['id'])
        numRecItems = int(inputData['Count'])
        recommenderType = inputData['type']
        criteria = inputData['criteria']
        
        customerIndex = MappingFunctions.getCustomerIndex(DB_NAME, customerId)
        # Check base cases
        if customerIndex == -99:
            self.write("Invalid Customer Id")
        elif recommenderType not in ["mix", "discover", "habit", "difference"]:
            self.write("Invalid Recommender Type. Type value must be mix, discover, habit or difference.")
        elif criteria not in [1, 2]:
            self.write("Invalid Criteria Value. It must be 1 (sum) or 2 (binary).")
        elif numRecItems <= 0:
            self.write("Invalid Count. Count must be bigger than 0.")
        # Get the recommendations
        else:
            shape1 = DATABASE_SHAPE[3]
            recommendedProducts = RecommendationFunctions.getRecommendationOfCustomer(DB_NAME, customerIndex, criteria, recommenderType, numRecItems, shape1)
            
            json_data = json.dumps({"Products": recommendedProducts})
            self.write(json_data)
            
            
### The Route Configurations
routes_config = [
    (r"/", MainPage), 
    (r"/customerSalesMap", CustomerSalesMap),
    (r"/customersOfProfile", CustomersOfProfile),
    (r"/customerWeblog", CustomerWeblogPlots),
    (r"/similarCustomers", similarCustomers),
    (r"/recommendProducts", RecommendProducts),
    (r"/recommendProducts2", RecommendProducts2),
    (r"/(.*\.png)", tornado.web.StaticFileHandler,{"path": "." }),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": TEMPLATE_DIRNAME, "default_filename": "index.html"})
]
application = tornado.web.Application(routes_config)


def start():
    print("Obase Tornado Server.\nStarting on host %s, port %s" % (HOST,PORT))
    http_server = HTTPServer(application, xheaders=True)
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
    return application


if __name__ == "__main__":
    start()