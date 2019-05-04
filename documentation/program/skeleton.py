from flask import Flask,request
from multiprocessing import Queue
from threading import Thread
import math
import json

app=Flask(__name__)

dataQ=Queue()

@app.route("/",methods=["GET"])
def getData():
	if("data" in request.args):
		data=request.args["data"].split(",")  
		if(len(data)==10):
			dataQ.put(data)
			return "Success"
	return "Failed"

@app.route("/getstatus",methods=["GET"])
def getstatus():
	data={
			"selected_ads" : ads_selected,
			"total_reward" : total_reward
	}
	return json.dumps(data,indent=4)



# Algorithm
d=10
ads_selected=[]
number_of_selections= [0]*d # Keeping track of selections
sum_of_rewards= [0]*d
total_reward=0

def UCB(dataQ):
	global d
	global ads_selected
	global number_of_selections
	global sum_of_rewards
	global total_reward
	rounds=0
	while(True):
		dataset=dataQ.get()
		ad=0
		max_upper_bound=0
		for i in range(0,d):
			if(number_of_selections[i]>0):
				average_reward= sum_of_rewards[i]/number_of_selections[i]
				delta_i= math.sqrt(3/2 * math.log(rounds+1)/ number_of_selections[i])
				upper_bound = average_reward+ delta_i
			else:
				upper_bound= 1e400
			if(upper_bound>max_upper_bound):
				max_upper_bound=upper_bound
				ad=i
		ads_selected.append(ad)
		number_of_selections[ad]= number_of_selections[ad] + 1
		reward = int(dataset[ad])
		sum_of_rewards[ad]+= reward
		total_reward+=reward
		rounds+=1
		print ("Total  Reward",total_reward)
		print ("ads_selected",ads_selected)
		print ("number_of_selections",number_of_selections)


def main():
	t=Thread(target=UCB,args=(dataQ,))
	t.start()
	app.run("0.0.0.0",5000)

if __name__ == '__main__':
	main()



# To test the server
# http://localhost:5000/getstatus
# http://localhost:5000/?data=0,0,0,0,0,0,0,0,1,0