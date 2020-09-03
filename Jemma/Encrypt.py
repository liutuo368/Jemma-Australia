import base64
from Crypto.Cipher import AES

import random
import configparser


def pkcs7padding(text):
    bs = AES.block_size  # 16
    length = len(text)
    bytes_length = len(bytes(text, encoding='utf-8'))
    padding_size = length if(bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    padding_text = chr(padding) * padding
    return text + padding_text


def pkcs7unpadding(text):
    length = len(text)
    unpadding = ord(text[length-1])
    return text[0:length-unpadding]


cf = configparser.ConfigParser()
cf.read('django_db.conf')
AES_KEY = cf.get('AES', 'AES_KEY')


def encrypt(content):
    key_bytes = bytes(AES_KEY, encoding='utf-8')
    iv = key_bytes
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    content_padding = pkcs7padding(content)
    encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
    result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
    return result


def decrypt(content):
    key_bytes = bytes(AES_KEY, encoding='utf-8')
    iv = key_bytes
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    encrypt_bytes = base64.b64decode(content)
    decrypt_bytes = cipher.decrypt(encrypt_bytes)
    result = str(decrypt_bytes, encoding='utf-8')
    result = pkcs7unpadding(result)
    return result


def get_key(n):
    c_length = int(n)
    source = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    length = len(source) - 1
    result = ''
    for i in range(c_length):
        result += source[random.randint(0, length)]
    return result

