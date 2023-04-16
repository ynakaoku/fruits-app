#!/usr/bin/python3
import socket
import cgi
from json import dumps
from pymongo import MongoClient
from pymongo import ASCENDING
from pymongo import DESCENDING
from bson.json_util import dumps, loads
from bson import decode

def get_host_info():
# Get Socket to investigate Pod address and hostname
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    h = socket.gethostname()
    return ip, h

def startup_db_client():
#    myclient = MongoClient("mongodb://localhost:27017/")
    myclient = MongoClient("mongodb://mongoadmin:password@172.19.64.14:32280/?authSource=fruitsdb&authMechanism=SCRAM-SHA-1") # nodeport
    print("Connected to the MongoDB database!")
    return myclient

def shutdown_db_client(myclient):
    myclient.close()
    print("Connection Closed!")

def find_from(mycol):
    if (data := mycol.find()) is not None:
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

# Check if Get query type is HTML or JSON, and get host ip nad hostname
form = cgi.FieldStorage()
query = form.getvalue("query")
ip, h = get_host_info()

#  connect to mongodb and get fruits table data
myclient = startup_db_client()

mydb   = myclient["fruitsdb"]
mycol  = mydb["fruits"]
cursor = mycol.find(projection={'_id':0, 'id':1, 'name':1, 'production':1, 'quantity':1}, sort=[('id',ASCENDING)])

#print(dumps(cursor, indent=2))

#for x in cursor:
#    print(x)

shutdown_db_client(myclient)

# Output html or json data based on query option
if "query" not in form or query == "html":

    color_seed = int(ip.split('.')[3]) % 6
    if color_seed == 0:
        color = '#FFA0A0'  # red
    if color_seed == 1:
        color = '#FFFFA0'  # yellow
    if color_seed == 2:
        color = '#A0FFA0'  # green
    if color_seed == 3:
        color = '#A0FFFF'  # bluegreen
    if color_seed == 4:
        color = '#A0A0FF'  # blue
    if color_seed == 5:
        color = '#FFA0FF'  # purple
    
    print("Content-Type: text/html;")
    print("")
    print("<!DOCTYPE html>")
    print("<html lang='ja'>")
    print("<head>")
    print("    <meta charset='utf-8'>")
    print("    <title>%s</title>" % ip)
    print("</head>")
    print("<body>")
    print("    <h1>NSX Solution Demo/Test Page")
    print("    <div style=\"background-color:%s;\">" % color)
    print("        <h2>IP address: %s</h2>" % ip)
    print("        <h2>Hostname: %s</h2>" % h)
    print("    </div>")
    for x in cursor:
        print(x)
    print("</body>")
    print("</html>")

elif query == "json":
    res = {"name":"NSX Solution Demo/Test Page", "address":ip, "hostname":h}
    print("Content-Type: text/json;")
    print("")
    print(dumps(res, indent=2, ensure_ascii=False))
    for x in cursor:
        print(x)

else:
    raise Exception("Invalid Parameter: query=" + query)

# end script