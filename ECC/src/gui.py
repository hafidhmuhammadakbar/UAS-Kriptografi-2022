import PySimpleGUI as sg
import rsa, paillier, diffiehellman, ecc, util

def saveFile(path, content):
    with open("../keys/"+path, 'w') as file:
        file.write(content)

def readFile(path):
    file = open(path, "r")
    return file.read()

sg.theme("Reddit")
layout = [
    [sg.T("M0521026 - UAS Kriptografi - ECC", font="Any 20")],
    [sg.TabGroup([[
        sg.Tab("RSA", [
            [sg.Text("Generate Keys", font="Any 10")],
            [sg.T("P (prime)", size=(8, 1)), sg.In(key="p_val_rsa", size=(60, 1))],
            [sg.T("Q (prime)", size=(8, 1)), sg.In(key="q_val_rsa", size=(60, 1))],
            [sg.Text("Output Keys", font="Any 10")],
            [sg.T("Public", size=(8, 1)), sg.In(key="public_out_rsa", size=(60, 1))],
            [sg.T("Private", size=(8, 1)), sg.In(key="private_out_rsa", size=(60, 1))],
        ], key="RSA"),
        sg.Tab("Diffie-Hellman", [
            [sg.Text("Generate Keys", font="Any 10")],
            [sg.T("P (prime)", size=(8, 1)), sg.In(key="p_val_diffiehellman", size=(60, 1))],
            [sg.Text("Output Keys", font="Any 10")],
            [sg.T("Public", size=(8, 1)), sg.In(key="public_out_diffiehellman", size=(60, 1))],
            [sg.T("Private", size=(8, 1)), sg.In(key="private_out_diffiehellman", size=(60, 1))],
        ], key="Diffie-Hellman"),
        sg.Tab("Paillier", [
            [sg.Text("Generate Keys", font="Any 10")],
            [sg.T("P (prime)", size=(8, 1)), sg.In(key="p_val_paillier", size=(60, 1))],
            [sg.T("Q (prime)", size=(8, 1)), sg.In(key="q_val_paillier", size=(60, 1))],
            [sg.Text("Output Keys", font="Any 10")],
            [sg.T("Public", size=(8, 1)), sg.In(key="public_out_paillier", size=(60, 1))],
            [sg.T("Private", size=(8, 1)), sg.In(key="private_out_paillier", size=(60, 1))],
        ], key="Paillier"),
        sg.Tab("ECEG", [
            [sg.Text("Generate Keys | Equation y^2 = x^3 + ax + b mod p", font="Any 10")],
            [   sg.T("a", size=(2, 1)), sg.In(key="a_val_eceg", size=(5, 1)),
                sg.T("b", size=(2, 1)), sg.In(key="b_val_eceg", size=(5, 1)),
                sg.T("p", size=(2, 1)), sg.In(key="p_val_eceg", size=(5, 1)),
                sg.Button("GenerateElipticGroup", pad=(5, 10)),
                sg.Text("Eliptic Group List", font="Any 10"), sg.Multiline(key="eliptic_group_list", size=(30, 3)),
            ],
            [sg.T("Chosen BasePoint", size=(15, 1)), sg.In(key="base_point_eceg", size=(15, 1))],
            [sg.Text("Output Keys", font="Any 10")],
            [sg.T("Public", size=(8, 1)), sg.In(key="public_out_eceg", size=(60, 1))],
            [sg.T("Private", size=(8, 1)), sg.In(key="private_out_eceg", size=(60, 1))],
        ], key="ECEG"),
    ]], key="current_action")],
    [
        sg.Button("GenerateKey", pad=(5, 10)),
        sg.T("Filename", size=(8, 1)),
        sg.In(key="filename", size=(25, 1)),
        sg.Button("SavePublicKey", pad=(5, 10)),
        sg.Button("SavePrivateKey", pad=(5, 10))
    ],
    [sg.Text("", key="Info")],
    [sg.T("Input", size=(5, 1)), sg.Multiline(key="input_text", size=(35, 7)), sg.T("Output", size=(5, 1)), sg.Multiline(key="output_text", size=(35, 7))],
    [sg.T("Key", size=(5, 1)), sg.In(key="key", size=(60, 1)), sg.Text("Key Filepath:"), sg.Input(size=(5, 1)), sg.FileBrowse(key='upload_key_loc'), sg.Button("SelectKey")],
    [sg.Button("Encrypt", pad=(5, 10)), sg.Button("Decrypt", pad=(5, 10))],
]

window = sg.Window("UAS Kriptografi - ECC", layout)
# event, values = window.read()
while True:
    event, values = window.read(timeout = 10)
    event = event.lower()
    window["Info"].update("Encrypt/Decrypt (26 Alphabet) using: " + str(values["current_action"]))
    current_mode = values["current_action"]
    if values["current_action"] == "ECEG":
        window["Info"].update("Encrypt/Decrypt (26 Alphabet) using: " + str(values["current_action"] + "\nPlease fill a,b,p,BasePoint in above section before encrypt/decrypt"))
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    if event == "generatekey":
        if current_mode == "RSA":
            keys = rsa.generateKey(int(values["p_val_rsa"]), int(values["q_val_rsa"]))
            if keys == None:
                window["public_out_rsa"].update("p,q tidak prima")
                window["private_out_rsa"].update("p,q tidak prima")
            else:
                window["public_out_rsa"].update(keys["public"])
                window["private_out_rsa"].update(keys["private"])
        if current_mode == "Diffie-Hellman":
            keys = diffiehellman.generateKey(int(values["p_val_diffiehellman"]))
            if keys == None:
                window["public_out_diffiehellman"].update("p tidak prima")
                window["private_out_diffiehellman"].update("p tidak prima")
            else:
                window["public_out_diffiehellman"].update(keys["public"])
                window["private_out_diffiehellman"].update(keys["private"])
        if current_mode == "Paillier":
            keys = paillier.generateKey(int(values["p_val_paillier"]), int(values["q_val_paillier"]))
            if keys == None:
                window["public_out_paillier"].update("p, q tidak memenuhi syarat")
                window["private_out_paillier"].update("p, q tidak memenuhi syarat")
            else:
                window["public_out_paillier"].update(keys["public"])
                window["private_out_paillier"].update(keys["private"])
        if current_mode == "ECEG":
            basePoint = values["base_point_eceg"].replace('(','').replace(')','').split(",")
            keys = ecc.generateKey(int(values["a_val_eceg"]), int(values["b_val_eceg"]), int(values["p_val_eceg"]), int(basePoint[0]), int(basePoint[1]))
            if keys == None:
                window["public_out_eceg"].update("base point tidak memenuhi syarat")
                window["private_out_eceg"].update("base point tidak memenuhi syarat")
            else:
                window["public_out_eceg"].update(keys["public"])
                window["private_out_eceg"].update(keys["private"])
        
    if event == "generateelipticgroup":
        eg = ecc.generateElipticGroup(int(values["a_val_eceg"]), int(values["b_val_eceg"]), int(values["p_val_eceg"]))
        window["eliptic_group_list"].update(eg)

    if event == "savepublickey":
        if values["filename"] == "":
            window["filename"].update("filename kosong")
        else:
            contentLoc = "public_out_" + current_mode.lower()
            content = ""
            for value in eval(values[contentLoc]):
                content += str(value) + " "
            saveFile(values["filename"], content.rstrip())
            window["filename"].update("tersimpan di folder keys")

    if event == "saveprivatekey":
        if values["filename"] == "":
            window["filename"].update("filename kosong")
        else:
            contentLoc = "private_out_" + current_mode.lower()
            if current_mode == "ECEG":
                content = values[contentLoc]
                saveFile(values["filename"], content)
            else:
                content = ""
                for value in eval(values[contentLoc]):
                    content += str(value) + " "
                saveFile(values["filename"], content.rstrip())
            window["filename"].update("tersimpan di folder keys")

    if event == "encrypt":
        # IF per action
        if current_mode == "RSA":
            input =  util.preprocessPlainText(str(values["input_text"]))
            key = values["key"].split(' ')
            cipher = rsa.encrypt(input, int(key[0]), int(key[1]))
            window["output_text"].update(cipher)
        if current_mode == "Diffie-Hellman":
            input =  util.preprocessPlainText(str(values["input_text"]))
            key = values["key"].split(' ')
            cipher = diffiehellman.encrypt(input, int(key[0]), int(key[1]), int(key[2]))
            window["output_text"].update(str(cipher))
        if current_mode == "Paillier":
            input =  util.preprocessPlainText(str(values["input_text"]))
            key = values["key"].split(' ')
            cipher = paillier.encrypt(input, int(key[0]), int(key[1]))
            window["output_text"].update(str(cipher))
        if current_mode == "ECEG":
            input =  util.preprocessPlainText(str(values["input_text"]))
            key = values["key"].split(' ')
            basepoint = eval(values["base_point_eceg"])
            cipher = ecc.encrypt(input, basepoint, (int(key[0]), int(key[1])), int(values["a_val_eceg"]), int(values["b_val_eceg"]), int(values["p_val_eceg"]), 3)
            result = ""
            for item in cipher:
                item1 = item[0]
                item2 = item[1]
                x1 = item1[0]
                y1 = item1[1]
                x2 = item2[0]
                y2 = item2[1]
                result += str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + "\n"
            window["output_text"].update(result)

    if event == "decrypt":
        if current_mode == "RSA":
            input =  str(values["input_text"])
            key = values["key"].split(' ')
            plain = rsa.decrypt(input, int(key[0]), int(key[1]))
            window["output_text"].update(util.decodeText(plain))
        if current_mode == "Diffie-Hellman":
            input =  str(values["input_text"])
            key = values["key"].split(' ')
            plain = diffiehellman.decrypt(input, int(key[0]), int(key[1]))
            window["output_text"].update(util.decodeText(plain))
        if current_mode == "Paillier":
            input =  str(values["input_text"])
            key = values["key"].split(' ')
            plain = paillier.decrypt(input, int(key[0]), int(key[1]), int(key[2]))
            window["output_text"].update(util.decodeText(plain))
        if current_mode == "ECEG":
            input =  values["input_text"]
            point_list = []
            for item in input.split('\n'):
                item = item.split(' ')
                tuple1 = (int(item[0]), int(item[1]))
                tuple2 = (int(item[2]), int(item[3]))
                point_list.append((tuple1, tuple2))
            
            key = values["key"]
            basepoint = eval(values["base_point_eceg"])
            plain = ecc.decrypt(point_list, int(key), int(values["a_val_eceg"]), int(values["p_val_eceg"]), 3)
            
            window["output_text"].update(plain)

    if event == "selectkey":
        window["key"].update(readFile(values["upload_key_loc"]))