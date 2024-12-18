from deepface import DeepFace

class EmotionAnalyzer:
    def analyze_emotions(self, image_path):
        """Анализ изображения для распознавания эмоций."""
        try:
            results = DeepFace.analyze(img_path=image_path, actions=['emotion'])
            if isinstance(results, list):
                return results[0]['dominant_emotion']
            return results['dominant_emotion']
        except Exception as e:
            raise RuntimeError(f"Ошибка анализа эмоций: {e}")