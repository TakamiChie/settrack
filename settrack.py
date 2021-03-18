from pathlib import Path
import re

from mutagen.easyid3 import EasyID3

def scan(trackno: int, dir: Path):
  for f in dir.iterdir():
    if f.is_dir():
      trackno = scan(trackno, f)
    elif f.is_file() and f.name.endswith("mp3"):
      tags = EasyID3(f)
      oldtrack = tags["tracknumber"]
      tags["tracknumber"] = f"{trackno}"
      print(f"> {f.name} {oldtrack} -> {trackno}")
      tags.save()
      f.rename(f.parent / re.sub(r"^\d+(-\d+)?\s*", "", f.name))
      trackno += 1
  return trackno

if __name__ == "__main__":
  scan(1, Path("."))
