"""Tests for the CLI module."""

import pytest
from filestat.cli import create_parser, main
import tempfile
from pathlib import Path


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("test content\n")
        temp_path = f.name
    yield temp_path
    import os
    os.unlink(temp_path)


class TestCLI:
    """Test suite for CLI module."""

    def test_parser_creation(self):
        """Test that parser is created successfully."""
        parser = create_parser()
        assert parser is not None

    def test_parser_accepts_path(self):
        """Test that parser accepts path argument."""
        parser = create_parser()
        args = parser.parse_args(["/some/path"])
        assert args.path == "/some/path"

    def test_parser_accepts_verbose_flag(self):
        """Test that parser accepts verbose flag."""
        parser = create_parser()
        args = parser.parse_args(["/some/path", "-v"])
        assert args.verbose is True

    def test_parser_accepts_verbose_long_flag(self):
        """Test that parser accepts --verbose flag."""
        parser = create_parser()
        args = parser.parse_args(["/some/path", "--verbose"])
        assert args.verbose is True

    def test_parser_path_is_optional(self):
        """Test that path argument is optional for parser (but required by main)."""
        parser = create_parser()
        args = parser.parse_args([])
        assert args.path is None

    def test_main_with_no_arguments(self):
        """Test main returns error code when no path provided."""
        import sys
        from io import StringIO
        
        # Mock sys.argv
        original_argv = sys.argv
        sys.argv = ["filestat"]
        
        try:
            exit_code = main()
            assert exit_code == 1
        finally:
            sys.argv = original_argv

    def test_main_with_invalid_path(self):
        """Test main returns error code with invalid path."""
        import sys
        
        original_argv = sys.argv
        sys.argv = ["filestat", "/nonexistent/path/xyz"]
        
        try:
            exit_code = main()
            assert exit_code == 1
        finally:
            sys.argv = original_argv

    def test_main_with_valid_file(self, temp_file):
        """Test main succeeds with valid file."""
        import sys
        
        original_argv = sys.argv
        sys.argv = ["filestat", temp_file]
        
        try:
            exit_code = main()
            assert exit_code == 0
        finally:
            sys.argv = original_argv

    def test_main_with_current_directory(self):
        """Test main succeeds with current directory."""
        import sys
        
        original_argv = sys.argv
        sys.argv = ["filestat", "."]
        
        try:
            exit_code = main()
            assert exit_code == 0
        finally:
            sys.argv = original_argv
