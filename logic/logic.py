#! /usr/bin/python3.8
# ¬ >> negació
# ^ >> conjunció
# + >> disjunció
# > >> condicional
# = >> bicondicional
# q > (p + (q ^ r) + ¬( s ^ (t + u)) + (g) = r

# TODO: parse ^+>= (L. 55+)

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
		while len(evaluated) != 1:
			evaluated = re.sub(r'\((\w)\)', r'\1', evaluated)
			evaluated = re.sub(r'¬V', r'F', evaluated)
			evaluated = re.sub(r'¬F', r'V', evaluated)


	finalstr += '| ' + evaluated.center(len(analize), ' ') + ' '

	print(finalstr)
