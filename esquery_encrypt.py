# rsa encryption

import rsa

a, b = rsa.newkeys(1024)
message = 'admin:W@terleaf33908'.encode('utf8')
encMessage = rsa.encrypt(message, a)

with open('esquery_key1.txt','wb') as f:
    f.write(encMessage)

with open('esquery_key2.pem','wb') as f:
    f.write(b.save_pkcs1('PEM'))
    
with open('esquery_key1.txt','rb') as f:
    mess = f.read()

with open('esquery_key2.pem','rb') as f:
    contents2 = rsa.PrivateKey.load_pkcs1(f.read())