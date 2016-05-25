tag1='kde'
tag2='ntp'
c=0
file=open('pkgstates','r')
text=file.readlines()
file.close
for x in range(0,len(text)):
	if text[x].startswith('User-Tags:'):
		if text[x].find(tag1) != -1:
			if text[x].find(tag2) != -1:
				text[x].replace((' '+tag2),'')
				c+=1
	x+=1
text=''.join(text)
file=open('pkgstates_new','w')
file.write(text)
file.close
print('Total changes: '+str(c))
