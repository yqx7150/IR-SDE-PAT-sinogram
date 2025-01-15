import tkinter as tk
from tkinter import messagebox
import paramiko
import os
import time
from PIL import Image, ImageTk

# 服务器配置
server_host = "222.204.17.186"  # 使用IP地址
server_user = "b110"            # 使用SSH配置文件中的User
server_password = "123"         # 你的密码

# 服务器端测试代码的路径和参数
test_command = "python test.py -opt=options/test/refusion-leejh.yml"
image_dir = "/home/b110/code/LZL/irsde/codes/config/deblurring/sde_state"
local_image_dir = "sde_state"  # 本地保存图片的目录

# 创建SSH客户端
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 定义一个函数，用于运行服务器端的测试代码
def run_training():
    try:
        ssh.connect(server_host, username=server_user, password=server_password)
        stdin, stdout, stderr = ssh.exec_command(f"conda activate lx_irsde && cd /home/b110/code/LZL/irsde/codes/config/deblurring && {test_command}")
        messagebox.showinfo("信息", "开始运行测试代码...")
    except Exception as e:
        messagebox.showerror("错误", f"无法连接到服务器: {e}")

# 定义一个函数，用于实时显示生成的图片
def display_images():
    try:
        ssh.connect(server_host, username=server_user, password=server_password)
        sftp = ssh.open_sftp()
        sftp.getcwd()
        sftp.chdir(image_dir)
        image_files = sorted([f for f in sftp.listdir() if f.endswith('.png')], key=lambda x: int(x.split('_')[-1].split('.')[0]), reverse=True)
        for image_file in image_files:
            remote_path = os.path.join(image_dir, image_file)
            local_path = os.path.join(local_image_dir, image_file)
            sftp.get(remote_path, local_path)
            print(f"下载文件: {local_path}")  # 调试信息
            img = Image.open(local_path)
            img = img.resize((512, 512), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk
            root.update()
            time.sleep(0.1)  # 控制显示速度
    except Exception as e:
        messagebox.showerror("错误", f"无法显示图片: {e}")

# 创建主窗口
root = tk.Tk()
root.title("测试过程实时显示")
root.geometry("600x600")

# 创建运行按钮
run_button = tk.Button(root, text="运行测试", command=run_training)
run_button.pack(pady=10)

# 创建显示图片的标签
image_label = tk.Label(root)
image_label.pack(pady=10)

# 创建显示图片的按钮
display_button = tk.Button(root, text="显示图片", command=display_images)
display_button.pack(pady=10)

# 运行主循环
root.mainloop()
