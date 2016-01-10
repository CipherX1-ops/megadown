#!/usr/bin/env python

import sys
import json
import hmac
import hashlib
import base64
import re

def json_param(json_data, json_var, index=0, undef_msg='', bool_msg={'true':1, 'false':0}):
	
	try:

		j = json.loads(json_data)

		if isinstance(j, list):
			j=j[index]

		if json_var not in j:
			j[json_var] = undef_msg
		elif isinstance(j[json_var], bool):
			j[json_var] = bool_msg['true'] if j[json_var] == True else bool_msg['false']
			
		return j[json_var]

	except ValueError:

		return undef_msg


def password_hmac(data, secret, iterations=1):

	data, secret, iterations = base64.b64decode(data), base64.b64decode(secret), int(iterations)
	last = xor = bytearray(hmac.new(secret, data, hashlib.sha256).digest())
	
	i=1
	while i<iterations:

		last = bytearray(hmac.new(secret, last, hashlib.sha256).digest())
		xor = [a ^ b for a, b in zip(xor, last)]
		i+=1

	return base64.b64encode(xor if i == 1 else bytearray(xor)).decode()


def regex_match(pattern, subject, group_index=0, trim_output=0):

	m = re.search(pattern, subject)
	res = m.group(int(group_index)) if m != None else ''

	return res if trim_output == 0 else res.strip()


def regex_imatch(pattern, subject, group_index=0, trim_output=0):

	m = re.search(pattern, subject, re.IGNORECASE)
	res = m.group(int(group_index)) if m != None else ''

	return res if trim_output == 0 else res.strip()


def str_ireplace(old, new, subject):

	pattern = re.compile(re.escape(old), re.IGNORECASE)

	return pattern.sub(new, subject)


def call_user_func_array(callback, param_arr):

	if callback in globals():
		return globals()[callback](*param_arr)
	else:
		return 'ERROR: '+callback+' is not defined!'


if __name__ == '__main__':
	print(call_user_func_array(sys.argv[1], sys.argv[2:]))