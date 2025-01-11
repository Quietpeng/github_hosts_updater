import tkinter as tk
from tkinter import messagebox
import requests
import os
import time
import threading
from pathlib import Path

class HostsUpdater:
    def __init__(self):
        self.url = "https://raw.hellogithub.com/hosts"
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.running = False
        self.original_hosts = ""  # 保存原始hosts内容
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("GitHub Hosts Updater")
        self.root.geometry("500x500")
        
        # 添加说明文本
        self.info_text = tk.Text(self.root, height=10, width=50)
        self.info_text.pack(pady=10)
        self.info_text.insert(tk.END, """
功能说明：
此程序将自动更新您的hosts文件，以优化GitHub访问速度。

注意事项：
1. 需要管理员权限
2. 会修改系统hosts文件
3. 请勿随意关闭程序窗口
4. 每10分钟自动更新一次

是否确认运行？
        """)
        self.info_text.config(state='disabled')

        # 添加hosts路径框架
        path_frame = tk.Frame(self.root)
        path_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(path_frame, text="Hosts文件路径:").pack(side='left')
        self.path_var = tk.StringVar(value=self.hosts_path)
        self.path_entry = tk.Entry(path_frame, textvariable=self.path_var, width=40)
        self.path_entry.pack(side='left', padx=5)
        tk.Button(path_frame, text="修改", command=self.change_hosts_path).pack(side='left')

        # 添加URL路径框架
        url_frame = tk.Frame(self.root)
        url_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(url_frame, text="更新源地址:").pack(side='left')
        self.url_var = tk.StringVar(value=self.url)
        self.url_entry = tk.Entry(url_frame, textvariable=self.url_var, width=40)
        self.url_entry.pack(side='left', padx=5)
        tk.Button(url_frame, text="修改", command=self.change_url).pack(side='left')

        # 添加状态信息
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(fill='x', padx=20, pady=5)
        
        self.status_label = tk.Label(self.status_frame, text="等待开始...")
        self.status_label.pack()
        
        self.next_update_label = tk.Label(self.status_frame, text="")
        self.next_update_label.pack()
        
        self.hosts_status_label = tk.Label(self.status_frame, text="")
        self.hosts_status_label.pack()

        # 添加启动按钮
        self.start_button = tk.Button(self.root, text="确认并开始运行", command=self.start_updating)
        self.start_button.pack(pady=10)

    def change_hosts_path(self):
        new_path = self.path_var.get()
        if self.check_hosts_file(new_path):
            self.hosts_path = new_path
            self.update_status("Hosts路径更新成功！")
        else:
            self.path_var.set(self.hosts_path)  # 恢复原路径

    def check_hosts_file(self, path):
        try:
            # 检查文件是否存在
            if not os.path.exists(path):
                self.update_status(f"错误: Hosts文件不存在: {path}")
                return False
            
            # 检查写入权限
            test_file = f"{path}.test"
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
            except PermissionError:
                self.update_status("错误: 没有写入权限，请以管理员身份运行")
                return False
            
            return True
        except Exception as e:
            self.update_status(f"错误: {str(e)}")
            return False

    def update_hosts(self):
        try:
            if not self.check_hosts_file(self.hosts_path):
                return False
            
            response = requests.get(self.url, headers=self.headers)
            
            with open(self.hosts_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            self.update_status("更新成功！")
            self.hosts_status_label.config(text=f"Hosts文件已更新: {self.hosts_path}")
            return True
        except Exception as e:
            self.update_status(f"更新失败: {str(e)}")
            return False

    def update_status(self, message):
        self.status_label.config(text=message)

    def update_loop(self):
        while self.running:
            self.update_hosts()
            time.sleep(600)  # 10分钟更新一次

    def update_countdown(self):
        remaining = 600  # 10分钟
        while self.running:
            mins, secs = divmod(remaining, 60)
            self.next_update_label.config(text=f"下次更新倒计时: {mins}分{secs}秒")
            time.sleep(1)
            remaining -= 1
            if remaining < 0:
                remaining = 600

    def start_updating(self):
        if not self.running:
            if not self.check_hosts_file(self.hosts_path):
                return
            
            # 保存原始hosts内容
            try:
                with open(self.hosts_path, 'r', encoding='utf-8') as f:
                    self.original_hosts = f.read()
            except Exception as e:
                self.update_status(f"保存原始hosts失败: {str(e)}")
                return
            
            self.running = True
            self.start_button.config(state='disabled')
            self.path_entry.config(state='disabled')
            self.url_entry.config(state='disabled')  # 运行时禁用URL修改
            self.update_status("程序已启动，正在后台运行...")
            
            # 启动更新线程
            update_thread = threading.Thread(target=self.update_loop)
            update_thread.daemon = True
            update_thread.start()
            
            # 启动倒计时线程
            countdown_thread = threading.Thread(target=self.update_countdown)
            countdown_thread.daemon = True
            countdown_thread.start()

    def restore_hosts(self):
        try:
            with open(self.hosts_path, 'w', encoding='utf-8') as f:
                f.write(self.original_hosts)
            self.update_status("已恢复原始hosts文件")
            return True
        except Exception as e:
            self.update_status(f"恢复hosts失败: {str(e)}")
            return False

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("确认", "是否恢复原始hosts文件并退出程序？"):
            self.running = False
            if self.original_hosts:  # 如果有保存原始内容才恢复
                self.restore_hosts()
            self.root.destroy()

    def change_url(self):
        new_url = self.url_var.get()
        try:
            # 测试新URL是否可访问
            response = requests.get(new_url, headers=self.headers)
            if response.status_code == 200:
                self.url = new_url
                self.update_status("更新源地址修改成功！")
            else:
                raise Exception(f"HTTP状态码: {response.status_code}")
        except Exception as e:
            self.update_status(f"更新源地址无效: {str(e)}")
            self.url_var.set(self.url)  # 恢复原地址

if __name__ == '__main__':
    updater = HostsUpdater()
    updater.run() 