import webbrowser
import requests
from threading import Thread
from flask import Flask, render_template, request, json
from queue import Queue
import socket
s = requests.Session()
app = Flask(__name__)


 
def UDP_Server(out_q):
    UDP_PORT       = 5001
    UDP_IP         = "192.168.66.3"
    UDP_bufferSize = 1024

    msgFromServer  = "NDI Switcher is up"
    bytesToSend    = str.encode(msgFromServer)
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((UDP_IP, UDP_PORT))

    print("Server is up")

    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(UDP_bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        
        clientMsg = "Message:{}".format(message)
        clientIP  = "Client IP:{}".format(address)
        
        #print(clientMsg)
        #print(message.decode())
        #print(clientIP)
        
        UDPServerSocket.sendto(bytesToSend, address)
        out_q.put(message.decode())
        #Test()
        
        msgDecode = message.decode()
        
        if msgDecode == "/device/1/get/ping":
            #get_ping()
            print("ping")
            msgFromServer = "I am alive"
            bytesToSend    = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
            
            
        if msgDecode == "/device/1/get/ndi-sources":
            #ten_sec()
            print("get-ndi-sources")
            #Source 1
            msgFromServer1 = '{"status": 0, "sources": [{"ndi-name": "MAGEWELL (USB Capture HDMI (D206191017871))", "ip-addr": "192.168.1.192:5963"}, {"ndi-name": "MAGEWELL (USB Capture HDMI (D206191017889))", "ip-addr": "192.168.1.192:5961"}]}'
            bytesToSend    = str.encode(msgFromServer1)
            UDPServerSocket.sendto(bytesToSend, address)
            #2
            #msgFromServer2 = '[2]{"Desktop-VRF01D - Nvidia Geforce 1050"}'
            #bytesToSend    = str.encode(msgFromServer2)
            #UDPServerSocket.sendto(bytesToSend, address)
            #3
            #msgFromServer3 = '[3]{"Desktop-VRF01D - Resolume Screen 1"}'
            #bytesToSend    = str.encode(msgFromServer3)
            #UDPServerSocket.sendto(bytesToSend, address)
            #4
            #msgFromServer4 = '[4]{"Pro convert - HDMI-NDI"}'
            #bytesToSend    = str.encode(msgFromServer4)
            #UDPServerSocket.sendto(bytesToSend, address)
            
        if msgDecode == "/device/1/set/ndi-source/1":
            get_ping()
            print("Source 1")
            msgFromServer = 'Source 1 is now selected, Signal name is"{"Desktop-VRF01D - Test Patterns"}'
            bytesToSend    = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
            selectedSource = '{"Desktop-VRF01D - Test Patterns"}'
            
        if msgDecode == "/device/1/set/ndi-source/2":
            get_ping()
            print("Source 2")
            msgFromServer = 'Source 2 is now selected, Signal name is"{"Desktop-VRF01D - Nvidia Geforce 1050"}'
            bytesToSend    = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
        
        if msgDecode == "/device/1/set/ndi-source/3":
            get_ping()
            print("Source 3")
            msgFromServer = 'Source 3 is now selected, Signal name is"{"Desktop-VRF01D - Resolume Screen 1"}'
            bytesToSend    = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
            
        if msgDecode == "/device/1/set/ndi-source/4":
            get_ping()
            print("Source 4")
            msgFromServer = 'Source 4 is now selected, Signal name is"{"Pro convert - HDMI-NDI"}'
            bytesToSend    = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
        
        if msgDecode == "/device/1/set/reboot":
            get_ping()
            print("Reboot 1")
            msgFromServer = 'I am not broken, but i restart anyway.... Please wait a minute before reconnecting'
            bytesToSend    = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
            
        if msgDecode == "/device/1/get/get-eth-status":
            #get_ping()
            print("Get eth status")
            msgFromServer = '{"status": 0, "use-dhcp": true}'
            #"{'status': 0, 'use-dhcp': true}"
                                 
            
            bytesToSend    = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
             
        
        if msgDecode == "/device/1/get/get-ndi-config":
            
            print("Get ndi config")
            msgFromServer = "1"
            bytesToSend    = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
        
            
q = Queue()
t1 = Thread(target=UDP_Server, args = (q, ), daemon=True)
t1.start()
    
    
try:
    with open("Response.json") as file1:
        Data = json.load(file1)
        #y = json.dumps(Data, sort_keys=True)
        
    with open("Signal_list.json") as file2:
        Data1 = json.load(file2)
        #y = json.dumps(Data1, sort_keys=True)
        #print(Data1)
except:
    print("fuck")



url = "http://192.168.66.1/mwapi?"       


def login_mw():  
    password = "e3afed0047b08059d0fada10f400c1e5"
    payload = {
                "method":"login",
                "id":"Admin",
                "pass":"e3afed0047b08059d0fada10f400c1e5"
              }
    
    login_magewell = s.get(url, params=payload)
    print("pass")
login_mw()
        
def get_summary():
    payload = {"method":"get-summary-info"}
    sum_info = s.get(url, params=payload)
    f = open("Response.json", "w")
    f.write(sum_info.text)
    f.close()
    print(sum_info.text)
    
def get_ping():
    payload = {"method":"ping"}
    sum_info = s.get(url, params=payload)
    f = open("Response.json", "w")
    

    


def sel(evt):
    
    selection = l1.get(l1.curselection())
    payload = {"method":"set-channel",
               "ndi-name":"true",
               "name":selection
               }
    ndi_list = s.get(url, params=payload)
    get_summary()
    signal_sel()
    print(selection)
    

app = Flask(__name__)
@app.route('/')
def home():
        return render_template('index.html', var1 = "test")
    




@app.route('/Device 1', methods=['POST'])
def ten_sec():
    if request.method == 'POST':
        payload = {"method":"get-ndi-sources"}
        ndi_list = s.get(url, params=payload)
        f = open("Signal_list.json", "w")
        f.write(ndi_list.text)
        f.close()
        print(ndi_list.text)
        
        return "OK"
    else:
        return "no ok"

@app.route('/api/<name>/') 
def api_get_name(name): 
    return json.jsonify({ 
        'name': name 
    })
    print("ok var")
 
 
if __name__ == '__main__': 
    app.run() 
