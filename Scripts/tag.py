#!/usr/bin/python3.4
tag1='init' #Тег с которого удаляем
tag2='kde' #Тег который удаляем
c=0 #Счётчик изменений
file=open('pkgstates','r') #Открываем файл со статусами пакетов
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
