import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, target_file, scene_name):
        self.target_file = os.path.abspath(target_file)
        self.scene_name = scene_name
        self.cmd = ["manim", "-pql", target_file, scene_name]

    def on_modified(self, event):
        # Only react if the target file changes
        if os.path.abspath(event.src_path) == self.target_file:
            print(f"[Watcher] Detected change in {self.target_file}, re-rendering...")
            subprocess.run(self.cmd)

def main():
    if len(sys.argv) < 3:
        print("Usage: python auto_manim.py <scene_file> <SceneClassName>")
        sys.exit(1)
    scene_file = sys.argv[1]
    scene_name = sys.argv[2]
    event_handler = ChangeHandler(scene_file, scene_name)
    observer = Observer()
    dirpath = os.path.dirname(os.path.abspath(scene_file))
    observer.schedule(event_handler, dirpath, recursive=False)
    observer.start()
    print(f"[Watcher] Watching {scene_file} for changes. Press Ctrl+C to quit.")
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
