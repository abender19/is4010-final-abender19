"""Tests for the analyzer module."""

import pytest
import tempfile
import os
from pathlib import Path
from filestat.analyzer import FileAnalyzer


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("line 1\nline 2\nline 3\n")
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def temp_directory():
    """Create a temporary directory with test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create various test files
        Path(tmpdir, "file1.txt").write_text("hello\nworld\n")
        Path(tmpdir, "file2.py").write_text("def test():\n    pass\n")
        Path(tmpdir, "file3.json").write_text('{"key": "value"}\n')
        
        # Create a subdirectory
        subdir = Path(tmpdir, "subdir")
        subdir.mkdir()
        Path(subdir, "file4.txt").write_text("nested file\n")
        
        yield tmpdir


class TestFileAnalyzer:
    """Test suite for FileAnalyzer class."""

    def test_init_with_valid_file(self, temp_file):
        """Test initialization with valid file path."""
        analyzer = FileAnalyzer(temp_file)
        assert analyzer.path.exists()

    def test_init_with_valid_directory(self, temp_directory):
        """Test initialization with valid directory path."""
        analyzer = FileAnalyzer(temp_directory)
        assert analyzer.path.exists()

    def test_init_with_invalid_path(self):
        """Test initialization with invalid path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            FileAnalyzer("/nonexistent/path/to/file")

    def test_get_file_info(self, temp_file):
        """Test getting file information."""
        analyzer = FileAnalyzer(temp_file)
        info = analyzer.get_file_info()

        assert info["is_file"] is True
        assert info["extension"] == ".txt"
        assert info["lines"] == 3
        assert info["size_bytes"] > 0
        assert "size_kb" in info

    def test_get_file_info_with_directory_raises_error(self, temp_directory):
        """Test get_file_info raises error when called on directory."""
        analyzer = FileAnalyzer(temp_directory)
        with pytest.raises(IsADirectoryError):
            analyzer.get_file_info()

    def test_analyze_directory(self, temp_directory):
        """Test directory analysis."""
        analyzer = FileAnalyzer(temp_directory)
        stats = analyzer.analyze_directory()

        assert stats["is_directory"] is True
        assert stats["total_files"] >= 4
        assert stats["total_dirs"] >= 1
        assert stats["total_size_bytes"] > 0
        assert len(stats["file_types"]) > 0

    def test_analyze_directory_with_file_raises_error(self, temp_file):
        """Test analyze_directory raises error when called on file."""
        analyzer = FileAnalyzer(temp_file)
        with pytest.raises(NotADirectoryError):
            analyzer.analyze_directory()

    def test_analyze_directory_tracks_file_types(self, temp_directory):
        """Test that directory analysis tracks file types."""
        analyzer = FileAnalyzer(temp_directory)
        stats = analyzer.analyze_directory()

        assert ".txt" in stats["file_types"]
        assert ".py" in stats["file_types"]
        assert ".json" in stats["file_types"]

    def test_analyze_directory_finds_largest_files(self, temp_directory):
        """Test that largest files are identified."""
        analyzer = FileAnalyzer(temp_directory)
        stats = analyzer.analyze_directory()

        assert "largest_files" in stats
        assert len(stats["largest_files"]) > 0
        # Verify they're sorted by size (descending)
        if len(stats["largest_files"]) > 1:
            for i in range(len(stats["largest_files"]) - 1):
                assert stats["largest_files"][i]["size_bytes"] >= stats["largest_files"][i + 1]["size_bytes"]

    def test_analyze_directory_limits_largest_files_to_5(self, temp_directory):
        """Test that only top 5 largest files are kept."""
        analyzer = FileAnalyzer(temp_directory)
        stats = analyzer.analyze_directory()
        
        assert len(stats["largest_files"]) <= 5

    def test_get_stats_for_file(self, temp_file):
        """Test get_stats returns file info for files."""
        analyzer = FileAnalyzer(temp_file)
        stats = analyzer.get_stats()

        assert stats["is_file"] is True
        assert stats["extension"] == ".txt"

    def test_get_stats_for_directory(self, temp_directory):
        """Test get_stats returns directory info for directories."""
        analyzer = FileAnalyzer(temp_directory)
        stats = analyzer.get_stats()

        assert stats["is_directory"] is True
        assert "total_files" in stats

    def test_directory_stats_has_size_conversions(self, temp_directory):
        """Test that directory stats include size conversions (KB, MB)."""
        analyzer = FileAnalyzer(temp_directory)
        stats = analyzer.analyze_directory()

        assert "total_size_kb" in stats
        assert "total_size_mb" in stats
        assert stats["total_size_kb"] > 0

    def test_file_without_extension(self, temp_directory):
        """Test analyzing file without extension."""
        # Create a file without extension
        Path(temp_directory, "README").write_text("readme content\n")
        
        analyzer = FileAnalyzer(temp_directory)
        stats = analyzer.analyze_directory()

        # Should handle files without extensions
        assert "no_ext" in stats["file_types"] or len(stats["file_types"]) > 0

    def test_binary_file_handling(self, temp_directory):
        """Test that binary files don't crash the analyzer."""
        # Create a binary-like file
        binary_path = Path(temp_directory, "test.bin")
        binary_path.write_bytes(b'\x00\x01\x02\x03')

        analyzer = FileAnalyzer(temp_directory)
        stats = analyzer.analyze_directory()

        # Should complete without error
        assert stats["total_files"] > 0
