"""命令列進入點。"""
import argparse
import json
import sys
from pathlib import Path
from .core import classify, load_dotenv


def main() -> None:
    parser = argparse.ArgumentParser(description="使用本地 Ollama 將客服信件分類為 JSON")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="直接輸入信件文字")
    source.add_argument("--file", type=Path, help="讀取 UTF-8 文字檔")
    parser.add_argument("--output", type=Path, help="將結果另存 JSON")
    parser.add_argument("--model", help="覆寫 OLLAMA_MODEL")
    args = parser.parse_args()
    load_dotenv()
    try:
        message = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
        result = classify(message, model=args.model)
        rendered = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered + "\n", encoding="utf-8")
        print(rendered)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
