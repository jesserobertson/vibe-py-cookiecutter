#!/usr/bin/env python3
"""
Shared utilities for script commands.
Provides a unified command runner with subprocess (reliable fallback).
"""

import subprocess
from pathlib import Path

import typer
from rich.console import Console

console = Console()

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent


class CommandResult:
    """Result wrapper for command execution."""

    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    @property
    def success(self) -> bool:
        """Whether the command was successful."""
        return self.returncode == 0


def run_command(
    cmd: list[str], capture_output: bool = False, check: bool = True
) -> CommandResult:
    """Run a shell command with proper error handling.

    Args:
        cmd: Command and arguments as list
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise on non-zero exit code

    Returns:
        CommandResult with returncode, stdout, stderr

    Raises:
        typer.Exit: If check=True and command fails
    """
    try:
        result = subprocess.run(
            cmd, capture_output=capture_output, text=True, check=False, cwd=PROJECT_ROOT
        )

        command_result = CommandResult(
            returncode=result.returncode,
            stdout=result.stdout if capture_output else "",
            stderr=result.stderr if capture_output else "",
        )

        if check and result.returncode != 0:
            console.print(f"[red]❌ Command failed: {' '.join(cmd)}[/red]")
            if capture_output:
                if result.stdout:
                    console.print(f"[yellow]STDOUT: {result.stdout}[/yellow]")
                if result.stderr:
                    console.print(f"[red]STDERR: {result.stderr}[/red]")
            raise typer.Exit(1)

        return command_result

    except Exception as e:
        console.print(f"[red]❌ Unexpected error running command: {e}[/red]")
        if check:
            raise typer.Exit(1)
        return CommandResult(returncode=1, stderr=str(e))


def run_command_simple(cmd: list[str]) -> bool:
    """Simple command runner that returns success/failure.

    Args:
        cmd: Command and arguments as list

    Returns:
        True if command succeeded, False otherwise
    """
    result = run_command(cmd, capture_output=False, check=False)
    return result.success


def run_command_capture(cmd: list[str]) -> CommandResult:
    """Run command and capture output without raising on failure.

    Args:
        cmd: Command and arguments as list

    Returns:
        CommandResult with captured output
    """
    return run_command(cmd, capture_output=True, check=False)
