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


@app.route("/api/search", methods=["GET"])
def api_search():
    q = request.args.get("q", "").strip()
    result_type = request.args.get("type", "Top").strip() or "Top"
    count_raw = request.args.get("count", "20")

    if not q:
        return jsonify({"ok": False, "error": "q 不能为空"}), 400

    try:
        count = int(count_raw)
    except ValueError:
        return jsonify({"ok": False, "error": "count 必须是整数"}), 400

    try:
        settings = load_settings()
        client = TwtApiClient(settings=settings)
        payload = client.search_tweets(q=q, result_type=result_type, count=count)
        return jsonify({"ok": True, "result": payload})
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500
    except TwtApiError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"ok": False, "error": f"unexpected error: {exc}"}), 500


@app.route("/api/user", methods=["GET"])
def api_user():
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify({"ok": False, "error": "username 不能为空"}), 400

    try:
        settings = load_settings()
        client = TwtApiClient(settings=settings)
        payload = client.get_user_by_screen_name(username=username)
        return jsonify({"ok": True, "result": payload})
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500
    except TwtApiError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"ok": False, "error": f"unexpected error: {exc}"}), 500


@app.route("/api/tweet-detail", methods=["GET"])
def api_tweet_detail():
    tweet_id = request.args.get("tweet_id", "").strip()
    if not tweet_id:
        return jsonify({"ok": False, "error": "tweet_id 不能为空"}), 400

    try:
        settings = load_settings()
        client = TwtApiClient(settings=settings)
        payload = client.get_tweet_detail(tweet_id=tweet_id)
        return jsonify({"ok": True, "result": payload})
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500
    except TwtApiError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"ok": False, "error": f"unexpected error: {exc}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
