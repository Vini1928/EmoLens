import tkinter as tk

class BaseUI:
    def __init__(self, root):
        self.root = root
        self.setup_base_ui()

    def setup_base_ui(self):
        """Базовый макет приложения."""
        self.root.title("Эмоциональная линза")
        self.root.geometry("800x600")
        self.root.configure(bg="#F7E01C")

        # Фото и результат
        self.photo_frame = tk.Label(self.root, text="ЗДЕСЬ ФОТО", bg="#FFEC69", height=20)
        self.photo_frame.pack(fill="both", expand=True)

        self.result_label = tk.Label(self.root, text="РЕЗУЛЬТАТ", bg="#FFEC69", height=5)
        self.result_label.pack(fill="both", expand=True)