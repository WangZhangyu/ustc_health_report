# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 17:42:36 2022

@author: Zhangyu Wang
"""

import json
from bs4 import BeautifulSoup
from lxml import etree
from utils.ustc_passport_login import USTCPassportLogin
from utils.wlt_auto_login import Wlt 

# CAS身份认证url
cas_url = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'
# 打卡url
clock_in_url = 'https://weixine.ustc.edu.cn/2020/daliy_report'
# 每周报备url
report_url = 'https://weixine.ustc.edu.cn/2020/apply/daliy/ipost'
# 图片上传get url
upload_url = 'https://weixine.ustc.edu.cn/2020/upload/xcm'
# 图片上传post url
upload_image_url = 'https://weixine.ustc.edu.cn/2020img/api/upload_for_student'
# 每日进出校申请url
stayinout_apply_url = 'https://weixine.ustc.edu.cn/2020/apply/daliy/ipost'
# 身份认证token
token = ''


with open('user_info.json', encoding='utf-8') as f:
    user_info = json.loads(f.read().replace("'","\""))
    
    
# step1: 检查网络，登录网络通
client, passwd = user_info['wlt_user'],  user_info['wlt_pwd']
wlt = Wlt()
if not wlt.stat():
    wlt.login(client,passwd)

user_info.pop('wlt_user')
user_info.pop('wlt_pwd')

# step2: 开始打卡

for userid in user_info:   
    login_bot = USTCPassportLogin()
    sess = login_bot.sess
    is_success = login_bot.login(user_info[userid][0], user_info[userid][1])
    if is_success:
        print('健康系统登录成功\t%s\t%s' % (user_info[userid][2],user_info[userid][0]))
        response = sess.get(cas_url)
        s = BeautifulSoup(response.text, 'html.parser')
        token = s.find(attrs={'name': '_token'}).get('value')        
    else:
        print('健康系统登录失败\t%s\t%s' % (user_info[userid][2],user_info[userid][0]))
        continue
    
    # 获取历史打卡记录信息，便于构建post_data，开始打卡   
    response = sess.get('https://weixine.ustc.edu.cn/2020/home')
    html = etree.HTML(response.text)
    try:
        dorm_building = html.xpath('//*[@id="daliy-report"]/form/div/div[3]/div[1]/input')[0].values()[2]
        dorm = html.xpath('//*[@id="daliy-report"]/form/div/div[3]/div[2]/input')[0].values()[2]
        jinji_lxr = html.xpath('//*[@id="daliy-report"]/form/div/div[12]/div[1]/input')[0].values()[3]
        jinji_guanxi = html.xpath('//*[@id="daliy-report"]/form/div/div[12]/div[2]/input')[0].values()[3]
        jiji_mobile = html.xpath('//*[@id="daliy-report"]/form/div/div[12]/div[3]/input')[0].values()[3]
        
        post_data = {
                  "gps_now_address": "",
                  "dorm_building": dorm_building,
                  "dorm": dorm,
                  "body_condition": "1",
                  "body_condition_detail": "",
                  "has_fever": "0",
                  "last_touch_sars": "0",
                  "last_touch_sars_date": "",
                  "last_touch_sars_detail": "1",
                  "body_condition_detail": "",
                  "is_danger": "0",
                  "is_goto_danger": "0",
                  "jinji_lxr": jinji_lxr,
                  "jinji_guanxi": jinji_guanxi,
                  "jiji_mobile": jiji_mobile,
                  "other_detail": ""    
                }
    except:
        continue
    
    # daily daka
    post_data['_token'] = token
    response = sess.post(clock_in_url, data=post_data)
    
    s = BeautifulSoup(response.text, 'html.parser')
    msg = s.select('.alert')[0].text
    print('\t'+msg)
    from datetime import datetime as dt
    with open('daka.log','a') as fp:
        fp.write(dt.now().strftime('%Y.%m.%d %H:%M:%S')+msg+'\r')
    
  


