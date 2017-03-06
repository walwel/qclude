#-*- coding: UTF-8 -*- 
import urllib2
import json
import time



def youdao(word):
	qword = urllib2.quote(word)
	print("youdao_etc>>>",word)
	baseurl =r'http://fanyi.youdao.com/openapi.do?keyfrom=wx-walwal&key=1167095508&type=data&doctype=json&version=1.1&q='
	url = baseurl+qword
	resp = urllib2.urlopen(url)
	fanyi = json.loads(resp.read())
	print("youdao_etc fanyi>>>",fanyi)
	if fanyi['errorCode'] == 0:        
		if 'basic' in fanyi.keys():
			trans = u'%s:\n%s\n%s\n网络释义：\n%s'%(fanyi['query'],''.join(fanyi['translation']),' '.join(fanyi['basic']['explains']),''.join(fanyi['web'][0]['value']))
			return trans
		else:
			trans =u'%s:\n基本翻译:%s\n'%(fanyi['query'],''.join(fanyi['translation']))        
			return trans
	elif fanyi['errorCode'] == 20:
		return u'对不起，要翻译的文本过长'
	elif fanyi['errorCode'] == 30:
		return u'对不起，无法进行有效的翻译'
	elif fanyi['errorCode'] == 40:
		return u'对不起，不支持的语言类型'
	else:
		return u'对不起，您输入的单词%s无法翻译,请检查拼写'% word
