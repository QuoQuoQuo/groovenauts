import base64
import urllib.request
import json
import time


class Magellan:

    def __init__(self, sex):
        if sex == 'male':
            pass
        elif sex == 'female':
            pass
        self.blocks_designer = 'ysmr3104blocksboard2ced63ca'
        self.blocks_flow = 'model1'
        self.headers = {"Content-Type": "application/json",
                        "Authorization": "Bearer 1eae21064b2548517d4c8e893546fb697dd30e241152067a20d8c25bb26858f2"}
        self.job_id = ""
        self.json_data = ""
        self.status = ""

    def image_to_base64(self, image_str):
        b64 = base64.encodebytes(open(image_str, 'rb').read())
        blocks_json = {'_': {'key': image_str, 'image': {'b64': b64.decode('utf8')}}}
        self.json_data = json.dumps(blocks_json).encode('utf-8')

    def start_flow(self):
        url = "https://" + self.blocks_designer + ".magellanic-clouds.net/flows/" + self.blocks_flow + ".json"
        method = "POST"
        headers = self.headers
        request = urllib.request.Request(url, data=self.json_data, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            json_obj = json.loads(response_body)
            result = json_obj['result']
            self.job_id = json_obj['job_id']
            if result is True:
                print("flow starting is successed.")
            else:
                print("flow starting is failed.")

    def check_status(self):
        url = "https://" + self.blocks_designer + ".magellanic-clouds.net/flows/" + self.blocks_flow + "/jobs/" + str(
            self.job_id) + "/status.json"
        method = "GET"
        headers = self.headers
        request = urllib.request.Request(url, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            json_obj = json.loads(response_body)
            self.status = json_obj['status']
            print(self.status)

    def check_result(self):
        url = "https://" + self.blocks_designer + ".magellanic-clouds.net/flows/" + self.blocks_flow + "/jobs/" + str(
            self.job_id) + "/variable.json"
        method = "GET"
        headers = self.headers
        request = urllib.request.Request(url, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            json_obj = json.loads(response_body)
            print(json_obj)
            return json_obj

    def predict(self, image_str):
        self.image_to_base64(image_str)
        self.start_flow()
        while True:
            time.sleep(1)
            self.check_status()
            if self.status in ['finished', 'failed', 'canceled']:
                return self.check_result()
