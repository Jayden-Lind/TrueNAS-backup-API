import requests
import json
import sys
import datetime

if len(sys.argv) != 4:
	sys.exit("Not enough args supplied")
else:
	hostname = sys.argv[1] 
	username = sys.argv[2]
	password = sys.argv[3]

	session = requests.session()

	session.auth = (username, password)

	base_url = f"http://{hostname}"

	download_url = base_url + "/api/v2.0/core/download"

	payload = json.dumps({
	"method": "config.save",
	"args": [],
	"filename": f"{hostname}.db",
	"buffered": False
	})

	response = session.post(download_url, data=payload)

	response_json = json.loads(response.text)

	backup_url = base_url + response_json[1]

	backup_file = session.get(backup_url)

	with open(f"{hostname}-{datetime.datetime.now().strftime('%I_%p_%d_%m_%Y')}.db", 'wb') as file:
		file.write(backup_file.content)
