# -*- coding:utf-8 -*-
import sys
sys.path.append('..')

import urllib2
import poster.encode
import tornado.gen
from poster.streaminghttp import register_openers
from chat import AccessToken


class UploadMedia(object):

    def __init__(self):
        register_openers()


    def upload(self):
        # access_token = yield AccessToken.get_access_token()
        access_token='15_dsraChMKQ_xlOZzpAVKCnfwaII_yoQZZ8b8GLvvBj_CdACR1uOLgRkMElE8y78lk6EZ7FkAzdULi3Czcl0IsvKgUsdlk4Otg6AJpEK83HWQqy7zj5ELt17XtPU_OFJ5_SOIzJpZJUggbiwpDRNBjAJADZN'
        print access_token,'access_toekn'
        media_type = 'image'

        openfile = open('statics/media/gsl.jpg', 'rb')
        param = {'media': openfile}
        postData, postHeader = poster.encode.multipart_encode(param)
        posturl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (
            access_token,media_type)
        request = urllib2.Request(posturl, postData, postHeader)
        urlResp = urllib2.urlopen(request)
        print posturl
        print urlResp.read()
        return


if __name__ == '__main__':
    myMedia = UploadMedia()
    myMedia.upload()
