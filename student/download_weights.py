from utils.google_utils import attempt_download

# Liste des modèles à télécharger
model_urls = [
    'https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt',
    'https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5m.pt',
    'https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5l.pt',
    'https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5x.pt'
]

# Télécharger chaque modèle
for url in model_urls:
    attempt_download(url)
