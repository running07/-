# -*- coding:utf-8 -*-

import os
import urllib2
import poster.encode
import tornado.gen
from poster.streaminghttp import register_openers
from chat import AccessToken


class UploadMaterial(object):

    def __init__(self):
        register_openers()


    def upload(self,access_token,filename):
        # access_token = yield AccessToken.get_access_token()
        # access_token='15_dsraChMKQ_xlOZzpAVKCnfwaII_yoQZZ8b8GLvvBj_CdACR1uOLgRkMElE8y78lk6EZ7FkAzdULi3Czcl0IsvKgUsdlk4Otg6AJpEK83HWQqy7zj5ELt17XtPU_OFJ5_SOIzJpZJUggbiwpDRNBjAJADZN'
        # print access_token,'access_toekn'
        media_type = 'image'

        openfile = open(filename, 'rb')
        param = {'media': openfile}
        postData, postHeader = poster.encode.multipart_encode(param)
        posturl = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" % (
            access_token,media_type)
        request =  urllib2.Request(posturl, postData, postHeader)
        urlResp = urllib2.urlopen(request)
        # print posturl
        print urlResp.read()
        return


if __name__ == '__main__':
    myMedia = UploadMaterial()
    access_token='15_Xo7jXb7F1jVtZTo1F07ZDkCqrYvO9pt6d2f4gjxXK3scJTy5GEPJWOSPoSPBmwCRk4O_WwdZT1N9nWq2NUucovFRSBxWgEF2k6t3lW7_2w-H8r5h_F5fuuPuUctMmL5M2Vf4ny5ZmidKCVKvJASiAIAWNF'
    DIR = 'statics/media/'
    print os.getcwd()
    for filename in os.listdir(DIR):
        filename = DIR + filename
        print filename
        try:
            open(filename,'r')
        except Exception as e:
            print e
        myMedia.upload(access_token,filename)
