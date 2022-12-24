import secrets, math
from rsa import decrypt
from util import decodeText, encodeText, isPrime, getInversion

def L(x, n):
    return int((x-1)/n)

def checkKey(p, q):
    return (isPrime(p) and isPrime(q) and (math.gcd(p*q, (p-1)*(q-1)) == 1))

def generateKey(p, q):
    if (isPrime(p) and isPrime(q) and (math.gcd(p*q, (p-1)*(q-1)) == 1)):
        n = p * q
        lamb = math.lcm(p-1, q-1)
        # found = False
        # while not(found): # mitigasi not invertible
        #     g = secrets.randbelow(n**2)
        #     l = L((g**lamb) % (n**2), n)
        #     miu = getInversion(n, l) 
        #     if miu != None:
        #         found = True
        g = n + 1
        l = L((g**lamb) % (n**2), n)
        miu = getInversion(n, l) 
        keys = {
            "public" : (g, n),
            "private" : (lamb, miu, n)
        }
        return keys
    else:
        print("p,q tidak memenuhi syarat")

def getRList(n):
    # Generate bilangan bulat acak r
    list = []
    for i in range(1,n):
        if math.gcd(i,n) == 1:
            list.append(i)
    return list

def encrypt(plainteks, g, n):
    enc = encodeText(plainteks)
    cipher = ''
    nBlock = len(str(n))
    r = secrets.choice(getRList(n))
    i = 0
    while i < (len(enc) - (len(enc) % nBlock)):
        strVal = enc[i:i+nBlock]
        val = int(strVal)
        isStartZero = False
        if (enc[i:i+nBlock][0] == '0'):
            isStartZero = True
        # cek apakah val >= n
        if val >= n:
            # ciphering
            strVal = enc[i:i+nBlock-1]
            val = int(strVal)
            i -= 1
        c = ((g**val) * (r**n)) % (n**2)
        if isStartZero:
            nPadding = len(strVal) - len(str(val))
            cipher += str(c).zfill(nPadding+len(str(c))) + " "
        else:
            cipher += str(c) + " "
        i += nBlock

    # sisa angka, jika ada
    if (i < len(enc)):
        val = int(enc[i:])
        isStartZero = False
        if (enc[i:] == '0'):
            isStartZero = True
        c = ((g**val) * (r**n)) % (n**2)
        if isStartZero:
            nPadding = len(enc[i:]) - len(str(val))
            cipher += str(c).zfill(nPadding+len(str(c))) + " "
        else:
            cipher += str(c) + " "

    return cipher.rstrip()

def decrypt(ciphertext, lamb, miu, n):
    cipher_list = ciphertext.split(" ")
    plain = ''
    for item in cipher_list:
        val = int(item)
        p = (L((val**lamb) % (n**2), n) * miu) % n
        i = 0
        while (item[i] == "0"):
            plain += "0"
            i += 1
        plain += str(p)

    return plain

if __name__ == "__main__":
    p = 43
    q = 37
    if (checkKey(p, q)):
        keys = generateKey(p, q)
        teks = "testingpailliersemogabisa"
        print(teks)
        enc = encrypt(teks, keys["public"][0], keys["public"][1])
        #print(enc)
        dec = decrypt(enc, keys["private"][0], keys["private"][1], keys["public"][1])
        #print(encodeText(teks))
        #print(dec)
        if (dec == encodeText(teks)):
            print("hasil dekripsi", decodeText(dec))
            print("oke bisa")