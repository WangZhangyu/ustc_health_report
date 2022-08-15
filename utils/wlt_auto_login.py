# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:23:21 2022

@author: Zhangyu Wang
"""


import subprocess
from subprocess import run, PIPE
import requests

class Wlt():

    def login_once(self,client,passwd):
        wlt_url = 'http://wlt.ustc.edu.cn/cgi-bin/ip'
        payload = {    'cmd':'login',
                       'url':'URL',
                       'name':client,
                       'password':passwd,
                       'set':'%D2%BB%BC%FC%C9%CF%CD%F8'
                }
        headers = {    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                       'Content-Type':'application/x-www-form-urlencoded',
                       'Connection':'keep-alive'
                   }
        
        
        r = requests.post(wlt_url,headers=headers,data = payload)
        return r
        
    
    def stat(self):
        from sys import platform
        if 'win' in platform:
            command = 'ping www.baidu.com'
        elif 'linux' in platform:
            command = 'ping -c 1 -W 0.1 www.baidu.com'
        else:
            command = ''
        r = subprocess.run(command,
                stdout=PIPE,
                stderr=PIPE,
                stdin=PIPE,
                shell=True)
        if r.returncode==0:
            print('wlt is good.')
            return True
        else:
            print('network error')
            return False


    def login(self,client,passwd,try_time_limits=5):
        try_time = 0
        while (not self.stat()) and try_time<=try_time_limits:
            if try_time==0:
                print('Connecting network...')
            else:
                print('retry -%d-' % try_time)
            self.login_once(client,passwd)
            try_time = try_time+1
        
