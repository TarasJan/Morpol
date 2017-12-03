# -*- coding: utf-8 -*-
#! usr/bin python

import io
import json

def enocoding_data(string):

	tr_len = 0
	sgn_len = 0
	wrd_len = 1

	for letter in string:
		if letter == '.':
			tr_len += 1
			sgn_len += 1

		if letter == '_':
			tr_len += 3
			sgn_len += 1

		if letter == '|':
			tr_len += 3
			wrd_len += 1
	return (tr_len, sgn_len, wrd_len)

def get_f(filename, scheme):
	output = ''
	
	with io.open('./korpusy_gutenberg/' + filename,'r',encoding='utf-8') as file:
		data = file.read()
		data = data.lower()

	with io.open('./morse_models/' + scheme, 'r', encoding='utf-8') as file:
		dictionary = json.loads(file.read())
	
	for sign in data:
		if sign in dictionary.keys():
			output += (dictionary[sign] + '|')
	return output



print enocoding_data(get_f('tvn', 'direct_map.json'))
print enocoding_data(get_f('internet', 'direct_map.json'))
print enocoding_data(get_f('korpus_kla', 'direct_map.json'))


