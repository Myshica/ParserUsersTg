import asyncio
import json
import os
import tkinter.messagebox
from tkinter import END, filedialog, Variable

import aiofiles
import loguru
from PIL import Image
from customtkinter import CTkImage


class AsyncTkUtils:
    def __init__(self):
        self.tasks = []
        self.loop = asyncio.get_event_loop()
        self.config = {}
        self.load_config()

    def start_task(self, task):
        _task = self.loop.create_task(task)
        self.tasks.append(_task)

    def stop_last_task(self):
        t = self.tasks[-1]
        t.cancel()
        self.tasks.remove(t)

    async def wait_all_tasks(self):
        await asyncio.gather(*self.tasks, return_exceptions=True)

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                self.config = json.loads(f.read())
        except:
            pass

    def save_config(self):
        with open("config.json", "w") as f:
            f.write(json.dumps(self.config))

    def get_image(self, path: str, size: tuple = (32, 32)):
        return CTkImage(Image.open(path), size=size)

    def input_text(self, app, textbox_name: str):
        attr = getattr(app, textbox_name)
        text = attr.get()
        setattr(app, textbox_name + "_string", text)
        self.config[textbox_name + "_string"] = text
        self.save_config()

    def file_dialog(self, app, textbox_name: str, file_ending: str = ".txt"):
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("Текстовые файлы", f"*{file_ending}")]
        )
        attr = getattr(app, textbox_name)
        if len(file_path) > 0 and os.path.exists(file_path) and file_path.endswith(file_ending):
            attr.configure(textvariable=Variable(app, file_path), border_color="green")
            setattr(app, textbox_name + "_string", file_path)
            self.config[textbox_name + "_string"] = file_path
            self.save_config()
        else:
            attr.configure(border_color="red")

    def file_dialog_dir(self, app, textbox_name: str):
        file_path = filedialog.askdirectory(
            title="Выберите папку"
        )
        attr = getattr(app, textbox_name)
        if len(file_path) > 0 and os.path.exists(file_path):
            attr.configure(textvariable=Variable(app, file_path), border_color="green")
            setattr(app, textbox_name + "_string", file_path)
            self.config[textbox_name + "_string"] = file_path
            self.save_config()
        else:
            attr.configure(border_color="red")

    def message_box(self, title: str, message: str, type: str = "ok"):
        if type == "ok":
            tkinter.messagebox.showinfo(title, message)
        elif type == "warning":
            tkinter.messagebox.showwarning(title, message)
        elif type == "error":
            tkinter.messagebox.showerror(title, message)
