import subprocess
import tkinter as tk
from tkinter import messagebox
import os
import requests

def fetch():
    head = {
        "authorization": "Bearer YOUR_NGROK_API_KEY", #api key
        "ngrok-version": "2"
    }
    try:
        respon = requests.get('https://api.ngrok.com/tunnels', headers=head)
        data = respon.json()

        for tunnel in data["tunnels"]:
            if tunnel["forwards_to"] == "localhost:3389":
                RDP_url = tunnel["public_url"].replace("tcp://", "")
                
                label_info_rdp = tk.Label(main_frame, text="Remote Desktop URL :")
                
                rdp_url_frame = tk.Frame(main_frame, relief=tk.SOLID, borderwidth=1)

                url_label_rdp = tk.Label(rdp_url_frame, fg="blue", text=RDP_url)
                copy_button_rdp = tk.Button(rdp_url_frame, text="Copy URL", command=lambda: copy(RDP_url))
                
                rdp_button = tk.Button(main_frame, text="Open on Remote Desktop", command=lambda: rdp(RDP_url))

                label_info_rdp.pack(pady=(5, 0))
                
                rdp_url_frame.pack(pady=(10, 0))
                url_label_rdp.pack(side=tk.LEFT, padx=10)
                copy_button_rdp.pack(side=tk.RIGHT)
                
                rdp_button.pack(pady=(10,15))
                
        for tunnel in data["tunnels"]:        
            if tunnel["forwards_to"] == "localhost:22":
                SSH_url = tunnel["public_url"].replace("tcp://", "")
                label_info_ssh = tk.Label(main_frame, text="SSH URL & Port :")
                
                ssh_url_frame = tk.Frame(main_frame, relief=tk.SOLID, borderwidth=1)
                url_label_ssh = tk.Label(ssh_url_frame, fg="blue", text=SSH_url)
                
                ssh_connect_frame = tk.Frame(main_frame)
                
                def on_click(event):
                    if user_entry.get() == "SSH Username":
                        user_entry.delete(0, "end")
                        user_entry.insert(0, "")
                        user_entry.config(fg="black")
                        
                
                def out_click(event):
                    if user_entry.get() == "":
                        user_entry.insert(0, "SSH Username")
                        user_entry.config(fg="gray")
                
                copy_button_ssh = tk.Button(ssh_url_frame, text="Copy URL", command=lambda: copy(SSH_url))
                
                user_entry = tk.Entry(ssh_connect_frame)
                user_entry.insert(0, "SSH Username")
                user_entry.bind('<FocusIn>', on_click)
                user_entry.bind('<FocusOut>', out_click)
                user_entry.config(fg="grey")
                
                open_ssh = tk.Button(ssh_connect_frame, text="Connect via SSH", command=lambda: ssh(SSH_url, user_entry.get()))
                
                label_info_ssh.pack(pady=(10, 0))
                
                ssh_url_frame.pack(pady=(5,0))
                url_label_ssh.pack(side=tk.LEFT, padx=10)
                copy_button_ssh.pack(side=tk.RIGHT)
                
                ssh_connect_frame.pack(pady=(5,0))
                user_entry.pack(side=tk.LEFT, padx=5, pady=5)
                open_ssh.pack(side=tk.RIGHT, pady=5)
                
    except Exception as e:
        messagebox.showerror(f"{e}")

def copy(url):
    if url:
        app.clipboard_clear()
        app.clipboard_append(url)
        app.update()  # necessary in some environments to make clipboard stick
        messagebox.showinfo("Info", "URL tersalin ke clipboard!")

def rdp(url):
    if url :
        cmd = f"mstsc /v:{url}"
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        messagebox.showwarning("RDP : invalid")

def ssh(url, user):
    user = user.strip()
    parts = url.split(":")
    host, port = parts
    if url:
        if user == "SSH Username" or not user:
            os.system(f"ssh {host} -p {port}")
        elif user:
            os.system(f"ssh \"{user}\"@{host} -p {port}")       

app = tk.Tk()
app.title("YOUR APP TITLE")
app.iconbitmap("E:\\Project\\Ngrok Tunnels App Clients\\mstsc_101.ico")

main_frame = tk.Frame(app, padx=20, pady=20)
main_frame.pack(padx=10, pady=5)

label_info = tk.Label(main_frame)
url_label = tk.Label(main_frame, fg="blue")
copy_button = tk.Button(main_frame, text="Copy URL")

fetch()

app.mainloop()