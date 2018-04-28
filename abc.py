#!/usr/bin/env python3
s = "bac bai jh bad bcd gf bbf jj ej ej jf hh jh bbf bbg fb ic bcf"

res = []
for i in s:
	if i == ' ':
		res.append(' ')
		continue
	res.append(str(ord(i)-ord('a')))

t = ''.join(res)

print(''.join(chr(int(i)) for i in t.split(' ')))
