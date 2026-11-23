"""
Точка входа для командной строки.

Запуск:

    python cli.py add --address "ул. Ленина" --area 65 --price 8500000
    python cli.py list
    python cli.py report
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from real_estate.cli import create_parser, Commands
from config import AGENCY_NAME, DB_PATH


def main() -> None:
    """Точка входа CLI."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = Commands(
        db_path=DB_PATH,
        autoload=True,
        autosave=True,
        agency_name=AGENCY_NAME,
    )
    handler = getattr(commands, f"cmd_{args.command}", None)

    if handler is None:
        print(f"✗ Неизвестная команда: {args.command}")
        parser.print_help()
        return

    handler(args)


if __name__ == "__main__":
    main()
