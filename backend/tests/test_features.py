# tests/test_features.py
print("Début des tests")
import requests

print("Début des tests")
import requests

url   = "http://127.0.0.1:5000/upload"
files = {'image': open('../tests/sample.jpg','rb')}  # si vous êtes dans backend/tests/
data  = {'annotation': 'pleine'}

resp = requests.post(url, files=files, data=data)

print("Status code:", resp.status_code)
print("Response body:", resp.text)

resp = requests.post(url, files=files, data=data)
assert resp.status_code == 201
print("assert 1 passé")
assert "annotation_auto" in resp.json()
print("assert 2 passé")
getr = requests.get("http://127.0.0.1:5000/images")
assert getr.status_code == 200
print("assert 3 passé")
found = any(i["annotation_auto"] in ("pleine","vide") for i in getr.json())
assert found

print("Tests passés ")
