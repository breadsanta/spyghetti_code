#!/usr/bin/env python
# Some people, when confronted with a problem, think: “I know, I'll use regular expressions.” Now they have two problems.
#
# ¬ >> negació
# + >> disjunció
# ^ >> conjunció
# > >> condicional
# = >> bicondicional
# q > (p + (q ^ r) + ¬( s ^ (t + u)) + (g) = r

import string, re, sys

if len(sys.argv) < 1:
	print('Usage: ./logic.py string')
	sys.exit()

analize = ''.join(sys.argv[1:]).lower().replace(' ', '')

if re.fullmatch(r'((\(*¬*)*[a-z]\)*[+^>=])*((\(*¬*)*[a-z]\)*)', analize) is None:
	print('Malformated input.', analize)
	sys.exit()
elif (diff := analize.count('(') - analize.count(')')) != 0:
	if diff > 0:
		for i in range(diff):
			analize += ')'
	else:
		for i in range(abs(diff)):
			analize = '(' + analize

variables = list(set([l for l in analize if l in string.ascii_lowercase]))
variables.sort()

vv = dict.fromkeys(variables)

header = ' ' + ' '.join(vv.keys()) + ' | ' + analize + ' '

print(header)

print(''.center(len(header), '-'))

for i in range(2**len(variables)):
	finalstr = ' '
	values = str(bin(i)[2:]).zfill(len(variables)).replace('0', 'V').replace('1', 'F')
	vv = dict(zip(variables, values))

	for val in vv.values():
		finalstr += val + ' '

	evaluated = analize

	for k in vv.keys():
		evaluated = evaluated.replace(k, vv[k])

	while len(evaluated) != 1: #'¬' in evaluated or '(' in evaluated:
		evaluated = re.sub(r'\((\w)\)', r'\1', evaluated)
		evaluated = re.sub(r'¬V', r'F', evaluated)
		evaluated = re.sub(r'¬F', r'V', evaluated)
		# god save stackoverflow https://stackoverflow.com/questions/5616822/python-regex-find-all-overlapping-matches
		matches = re.finditer(r'\w[+^>=](?=(\w))', evaluated)
		offset = 0
		#print(evaluated)
		for match in matches:
			start = match.start() - offset
			end = match.end() - offset
			operation = evaluated[start+1]
			char = 'F'
			if operation == '+':
				if evaluated[start] == 'V' or evaluated[end] == 'V':
					char = 'V'
			elif operation == '^':
				if evaluated[start] == 'V' and evaluated[end] == 'V':
					char = 'V'
			elif operation == '>':
				if (evaluated[start] == 'F' and evaluated[end] == 'F') or evaluated[end] == 'V':
					char = 'V'
			elif operation == '=':
				if evaluated[start] == evaluated[end]:
					char = 'V'

			evaluated = evaluated[:start] + char + evaluated[end+1:]
			#print(evaluated)
			
			offset += 2

	finalstr += '| ' + evaluated.center(len(analize), ' ') + ' '

	print(finalstr)
