import urllib
import json
import os
import urllib2
from urllib2 import urlopen
import time
import datetime
import re
import math
from flask import Flask
from flask import request
from flask import make_response

# start app in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)

	print('Request:')
	print(json.dumps(req, indent=4))

	res = makeWebhookResult(req)

	res = json.dumps(res, indent=4)
	print(res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

def makeWebhookResult(req):
	
	# demo account login - use manual request key everyday
	#login_url= 'https://api.sikkasoft.com/auth/v2/provider_accounts?un=ddemo2&pw=$Sikka4040&app_id=cf345eef7cb42a39cff6972d57fe6149&app_key=8003044355153fe930ec82ca091e334e&encrypted=false&device_id=fOinX6aGKzc:APA91bHer7V6YQM5re379jNRlc4fnXBmo3ElTB0ivPgINJ76HURuabkzKXmXFZ2ITk9yBFHHDu3dCbq2s8RcuDhWdqyC8BYSAdajjp8ep3TaC_T8k4dHZJZJ-cDeH0NU6ZRjOY1O6ljb&device_type=android'
	#html = urlopen(login_url)
	#login_response = json.load(html)
	#request_key = login_response['profiles'][0]['request_key']
	#domain = login_response['profiles'][0]['profile_type']
	request_key = 'a53235cdca6a5ac9da353d6043dcc056'
	domain = 'Dental'
	
	speech = ""
	
	# get morning report
	today = ( datetime.datetime.utcnow() - datetime.timedelta(hours = 8) ).strftime("%Y/%m/%d")
	if(request_key):
		if req.get("result").get("action") == 'morning_report':
			url2  = 'https://api.sikkasoft.com/v2/sikkanet_cards/Morning%20Report?request_key='+request_key+'&startdate='+today+'&enddate='+today
			html2 = urlopen(url2)
        		response = json.load(html2)
			if(response):
				speech = "Read morning report..."
		elif req.get("result").get("action") == 'appointments':
			url3  = 'https://api.sikkasoft.com/v2/appointments?request_key='+request_key+'&startdate='+today+'&enddate='+today+'&sort_order=asc&sort_by=appointment_time&fields=patient_name,time,type,guarantor_name,length'
			html3 = urlopen(url3)
        		response = json.load(html3)
			if(response):
				speech = "Read schedule card..."

	return {
	 	"speech":speech,
	 	"displayText":speech,
	 	"source":"apiai-dental"
	 }

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000)) # flask is on 5000

	print "Starting app om port %d", port
	
	app.run(debug=True, port=port, host='0.0.0.0')
	
