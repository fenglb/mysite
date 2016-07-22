from django.shortcuts import render
from django.core import serializers
from .WXBizMsgCrypt import WXBizMsgCrypt

# Create your views here.

Token = "fengliubinxmunmrcen"
EncodingAESKey = "LlOjJfg6ohuB5HR6XxmOggajsNJMxgaQZ06px2Emqjb"
CorpID = "wx0d42078f5b6314e1"

def index(request):
    if request.method == 'GET':
        msg_signature = request.GET['msg_signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        echostr = request.GET['echostr']
        xml = WXBizMsgCrypt(Token, EncodingAESKey, CorpID)
        ret, reply = xml.VerifyURL(msg_signature, timestamp, nonce, echostr)

        return render(request, 'weixin/index.xml', {'msg_signature': msg_signature, 'timestamp': timestamp, 'nonce': nonce, 'echostr':reply})
