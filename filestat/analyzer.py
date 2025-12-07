"""Core analysis functionality for file statistics."""

import os
from pathlib import Path
from collections import defaultdict
from typing import Any, Dict


class FileAnalyzer:
    """Analyzes files and directories for statistics."""

    def __init__(self, path: str):
        """Initialize the analyzer with a target path.
        
        Args:
            path: Path to file or directory to analyze
            
        Raises:
            FileNotFoundError: If the path does not exist
        """
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")

    def get_file_info(self) -> Dict[str, Any]:
        """Get statistics for a single file.
        
        Returns:
            Dictionary with file information
            
        Raises:
            IsADirectoryError: If path is a directory
        """
        if self.path.is_dir():
            raise IsADirectoryError("Use analyze_directory() for directory paths")

        size = self.path.stat().st_size
        extension = self.path.suffix or "no extension"
        
        line_count = 0
        try:
            with open(self.path, 'r', encoding='utf-8', errors='ignore') as f:
                line_count = sum(1 for _ in f)
        except Exception:
            line_count = 0

        return {
            "name": self.path.name,
            "size_bytes": size,
            "size_kb": round(size / 1024, 2),
            "extension": extension,
            "lines": line_count,
            "is_file": True
        }

    def analyze_directory(self) -> Dict[str, Any]:
        """Analyze directory and return statistics.
        
        Returns:
            Dictionary with directory analysis results
            
        Raises:
            NotADirectoryError: If path is not a directory
        """
        if not self.path.is_dir():
            raise NotADirectoryError("Use get_file_info() for file paths")

        stats = {
            "total_files": 0,
            "total_dirs": 0,
            "total_size_bytes": 0,
            "total_lines": 0,
            "file_types": defaultdict(int),
            "largest_files": [],
            "is_directory": True
        }

        try:
            for root, dirs, files in os.walk(self.path):
                stats["total_dirs"] += len(dirs)

                for file in files:
                    stats["total_files"] += 1
                    file_path = Path(root) / file

                    try:
                        size = file_path.stat().st_size
                        stats["total_size_bytes"] += size

                        ext = file_path.suffix or "no_ext"
                        stats["file_types"][ext] += 1

                        # Count lines if text file
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                stats["total_lines"] += sum(1 for _ in f)
                        except Exception:
                            pass

                        stats["largest_files"].append({
                            "name": file_path.name,
                            "size_bytes": size,
                            "path": str(file_path.relative_to(self.path))
                        })

                    except (OSError, PermissionError):
                        pass

        except PermissionError as e:
            raise PermissionError(f"Permission denied accessing directory: {e}")

        # Sort and keep top 5 largest files
        stats["largest_files"].sort(key=lambda x: x["size_bytes"], reverse=True)
        stats["largest_files"] = stats["largest_files"][:5]

        # Convert defaultdict to regular dict
        stats["file_types"] = dict(stats["file_types"])

        # Add summary sizes
        stats["total_size_kb"] = round(stats["total_size_bytes"] / 1024, 2)
        stats["total_size_mb"] = round(stats["total_size_bytes"] / (1024 * 1024), 2)

        return stats

    def get_stats(self) -> Dict[str, Any]:
        """Get appropriate statistics for the path (file or directory).
        
        Returns:
            File or directory statistics
        """
        if self.path.is_file():
            return self.get_file_info()
        else:
            return self.analyze_directory()
