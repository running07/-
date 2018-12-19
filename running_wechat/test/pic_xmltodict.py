# -*- coding:utf-8 -*-
import xmltodict
pic_xml="""
 <xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<PicUrl><![CDATA[this is a url]]></PicUrl>
<MediaId><![CDATA[media_id]]></MediaId>
<MsgId>1234567890123456</MsgId>
</xml>"""
dic=xmltodict.parse(pic_xml)['xml']
print dic
for key ,value in dic.items():
    print key,value

'''
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<Image>
<MediaId><![CDATA[media_id]]></MediaId>
</Image>
</xml>
'''
dic_data={
"ToUserName": "toUser",
"FromUserName" :"fromUser",
"CreateTime" :"1348831860",
"MsgType" :"image",
"Image":{"MediaId":"media_id"},
}
pic_xml=xmltodict.unparse({"xml":dic_data},pretty=True)
print pic_xml