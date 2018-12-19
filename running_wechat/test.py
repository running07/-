# -*- coding:utf-8 -*-
import json
import chardet

# with open('image_media_id2.json', 'r') as json_file:
   # data=json_file.read()
#    print type(data)
with open('image_media_id2.json', 'r') as json_file:
   item_dict = json.load(json_file)
print len(item_dict['item'])
for item in item_dict['item']:
    name= item['name']
    print type(name)
    # print chardet.detect(name)
#
    # item_dict = json.load(json_file)
# dict_data=json.dumps(data,ensure_ascii=False)
# print dict_data
# print type(dict_data)
# print item_dict
# for item in item_dict[u'item']:
#     print item
# with open('media_id.json', 'r') as json_file:
#     # data=json_file.read()
#     # print type(data)
#     item_dict = json.load(json_file)
#     print type(item_dict)
# for item in item_dict['item']:
#     print item
dict={'sex':0}
sex='男'if dict.get('sex')==1 else '女'
print sex