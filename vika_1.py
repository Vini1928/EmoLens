import cv2
from PIL import Image

class ImageCapture:
    def __init__(self):
        self.cap = None

    def capture_from_camera(self):
        """Захват изображения с камеры в реальном времени."""
        self.cap = cv2.VideoCapture(0)
        ret, frame = self.cap.read()
        if ret:
            temp_path = "live_image.jpg"
            Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).save(temp_path)
            return temp_path
        else:
            raise RuntimeError("Не удалось получить изображение с камеры.")

    def release_camera(self):
        """Освобождение камеры."""
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()

    def load_from_file(self, file_path):
        """Загрузка изображения из файла."""
        if file_path:
            return file_path
        else:
            raise ValueError("Путь к файлу пустой.")