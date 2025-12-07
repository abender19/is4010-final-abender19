"""Command-line interface for File Statistics Analyzer."""

import sys
import argparse
from pathlib import Path
from filestat.analyzer import FileAnalyzer
from filestat.formatter import format_output, console


def create_parser() -> argparse.ArgumentParser:
    """Create and return argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="filestat",
        description="Analyze files and directories to get statistics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  filestat path/to/file.txt          Analyze a single file
  filestat path/to/directory         Analyze a directory
  filestat .                          Analyze current directory
        """
    )

    parser.add_argument(
        "path",
        help="Path to file or directory to analyze",
        nargs="?"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show additional details"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    return parser


def main() -> int:
    """Main entry point for the CLI application.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Validate path argument
    if not args.path:
        console.print("[red]Error: Path argument is required[/red]")
        parser.print_help()
        return 1

    try:
        # Expand user path and normalize
        path = Path(args.path).expanduser().resolve()

        # Create analyzer and get stats
        analyzer = FileAnalyzer(str(path))
        stats = analyzer.get_stats()

        # Format and display output
        format_output(stats)

        return 0

    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1
    except PermissionError as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1
    except IsADirectoryError as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1
    except NotADirectoryError as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
