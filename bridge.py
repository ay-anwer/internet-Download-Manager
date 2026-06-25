import os
import requests
import certifi
import urllib3
from PySide6.QtCore import QObject, Slot, Signal, QThread, QUrl
from PySide6.QtQml import QmlElement


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QML_IMPORT_NAME = "Backend"
QML_IMPORT_MAJOR_VERSION = 1

class DownloadWorker(QThread):
    progress = Signal(int)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path


    def run(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            }

            response = requests.get(self.url, stream=True, verify=certifi.where(), headers=headers, timeout=15)
            response.raise_for_status()

            total_length = response.headers.get('content-length')

            with open(self.save_path, "wb") as f:
                if total_length is None:
                    f.write(response.content)
                    self.progress.emit(100)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(100 * dl / total_length)
                        self.progress.emit(done)
        except Exception as e:
            print(f"\n[Error] Download Failed: {e}\n")


@QmlElement
class Bridge(QObject):
    progressUpdated = Signal(int)
    downloadCompleted = Signal()

    def __init__(self):
        super().__init__()
        self.worker = None

    @Slot(str, str, int)
    def startDownload(self, url, folder_url, connections):
        folder_path = QUrl(folder_url).toLocalFile()
        filename = url.split('/')[-1]
        if not filename:
            filename = "downloaded_file"
            
        save_path = os.path.join(folder_path, filename)
        
        self.worker = DownloadWorker(url, save_path)
        self.worker.progress.connect(self.progressUpdated)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_worker_finished(self):
        self.downloadCompleted.emit()
        if self.worker is not None:
            self.worker.deleteLater()
            self.worker = None
