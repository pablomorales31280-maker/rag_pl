import os
import json
import zipfile
from tqdm import tqdm

from src.config import SETTINGS
from src.html_parser import parse_html_page

def main():
    os.makedirs("data/processed", exist_ok=True)

    with zipfile.ZipFile(SETTINGS.raw_zip_path, "r") as z:
        html_files = [f for f in z.namelist() if f.lower().endswith(".html")]

        with open(SETTINGS.documents_path, "w", encoding="utf-8") as out:
            for path in tqdm(html_files, desc="Parsing HTML"):
                raw = z.read(path).decode("utf-8", errors="ignore")
                doc = parse_html_page(raw, source_file=path)

                # Si pas d'URL canonique, garde au moins le fichier
                if not doc["source_url"]:
                    doc["source_url"] = None

                out.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(f"OK -> {SETTINGS.documents_path}")

if __name__ == "__main__":
    main()