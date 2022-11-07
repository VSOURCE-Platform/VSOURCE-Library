#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Description: 
@Author: Kermit
@Date: 2022-10-06 12:30:47
@LastEditors: Kermit
@LastEditTime: 2022-11-05 16:17:20
'''

import os
import json
import time
import requests
import traceback
import vsource

import vsource.exceptions as exceptions
from vsource.login import login_instance
import vsource.configs as configs


def textbox_generate_sentence(version='', max_interval=configs.max_interval):
	# default version:
	algorithm_name = 'textbox-generate-sentence'
	algorithm_version = 'v1.0'
	algorithm_port = 17791
	algorithm_ip = '120.26.143.61'

	full_algorithm_name = algorithm_name+'-'+algorithm_version
	lower_name = full_algorithm_name.replace('-', '_').replace('.', '_').lower()
	upper_name = full_algorithm_name.replace('-', '_').replace('.', '_').upper()

	params = {
		'nonsense': 'nonsense',
	}
	submit_url = 'http://{}:{}/{}_submit'.format(algorithm_ip, algorithm_port, lower_name)
	result_url = 'http://{}:{}//{}/get_result'.format(algorithm_ip, algorithm_port, lower_name)
	headers = {'Cookie': login_instance.cookie}
	response = requests.post(submit_url, data=params, headers=headers)
	if response.status_code == 403:
		raise exceptions.LoginError('[VSOURCE-Lib] 登陆信息失败，请先正常的登陆')
	response_dict = json.loads(response.content)
	task_id = response_dict['id']
	start_time = time.time()
	while True:
		# 轮询查询结果
		if time.time()-start_time>=max_interval:
			raise exceptions.TimeOutException('[VSOURCE-Lib] 请求超时，未知错误')
		face_result = requests.get(result_url, params={'id': task_id}, headers=headers, timeout=max_interval)
		face_ans = json.loads(face_result.content)
		if face_ans['status'] != 200:
			time.sleep(configs.interval)
			continue
		assert face_ans['status'] == 200
		if face_ans['result']['status'] == 'error':
			return -1
		sentence = face_ans['result']['result']['generate_sentence']

		out = {
			'generate_sentence': sentence,
		}
		return out
	raise exceptions.TimeOutException('[VSOURCE-Lib] 请求超时，未知错误')