import os
import requests

def attempt_download(url, path=None):
    if path is None:
        path = os.path.join('weights', url.split('/')[-1])
    
    if not os.path.exists(path):
        print(f"Downloading {url} to {path}...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(path), exist_ok=True)  # Crée le dossier si nécessaire
            with open(path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Download completed: {path}")
        else:
            print(f"Failed to download {url} (status code {response.status_code})")
    else:
        print(f"{path} already exists, skipping download.")
