"""Output formatting for file statistics."""

from typing import Any, Dict
from rich.console import Console
from rich.table import Table


console = Console()


def format_file_output(file_info: Dict[str, Any]) -> None:
    """Format and print file statistics.
    
    Args:
        file_info: Dictionary containing file information
    """
    console.print(f"\n[bold cyan]File Analysis: {file_info['name']}[/bold cyan]\n")
    
    table = Table(title="File Statistics")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("File Name", file_info["name"])
    table.add_row("Size (bytes)", str(file_info["size_bytes"]))
    table.add_row("Size (KB)", str(file_info["size_kb"]))
    table.add_row("File Type", file_info["extension"])
    table.add_row("Lines", str(file_info["lines"]))

    console.print(table)


def format_directory_output(dir_info: Dict[str, Any]) -> None:
    """Format and print directory statistics.
    
    Args:
        dir_info: Dictionary containing directory analysis
    """
    console.print(f"\n[bold cyan]Directory Analysis[/bold cyan]\n")

    # Summary table
    summary_table = Table(title="Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green")

    summary_table.add_row("Total Files", str(dir_info["total_files"]))
    summary_table.add_row("Total Directories", str(dir_info["total_dirs"]))
    summary_table.add_row("Total Size (bytes)", str(dir_info["total_size_bytes"]))
    summary_table.add_row("Total Size (KB)", str(dir_info["total_size_kb"]))
    summary_table.add_row("Total Size (MB)", str(dir_info["total_size_mb"]))
    summary_table.add_row("Total Lines of Code", str(dir_info["total_lines"]))

    console.print(summary_table)

    # File types table
    console.print()
    file_types_table = Table(title="File Types")
    file_types_table.add_column("Extension", style="cyan")
    file_types_table.add_column("Count", style="green")

    for ext, count in sorted(dir_info["file_types"].items(), key=lambda x: x[1], reverse=True):
        file_types_table.add_row(ext, str(count))

    console.print(file_types_table)

    # Largest files table
    if dir_info["largest_files"]:
        console.print()
        largest_table = Table(title="Largest Files")
        largest_table.add_column("File Name", style="cyan")
        largest_table.add_column("Size (KB)", style="green")
        largest_table.add_column("Path", style="yellow")

        for file_info in dir_info["largest_files"]:
            size_kb = round(file_info["size_bytes"] / 1024, 2)
            largest_table.add_row(file_info["name"], str(size_kb), file_info["path"])

        console.print(largest_table)

    console.print()


def format_output(stats: Dict[str, Any]) -> None:
    """Format and print statistics based on type.
    
    Args:
        stats: Statistics dictionary (file or directory)
    """
    if stats.get("is_directory"):
        format_directory_output(stats)
    else:
        format_file_output(stats)
