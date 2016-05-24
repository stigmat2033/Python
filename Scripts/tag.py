tag1='init'
tag2='kde'
c=0
file=open('pkgstates','r')
text=file.readlines()
file.close
for x in range(0,len(text)):
	i=text[x]
	if i.startswith('User-Tags:'):
		if i.find(tag1) != -1:
			if i.find(tag2) != -1:
				i=i.replace((', '+tag2),'')
				text[x]=i
				с+=1
	x+=1
text=''.join(text)
file=open('pkgstates_new','w')
file.write(text)
file.close
print('Изменено: '+str(x)+' строк')
