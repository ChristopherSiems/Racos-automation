import os

for root, dirs, files in os.walk('plots'):
  for filename in files:
    if filename.startswith('plot'):
      file_path = os.path.join(root, filename)
      os.remove(file_path)
      print(f"Removed: {file_path}")