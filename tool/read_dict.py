from read_image import connect
import json
res = connect()
print(res)
data_dict = eval(res)
data_json = json.dumps(data_dict)
file_path = './data/data.json'
with open(file_path, 'w') as f:
    json.dump(data_json, f, indent=4)
