from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from src.config import load_settings
from src.twtapi_client import TwtApiClient, TwtApiError

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/api/trends", methods=["GET"])
def api_trends():
    woeid_raw = request.args.get("woeid", "1")
    try:
        woeid = int(woeid_raw)
    except ValueError:
        return jsonify({"ok": False, "error": "woeid 必须是整数"}), 400

    try:
        settings = load_settings()
        client = TwtApiClient(settings=settings)
        payload = client.get_trends(woeid=woeid)
        return jsonify({"ok": True, "result": payload})
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500
    except TwtApiError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"ok": False, "error": f"unexpected error: {exc}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
