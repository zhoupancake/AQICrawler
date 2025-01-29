import js2py
import re
import base64
import hashlib
import json
import time
import pandas as pd

def eval_decoder(code):
    print("decrypting the code...")
    while True:
        if code.startswith('eval'):
            code = code[:-1]
            code = code.replace('eval', '')
            code = js2py.eval_js(code)
        elif code.startswith('k'):
            code = code[:-1]
            code = code.replace('k(', '')
        elif code.startswith('dweklxde'):
            code = code[:-1]
            code = code.replace('dweklxde(\'', '')
            code = base64.b64decode(code).decode()
        else:
            return code
        
def re_extractor(code):
    print("extracting the encrypt & decrypt key...")
    def extract_decrypt_key(code):
        pattern_DES_key = r"data = DES\.decrypt\(([^,]+),\s*([^,]+),\s*([^)]+)\)"
        pattern_AES_key = r"data = AES\.decrypt\(([^,]+),\s*([^,]+),\s*([^)]+)\)"
        match_DES_key = re.search(pattern_DES_key, code)
        match_AES_key = re.search(pattern_AES_key, code)

        decrypt_DES_key_key = match_DES_key.group(2) if match_DES_key else None
        decrypt_DES_iv_key = match_DES_key.group(3) if match_DES_key else None
        decrypt_AES_key_key = match_AES_key.group(2) if match_AES_key else None
        decrypt_AES_iv_key = match_AES_key.group(3) if match_AES_key else None
        return  decrypt_DES_key_key, decrypt_DES_iv_key, decrypt_AES_key_key, decrypt_AES_iv_key
    
    def extract_encrypt_key(code):
        pattern_AES_key = r"pKmSFk8 = AES\.encrypt\(([^,]+),\s*([^,]+),\s*([^)]+)\)"
        match_AES_key = re.search(pattern_AES_key, code)
        encrypt_AES_key_key = match_AES_key.group(2) if match_AES_key else None
        encrypt_AES_iv_key = match_AES_key.group(3) if match_AES_key else None
        return encrypt_AES_key_key, encrypt_AES_iv_key

    def extract_app_id(code):
        pattern_app_id = r"var aMFs = '([^']+)';"
        match_app_id = re.search(pattern_app_id, code)    
        app_id = match_app_id.group(1) if match_app_id else None
        return app_id
    
    def extract_decrypt_value(code, DES_key_key, DES_iv_key, AES_key_key, AES_iv_key):
        pattern_DES_key = r'const\s+' + re.escape(DES_key_key) + r'\s*=\s*"(?P<extracted_string>[a-zA-Z0-9]+)";'
        pattern_DES_iv = r'const\s+' + re.escape(DES_iv_key) + r'\s*=\s*"(?P<extracted_string>[a-zA-Z0-9]+)";'
        pattern_AES_key = r'const\s+' + re.escape(AES_key_key) + r'\s*=\s*"(?P<extracted_string>[a-zA-Z0-9]+)";'
        pattern_AES_iv = r'const\s+' + re.escape(AES_iv_key) + r'\s*=\s*"(?P<extracted_string>[a-zA-Z0-9]+)";'
        match_DES_key_value = re.search(pattern_DES_key, code)
        match_DES_iv_value = re.search(pattern_DES_iv, code)
        match_AES_key_value = re.search(pattern_AES_key, code)
        match_AES_iv_value = re.search(pattern_AES_iv, code)

        DES_key_value = match_DES_key_value.group("extracted_string") if match_DES_key_value else None
        DES_iv_value = match_DES_iv_value.group("extracted_string") if match_DES_iv_value else None
        AES_key_value = match_AES_key_value.group("extracted_string") if match_AES_key_value else None
        AES_iv_value = match_AES_iv_value.group("extracted_string") if match_AES_iv_value else None
        return  DES_key_value, DES_iv_value, AES_key_value, AES_iv_value
    
    def extract_encrypt_value(code, AES_key_key, AES_iv_key):
        pattern_AES_key = r'const\s+' + re.escape(AES_key_key) + r'\s*=\s*"(?P<extracted_string>[a-zA-Z0-9]+)";'
        pattern_AES_iv = r'const\s+' + re.escape(AES_iv_key) + r'\s*=\s*"(?P<extracted_string>[a-zA-Z0-9]+)";'
        match_AES_key = re.search(pattern_AES_key, code)
        match_AES_iv = re.search(pattern_AES_iv, code)
        
        AES_key_value = match_AES_key.group("extracted_string") if match_AES_key else None
        AES_iv_value = match_AES_iv.group("extracted_string") if match_AES_iv else None
        return AES_key_value, AES_iv_value
    
    decrypt_DES_key_key, decrypt_DES_iv_key, decrypt_AES_key_key, decrypt_AES_iv_key = extract_decrypt_key(code)
    decrypt_DES_key_value, decrypt_DES_iv_value, decrypt_AES_key_value, decrypt_AES_iv_value = extract_decrypt_value(code, decrypt_DES_key_key, decrypt_DES_iv_key, decrypt_AES_key_key, decrypt_AES_iv_key)
    encrypt_AES_key_key, encrypt_AES_iv_key = extract_encrypt_key(code)
    encrypt_AES_key_value, encrypt_AES_iv_value = extract_encrypt_value(code, encrypt_AES_key_key, encrypt_AES_iv_key)
    app_id = extract_app_id(code)
    return  decrypt_DES_key_value, decrypt_DES_iv_value, encrypt_AES_key_value, encrypt_AES_iv_value, decrypt_AES_key_value, decrypt_AES_iv_value, app_id

def re_extractor_observe(code):
    print("use the cached encrypt and decrypt key...") 
    def extract_app_id(code):
        pattern_app_id = r"var aMFs = '([^']+)';"
        match_app_id = re.search(pattern_app_id, code)    
        app_id = match_app_id.group(1) if match_app_id else None
        return app_id
    app_id = extract_app_id(code)
    return  "hEaIOlrX7tlhAOkz", "xMBwDXG1HOubUV04", "a0QHmC1Ova5958nC", "bMu71lHRX6bRmPxU","dLRSzDrm8xkryEyL", "fex6AA4zRfVrSPmr", '3c9208efcfb2f5b843eec8d96de6d48a'

def sort_object(obj):
    sorted_keys = sorted(obj.keys())
    new_dict = {key: obj[key] for key in sorted_keys}
    return new_dict

def headerCreator(method, params, AES_key, AES_iv, app_id, ctx):
    print("creating the payload...")
    client_type = 'WEB'
    timestamp = int(time.time() * 1000)
    sorted_params = sort_object(params)
    hash_md5 = hashlib.md5()
    hash_md5.update((app_id + method + str(timestamp) + client_type + json.dumps(sorted_params, ensure_ascii=False)).replace(" ","").encode())
    secret = hash_md5.hexdigest()
    data = {
      'appId': app_id,
      'method': method,
      'timestamp': timestamp,
      'clienttype': client_type,
      'object': sorted_params,
      'secret': secret
    }
    pKmSFk8 = base64.b64encode(json.dumps(data).encode('utf-8')).decode()
    pKmSFk8 = ctx.call("AES.encrypt", pKmSFk8, AES_key, AES_iv)
    return pKmSFk8

def data_decoder(data_encrypted, decrypt_DES_key, decrypt_DES_iv, decrypt_AES_key, decrypt_AES_iv, ctx):
    print("decrypting data...")
    data_encrypted = base64.b64decode(data_encrypted.encode('utf-8')).decode('utf-8')
    data = ctx.call("DES.decrypt", data_encrypted, decrypt_DES_key, decrypt_DES_iv)
    data = ctx.call("AES.decrypt", data, decrypt_AES_key, decrypt_AES_iv)
    data = base64.b64decode(data).decode()
    return data

def extract_data_to_dataframe(json_string):
    try:
        data = json.loads(json_string)
        items = data.get("result", {}).get("data", {}).get("items")

        if items:
            df = pd.DataFrame(items)
            return df
        else:
            return None

    except json.JSONDecodeError:
      print("Error: Invalid JSON format.")
      return None
    except Exception as e:
      print(f"An error occurred: {e}")
      return None