import subprocess, sys

subprocess.run([sys.executable, "-m", "pip", "install", "textblob", "nltk"])
subprocess.run([sys.executable, "-m", "textblob.download_corpora"])
