class EmoLensCore(ImageCapture, EmotionAnalyzer):
    """Основной класс, объединяющий захват изображений и анализ эмоций."""
    def __init__(self):
        super().__init__()