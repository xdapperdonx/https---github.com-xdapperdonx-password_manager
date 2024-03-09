import sqlite3
from secrets import token_bytes 
from Cryptodome.Cipher import AES 

def generate_key(): 
        key = token_bytes(32) 
        filepath = "./key.bin" 
        with open(filepath, "wb") as file: 
            file.write(key) 

def open_key(): 
        filepath = "./key.bin" 
        with open(filepath, "rb") as file: 
            return file.read() 

def encrypt(website, username, password): 
        #creation of DB connection 
        conn = sqlite3.connect("password.db") 
        c = conn.cursor() 

        c.execute(f"SELECT COUNT(*) FROM passwords WHERE website='{website}'") 
        conn.commit()

        if(c.fetchone()[0] != 0):
            return False 
    
        #opens key
        key = open_key()

        #encryption
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        encrypted_data, tag = cipher.encrypt_and_digest(password.encode("ascii"))

        #SQL query
        c.execute(f"INSERT INTO passwords VALUES('{website}', '{username}', '{encrypted_data.hex()}', '{tag.hex()}', '{nonce.hex()}')") 
        conn.commit()

        conn.close()

        return encrypted_data, tag, nonce

def decrypt(website): 
        #creation of connection
        conn = sqlite3.connect("password.db") 
        c = conn.cursor()           
 
        #SQL query
        c.execute(f"SELECT username, password, tag, nonce FROM passwords WHERE website='{website}'")
        conn.commit()

        response = c.fetchone()        
        if(response == None):
            return False        

        #hex to bytes
        username = response[0]
        plaintext = bytes.fromhex(response[1])
        tag = bytes.fromhex(response[2])
        nonce = bytes.fromhex(response[3])

        #decryption
        key = open_key()
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        password = cipher.decrypt(plaintext)

        try:
            cipher.verify(tag)
            return username, password.decode("ascii")
        except:
            return False
        
        conn.close() 
  
def update_username(website, new_username):
    conn = sqlite3.connect("password.db")
    c = conn.cursor()

    c.execute(f"UPDATE passwords SET username = '{new_username}' WHERE website = '{website}'")
    conn.commit()

    conn.close()


def update_password(website, new_password):
    conn = sqlite3.connect("password.db")
    c = conn.cursor()

    key = open_key()

    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    encrypted_data, tag = cipher.encrypt_and_digest(new_password.encode("ascii"))

    conn.execute(f"UPDATE passwords SET password = '{encrypted_data.hex()}', tag = '{tag.hex()}', nonce = '{nonce.hex()}' WHERE website = '{website}'")
    conn.commit()

    conn.close()

def delete(website):
        conn = sqlite3.connect("password.db")
        c = conn.cursor()

        c.execute(f"SELECT COUNT(*) FROM passwords WHERE website='{website}'")
        conn.commit()
        
        if (c.fetchone()[0] == 0):
            return False
        else:  
            c.execute(f"DELETE FROM passwords WHERE website='{website}'")
            conn.commit()
            return True

        conn.close()

if __name__=="__main__":
        print(('-' * 20) + " PASSWORD MANAGER " + ('-' * 20))
        print("enter '1' to  create a new key")
        print("enter '2' to  encrypt a record")
        print("enter '3' to decrypt a record")
        print("enter '4' to update a record")
        print("enter '5' to delete a record")
        print("enter 'q' to quit")

        usr_input = input(':')
        print('-'*58)

        if(usr_input == '1'):
            conf_key_input = input("Are you sure you want to create a new key? y/n: ")

            if(conf_key_input == 'y'):
                    generate_key()
                    print("status: key generated successfully")
            elif(conf_key_input == 'n'):
                    print("status: exiting programming")
                    print('-' * 58)
                    exit()
            else:
                    print("error: input not valid, exiting program") 
                    print('-' * 58)
                    exit()

        elif(usr_input == '2'):
            website = input("enter website: ")
            username = input("enter username: ")
            password = input("enter password: ")
            verify_password = input("enter password again: ")
            flag_pass_verification = False

            if(password == verify_password):
                 flag_pass_verification = True

            if(encrypt(website, username, password) != False and flag_pass_verification):
                    print("status: website succesfully encrypted")
            elif(encrypt(website, username, password) == False):
                    print("error: website already exist")

        elif(usr_input == '3'):
            website = input("enter website to decrypt: ")

            flag = decrypt(website)

            if(flag != False):
                    (username, password) = flag

                    print(f"username: {username}")
                    print(f"password: {password}")
            else:
                    print("error: website not found")

        elif(usr_input == '4'):
            website =  input("enter website to update: ")
            usr_choice = input("press 'u' to update username, press 'p' to update password: ")

            if(usr_choice == 'u'):
                new_username = input("enter new username: ")

                update_username(website, new_username)
                print("status: username was updated") 

            elif(usr_choice == 'p'):
                new_password = input("enter new password: ")
                verify_new_password = input("enter password again: ")
                flag_pass_verification = False
                
                if(new_password == verify_new_password):
                    update_password(website, new_password)
                    print("status: password was updated")
                else:
                     print("error: passwords do not match")

            else:
                print("error: input not valid, exiting program")
 
        elif(usr_input == '5'):
            website = input("enter website to delete: ")
            verification = input(f"are you sure you want to delete {website}? y/n: ")

            if(verification == 'y'):
                flag = delete(website)
                if(flag == True):
                    print("status: record deleted")
                elif(flag == False):
                    print("error: website not found")
            elif(verification == 'n'):
                print("status: exiting program")
            else:
                print("error: input not valid, exiting program")

        elif(usr_input == 'q'):
            print("status: exiting program") 
            print('-' * 58)
            exit()

        else:
            print("error: input not valid, exiting program") 
            print('-' * 58)
            exit()
