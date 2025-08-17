# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Features

- Modern Python {{ cookiecutter.python_version }}+ with comprehensive type hints
- Unified development experience with pixi task management
- Comprehensive testing with pytest{% if cookiecutter.use_hypothesis == "yes" %} and hypothesis{% endif %}
- Code quality enforcement with ruff and mypy
{%- if cookiecutter.use_async == "yes" %}
- Both synchronous and asynchronous APIs
{%- endif %}
{%- if cookiecutter.database_backend != "none" %}
- {{ cookiecutter.database_backend.title() }} integration{% if cookiecutter.use_async == "yes" %} with async support{% endif %}
{%- endif %}
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
- Beautiful documentation with MkDocs Material
{%- endif %}
- Automated CI/CD with GitHub Actions
- Security scanning and dependency management

## Quick Start

### Installation

```bash
pip install {{ cookiecutter.package_name }}
```

### Basic Usage

```python
import {{ cookiecutter.package_name }}

# Your code here
```

{%- if cookiecutter.use_async == "yes" %}

### Async Usage

```python
import asyncio
import {{ cookiecutter.package_name }}

async def main():
    # Your async code here
    pass

asyncio.run(main())
```
{%- endif %}

## Links

- [GitHub Repository](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
- [PyPI Package](https://pypi.org/project/{{ cookiecutter.package_name }})
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
- [Documentation](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }})
{%- endif %}
- [Issue Tracker](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues)

## License

This project is licensed under the {{ cookiecutter.license }} License.