def analyze_image(self):
    if not self.file_path:
        messagebox.showwarning("Внимание", "Сначала загрузите изображение.")
        return
    try:
        emotion = self.core.analyze_emotions(self.file_path)
        self.result_label.config(text=f"Эмоция: {emotion}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))