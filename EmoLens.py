import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from deepface import DeepFace
import cv2
import os
import matplotlib.pyplot as plt

class EmoLensApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Эмоциональная линза (EmoLens)")
        self.root.geometry("1200x900")
        self.root.configure(bg="#F7E01C")  # Светло-желтый фон
        self.camera_active = False
        self.cap = None  # Для захвата видеопотока

        # Заголовок
        title_label = tk.Label(root, text="Эмоциональная линза (EmoLens)", font=("Helvetica", 28), bg="#F7E01C", fg="#4B4B4B")
        title_label.pack(pady=10)

        # Основной фрейм
        main_frame = tk.Frame(root, bg="#F7E01C")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Левые и правые панели
        left_panel = tk.Frame(main_frame, bg="#FFF5A5")
        left_panel.pack(side="left", fill="both", expand=True, padx=10)
        right_panel = tk.Frame(main_frame, bg="#FFF5A5")
        right_panel.pack(side="right", fill="both", expand=True, padx=10)

        # Окно для фото
        self.photo_frame = tk.Label(left_panel, text="PHOTO", relief="solid", bg="#FFEC69")
        self.photo_frame.pack(fill="both", expand=True, pady=20)

        # Поле ввода и кнопки
        input_frame = tk.Frame(left_panel, bg="#FFF5A5")
        input_frame.pack(fill="x", pady=5)
        self.file_path = tk.StringVar()
        path_entry = tk.Entry(input_frame, textvariable=self.file_path, font=("Helvetica", 12), bg="white")
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        browse_button = tk.Button(input_frame, text="Search", command=self.browse_file, font=("Helvetica", 12), bg="#F9A825", fg="white")
        browse_button.pack(side="left", padx=(0, 5))
        send_button = tk.Button(input_frame, text="Send", command=self.process_emotion, font=("Helvetica", 12), bg="#FF9800", fg="white")
        send_button.pack(side="left")

        # Кнопка Live
        live_button = tk.Button(left_panel, text="LIVE", command=self.start_live_feed, font=("Helvetica", 12), bg="#FF5722", fg="white")
        live_button.pack(fill="x", pady=5)

        # Окно для результата
        self.result_frame = tk.Label(right_panel, text="RESULT", relief="solid", bg="#FFEC69")
        self.result_frame.pack(fill="both", expand=True, pady=20)

        # Emotion и проценты
        emotion_info_frame = tk.Frame(right_panel, bg="#FFF5A5")
        emotion_info_frame.pack(fill="x", pady=5)
        emotion_label = tk.Label(emotion_info_frame, text="Emotion:", font=("Helvetica", 12), bg="#FFF5A5", fg="black")
        emotion_label.pack(side="left", padx=(0, 5))
        self.emotion_percentage = tk.Label(emotion_info_frame, text="xx%", font=("Helvetica", 12), bg="#FFF5A5", fg="black")
        self.emotion_percentage.pack(side="left")

        # Панель с кнопками Graphic и Info
        bottom_right_frame = tk.Frame(right_panel, bg="#FFF5A5")
        bottom_right_frame.pack(side="bottom", fill="x", pady=5)

        graphic_button = tk.Button(bottom_right_frame, text="Graphic", command=self.show_graph, font=("Helvetica", 12), bg="#F9A825", fg="white")
        graphic_button.pack(side="left", padx=5)

        info_button = tk.Button(bottom_right_frame, text="Info", command=self.show_info, font=("Helvetica", 12), bg="#FF9800", fg="white")
        info_button.pack(side="right", padx=5)

    def browse_file(self):
        if self.camera_active:
            self.stop_live_feed()
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.file_path.set(file_path)
            self.display_image(file_path)

    def start_live_feed(self):
        if not self.camera_active:
            self.camera_active = True
            self.cap = cv2.VideoCapture(0)
            self.update_live_feed()
        else:
            self.stop_live_feed()

    def stop_live_feed(self):
        self.camera_active = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def update_live_feed(self):
        if self.camera_active and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                window_width = self.photo_frame.winfo_width()
                new_size = int(window_width * 0.45)
                img = img.resize((new_size, new_size))
                photo = ImageTk.PhotoImage(img)
                self.photo_frame.config(image=photo)
                self.photo_frame.image = photo
                self.root.after(10, self.update_live_feed)
            else:
                self.stop_live_feed()

    def process_emotion(self):
        try:
            if self.camera_active:
                ret, frame = self.cap.read()
                if ret:
                    temp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    temp_frame = Image.fromarray(temp_frame)
                    temp_frame = temp_frame.resize((900, 600))
                    temp_frame_path = "temp_frame.jpg"
                    temp_frame.save(temp_frame_path)
                    self.analyze_image(temp_frame_path)
                else:
                    messagebox.showerror("Error", "Failed to capture live image.")
            else:
                file_path = self.file_path.get()
                if file_path:
                    self.analyze_image(file_path)
                else:
                    messagebox.showwarning("Warning", "Please select an image first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze emotion: {e}")

    def analyze_image(self, image_path):
        try:
            self.result_data = DeepFace.analyze(img_path=image_path, actions=['emotion'])
            if isinstance(self.result_data, list):
                self.result_data = self.result_data[0]
            emotion = self.result_data['dominant_emotion']
            confidence = f"{self.result_data['emotion'][emotion]:.2f}%"
            self.emotion_percentage.config(text=f"{emotion}: {confidence}")
            emotion_image_path = os.path.join("emotionspng", f"{emotion}.png")
            if os.path.exists(emotion_image_path):
                self.display_result_image(emotion_image_path)
            else:
                messagebox.showwarning("Warning", "Emotion image not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze emotion: {e}")

    def show_graph(self):
        try:
            if hasattr(self, 'result_data') and 'emotion' in self.result_data:
                emotions = list(self.result_data['emotion'].keys())
                scores = list(self.result_data['emotion'].values())
                plt.figure(figsize=(10, 5))
                plt.bar(emotions, scores, color='#FFEC69')  # Мягкий желтый цвет
                plt.xlabel('Emotions', fontsize=14)
                plt.ylabel('Confidence (%)', fontsize=14)
                plt.title('Emotion Analysis', fontsize=16)
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=12)
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.show()
            else:
                messagebox.showwarning("Warning", "No emotion data available for graph.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate graph: {e}")

    def show_info(self):
        info_text = (
            "Эмоциональная линза (EmoLens)\n\n"
            "Описание:\n"
            "Программа предназначена для определения эмоций человека на изображениях или в реальном времени через камеру.\n\n"
            "Функциональность:\n"
            "- 'Search': Загрузка изображения для анализа.\n"
            "- 'Send': Анализ загруженного изображения.\n"
            "- 'LIVE': Включение/выключение анализа в реальном времени с камеры.\n"
            "- 'Graphic': Построение графика распределения эмоций.\n"
            "- 'Info': Отображение справочной информации о программе.\n\n"
            "Инструкция по эксплуатации:\n"
            "1. Загрузите изображение с помощью кнопки 'Search' или активируйте камеру через 'LIVE'.\n"
            "2. Нажмите 'Send' для анализа эмоций на изображении.\n"
            "3. Для визуализации распределения эмоций нажмите 'Graphic'.\n"
            "4. Для справки и версии программы используйте 'Info'.\n\n"
            "Авторы:\nКожемяк Максим,\nРябова Виктория,\nМерзенев Георгий\n"
        )
        messagebox.showinfo("Info", info_text)

    def display_image(self, file_path):
        try:
            image = Image.open(file_path)
            window_width = self.photo_frame.winfo_width()
            new_size = int(window_width * 0.45)
            image = image.resize((new_size, new_size))
            photo = ImageTk.PhotoImage(image)
            self.photo_frame.config(image=photo)
            self.photo_frame.image = photo
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

    def display_result_image(self, image_path):
        try:
            image = Image.open(image_path)
            window_width = self.result_frame.winfo_width()
            new_size = int(window_width * 0.45)
            image = image.resize((new_size, new_size))
            photo = ImageTk.PhotoImage(image)
            self.result_frame.config(image=photo)
            self.result_frame.image = photo
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение эмоции: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmoLensApp(root)
    root.mainloop()
