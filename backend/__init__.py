import json
from pathlib import Path

from flask import Flask

app = Flask(__name__)

data_path = Path(__file__).parent / "data" / "pictures.json"
with data_path.open(encoding="utf-8") as pictures_file:
    data = json.load(pictures_file)

from . import routes  # noqa: E402,F401