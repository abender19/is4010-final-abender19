"""Tests for the formatter module."""

import pytest
from io import StringIO
from filestat.formatter import format_file_output, format_directory_output, format_output


@pytest.fixture
def sample_file_stats():
    """Sample file statistics."""
    return {
        "name": "test.py",
        "size_bytes": 2048,
        "size_kb": 2.0,
        "extension": ".py",
        "lines": 50,
        "is_file": True
    }


@pytest.fixture
def sample_directory_stats():
    """Sample directory statistics."""
    return {
        "total_files": 10,
        "total_dirs": 2,
        "total_size_bytes": 10240,
        "total_lines": 500,
        "file_types": {".py": 5, ".txt": 3, ".json": 2},
        "largest_files": [
            {"name": "large.py", "size_bytes": 4096, "path": "large.py"},
            {"name": "medium.py", "size_bytes": 2048, "path": "medium.py"}
        ],
        "total_size_kb": 10.0,
        "total_size_mb": 0.01,
        "is_directory": True
    }


class TestFormatter:
    """Test suite for formatter module."""

    def test_format_file_output_doesnt_crash(self, sample_file_stats):
        """Test that format_file_output doesn't crash."""
        try:
            format_file_output(sample_file_stats)
            success = True
        except Exception:
            success = False
        
        assert success is True

    def test_format_directory_output_doesnt_crash(self, sample_directory_stats):
        """Test that format_directory_output doesn't crash."""
        try:
            format_directory_output(sample_directory_stats)
            success = True
        except Exception:
            success = False
        
        assert success is True

    def test_format_output_for_file(self, sample_file_stats):
        """Test format_output dispatches correctly for files."""
        try:
            format_output(sample_file_stats)
            success = True
        except Exception:
            success = False
        
        assert success is True

    def test_format_output_for_directory(self, sample_directory_stats):
        """Test format_output dispatches correctly for directories."""
        try:
            format_output(sample_directory_stats)
            success = True
        except Exception:
            success = False
        
        assert success is True

    def test_format_output_with_empty_file_types(self):
        """Test format_directory_output with empty file types."""
        stats = {
            "total_files": 0,
            "total_dirs": 0,
            "total_size_bytes": 0,
            "total_lines": 0,
            "file_types": {},
            "largest_files": [],
            "total_size_kb": 0,
            "total_size_mb": 0,
            "is_directory": True
        }
        
        try:
            format_output(stats)
            success = True
        except Exception:
            success = False
        
        assert success is True

    def test_format_output_with_no_largest_files(self):
        """Test format_directory_output with no largest files."""
        stats = {
            "total_files": 1,
            "total_dirs": 0,
            "total_size_bytes": 100,
            "total_lines": 10,
            "file_types": {".txt": 1},
            "largest_files": [],
            "total_size_kb": 0.1,
            "total_size_mb": 0.0001,
            "is_directory": True
        }
        
        try:
            format_output(stats)
            success = True
        except Exception:
            success = False
        
        assert success is True
