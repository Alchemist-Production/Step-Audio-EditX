import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext

class Installer:
    def __init__(self, master):
        self.master = master
        master.title("Step-Audio-EditX Installer")

        self.label = tk.Label(master, text="Welcome to the Step-Audio-EditX Installer!")
        self.label.pack()

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack()

        self.install_button = tk.Button(master, text="Install", command=self.install)
        self.install_button.pack()

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

    def log(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)
        self.master.update_idletasks()

    def run_command(self, command):
        self.log(f"Running command: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        for line in process.stdout:
            self.log(line.strip())
        process.wait()
        if process.returncode != 0:
            self.log(f"Error executing command: {' '.join(command)}")
            messagebox.showerror("Error", f"An error occurred. Please check the log for details.")
            return False
        return True

    def check_prerequisites(self):
        self.log("Checking for prerequisites...")
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            self.log("Git is installed.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log("Git is not installed. Please install Git and try again.")
            messagebox.showerror("Error", "Git is not installed. Please install Git and try again.")
            return False

        try:
            subprocess.run(["conda", "--version"], capture_output=True, check=True)
            self.log("Conda is installed.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log("Conda is not installed. Please install Conda and try again.")
            messagebox.showerror("Error", "Conda is not installed. Please install Conda and try again.")
            return False
        return True

    def install(self):
        self.install_button.config(state=tk.DISABLED)
        if not self.check_prerequisites():
            self.install_button.config(state=tk.NORMAL)
            return

        self.log("Creating Conda environment...")
        if not self.run_command(["conda", "create", "-n", "stepaudioedit", "python=3.10", "-y"]):
            self.install_button.config(state=tk.NORMAL)
            return

        self.log("Activating Conda environment...")
        # This is tricky as we can't activate in the same shell.
        # We will run subsequent commands using `conda run`

        self.log("Installing dependencies...")
        if not self.run_command(["conda", "run", "-n", "stepaudioedit", "pip", "install", "-r", "requirements.txt"]):
            self.install_button.config(state=tk.NORMAL)
            return

        self.log("Downloading models...")
        if not self.run_command(["conda", "run", "-n", "stepaudioedit", "git", "lfs", "install"]):
            self.install_button.config(state=tk.NORMAL)
            return
        if not self.run_command(["conda", "run", "-n", "stepaudioedit", "git", "clone", "https://huggingface.co/stepfun-ai/Step-Audio-Tokenizer"]):
            self.install_button.config(state=tk.NORMAL)
            return
        if not self.run_command(["conda", "run", "-n", "stepaudioedit", "git", "clone", "https://huggingface.co/stepfun-ai/Step-Audio-EditX"]):
            self.install_button.config(state=tk.NORMAL)
            return

        self.log("Installation complete!")
        messagebox.showinfo("Success", "Installation complete!")
        self.install_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    installer = Installer(root)
    root.mainloop()
