import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class Installer:
    def __init__(self, master):
        self.master = master
        master.title("Step-Audio-EditX Installer")

        self.label = tk.Label(master, text="Welcome to the Step-Audio-EditX Installer!")
        self.label.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=25)
        self.text_area.pack(pady=10, padx=10)

        self.progress = ttk.Progressbar(master, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.install_button = tk.Button(master, text="Install", command=self.install)
        self.install_button.pack(pady=5)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack(pady=5)

    def log(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)
        self.master.update_idletasks()

    def run_command(self, command, step, total_steps):
        self.log(f"--- Step {step}/{total_steps}: {' '.join(command)} ---")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        for line in process.stdout:
            self.log(line.strip())
        process.wait()

        self.progress['value'] = (step / total_steps) * 100
        self.master.update_idletasks()

        if process.returncode != 0:
            self.log(f"--- ERROR: Command failed: {' '.join(command)} ---")
            messagebox.showerror("Error", "An error occurred. Please check the log for details.")
            return False
        return True

    def check_prerequisites(self):
        self.log("--- Checking prerequisites ---")
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            self.log("✅ Git is installed.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log("❌ Git is not installed. Please install Git and try again.")
            messagebox.showerror("Error", "Git is not installed. Please install Git and try again.")
            return False

        try:
            subprocess.run(["conda", "--version"], capture_output=True, check=True)
            self.log("✅ Conda is installed.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log("❌ Conda is not installed. Please install Conda and try again.")
            messagebox.showerror("Error", "Conda is not installed. Please install Conda and try again.")
            return False
        self.log("--- Prerequisites check complete ---")
        return True

    def install(self):
        self.install_button.config(state=tk.DISABLED)
        self.progress['value'] = 0
        total_steps = 5

        if not self.check_prerequisites():
            self.install_button.config(state=tk.NORMAL)
            return

        commands = [
            ["conda", "create", "-n", "stepaudioedit", "python=3.10", "-y"],
            ["conda", "run", "-n", "stepaudioedit", "pip", "install", "-r", "requirements.txt"],
            ["conda", "run", "-n", "stepaudioedit", "git", "lfs", "install"],
            ["conda", "run", "-n", "stepaudioedit", "git", "clone", "https://huggingface.co/stepfun-ai/Step-Audio-Tokenizer"],
            ["conda", "run", "-n", "stepaudioedit", "git", "clone", "https://huggingface.co/stepfun-ai/Step-Audio-EditX"]
        ]

        for i, cmd in enumerate(commands):
            if not self.run_command(cmd, i + 1, total_steps):
                self.install_button.config(state=tk.NORMAL)
                return

        self.log("\n🎉 Installation complete! You can now close this window and run the launcher.")
        messagebox.showinfo("Success", "Installation complete!")
        self.install_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    installer = Installer(root)
    root.mainloop()
