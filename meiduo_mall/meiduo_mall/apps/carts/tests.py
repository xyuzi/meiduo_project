from django.test import TestCase

# Create your tests here.
import pickle
import base64

dict = {
    'name': 'nnk',
    'age': 8,
    'like': 'none'
}
print(dict)
# 加密
# data_by = pickle.dumps(dict)
# print(data_by)
# data_by64 = base64.b64encode(data_by)
# print(data_by64)
# 解密
# data64 = base64.b64decode(data_by64)
# print(data64)
# data = pickle.loads(data64)
# print(data)
data_by64 = base64.b64encode(pickle.dumps(dict)).decode()
print(data_by64)
data = pickle.loads(base64.b64decode(data_by64))
print(data)