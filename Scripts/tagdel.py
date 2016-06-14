import sys
try:
    file=open('pkgstates','r')
except FileNotFoundError:
    print('No file')
    sys.exit
text=file.readlines()
file.close()
tag1=str(input('First tag:'))
tag2=str(input('Second tag:'))
for a in range(0,len(text)):
    if -1<text[a].replace('\n',' ').find(' '+tag1+' ')<text[a].replace('\n',' ').find(' '+tag2+' '):
        text[a]=text[a].replace('\n',' ').replace(' '+tag2+' ','')+'\n'
file=open('pkgstates_new','w')
file.write(''.join(text))
file.close()
