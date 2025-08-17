#!/usr/bin/env python3
"""
Documentation management script.
Unified interface for building, serving, and deploying documentation.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.status import Status

app = typer.Typer(
    name="docs",
    help="Documentation Management Script", 
    add_completion=False,
)
console = Console()

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
SITE_DIR = DOCS_DIR / "site"
CONFIG_FILE = DOCS_DIR / "mkdocs.yml"
{%- elif cookiecutter.documentation_tool == "sphinx" %}
BUILD_DIR = DOCS_DIR / "_build"
CONFIG_FILE = DOCS_DIR / "conf.py"
{%- endif %}


def run_command(cmd: list[str], capture_output: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command with proper error handling."""
    try:
        if capture_output:
            return subprocess.run(cmd, capture_output=True, text=True, check=check, cwd=PROJECT_ROOT)
        else:
            return subprocess.run(cmd, check=check, cwd=PROJECT_ROOT)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Command failed: {' '.join(cmd)}[/red]")
        if capture_output and e.stdout:
            console.print(f"[yellow]STDOUT: {e.stdout}[/yellow]")
        if capture_output and e.stderr:
            console.print(f"[red]STDERR: {e.stderr}[/red]")
        raise typer.Exit(1)


@app.command()
def serve(
    port: int = typer.Option(8000, "--port", "-p", help="Port to serve on"),
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
    live_reload: bool = typer.Option(True, "--live-reload/--no-live-reload", help="Enable live reload")
{%- endif %}
) -> None:
    """Serve documentation locally for development."""
    panel = Panel.fit("📚 Serving Documentation", style="blue")
    console.print(panel)
    
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
    cmd = ["mkdocs", "serve", "--config-file", str(CONFIG_FILE), "--dev-addr", f"localhost:{port}"]
    if not live_reload:
        cmd.append("--no-livereload")
{%- elif cookiecutter.documentation_tool == "sphinx" %}
    cmd = ["sphinx-autobuild", "docs", f"docs/_build/html", "--port", str(port)]
{%- endif %}
    
    console.print(f"[green]🌐 Documentation will be available at http://localhost:{port}[/green]")
    console.print("[yellow]Press Ctrl+C to stop the server[/yellow]")
    
    try:
        run_command(cmd)
    except KeyboardInterrupt:
        console.print("\n[yellow]📚 Documentation server stopped[/yellow]")


@app.command()
def build(
    clean: bool = typer.Option(False, "--clean", help="Clean build directory first"),
    strict: bool = typer.Option(False, "--strict", help="Enable strict mode (warnings as errors)")
) -> None:
    """Build documentation."""
    panel = Panel.fit("🔨 Building Documentation", style="blue")
    console.print(panel)
    
    if clean:
        console.print("🧹 Cleaning previous build...")
        clean_docs()
    
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
    cmd = ["mkdocs", "build", "--config-file", str(CONFIG_FILE)]
    if strict:
        cmd.append("--strict")
{%- elif cookiecutter.documentation_tool == "sphinx" %}
    cmd = ["sphinx-build", "-b", "html", "docs", "docs/_build/html"]
    if strict:
        cmd.extend(["-W", "--keep-going"])
{%- endif %}
    
    with Status("Building documentation...", console=console, spinner="dots"):
        run_command(cmd)
    
    console.print("[green]✅ Documentation built successfully![/green]")
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
    console.print(f"[cyan]📁 Output: {SITE_DIR}[/cyan]")
{%- elif cookiecutter.documentation_tool == "sphinx" %}
    console.print(f"[cyan]📁 Output: {BUILD_DIR / 'html'}[/cyan]")
{%- endif %}


{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
@app.command()
def deploy(
    message: str = typer.Option("Update documentation", "--message", "-m", help="Commit message"),
    remote: str = typer.Option("origin", "--remote", help="Git remote to push to"),
    branch: str = typer.Option("gh-pages", "--branch", help="Branch to deploy to")
) -> None:
    """Deploy documentation to GitHub Pages."""
    panel = Panel.fit("🚀 Deploying Documentation", style="blue")
    console.print(panel)
    
    cmd = ["mkdocs", "gh-deploy", "--config-file", str(CONFIG_FILE), "--message", message, "--remote-name", remote, "--remote-branch", branch]
    
    with Status("Deploying documentation...", console=console, spinner="dots"):
        run_command(cmd)
    
    console.print("[green]✅ Documentation deployed successfully![/green]")
    console.print(f"[cyan]🌐 Available at: https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}/[/cyan]")
{%- endif %}


@app.command()
def status() -> None:
    """Show documentation status."""
    panel = Panel.fit("📊 Documentation Status", style="cyan")
    console.print(panel)
    
    from rich.table import Table
    
    table = Table(title="Documentation Information", show_header=True, header_style="bold magenta")
    table.add_column("Item", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details")
    
    # Check configuration file
    if CONFIG_FILE.exists():
        table.add_row("Configuration", "✅ Found", str(CONFIG_FILE.name))
    else:
        table.add_row("Configuration", "❌ Missing", str(CONFIG_FILE.name))
    
    # Check docs directory
    if DOCS_DIR.exists():
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
        md_files = list(DOCS_DIR.rglob("*.md"))
        table.add_row("Source Files", "✅ Present", f"{len(md_files)} markdown files")
{%- elif cookiecutter.documentation_tool == "sphinx" %}
        rst_files = list(DOCS_DIR.rglob("*.rst"))
        py_files = list(DOCS_DIR.rglob("*.py"))
        table.add_row("Source Files", "✅ Present", f"{len(rst_files)} RST, {len(py_files)} Python files")
{%- endif %}
    else:
        table.add_row("Source Files", "❌ Missing", "docs/ directory not found")
    
    # Check build output
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
    if SITE_DIR.exists():
        html_files = list(SITE_DIR.rglob("*.html"))
        table.add_row("Built Docs", "✅ Available", f"{len(html_files)} HTML files")
    else:
        table.add_row("Built Docs", "❌ Not Built", "Run 'pixi run docs build'")
{%- elif cookiecutter.documentation_tool == "sphinx" %}
    html_dir = BUILD_DIR / "html"
    if html_dir.exists():
        html_files = list(html_dir.rglob("*.html"))
        table.add_row("Built Docs", "✅ Available", f"{len(html_files)} HTML files")
    else:
        table.add_row("Built Docs", "❌ Not Built", "Run 'pixi run docs build'")
{%- endif %}
    
    console.print(table)


@app.command()
def clean() -> None:
    """Clean documentation build artifacts."""
    clean_docs()


def clean_docs() -> None:
    """Internal function to clean documentation artifacts."""
    console.print("🧹 Cleaning documentation artifacts...")
    
    artifacts_cleaned = []
    
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
    # Clean site directory
    if SITE_DIR.exists():
        import shutil
        shutil.rmtree(SITE_DIR)
        artifacts_cleaned.append("Site directory")
{%- elif cookiecutter.documentation_tool == "sphinx" %}
    # Clean build directory
    if BUILD_DIR.exists():
        import shutil
        shutil.rmtree(BUILD_DIR)
        artifacts_cleaned.append("Build directory")
{%- endif %}
    
    # Clean any doctree caches
    doctree_dirs = list(PROJECT_ROOT.rglob(".doctrees"))
    for doctree_dir in doctree_dirs:
        if doctree_dir.is_dir():
            import shutil
            shutil.rmtree(doctree_dir)
            artifacts_cleaned.append(f"Doctree cache: {doctree_dir}")
    
    if artifacts_cleaned:
        console.print("[green]✅ Cleaned documentation artifacts:[/green]")
        for artifact in artifacts_cleaned:
            console.print(f"  • {artifact}")
    else:
        console.print("[yellow]⚠️ No documentation artifacts to clean[/yellow]")


if __name__ == "__main__":
    # Change to project root directory
    import os
    os.chdir(PROJECT_ROOT)
    app()