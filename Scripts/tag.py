#!/usr/bin/python3.4
tag1='init' #Тег с которого удаляем
tag2='kde' #Тег который удаляем
c=0 #Счётчик изменений
file=open('pkgstates','r') #Открываем файл со статусами пакетов
text=file.readlines() # Считываем все строки из файла
file.close # Отпускаем файл
for x in range(0,len(text)): # Цикл должен обходить все строки файла
	if text[x].startswith('User-Tags:'): # Если строка начинается с 'User-Tags:' то:
		if text[x].find(tag1) != -1: # Если в строке есть содержимое переменной tag1 то:
			if text[x].find(tag2) != -1: # Если в строке есть содержимое переменной tag2 то:
				text[x].replace((' '+tag2),'') # Заменить содержимое строки равное tag2 на ничего
				c+=1 # Счётчик изменений +1
text=''.join(text) # Объединяем все строки
file=open('pkgstates_new','w') # Открываем файл на запись
file.write(text) # Записываем в файл переменную text
file.close # Отпускаем файл
print('Total changes: '+str(c)) # Сообщаем сколько всего строк изменили
