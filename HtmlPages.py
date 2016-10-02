
def getUpdateDetails():
    text = '<h2> Son Guncelleme </h2>'
    text = text + '22.09.2016 17:15 <br><br>'
    text = text + '* Obase Version 2 yazilmaya baslandi.<br><br>'
    return text

def getToDoItems():
    text = '<h2> Yapilacak Isler </h2>'
    text = text + '* Obase Version 2 fonksiyonlari tamamlanacak.<br>'
    text = text + '* Database olusturulacak.<br>'
    text = text + '* Fonksiyonlar yeni yapiya gore guncellenecek.<br>'
    text = text + '* CustomerSalesMap fonksiyonunda time slot icin label araligi ve dow icin tick ayarlanacak.<br>'
    text = text + '* CustomerSalesMap fonksiyonuna weblog matrix ve graph eklenecek.<br>'
    text = text + '* Main Pagedeki bilgiler guncellenecek.<br><br>'
    return text
    
def getDatasetDetails():
    text = '<h2> Dataset Bilgileri </h2>'
    text = text + 'Ilk Alisveris Tarihi: 05.01.2015 00:00 <br>'
    text = text + 'Son Alisveris Tarihi: 16.05.2016 15:00 <br>'
    text = text + 'Toplam Satis Miktari: 432.636 <br>'
    text = text + 'Musteri Sayisi: 3.193 <br>'
    text = text + 'Gecerli Urun Sayisi: 6.087 <br>'
    text = text + 'Gecerli Urun Grup3 Sayisi: 180 <br><br>'
    text = text + 'recommendProducts2 fonksiyonu daha farkli bir dataset kullaniyor. <br><br>'
    return text

def getFunctionTemplate(SERVER_IP, PORT):
    text = '<h2> Genel Kullanim </h2>'
    text = text + '%s:%d/<b>FonksiyonIsmi</b>?jsonData=<b>JsonInputu</b> <br><br>' % (SERVER_IP, PORT)
    text = text + 'Asagida listelenen butun fonksiyonlarda veriler Json formatinda alinip, sonuclar Json formatinda geri dondurulecektir. <br>'
    text = text + '<b>FonksiyonIsmi</b> yazan yere asagida siralanan fonksiyonlardan birinin adinin yazilmasi gerekiyor. <br>'
    text = text + '<b>JsonInputu</b> yazan kisma ise verilerin Json formatinda girilmesi gerekiyor. <br><br>'  
    text = text + 'Her fonksiyon icin dikkat edilmesi gerekilen noktalar ve ornek kullanimlar ilerleyen kisimlarda gosterilmistir. <br>'  
    text = text + 'Ornek kullanimlardaki Json inputlari, fonksiyonlarin calisabilmesi icin gerekli olan temel yapiyi gostermektedir. <br>'    
    text = text + 'Bu temel yapiya ek olarak baska bilgiler de ayni Json inputunun icerisinde gonderilebilir. <br>'    
    return text

def getCustomersOfProfileFunction(SERVER_IP, PORT):        
    text = '<h3> customersOfProfile </h3>'
    text = text + 'Verilen urun listesine (kullanici profiline) ve kriterlere gore, bu profile uyan musterilerin idleri ve profile olan uygunluklari listelenecektir. <br>'
    text = text + 'MinPercentage parametresi, belirli bir profil uygunluguna sahip musterilerin siralanmasini sagliyor. '
    text = text + 'Count parametresi ise listelenecek maksimum musteri sayisini belirtiyor. <br>'
    text = text + 'ProfileId ve ProfileDs inputları profilin id numarasını ve ismini ifade etmek için gerekiyor. Bu id ve isim daha sonra similarCustomers fonksiyonunda kullanılacak. <br>'
    text = text + 'Musteriler, profile uygunluklarina gore siralanmistir (yuksek yuzdeden dusuk yuzdeye gore). <br><br>'               
    text = text + 'Type:'           
    text = text + '<table border="1" width=500>'            
    text = text + '<tr><td> 0 </td><td> 1 </td><td> 2 </td></tr><br>'            
    text = text + '<tr><td> Toplam Satis Sayisi </td><td> Toplam Satis Tutari </td><td> Satis yapilip yapilmadigi (0 veya 1 seklinde) </td></tr><br>'             
    text = text + '</table> <br>'              
    text = text + '<b> Input: </b> %s:%d/<b>customersOfProfile</b>?jsonData=<b>{"Count":5, "MinPercentage":60, "Type": 0, "ProfileId": 11, "ProfileDs": "Bebek", "Products": [{"id": 9556}, {"id": 34398}, {"id": 5974}]}</b> <br>' % (SERVER_IP, PORT)
    text = text + '<b> Output: </b> {"Customers": [{"percentage":98, "id": 90361}, {"percentage":80, "id": 90412}, {"percentage":77, "id": 1073258}]} <br>'
    text = text + 'Bu ornekte, verilen urunlere uyan, profil uygunlugu %60in uzerinde olan maksimum 5 musteri listeleniyor. <br>'             
    text = text + 'Profile uyan müsterilerin bilgileri, daha sonra kullanılmak için arka planda kaydediliyor. <br><br>'
    return text

def getCustomerSalesMapFunction(SERVER_IP, PORT):        
    text = '<h3> customerSalesMap </h3>'
    text = text + 'Verilen musteri idsine ve istenilen grafik kriterlerine gore, musteri haritasinin url bilgisi dondurulur. <br><br>'
    text = text + 'Grafik kriterlerinin alabilecegi degerler ve ifade ettikleri durumlar asagidaki tablolarda gosterilmistir. <br>'
    text = text + 'X ve Y Duzlemleri:'
    text = text + '<table border="1" width=600>'
    text = text + '<tr><td> 0 </td><td> 1 </td><td> 2 </td><td> 3 </td><td> 4 </td><td> 5 </td><td> 6 </td></tr><br>'           
    text = text + '<tr><td> Hafta </td><td> Haftanin Gunu </td><td> Saat </td><td> Urun </td><td> Weblog Matrix </td><td> Weblog Graph </td><td> Saat Araligi </td></tr><br>'           
    text = text + '</table><br>'            
    text = text + 'Type:'           
    text = text + '<table border="1" width=500>'            
    text = text + '<tr><td> 1 </td><td> 2 </td></tr><br>'            
    text = text + '<tr><td> Toplam Satis Tutari </td><td> Satis yapilip yapilmadigi (0 veya 1 seklinde) </td></tr><br>'             
    text = text + '</table> <br>'              
    text = text + 'Musterilerin satis grafiklerinin bar chartlarini gorebilmek icin xAxis ve yAxis degerlerinin ayni sayi olmasi gerekli. <br>'              
    text = text + 'Musterilerin web aktivitelerinin grafiklerinin de xAxis ve yAxis degerlerinin ayni sayi olmasi gerekiyor. <br>'               
    text = text + 'Saat araliklarina bakilabilmesi icin input olarak slots parametresi de verilmesi gerekiyor. <br>'                
    text = text + 'Saat araligi belirlerken istenilen sayida aralik boyutu belirlenebiliyor. <br><br>'                 
    text = text + '<b> Input: </b> %s:%d/<b>customerSalesMap</b>?jsonData=<b>{"id": 90412, "xAxis":0, "yAxis": 6, "type": 1, "slots": [{"x":0,"y":10},{"x":10,"y":20},{"x":20,"y":24}]} </b><br>' % (SERVER_IP, PORT)                 
    text = text + '<b> Output: </b> {"image_url": "/files/90412_0_6_1.png"} <br>'
    text = text + 'Bu ornekte 90412 numarali musterinin haftalara ve saat araliklarina ([0,8),[10,20),[20,24)) gore yaptigi toplam harcama gosterilmektedir. <br><br>'                          
    text = text + 'Ornek olarak kullanilabilecek musteri idleri: 1073258, 999538, 1155093. <br><br>'
    return text

def getSimilarCustomersFunction(SERVER_IP, PORT):        
    text = '<h3> similarCustomers </h3>'
    text = text + 'Verilen musteri idsine, grafik kriterlerine, kisi sayisi, uzaklik tipine ve uygunluk sinirina gore, musteriye benzer olan diger musterilerin listesi, benzerlik oranlari ve diger musterilere onerilebilecek urun listesi dondurulur. <br>'                
    text = text + 'Su anda onerilen urun listesi random bicimde uretiliyor (gercek urun idleri ile). Ilerleyen gunlerde bu kisim degistirilecek. <br><br>'                
    text = text + 'Grafik kriterlerinin alabilecegi degerler ve ifade ettikleri durumlar customerSalesMap fonksiyonundaki gibidir. <br>'                   
    text = text + 'Count ve MinPercentage parametrelerinin islevleri customersOfProfile fonksiyonundaki islevleriyle aynidir. <br><br>'                   
    text = text + 'distanceType parametresinin alabilecegi degerler ve ifade ettigi uzakliklar asagidaki gibidir.'                   
    text = text + '<table border="1" width=1150>'
    text = text + '<tr><td> 0 </td><td> 1 </td><td> 2 </td><td> 3 </td></tr><br>'                   
    text = text + '<tr><td> Kullback-Leibler (KL) Divergence </td><td> Itakura-Saito (IS) Distance </td><td> Hellinger Distance </td><td> Euclidean Distance </td></tr><br>'                  
    text = text + '<tr><td> KL(P,Q) = P * log(P/Q) - P + Q </td><td> IS(P,Q) = (P/Q) * log(P/Q) - 1 </td><td> H(P,Q) = (1/sqrt(2)) * sqrt((sqrt(P) - sqrt(Q))*(sqrt(P) - sqrt(Q))) </td><td> EUC(P,Q) = (1/2) * (P-Q) * (P-Q) </td></tr><br>'                  
    text = text + '</table><br>'                  
    text = text + 'searchType parametresinin alabilecegi degerler ve anlamları asagidaki gibidir.'                  
    text = text + '<table border="1" width=500>'                  
    text = text + '<tr><td> 0 </td><td> 1 </td><br>'                  
    text = text + '<tr><td> Bütün müşterilerde ara </td><td> Sadece o profildeki müşterilerde ara </td></tr><br>'                  
    text = text + '</table><br>'
    text = text + 'searchType parametresi 1 değerini aldığında, input olarak ayrıca profilin id numarasının ve isminin verilmesi gerekiyor (customersOfProfile fonksiyonunda kullanılan). <br><br>'         
    text = text + 'baseCount parametresi, benzer urunlerin kac musteri temel alinarak hesaplanacagini belirtiyor. Parametre 0 degerini aldiginda, o profildeki/listedeki butun musteriler icin calisiyor. <br><br> '            
    text = text + 'productCount parametresi, musterilere onerilen ilk kac urunu goz onunde bulunduracagimizi belirtiyor. <br><br>'          
    text = text + 'baseCount ve productCount parametrelerine verilen degerlere gore fonksiyonun calisma suresinde farkliliklar oluyor. <br><br>'      
    text = text + 'Musterilerin benzerlik yuzdesi bu formulle hesaplaniyor; percentage = 100 - (100 * distance / maxDistance) <br><br>'             
    text = text + '<b> Input: </b> %s:%d/<b>similarCustomers</b>?jsonData=<b>{"id": 1279930, "xAxis":1, "yAxis": 2, "type": 2, "distanceType": 3, "Count":15, "MinPercentage":10, "productCount": 10, "baseCount": 50, "recommenderType": "mix", "searchType": 1, "ProfileId": 123, "ProfileDs": "Bebek", "slots": [{"x":0,"y":8},{"x":10,"y":20},{"x":20,"y":24}]} </b><br>' % (SERVER_IP, PORT)            
    text = text + '<b> Output: </b> {"Customers": [{"distances": 0, "percentage": 100, "id": 1279930}, {"distances": 35, "percentage": 72, "id": 1406410}, {"distances": 42, "percentage": 66, "id": 1058305}, {"distances": 42, "percentage": 66, "id": 1366933}, {"distances": 44, "percentage": 65, "id": 91248}], "Products": [{"id": 12680, "percentage": 62}, {"id": 12667, "percentage": 48}, {"id": 20083, "percentage": 48}, {"id": 12700, "percentage": 46}, {"id": 12677, "percentage": 46}, {"id": 12719, "percentage": 44}, {"id": 12678, "percentage": 38}, {"id": 10981, "percentage": 36}, {"id": 12689, "percentage": 32}, {"id": 12668, "percentage": 27}], "MinDistance": 0, "MaxDistance": 128} <br>'                 
    text = text + 'Bu ornekte 1279930 numarali musterinin alim aliskanligina (haftalara ve saat araliklarina gore, alisveris yapip yapmadigi) en cok benzerlik gosteren, profil uygunlugu %60in uzerinde olan maksimum 5 musteri listeleniyor.'                 
    text = text + 'Bu müşteriler, 11 numaralı Bebek profilindeki müşterilerden seçiliyor. <br><br>'         
    text = text + 'Bu ornekte benzerlik yuzdeleri su sekilde hesaplaniyor (maxDistance=128): <br>'
    text = text + 'Musterinin kendisine olan uzakligi distance(1279930,1279930) = 0. percentage = 100 <br>'                 
    text = text + '1406410 id numarali musteriye olan uzakligi distance(1279930,1406410) = 35. percentage = 100 - (100 * 35 / 128) = 72 <br>'             
    text = text + 'Musterinin kendisine en benzemeyen kisiyle olan uzakligi distance = maxDistance. percentage = 100 - (100 * 128 / 128) = 0 <br><br>'                 
    text = text + 'Bu ornekte onerilen urunleri inceledigimizde; <br>'                  
    text = text + '12680 id numarali urun, 50 kisiden (baseCount) 31 kisiye onerilmis. O yuzden onerilme yuzdesi 62 olarak hesaplaniyor. <br> '                 
    text = text + '12667 id numarali urun, 50 kisiden 24 kisiye onerilmis. O yuzden onerilme yuzdesi 48 olarak hesaplaniyor. <br><br> '                 
    text = text + 'Ornek olarak kullanilabilecek musteri idleri: 1073258, 999538, 1155093. <br><br>'
    return text

def getCustomerWeblogFunction(SERVER_IP, PORT):        
    text = '<h3> customerWeblog </h3>'
    text = text + 'Verilen musteri idsine gore, webdeki hareket grafiklerinin url bilgisi dondurulur. <br><br>'              
    text = text + '<b> Input: </b> %s:%d/<b>customerWeblog</b>?jsonData=<b>{"id": 90412} </b><br>' % (SERVER_IP, PORT)               
    text = text + '<b> Output: </b> {"image_url": "%s:%d/files/90412_webmatrix.png","image_url_graph": "{SERVER_IP}:{PORT}/files/90412_webgraph.png"} <br>'               
    text = text + 'Ornek olarak kullanilabilecek musteri idleri: 1073258, 999538. <br><br>'           
    return text

def getRecommendProductsFunction(SERVER_IP, PORT):        
    text = '<h3> recommendProducts </h3>'
    text = text + 'Verilen musteri idsi, tavsiye tipi ve sayiya gore onerilen urunlerin idleri dondurulur. <br>'              
    text = text + 'Su anda onerilen urunlerin IdUrunGrup3 degerleri donduruluyor. Ilerleyen asamalarda IdUrun degerleri dondurulecek. <br><br> '              
    text = text + 'type parametresi oneri listesinin nasil duzenlenecegini belirtiyor. Parametrenin alabilecegi degerler ve anlamlari asagidaki gibidir. '              
    text = text + '<table border="1" width=800>'               
    text = text + '<tr><td> mix </td><td> Hem simdiye kadar alinan hem de henuz alinmamis ama alinma ihtimali yuksek urunler listelenir </td></tr><br>'               
    text = text + '<tr><td> discover </td><td> Yalnizca henuz alinmamis ama alinma ihtimali yuksek urunler listelenir </td></tr><br>'                
    text = text + '<tr><td> habit </td><td> Yalnizca simdiye kadar alinan urunler listelenir </td></tr><br>'                 
    text = text + '</table><br>'
    text = text + '<b> Input: </b> %s:%d/<b>recommendProducts</b>?jsonData=<b>{"id": 737293, "type": "mix", "Count":5, "criteria": 1} </b><br>' % (SERVER_IP, PORT) 
    text = text + '<b> Output: </b> {"Products": [{"id": 597}, {"id": 454}, {"id": 457}, {"id": 553}, {"id": 636}]} <br>'                  
    text = text + 'Bu ornekte 737293 numarali musteri icin maksimum 5 tane urun oneriliyor. Urun listesi musterinin hem simdiye kadar aldigi hem de henuz almadigi fakat alma ihtimali yuksek urunlerden olusuyor. <br><br>'                 
    return text
  
def getRecommendProducts2Function(SERVER_IP, PORT):        
    text = '<h3> recommendProducts2 </h3>'
    text = text + 'Verilen musteri idsi, tavsiye tipi ve sayiya gore onerilen urunlerin idleri dondurulur. <br>'              
    text = text + 'Bu fonksiyonda kullanilan dataset, serverin geri kalanindan farkli. Butun server bu datasete gore update edilecek. <br>'
    text = text + 'Dataset 05.01.2015 00:00 - 18.07.2016 14:00 tarihleri arasinda yapilan satislari kapsiyor. <br>'            
    text = text + '81 Hafta, 7 Gun, 24 Saat, 7.269 Urun, 3.392 Musteri <br><br>'
    text = text + 'type parametresi oneri listesinin nasil duzenlenecegini belirtiyor. Parametrenin alabilecegi degerler ve anlamlari asagidaki gibidir. '              
    text = text + '<table border="1" width=800>'               
    text = text + '<tr><td> mix </td><td> Hem simdiye kadar alinan hem de henuz alinmamis ama alinma ihtimali yuksek urunler listelenir </td></tr><br>'               
    text = text + '<tr><td> discover </td><td> Yalnizca henuz alinmamis ama alinma ihtimali yuksek urunler listelenir </td></tr><br>'                
    text = text + '<tr><td> habit </td><td> Yalnizca simdiye kadar alinan urunler listelenir </td></tr><br>'                 
    text = text + '</table><br>'
    text = text + '<b> Input: </b> %s:%d/<b>recommendProducts2</b>?jsonData=<b>{"id": 737293, "type": "mix", "Count":5, "criteria": 2} </b><br>' % (SERVER_IP, PORT) 
    text = text + '<b> Output: </b> {"Products": [{"id": 32823}, {"id": 18110}, {"id": 18109}, {"id": 1808}, {"id": 18107}]} <br>'
    text = text + 'Bu ornekte 737293 numarali musteri icin maksimum 5 tane urun oneriliyor. Urun listesi musterinin hem simdiye kadar aldigi hem de henuz almadigi fakat alma ihtimali yuksek urunlerden olusuyor. <br><br>'
    return text

def getFunctions(SERVER_IP, PORT):
    text = '<h2> Fonksiyonlar </h2>'
    text = text + getCustomersOfProfileFunction(SERVER_IP, PORT)
    text = text + getCustomerSalesMapFunction(SERVER_IP, PORT)
    text = text + getSimilarCustomersFunction(SERVER_IP, PORT)
    text = text + getCustomerWeblogFunction(SERVER_IP, PORT)
    text = text + getRecommendProductsFunction(SERVER_IP, PORT)
    text = text + getRecommendProducts2Function(SERVER_IP, PORT)
    return text

def getFinishedItems():
    text = '<h2> Bitirilen Isler </h2>'
    text = text + '* 22.09.2016 Database icin CustomerMapping.txt, ItemMapping.txt ve SalesTensor.txt dosyalari olusturuldu.<br>'
    text = text + '* 20.09.2016 recommendProducts2 fonksiyonu hizlandirildi.<br><br>'
    return text

def getDatasetStructure():
    filename = 'otherFiles/newDb.png'
    text = '<h2> Dataset Yapisi </h2>'
    text = text + '<img src="%s">' % filename
    return text

def getHtmlContent(SERVER_IP, PORT):
    htmlContent = '<html><head><h1> Obase Tornado Server - Version 2 </h1></head><body>'
    htmlContent = htmlContent + getUpdateDetails()
    htmlContent = htmlContent + getToDoItems()
    htmlContent = htmlContent + getDatasetDetails()
    htmlContent = htmlContent + getFunctionTemplate(SERVER_IP, PORT)
    htmlContent = htmlContent + getFunctions(SERVER_IP, PORT)
    htmlContent = htmlContent + getFinishedItems()
    htmlContent = htmlContent + getDatasetStructure()
    htmlContent = htmlContent + '</body></html>'
    
    return htmlContent