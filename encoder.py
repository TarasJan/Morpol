# -*- coding: utf-8 -*-
#! usr/bin/python
import io
import json
import itertools
import re

def fetch_max(dictio):
	key = max(dictio, key=dictio.get)
	del dictio[key]
	return key

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# for filtering out numerical sings
def num_sign(s):
	return len(s) == 5 and  (bool(re.search(r'^_*\.*$',s)) or bool(re.search(r'^\.*_*$',s)))

# Mapowanie bezposrednie

with io.open('./frequencies/pl.json','r',encoding='utf-8') as file:
	dictionary = file.read()
frequencies = json.loads(dictionary)

encoded_dict = {}

char_array = '._'
sign_length = 1

while frequencies:
	product_pool = itertools.product(char_array, repeat=sign_length)
	for sign in product_pool:
		if not frequencies:
			break
		znak = ''.join(sign)
		if num_sign(znak):
			continue
		encoded_dict[fetch_max(frequencies)] = znak
	sign_length +=1

with io.open('./morse_models/direct_map.json', 'w', encoding='utf-8') as output:
	json_body = json.dumps(encoded_dict, ensure_ascii=False)
	output.write(json_body)

# Mapowanie ze znakiem diakletyzacji

frequencies = json.loads(dictionary)

encoded_dict = {}
sign_length = 1

sum_diak = 0

for l in frequencies:
	if not is_ascii(l):
		sum_diak += frequencies[l]

frequencies = {k: v for k, v in frequencies.iteritems() if is_ascii(k)}
frequencies['diak'] = sum_diak

while frequencies:
	product_pool = itertools.product(char_array, repeat=sign_length)
	for sign in product_pool:
		if not frequencies:
			break
		znak = ''.join(sign)
		if num_sign(znak):
			continue
		key = fetch_max(frequencies)
		encoded_dict[key] = znak
	sign_length +=1

# tabela diakletyzacji 
tab = {
	'ą': encoded_dict['a'] + '|' + encoded_dict['diak'], 
	'ę': encoded_dict['e'] + '|' + encoded_dict['diak'], 
	'ó': encoded_dict['o'] + '|' + encoded_dict['diak'], 
	'ś': encoded_dict['e'] + '|' + encoded_dict['diak'], 
	'ż': encoded_dict['z'] + '|' + encoded_dict['diak'], 
	'ć': encoded_dict['c'] + '|' + encoded_dict['diak'], 
	'ń': encoded_dict['n'] + '|' + encoded_dict['diak'], 
}

with io.open('./morse_models/diak_map.json', 'w', encoding='utf-8') as output:
	json_body = json.dumps(encoded_dict, ensure_ascii=False)
	output.write(json_body)


with io.open('./morse_models/diak_tab.json', 'w', encoding='utf-8') as output:
	json_body = unicode(json.dumps(tab, ensure_ascii=False).decode('utf-8'))
	output.write(json_body)
