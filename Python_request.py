
import requests
import time
import random
import tkinter as tk
from tkinter import ttk
import threading

# Replace these with the IP address and port of your server
server_ip = "192.168.1.11"
server_port = 8080

def send_get_request():
    url = f"http://{server_ip}:{server_port}"
    response = requests.get(url)
    if response.status_code == 200:
        print("GET response:")
        print(response.text)
    else:
        print(f"GET request failed with status code {response.status_code}")


def send_post_request(custom_msg=None):
    url = f"http://{server_ip}:{server_port}"
    if custom_msg:
        data = custom_msg
    else:
        data = {
            "sensor1": str(random.randint(0, 5000)),
            "sensor2": str(random.uniform(0, 5000))
        }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("POST response:")
        print(response)
    else:
        print(f"POST request failed with status code {response.status_code}")


def loop_requests():
    global stop_looping
    stop_looping = False
    
    loop_count = int(loop_count_entry.get())
    delay = float(delay_entry.get())
    
    loop_thread = threading.Thread(target=loop_requests_helper, args=(loop_count, delay), daemon=True)
    loop_thread.start()

def loop_requests_helper(loop_count, delay):
    for _ in range(loop_count):
        if stop_looping:
            break
        
        submit()
        time.sleep(delay)

def stop_loop():
    global stop_looping
    stop_looping = True


def submit():
    global server_ip, server_port
    server_ip = ip_entry.get()
    server_port = int(port_entry.get())
    request_type = request_type_var.get()
    if request_type == 'GET':
        send_get_request()
    elif request_type == 'POST':
        custom_msg = custom_msg_entry.get()
        if custom_msg.strip():
            send_post_request(custom_msg=custom_msg)
        else:
            send_post_request(custom_msg=None)

    # Update the visual log
    log_text.insert(tk.END, f"Sent {request_type} request to {server_ip}:{server_port}\n")
    log_text.see(tk.END)


app = tk.Tk()
app.title('Request Sender')

ip_label = ttk.Label(app, text='Server IP:')
ip_label.grid(column=0, row=0)
# Create a grid frame for better organization
grid_frame = ttk.Frame(app)
grid_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Place all widgets inside the grid_frame
ip_label = ttk.Label(grid_frame, text='Server IP:')
ip_label.grid(column=0, row=0)
ip_entry = ttk.Entry(grid_frame)
ip_entry.grid(column=1, row=0)
ip_entry.insert(0, server_ip)

port_label = ttk.Label(grid_frame, text='Server Port:')
port_label.grid(column=0, row=1)
port_entry = ttk.Entry(grid_frame)
port_entry.grid(column=1, row=1)
port_entry.insert(0, server_port)

request_type_label = ttk.Label(grid_frame, text='Request Type:')
request_type_label.grid(column=0, row=2)
request_type_var = tk.StringVar()
request_type_combobox = ttk.Combobox(grid_frame, textvariable=request_type_var, values=['GET', 'POST'], state='readonly')
request_type_combobox.current(1)
request_type_combobox.grid(column=1, row=2)

custom_msg_label = ttk.Label(grid_frame, text='Custom Message (POST):')
custom_msg_label.grid(column=0, row=3)
custom_msg_entry = ttk.Entry(grid_frame)
custom_msg_entry.grid(column=1, row=3)

submit_button = ttk.Button(grid_frame, text='Send Request', command=submit)
submit_button.grid(column=0, row=4, columnspan=2)
# Add a loop count input
loop_count_label = ttk.Label(grid_frame, text='Loop Count:')
loop_count_label.grid(column=0, row=5)
loop_count_entry = ttk.Entry(grid_frame)
loop_count_entry.grid(column=1, row=5)
loop_count_entry.insert(0, '1')

# Add a button to start looping requests
loop_button = ttk.Button(grid_frame, text='Loop Requests', command=loop_requests)
loop_button.grid(column=0, row=6, columnspan=2)

# Add a visual log using a Text widget
log_label = ttk.Label(grid_frame, text='Log:')
log_label.grid(column=0, row=7)
log_text = tk.Text(grid_frame, wrap=tk.WORD, height=10, width=40)
log_text.grid(column=0, row=8, columnspan=2)
log_scrollbar = ttk.Scrollbar(grid_frame, orient=tk.VERTICAL, command=log_text.yview)
log_scrollbar.grid(column=2, row=8, sticky=tk.N + tk.S)
log_text.configure(yscrollcommand=log_scrollbar.set)

delay_label = ttk.Label(grid_frame, text='Delay (sec):')
delay_label.grid(column=0, row=6)
delay_entry = ttk.Entry(grid_frame)
delay_entry.grid(column=1, row=6)
delay_entry.insert(0, '1')

stop_button = ttk.Button(app, text='Stop Loop', command=stop_loop)
stop_button.grid(column=0, row=9, columnspan=2)

app.mainloop()