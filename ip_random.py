import random
ip_r=[1,2,3,4]
mask=''
mask_r=[1,2,3,4]
for i in range(0,4):
    ip_r[i]=random.randint(1,255)
print(ip_r)
zeros=random.randint(1,32)
mask+=str(('1'*zeros)+('0'*(32-zeros)))
for i in range(0,4):
    mask_r[i]=int((mask[(8*i):((8*i)+8)]),2)
print(mask_r)