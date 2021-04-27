from flask import Flask
from flask import jsonify
from flask import request
import json
from runSLAM import RunBreezySlam
from data_utils import *
import time
app = Flask(__name__)
lidarScans=[]
@app.route('/', methods=["GET"])
def index():
    time.sleep(10)
    return "Hello, World!"


@app.route('/clear',methods=["GET"])
def clear():
	with open ("lidar_data",'w') as file:
		file.truncate(0)
	return "Success"


@app.route('/update',methods=["POST"])
def updateFile():
	to_add=json.loads(request.get_json())
	with open ("lidar_data",'a') as file:
		if not isinstance(to_add[0], list):
			for j in range(len(to_add)):
				s=str(to_add[j])
				if j<len(to_add)-1:
					s+=" "
				file.write(s)
			file.write("\n")
		else:
			for i in to_add:
				for j in range(len(i)):
					s=str(i[j])
					if j<len(i)-1:
						s+=" "
					file.write(s)
				file.write("\n")
	return jsonify(to_add)
@app.route('/slam',methods=["GET"])
def do_slam():
	d={}
	arr=RunBreezySlam("lidar_data",True,9999)
	arr=arr.tolist()
	return json.dumps(arr)


@app.route('/check',methods=["GET"])
def check():
	return json.dumps(np.loadtxt("lidar_data").tolist())
if __name__ == '__main__':
    app.run(debug=True)


#comma_to_space("lidar_readings.csv","lidar_data")
#remove_empty_line("lidar_data.dat","lidar_data")

#RunBreezySlam("lidar_data",False,9999)


