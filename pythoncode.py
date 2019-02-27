import requests
# import pandas
import os
import json
import re
import math
from dateutil.parser import parse
from datetime import datetime
import pytz
from dateutil import tz
import sys
from flask import Flask, request, render_template
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
 
@app.route('/')
def form():
   return render_template('form.html')

@app.route("/data",methods=['POST'])
def data():
	# print(request.form.items())
	
	url_string = request.form['stringInput']
	
	print("URL"+url_string)
	url_string = url_string.split("/")
	user_id = url_string[len(url_string)-2]
	repo = url_string[len(url_string)-1]

	api_url_gen = "http://api.github.com/repos/<x>/<y>"

	api_url_gen = re.sub("<x>",user_id,api_url_gen)
	api_url_gen = re.sub("<y>",repo,api_url_gen)

	print("Git API: "+api_url_gen)

	try:
		res = requests.get(api_url_gen, auth=HTTPBasicAuth('saumya1593','Zindagi@123'))
		print("Ststus Code: "+str(res.status_code))
		if res.status_code == 200:
			pass
		else:
			return render_template("error.html")
			sys.exit()
	except:
	    return render_template("error.html")
	try:
		res = requests.get(api_url_gen)
	except:
		return render_template("error.html")

	json_content= json.loads(res.text)
	total_open_issues = json_content['open_issues_count']

	no_of_pages = math.ceil(total_open_issues/100)

	api_url = "https://api.github.com/repos/" + user_id + "/" + repo + "/issues?page=<ff>&per_page=100"

	total_issues = []
	issues_opened_in_last_24 = []
	issues_opened_in_1_to_7 = []
	issues_opened_in_more_than_7 = []
	for i in range(1,(no_of_pages+1)):
	    url = re.sub("<ff>",str(i),api_url)
	    response = requests.get(url,auth=HTTPBasicAuth('saumya1593','Zindagi@123'))
	    issue_json_content= json.loads(response.text)
	    for j in range(len(issue_json_content)):
	        issue_dict = issue_json_content[j]
	        total_issues.append(datetime.now(pytz.utc) - parse(issue_dict['created_at']))
	        x = datetime.now(pytz.utc) - parse(issue_dict['created_at'])
	        if x.days == 0:
	            issues_opened_in_last_24.append(x)
	        elif x.days > 0 and x.days <= 7:
	            issues_opened_in_1_to_7.append(x)
	        else:
	            issues_opened_in_more_than_7.append(x)

	total_issues = len(total_issues)
	issues_opened_in_last_24 = len(issues_opened_in_last_24)
	issues_opened_in_1_to_7 = len(issues_opened_in_1_to_7)
	issues_opened_in_more_than_7 = len(issues_opened_in_more_than_7)   
	        
	# print(time.time()-st)
	print(total_issues)
	print(issues_opened_in_last_24)
	print(issues_opened_in_1_to_7)
	print(issues_opened_in_more_than_7) 
	return render_template("data.html",total_issues=total_issues,issues_opened_in_last_24=issues_opened_in_last_24,issues_opened_in_1_to_7=issues_opened_in_1_to_7,issues_opened_in_more_than_7=issues_opened_in_more_than_7)
	
	
if __name__ == "__main__":
	# app.run(debug = True)
	# Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
