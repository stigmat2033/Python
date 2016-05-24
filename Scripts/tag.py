file=open('pkgstates','r+x')
out=open('pkgstates_new','w')
text=file.readlines()
tag1='init'
tag2='kde'
i=''
for x in range(0,len(text)):
	i=text[x]
	if i.startswith('User-Tags:'):
		if i.find(tag1) != -1:
			if i.find(tag2) != -1:
				i=i.replace((', '+tag2),'')
				text[x]=i
				print(i)
	x+=1
text=''.join(text)
out.write(text)
file.close
out.close