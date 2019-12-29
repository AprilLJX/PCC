#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from random import choice
client = AcsClient('LTAI4FoqkVAaNdyWkFNQv1Kk', 'DTfwoggcKGA3E3xQVwxP6pnkq34k7s', 'cn-hangzhou')

# 定义一个种子，从这里面随机拿出一个值，可以是字母
seeds = "1234567890"
# 定义一个空列表，每次循环，将拿到的值，加入列表
random_num = []
# choice函数：每次从seeds拿一个值，加入列表
for i in range(4):
    random_num.append(choice(seeds))
# 将列表里的值，变成四位字符串
random_str = "" . join(random_num)
code = "{\"code\":\""+random_str+"\"}"
request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2017-05-25')
request.set_action_name('SendSms')

request.add_query_param('RegionId', "cn-hangzhou")
request.add_query_param('SignName', "拼车车")
request.add_query_param('TemplateCode', "SMS_181501054")
request.add_query_param('TemplateParam', code)

request.add_query_param('PhoneNumbers', "15387594636")


response = client.do_action(request)
# python2:  print(response)
print(str(response, encoding = 'utf-8'))
