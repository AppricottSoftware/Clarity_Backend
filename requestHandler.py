#!/usr/bin/env python
from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
from urllib.parse import urlparse

import settings
import pymysql

# Simple routine to run a query on a database and print the results:
def printAllUsers(conn) :
    print("Running printAllUsers")
    cur = conn.cursor()

    cur.execute("select * from userData")
    for row in cur.fetchall():
        print(row)

def getUserPassword(conn, usernameString) :
    print("Running getUserPassword()")
    cur = conn.cursor()

    userPassword = "select password from userData where email=\"" + usernameString + "\";"

    cur.execute(userPassword)
    result = cur.fetchall()
    if result : 
        print("Found user... Returning User") 
        return result[0][0]
    else : 
        return 0
    
# Returns true if user creditentials is correct 
# Return false if not
def verifyUser(myConnection, userJson):
    print("Running verifyUser()")
    # Grabs the user's credentials 
    email = userJson["email"]
    password = userJson["password"]
    actualpass = getUserPassword( myConnection, email )

    print("Found password: ", password, "vs", getUserPassword( myConnection, email ))
    # Password accepted 
    if password == getUserPassword( myConnection, email ): 
        print("Found password: ", password)
        return True
    return False

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        request_path = self.path
        
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))

        print("Running Get")
        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)
        print("Request headers:", self.headers)

        # Grabbing the type of request and processes it accordingly 
        typeOfRequest = query_components["typeOfRequest"]

        # Case for login 
        if typeOfRequest == "verifyLogin": 
            myConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            printAllUsers(myConnection)
            if verifyUser(myConnection, query_components) is True : 
                print("TRUEEEEE") 
            else: 
                print("FALSEEEEE")
            myConnection.close()
            return

        print("<----- Request End -----\n")
        
        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")
        self.end_headers()
        return
      
    def do_POST(self):
        print("Running Post")
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)
        
        request_headers = self.headers
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0
        
        print("Content Length:", length)
        print("Request headers:", request_headers)
        print("Request payload:", self.rfile.read(length))
        print("<----- Request End -----\n")
        
        self.send_response(200)
        self.end_headers()
        return
    
    do_PUT = do_POST
    do_DELETE = do_GET
        
def main():
    port = 8080
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()
        
if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
                    "Run:\n\n"
                    "   reflect")
    (options, args) = parser.parse_args()
    
    main()
