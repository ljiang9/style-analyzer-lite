"""命令行：python3 cli.py "文本" 或 -f file.txt"""
import argparse
import json
import sys

from analyzer import analyze_style, report


def main(argv=None):
    p = argparse.ArgumentParser(description="style-analyzer-lite 文风分析")
    p.add_argument("text", nargs="?", help="待分析文本")
    p.add_argument("-f", "--file")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.text or sys.stdin.read()
    if not text.strip():
        print("错误：未提供文本", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(analyze_style(text), ensure_ascii=False, indent=2))
    else:
        print(report(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
