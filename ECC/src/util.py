import string, re

def isPrime(x):
    # Cek apakah sebuah angka bilangan prima
    if x > 1:
        for i in range(2, int(x/2)+1):
            if (x%i) == 0:
                return False
        return True

    return False

def getInversion(n, m):
    # cari inversi m (mod n)   
    try:
        val = pow(m, -1, n)
        return val
    except:
        return None 

def encodeText(p):
    enc = ''
    for char in p.lower():
        # A=01, B=02, ..., Z = 26
        idx = str(string.ascii_lowercase.rfind(char)+1)
        enc += idx.zfill(2)
    return enc

def encodeTextOneDigit(p):
    enc = ''
    for char in p.lower():
        # A=1, B=2, ..., Z = 26
        idx = str(string.ascii_lowercase.rfind(char)+1)
        enc += idx
    return enc

def decodeTextOneDigit(p):
    dec = ''
    for item in p:
        char = string.ascii_lowercase[int(item)-1]
        dec += char
    return dec

def decodeText(c):
    dec = ''
    list = []
    for idx in range(0, len(c), 2):
        list.append(c[idx:idx+2])
    
    for item in list:
        dec += string.ascii_lowercase[(int(item)-1)%26]

    return dec
    
def preprocessPlainText(plaintext):
    '''
    Preprocess plain text (except for Extended Vigenere Ciphere)
    Remove all non-alphabet characters from the plaintext
    Return the new pre-processed plaintext
    '''
    # remove digit
    remove_digit = str.maketrans('','', string.digits)
    plaintext = plaintext.translate(remove_digit)

    # remove enter and whitespace
    plaintext = plaintext.replace("\n", "")
    plaintext = plaintext.replace(" ", "")

    # remove tanda baca
    plaintext = re.sub(r'[^\w\s]', '', plaintext)
    
    return plaintext.lower()