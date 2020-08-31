from pymavlink import mavutil
master = mavutil.mavlink_connection("udpin:0.0.0.0:14550")

def get_imu_data():
	while True:
	    msg = master.recv_match()
	    if not msg:
	        continue
	    if msg.get_type() == 'RAW_IMU':
	    	data = str(msg)
	    	try:
		    	data = data.split(":")
		    	xacc = data[2].split(",")[0]
		    	yacc = data[3].split(",")[0]
		    	zacc = data[4].split(",")[0]
		    	xgyro = data[5].split(",")[0]
		    	ygyro = data[6].split(",")[0]
		    	zgyro = data[7].split(",")[0]
		    	xmag = data[8].split(",")[0]
		    	ymag = data[9].split(",")[0]
		    	zmag = data[10].split(",")[0][0:-1]
	    	except:
	    		print(data)
	    	print("RAW_IMU Data: ",xacc,yacc,zacc,xgyro,ygyro,zgyro,xmag,ymag,zmag)
get_imu_data()
