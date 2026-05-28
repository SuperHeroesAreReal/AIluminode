from __future__ import annotations

import sys

from .eeg import render, scan


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args or args[0].lower() in {"-h", "--help", "help"}:
        print_usage()
        return 0 if args else 1

    command = args.pop(0).lower()
    if command != "scan":
        print_usage()
        return 1

    prompt = " ".join(args).strip()
    if not prompt:
        print('Usage: ailuminode scan "<prompt>"')
        return 1

    print(render(scan(prompt)))
    return 0


def print_usage() -> None:
    print("AIluminode - wieldable AI cognitive-orientation EEG")
    print()
    print('Usage: ailuminode scan "<prompt>"')
    print()
    print("No crawling. No persistence. No telemetry. No memory ownership.")


if __name__ == "__main__":
    raise SystemExit(main())
