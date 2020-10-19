from cryptography.fernet import Fernet
import os

class Magic:

    def __init__(self):
        ''' do the magic trick '''
        self.key = ''

    def gen_key(self):
        self.key = Fernet.generate_key()
        with open('key.key','wb') as binary_file:
            binary_file.write(self.key)
        print('[*] Key generated and saved!')

    def get_key(self):
        with open('key.key','rb') as r:
            self.key = r.read()
        print('[+] Key retrieved')    

    def encrypt(self,filename):
        if os.path.exists('key.key'):
            print('[-] Key already exists!')
            self.get_key()                
        else:
            print('[-] Previous key doesn\'t exists!')
            self.gen_key()
        
        f = Fernet(self.key)
        encrypted_token = ''
        with open(filename,'rb') as rf:
            text = rf.read()        
            encrypted_token = f.encrypt(text)
            print('[-] {} has been encrypted!'.format(filename))

            rf.close()
        
        os.remove(filename)
        
        with open('{}.encrypted'.format(filename),'wb') as wf:
            wf.write(encrypted_token)
            wf.close()
    
    def decrypt(self,filename):
        if not os.path.exists('key.key'):
            print('[*] Key file didn\'t  found! You are doomed!')
            exit(0)
        
        self.get_key()

        f = Fernet(self.key)

        decrypted_string = ''
        with open('{}'.format(filename),'rb') as rf:
            text = rf.read()
            # print(text)
            decrypted_string = f.decrypt(text)
        
        os.remove(filename)
        
        with open(filename.replace('.encrypted',''),'wb') as wf:
            wf.write(decrypted_string)
            wf.close()
        print('[-] File has been decrypted')
        
if __name__ == '__main__':
    m = Magic()    
    m.encrypt('data.json')
    # m.decrypt('data.json.encrypted')
