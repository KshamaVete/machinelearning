import sys
sys.path.append('libraries')

import requests
import time

counter=0
while(counter<10):
	f=requests.get("http://localhost:5000/getstatus")
	print (f.json())
	time.sleep(4)
	counter+=1
