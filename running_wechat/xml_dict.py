# -*- coding:utf-8 -*-
import xmltodict
import hashlib

xml_str = """
<xml>
<ToUserName><![CDATA[gh_866835093fea]]></ToUserName>
<FromUserName><![CDATA[ogdotwSc_MmEEsJs9-ABZ1QL_4r4]]></FromUserName>
<CreateTime>1478317060</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[你好]]></Content>
<MsgId>6349323426230210995</MsgId>
</xml>
"""

xml_dict = xmltodict.parse(xml_str)
print type(xml_dict)
print xml_dict['xml']
xml_data = xml_dict['xml']
for key, value in xml_data.items():
    print '%s=%s' % (key, value)

print
print
# xml_str = dict(xml=dict(ToUserName=u'gh_866835093fea',
#                         FromUserName=u'ogdotwSc_MmEEsJs9-ABZ1QL_4r4',
#                         CreateTime=u'1478317060',
#                         MsgType=u'text',
#                         Content=u'你好',
#                         MsgId=u'6349323426230210995'))
# print xmltodict.unparse(xml_str,pretty=True)
xml_content = {
                'ToUserName': u'ogdotwSc_MmEEsJs9-ABZ1QL_4r4',
                'FromUserName': u'1478317060',
                'CreateTime': u'1478317060',
                'MsgType': 'text',
                'Content': u'你好',
            }
print xmltodict.unparse({'xml':xml_content},pretty=True)