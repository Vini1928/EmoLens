from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class FullUI(BaseUI):
    def __init__(self, root, core):
        super().__init__(root)
        self.core = core
        self.file_path = None
        self.add_buttons()

    def add_buttons(self):
        """Добавление кнопок управления."""
        button_frame = tk.Frame(self.root, bg="#F7E01C")
        button_frame.pack()

        tk.Button(button_frame, text="Загрузить файл", command=self.load_file).pack(side="left", padx=5)
        tk.Button(button_frame, text="LIVE", command=self.capture_live).pack(side="left", padx=5)
        tk.Button(button_frame, text="Анализировать", command=self.analyze_image).pack(side="left", padx=5)

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png")])
        if self.file_path:
            self.display_image(self.file_path)

    def capture_live(self):
        try:
            temp_path = self.core.capture_from_camera()
            self.file_path = temp_path
            self.display_image(temp_path)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def display_image(self, path):
        image = Image.open(path).resize((300, 300))
        photo = ImageTk.PhotoImage(image)
        self.photo_frame.config(image=photo)
        self.photo_frame.image = photo

    def analyze_image(self):
        if not self.file_path:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение.")
            return
        try:
            emotion = self.core.analyze_emotions(self.file_path)
            self.result_label.config(text=f"Эмоция: {emotion}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))