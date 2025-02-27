import asyncio
import logging
from src.asynctk import AsyncTkUtils
from customtkinter import *
from tkinter import messagebox, PhotoImage

from src.soft import Soft


class AsyncAppCtk(CTk, AsyncTkUtils):
    def __init__(self, width=500, height=600, title="GetUsersTelegram", fg_color="#313034"):

        self._title = title
        self.fg_color = fg_color

        CTk.__init__(self)
        AsyncTkUtils.__init__(self)

        self.width, self.height = self.config.get("width", width), self.config.get("height", height)

        self.result_textbox = None

        self.group_textbox = None
        self.group_textbox_string = self.config.get("group_textbox_string", "")

        self.session_path_textbox = None
        self.session_path_string = self.config.get("session_path_textbox_string", "")

        self.api_id_textbox = None
        self.api_id_textbox_string = self.config.get("api_id_textbox_string", "")

        self.api_hash_textbox = None
        self.api_hash_textbox_string = self.config.get("api_hash_textbox_string", "")

        self.proxy_path_textbox = None
        self.proxy_path_textbox_string = self.config.get("proxy_path_textbox_string", "")

    def run(self):
        logging.info("Запуск программы")

        self.create_window()
        self.create_elements()

        while True:
            self.update()
            self.loop.run_until_complete(asyncio.sleep(0.01))

    def start(self):
        if not self.validate():
            return

        self.start_task(Soft(
            group_name=self.group_textbox_string,
            session_path=self.session_path_string,
            api_id=self.api_id_textbox_string,
            api_hash=self.api_hash_textbox_string,
            proxy=self.proxy_path_textbox_string,
            logger=self.result_textbox,
        ).get_users_telegram())

        self.config["width"], self.config["height"] = self.winfo_width(), self.winfo_height()
        self.save_config()

    def stop(self):
        self.stop_last_task()
        logging.info("Завершение работы программы")

    def copy_all(self):
        self.clipboard_append(self.result_textbox.get("1.0", "end-1c"))

    def validate(self):
        if len(self.group_textbox_string) == 0:
            self.message_box("Not data", "Your missed group name", type="error")
            return False

        if len(self.session_path_string) == 0:
            self.message_box("Not data", "Your missed session path", type="error")
            return False

        if not os.path.exists(self.session_path_string):
            self.message_box("Not data", f"Your session path is not exist - {self.session_path_string}", type="error")
            return False

        if len(self.api_id_textbox_string) == 0:
            self.message_box("Not data", "Your missed API ID", type="error")
            return False

        if len(self.api_hash_textbox_string) == 0:
            self.message_box("Not data", "Your missed API HASH", type="error")
            return False

        if len(self.proxy_path_textbox_string) == 0:
            self.message_box("Not data", "Your missed proxy path", type="error")
            return False

        return True

    def create_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width - self.width) / 2)
        y = int((screen_height - self.height) / 2)

        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.title(self._title)
        self.configure(fg_color=self.fg_color)
        app_icon = "src/files/app.ico"

        if os.path.exists(app_icon):
            self.after(201, lambda: self.iconbitmap(app_icon))
        else:
            logging.error("Error with set icon app")

        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        for i in range(5):
            self.grid_rowconfigure(i, weight=1)

    def create_elements(self):
        self.group_textbox = CTkEntry(self, height=28, width=200, corner_radius=10, placeholder_text="Enter group name:", fg_color="#343a40",
                                      textvariable=Variable(self, self.group_textbox_string) if len(self.group_textbox_string) > 0 else None, font=('Segoe UI', 15), text_color="white",
                                      border_color="#212529")
        self.group_textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.group_textbox.bind("<KeyRelease>", lambda e: self.input_text(self, "group_textbox"))

        self.result_textbox = CTkTextbox(self, width=400, height=400, corner_radius=25, fg_color="#212529", font=('Segoe UI', 20), text_color="#FFFAE3")
        self.result_textbox.grid(row=3, column=0, padx=4, pady=5, sticky="nsew", columnspan=2)

        self.session_path_textbox = CTkEntry(self, height=28, width=200, corner_radius=10, placeholder_text="Session path:", fg_color="#343a40",
                                             textvariable=Variable(self, self.session_path_string) if len(self.session_path_string) > 0 else None, font=('Segoe UI', 15), text_color="white",
                                             border_color="#212529")
        self.session_path_textbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.session_path_textbox.bind("<Button-1>", lambda e: self.file_dialog(self, "session_path_textbox", '.session'))

        self.api_id_textbox = CTkEntry(self, height=28, width=200, corner_radius=10, placeholder_text="API ID:", fg_color="#343a40",
                                       textvariable=Variable(self, self.api_id_textbox_string) if len(self.api_id_textbox_string) > 0 else None, font=('Segoe UI', 15), text_color="white",
                                       border_color="#212529")
        self.api_id_textbox.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.api_id_textbox.bind("<KeyRelease>", lambda e: self.input_text(self, "api_id_textbox"))

        self.api_hash_textbox = CTkEntry(self, height=28, width=200, corner_radius=10, placeholder_text="API HASH:", fg_color="#343a40",
                                         textvariable=Variable(self, self.api_hash_textbox_string) if len(self.api_hash_textbox_string) > 0 else None, font=('Segoe UI', 15), text_color="white",
                                         border_color="#212529")
        self.api_hash_textbox.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.api_hash_textbox.bind("<KeyRelease>", lambda e: self.input_text(self, "api_hash_textbox"))

        copy_all_button = CTkButton(self, text="", fg_color="#212529", hover_color="#22333b", command=self.copy_all, width=50, height=50, image=self.get_image("src/files/interface.png", (32, 32)))
        copy_all_button.grid(row=3, column=1, sticky="en", padx=30, pady=20)

        start_button = CTkButton(self, text="Start search", fg_color="#74F757", command=self.start, width=80, height=40, font=('Segoe UI', 10), text_color="black", hover_color="#06d6a0")
        start_button.grid(row=4, column=0, columnspan=2)

        self.proxy_path_textbox = CTkEntry(self, height=28, width=200, corner_radius=10, placeholder_text="Proxy:", fg_color="#343a40",
                                         textvariable=Variable(self, self.proxy_path_textbox_string) if len(self.proxy_path_textbox_string) > 0 else None, font=('Segoe UI', 15), text_color="white",
                                         border_color="#212529")
        self.proxy_path_textbox.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.proxy_path_textbox.bind("<KeyRelease>", lambda e: self.input_text(self, "proxy_path_textbox"))
