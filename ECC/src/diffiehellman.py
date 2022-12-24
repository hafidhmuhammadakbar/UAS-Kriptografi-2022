import secrets

from util import decodeText, encodeText, isPrime

def generateKey(p):
    if (isPrime(p)):
        # g < p
        g = secrets.randbelow(p)
        # 1 <= x <= p-2
        x = secrets.choice(range(1,p-1))
        y = (g ** x) % p
        keys = {
            "public" : (y, g, p),
            "private" : (x, p)
        }
        return keys
    else:
        print("p tidak prima")

def pickK(p):
    return secrets.choice(range(1,p-1))

def encrypt(plainteks, y, g, p):
    enc = encodeText(plainteks)
    cipher = ''
    nBlock = len(str(p))
    k = pickK(p)
    i = 0
    while i < (len(enc) - (len(enc) % nBlock)):
        val = int(enc[i:i+nBlock])
        isStartZero = False
        if (enc[i:i+nBlock][0] == '0'):
            isStartZero = True
        # cek apakah val >= p-1
        if val >= p-1:
            # ciphering 
            val = int(enc[i:i+nBlock-1])
            i -= 1
        
        a = (g**k) % p
        b = ((y**k) * val) % p
        if (isStartZero):
            cipher += "0" + str(a) + " " + str(b) + " "
        else:
            cipher += str(a) + " " + str(b) + " "
        i += nBlock

    # sisa angka, jika ada
    if (i < len(enc)):
        val = int(enc[i:])
        isStartZero = False
        if (enc[i:i+nBlock][0] == '0'):
            isStartZero = True
        a = (g**k) % p
        b = ((y**k) * val) % p
        if (isStartZero):
            cipher += "0" + str(a) + " " + str(b) + " "
        else:
            cipher += str(a) + " " + str(b) + " "

    return cipher.rstrip()

def decrypt(ciphertext, x, p):
    plain = ''
    cipher_list = ciphertext.split(" ")
    
    for i in range(0, len(cipher_list), 2):
        a = cipher_list[i]
        b = cipher_list[i+1]
        a_inv = pow(int(a), p-1-x)
        m = (int(b) * a_inv) % p
        
        if (a[0] == '0'):
            plain += "0" + str(m)
        else:
            plain += str(m)

    return plain

if __name__ == "__main__":
    keys = generateKey(41)
    #print(keys)
    text = "testingdiffiehelmansemogabisa"
    enc = encrypt(text, keys["public"][0], keys["public"][1], keys["public"][2])
    #print(encodeText(text))
    print(enc)
    dec = decrypt(enc, keys["private"][0], keys["private"][1])
    #print(dec)
    if (dec == encodeText(text)):
        print("oke bisa")
        print(decodeText(dec))