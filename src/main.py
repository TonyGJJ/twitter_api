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
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        settings = load_settings()
        client = TwtApiClient(settings=settings)

        if args.command == "trends":
            result = client.get_trends(woeid=args.woeid)
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
