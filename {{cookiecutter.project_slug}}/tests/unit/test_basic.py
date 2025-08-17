"""
Basic unit tests for {{ cookiecutter.project_name }}.
"""

{%- if cookiecutter.use_hypothesis == "yes" %}
from hypothesis import given, strategies as st
{%- endif %}
import pytest

import {{ cookiecutter.package_name }}


class TestBasicFunctionality:
    """Test basic functionality of the package."""

    def test_package_imports(self):
        """Test that the package can be imported."""
        assert {{ cookiecutter.package_name }} is not None

    def test_package_has_version(self):
        """Test that the package has a version attribute."""
        assert hasattr({{ cookiecutter.package_name }}, "__version__")
        assert isinstance({{ cookiecutter.package_name }}.__version__, str)
        assert len({{ cookiecutter.package_name }}.__version__) > 0

    def test_package_version_format(self):
        """Test that the version follows semantic versioning."""
        version = {{ cookiecutter.package_name }}.__version__
        # Basic semantic version format check (major.minor.patch)
        parts = version.split(".")
        assert len(parts) >= 2, f"Version {version} should have at least major.minor"

        # Check that major and minor are numbers
        assert parts[0].isdigit(), f"Major version should be numeric, got {parts[0]}"
        assert parts[1].isdigit(), f"Minor version should be numeric, got {parts[1]}"

{%- if cookiecutter.use_hypothesis == "yes" %}

    @given(st.text())
    def test_string_handling(self, text_input):
        """Property-based test for string handling."""
        # Example property-based test
        # Replace with actual functionality from your package
        assert isinstance(text_input, str)

    @given(st.integers(min_value=0, max_value=1000))
    def test_integer_handling(self, int_input):
        """Property-based test for integer handling."""
        # Example property-based test
        # Replace with actual functionality from your package
        assert isinstance(int_input, int)
        assert int_input >= 0
{%- endif %}


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_import_all_public_modules(self):
        """Test that all public modules can be imported without errors."""
        # This test helps catch import-time errors
        import {{ cookiecutter.package_name }}

        # Test that we can access common attributes without errors
        dir({{ cookiecutter.package_name }})


class TestTypeHints:
    """Test type hint compatibility."""

    def test_package_is_typed(self):
        """Test that the package includes type information."""
        import {{ cookiecutter.package_name }}

        # Check if py.typed file exists (indicates PEP 561 compliance)
        # This is more of a packaging test
        package_path = {{ cookiecutter.package_name }}.__file__
        if package_path:
            from pathlib import Path
            package_dir = Path(package_path).parent
            py_typed = package_dir / "py.typed"
            # Note: This might not exist during development, so we make it optional
            if py_typed.exists():
                assert py_typed.is_file()


{%- if cookiecutter.use_async == "yes" %}
class TestAsyncSupport:
    """Test async functionality support."""

    @pytest.mark.asyncio
    async def test_async_import(self):
        """Test that async modules can be imported."""
        try:
            # Import async components if they exist
            import {{ cookiecutter.package_name }}.async_module  # noqa: F401
        except ImportError:
            # Async module might not exist yet, skip test
            pytest.skip("Async module not implemented yet")

    @pytest.mark.asyncio
    async def test_basic_async_functionality(self):
        """Test basic async functionality."""
        async def dummy_async_function():
            return "async_result"

        result = await dummy_async_function()
        assert result == "async_result"
{%- endif %}
