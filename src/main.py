from __future__ import annotations

import argparse
import json
import sys

from .config import load_settings
from .twtapi_client import TwtApiClient, TwtApiError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TwtAPI Python Demo CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    trends = subparsers.add_parser("trends", help="获取趋势话题")
    trends.add_argument("--woeid", type=int, default=1, help="地区 WOEID，默认 1(全球)")

    search = subparsers.add_parser("search", help="搜索推文")
    search.add_argument("--q", required=True, help="关键词或搜索表达式")
    search.add_argument("--type", default="Top", help="Top/Latest/User/Image/Video")
    search.add_argument("--count", type=int, default=20, help="返回条数，默认 20")

    user = subparsers.add_parser("user", help="根据用户名获取用户信息")
    user.add_argument("--username", required=True, help="Twitter 用户名（不含 @）")

    tweet_detail = subparsers.add_parser("tweet-detail", help="获取推文详情")
    tweet_detail.add_argument("--tweet-id", required=True, help="推文 ID（Rest ID）")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        settings = load_settings()
        client = TwtApiClient(settings=settings)

        if args.command == "trends":
            result = client.get_trends(woeid=args.woeid)
        elif args.command == "search":
            result = client.search_tweets(q=args.q, result_type=args.type, count=args.count)
        elif args.command == "user":
            result = client.get_user_by_screen_name(username=args.username)
        elif args.command == "tweet-detail":
            result = client.get_tweet_detail(tweet_id=args.tweet_id)
        else:
            parser.error(f"不支持的命令: {args.command}")
            return 2

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, TwtApiError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[UNEXPECTED ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
