import json
import logging

class JSONExporter:
    def export(self, path: str, data: list):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error writing file {path}: {e}")
            raise