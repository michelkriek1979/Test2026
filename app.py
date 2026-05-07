from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

CITY_TRIPS = [
    "Parijs",
    "Rome",
    "Barcelona",
    "Lissabon",
    "Berlijn",
    "Praag",
    "Wenen",
    "Boedapest",
    "Kopenhagen",
    "Dublin",
]

SELECTIONS_FILE = Path("geselecteerde_stedentrips.json")


def load_selected_trips() -> list[str]:
    if not SELECTIONS_FILE.exists():
        return []

    try:
        with SELECTIONS_FILE.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except (json.JSONDecodeError, OSError):
        return []

    selected = data.get("geselecteerde_stedentrips", [])
    if not isinstance(selected, list):
        return []

    return [trip for trip in selected if trip in CITY_TRIPS]


def save_selected_trips(selected_trips: list[str]) -> None:
    data = {"geselecteerde_stedentrips": selected_trips}
    with SELECTIONS_FILE.open("w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


@app.route("/", methods=["GET"])
def index():
    selected_trips = load_selected_trips()
    return render_template(
        "index.html",
        city_trips=CITY_TRIPS,
        selected_trips=selected_trips,
    )


@app.route("/stedentrip/<stad>", methods=["GET"] )
def stedentrip_detail(stad: str):
    if stad.lower() != "barcelona":
        abort(404)
    return render_template("barcelona.html")


@app.route("/opslaan", methods=["POST"])
def opslaan():
    selected_trips = request.form.getlist("stedentrips")
    valid_selected_trips = [trip for trip in selected_trips if trip in CITY_TRIPS]
    save_selected_trips(valid_selected_trips)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
