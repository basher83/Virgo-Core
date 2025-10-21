# Knowledge Base: Using Astral uv for Single File Python Scripts

## Overview

uv is a fast Python package manager and project manager written in Rust that revolutionizes how we handle single file Python scripts. It implements PEP 723 (Inline Script Metadata), allowing scripts to declare their dependencies directly within the file itself, eliminating the need for manual virtual environment management.

## Table of Contents

1. [Basic Script Execution](#basic-script-execution)
2. [Scripts with Dependencies](#scripts-with-dependencies)
3. [Inline Script Metadata (PEP 723)](#inline-script-metadata-pep-723)
4. [Creating Self-Executable Scripts](#creating-self-executable-scripts)
5. [Advanced Configuration](#advanced-configuration)
6. [Best Practices](#best-practices)
7. [Common Use Cases](#common-use-cases)
8. [Troubleshooting](#troubleshooting)

## Basic Script Execution

### Running Simple Scripts

For scripts without external dependencies, `uv run` provides a clean execution environment:

```python
# hello.py
print("Hello world")
```

```bash
uv run hello.py
```

### Standard Library Scripts

Scripts using Python's standard library work seamlessly:

```python
# system_info.py
import os
import sys
import platform

print(f"Python version: {sys.version}")
print(f"Platform: {platform.system()}")
print(f"Home directory: {os.path.expanduser('~')}")
```

```bash
uv run system_info.py
```

### Passing Arguments

Scripts can receive command-line arguments normally:

```python
# greet.py
import sys

if len(sys.argv) < 2:
    print("Usage: python greet.py <name>")
    sys.exit(1)

name = " ".join(sys.argv[1:])
print(f"Hello, {name}!")
```

```bash
uv run greet.py Alice Bob
# Output: Hello, Alice Bob!
```

### Reading from stdin

uv supports script execution from stdin for quick prototyping:

```bash
# Direct piping
echo 'print("Hello from stdin!")' | uv run -

# Here-document (bash/zsh)
uv run - <<EOF
import json
data = {"message": "Hello", "source": "stdin"}
print(json.dumps(data, indent=2))
EOF
```

## Scripts with Dependencies

### Using --with Flag

For one-off script execution with external dependencies:

```python
# progress_demo.py
import time
from rich.progress import track

for i in track(range(20), description="Processing..."):
    time.sleep(0.05)
```

```bash
# Single dependency
uv run --with rich progress_demo.py

# Multiple dependencies
uv run --with rich --with requests --with click script.py

# Version constraints
uv run --with 'rich>=12,<14' --with 'requests>=2.28' script.py
```

### Project vs Non-Project Context

When running in a directory with `pyproject.toml`, uv treats it as a project:

```bash
# In project directory - includes project dependencies
uv run script.py

# Ignore project context
uv run --no-project script.py
```

## Inline Script Metadata (PEP 723)

### Creating Scripts with Metadata

Initialize a new script with inline metadata:

```bash
uv init --script analysis.py --python 3.12
```

### Adding Dependencies

Use `uv add --script` to declare dependencies:

```bash
uv add --script analysis.py pandas matplotlib seaborn
```

This creates a script with inline metadata:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pandas",
#   "matplotlib",
#   "seaborn",
# ]
# ///

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Your analysis code here
df = pd.read_csv('data.csv')
sns.scatterplot(data=df, x='x', y='y')
plt.savefig('output.png')
```

### Manual Metadata Definition

You can also add metadata manually using the standardized format:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.25.0",
#   "click>=8.0.0",
#   "rich>=13.0.0",
# ]
# ///

import httpx
import click
from rich.console import Console

console = Console()

@click.command()
@click.argument('url')
def fetch(url):
    """Fetch and display HTTP response."""
    with httpx.Client() as client:
        response = client.get(url)
        console.print(f"Status: {response.status_code}")
        console.print(response.text[:500])

if __name__ == "__main__":
    fetch()
```

### Important Metadata Rules

-   The `dependencies` field **must** be present, even if empty: `dependencies = []`
-   Metadata is enclosed in `# /// script` and `# ///` comments
-   When inline metadata is present, project dependencies are ignored (no need for `--no-project`)
-   Python version requirements are automatically resolved and downloaded if needed

## Creating Self-Executable Scripts

### Basic Shebang Setup

Make scripts executable without explicit `uv run`:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
# ]
# ///

import requests
import json

def get_weather(city="London"):
    # Note: This is a demo - you'd need a real API key
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": "your_api_key"}

    response = requests.get(url, params=params)
    data = response.json()

    print(f"Weather in {city}: {data['weather'][0]['description']}")

if __name__ == "__main__":
    get_weather()
```

Make it executable and run:

```bash
chmod +x weather_check.py
./weather_check.py
```

### Silent Execution

Add `--quiet` flag to suppress uv output:

```python
#!/usr/bin/env -S uv run --script --quiet
```

### Windows Compatibility

For Windows GUI applications, use `.pyw` extension:

```python
# gui_hello.pyw
# /// script
# dependencies = [
#   "tkinter",  # Usually included with Python
# ]
# ///

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("uv GUI Demo")
root.geometry("300x200")

label = ttk.Label(root, text="Hello from uv!", font=("Arial", 16))
label.pack(expand=True)

button = ttk.Button(root, text="Close", command=root.quit)
button.pack(pady=10)

root.mainloop()
```

## Advanced Configuration

### Alternative Package Indexes

Use custom package indexes for dependencies:

```bash
uv add --index "https://pypi.example.com/simple" --script script.py custom-package
```

This adds index information to the script:

```python
# /// script
# dependencies = ["custom-package"]
#
# [[tool.uv.index]]
# url = "https://pypi.example.com/simple"
# ///
```

### Locking Dependencies

Create lockfiles for reproducible script execution:

```bash
# Generate lockfile
uv lock --script analysis.py

# This creates analysis.py.lock alongside your script
```

Subsequent runs use locked versions:

```bash
uv run --script analysis.py  # Uses locked dependencies
```

### Improving Reproducibility

Use `exclude-newer` to limit package versions by date:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "pandas",
# ]
# [tool.uv]
# exclude-newer = "2024-01-01T00:00:00Z"
# ///
```

### Python Version Management

Specify and use different Python versions:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

# Use Python 3.12+ features
type Point = tuple[float, float]  # Type alias (3.12+)

def distance(p1: Point, p2: Point) -> float:
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

print(distance((0, 0), (3, 4)))  # Output: 5.0
```

```bash
# Use specific Python version (overrides script requirement)
uv run --python 3.13 script.py
```

## Best Practices

### 1. Version Pinning Strategy

```python
# /// script
# dependencies = [
#   "requests>=2.28.0,<3.0.0",    # Major version pinning
#   "pandas~=2.1.0",              # Compatible release
#   "click==8.1.7",               # Exact pinning for tools
# ]
# ///
```

### 2. Script Organization

Structure complex scripts clearly:

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "typer>=0.9.0",
#   "rich>=13.0.0",
#   "httpx>=0.25.0",
# ]
# ///

"""
Data fetcher utility.

Usage:
    ./fetch_data.py --url https://api.example.com --format json
"""

import typer
from rich.console import Console
import httpx
from typing import Optional

console = Console()
app = typer.Typer()

@app.command()
def fetch(
    url: str = typer.Argument(..., help="URL to fetch"),
    format: str = typer.Option("json", help="Output format"),
    timeout: int = typer.Option(30, help="Request timeout"),
):
    """Fetch data from URL and display formatted output."""
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url)
            response.raise_for_status()

        if format == "json":
            console.print_json(response.text)
        else:
            console.print(response.text)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
```

### 3. Development Workflow

```bash
# 1. Create script template
uv init --script data_processor.py --python 3.12

# 2. Add dependencies incrementally
uv add --script data_processor.py pandas click

# 3. Test with dependencies
uv run data_processor.py --help

# 4. Lock for production
uv lock --script data_processor.py

# 5. Make executable
chmod +x data_processor.py
```

### 4. Error Handling

Include robust error handling for distribution:

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# dependencies = ["requests"]
# ///

import sys
import requests
from typing import Optional

def safe_request(url: str, timeout: int = 10) -> Optional[dict]:
    """Make a safe HTTP request with error handling."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None
    except ValueError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    data = safe_request("https://api.github.com/repos/astral-sh/uv")
    if data:
        print(f"Repository: {data['full_name']}")
        print(f"Stars: {data['stargazers_count']}")
    else:
        sys.exit(1)
```

## Common Use Cases

### 1. Data Analysis Scripts

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas>=2.0.0",
#   "matplotlib>=3.7.0",
#   "seaborn>=0.12.0",
# ]
# ///

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

def analyze_data(csv_path: str):
    """Analyze CSV data and generate plots."""
    try:
        df = pd.read_csv(csv_path)

        # Basic statistics
        print("Dataset Info:")
        print(f"Shape: {df.shape}")
        print("\nSummary Statistics:")
        print(df.describe())

        # Generate correlation heatmap
        if len(df.select_dtypes(include=['number']).columns) > 1:
            plt.figure(figsize=(10, 8))
            sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
            plt.title('Correlation Matrix')
            plt.tight_layout()

            output_path = Path(csv_path).stem + '_correlation.png'
            plt.savefig(output_path)
            print(f"\nCorrelation plot saved: {output_path}")

    except Exception as e:
        print(f"Error analyzing {csv_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./analyze_data.py <csv_file>")
        sys.exit(1)

    analyze_data(sys.argv[1])
```

### 2. API Testing Tools

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# dependencies = [
#   "httpx>=0.25.0",
#   "typer>=0.9.0",
#   "rich>=13.0.0",
# ]
# ///

import httpx
import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
import json

console = Console()
app = typer.Typer()

@app.command()
def test_endpoint(
    url: str,
    method: str = typer.Option("GET", help="HTTP method"),
    headers: Optional[str] = typer.Option(None, help="JSON headers"),
    data: Optional[str] = typer.Option(None, help="JSON data"),
):
    """Test HTTP endpoints with formatted output."""

    # Parse headers and data
    parsed_headers = json.loads(headers) if headers else {}
    parsed_data = json.loads(data) if data else None

    with httpx.Client() as client:
        response = client.request(
            method=method.upper(),
            url=url,
            headers=parsed_headers,
            json=parsed_data
        )

    # Create results table
    table = Table(title="API Response")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Status Code", str(response.status_code))
    table.add_row("Response Time", f"{response.elapsed.total_seconds():.3f}s")
    table.add_row("Content Type", response.headers.get("content-type", "N/A"))

    console.print(table)

    # Show response body
    try:
        console.print("\n[bold]Response Body:[/bold]")
        console.print_json(response.text)
    except:
        console.print(response.text)

if __name__ == "__main__":
    app()
```

### 3. System Administration Scripts

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "psutil>=5.9.0",
#   "rich>=13.0.0",
# ]
# ///

import psutil
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
import time

console = Console()

def show_system_info():
    """Display comprehensive system information."""

    # CPU Information
    table = Table(title="System Information")
    table.add_column("Component", style="cyan")
    table.add_column("Details", style="white")

    table.add_row("CPU Count", str(psutil.cpu_count()))
    table.add_row("CPU Usage", f"{psutil.cpu_percent():.1f}%")

    # Memory Information
    memory = psutil.virtual_memory()
    table.add_row("Total RAM", f"{memory.total / (1024**3):.1f} GB")
    table.add_row("Available RAM", f"{memory.available / (1024**3):.1f} GB")
    table.add_row("Memory Usage", f"{memory.percent:.1f}%")

    # Disk Information
    disk = psutil.disk_usage('/')
    table.add_row("Total Disk", f"{disk.total / (1024**3):.1f} GB")
    table.add_row("Free Disk", f"{disk.free / (1024**3):.1f} GB")
    table.add_row("Disk Usage", f"{(disk.used / disk.total * 100):.1f}%")

    console.print(table)

    # Real-time CPU monitoring
    console.print("\n[bold]Real-time CPU Usage (5 seconds):[/bold]")
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:

        task = progress.add_task("CPU", total=100)

        for _ in range(50):  # 5 seconds at 0.1s intervals
            cpu_percent = psutil.cpu_percent()
            progress.update(task, completed=cpu_percent)
            time.sleep(0.1)

if __name__ == "__main__":
    show_system_info()
```

## Troubleshooting

### Common Issues

1. **Script metadata not recognized**

```bash
# Ensure proper format - common mistakes:
# ❌ Wrong comment style
/// script

# ✅ Correct format
# /// script
# dependencies = []
# ///
```

2. **Dependencies not found**

```bash
# Check if you're in a project directory
uv run --no-project script.py

# Or use explicit dependencies
uv run --with requests script.py
```

3. **Python version conflicts**

```bash
# Check available Python versions
uv python list

# Install specific version
uv python install 3.12

# Use specific version
uv run --python 3.12 script.py
```

4. **Shebang not working**

```bash
# Ensure script is executable
chmod +x script.py

# Check uv is in PATH
which uv

# Test shebang manually
/usr/bin/env -S uv run --script script.py
```

### Performance Tips

1. **Use locked dependencies for faster startup**

```bash
uv lock --script script.py
```

2. **Cache environments for repeated execution**
    - uv automatically caches virtual environments
    - Identical dependency sets reuse cached environments
3. **Minimize dependencies**
    - Only include necessary packages
    - Use standard library when possible

### Debugging

Enable verbose output for troubleshooting:

```bash
# Show what uv is doing
uv run -v script.py

# Show environment details
uv run --verbose script.py

# Check environment location
uv run --show-deps script.py
```

## Next Steps

-   Explore [uv project management](https://docs.astral.sh/uv/concepts/projects/) for larger applications
-   Learn about [uv tool management](https://docs.astral.sh/uv/guides/tools/) for global tool installation
-   Check the [uv command reference](https://docs.astral.sh/uv/reference/cli/) for advanced options
-   Review [PEP 723](https://peps.python.org/pep-0723/) specification for complete metadata format details

This knowledge base provides a comprehensive foundation for using uv with single file Python scripts, enabling you to create portable, self-contained, and reproducible Python utilities.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://docs.astral.sh/uv/guides/scripts/
[^2]: https://peps.python.org/pep-0723/
[^3]: https://www.reddit.com/r/Python/comments/1jqj0fq/easily_share_python_scripts_with_dependencies_uv/
[^4]: https://thisdavej.com/share-python-scripts-like-a-pro-uv-and-pep-723-for-easy-deployment/
[^5]: https://zenzes.me/til-one-file-to-rule-them-all-pep-723-and-uv/
[^6]: https://realpython.com/python-uv/
[^7]: https://akrabat.com/using-uv-as-your-shebang-line/
[^8]: https://pydevtools.com/handbook/how-to/how-to-write-a-self-contained-script/
[^9]: https://www.datacamp.com/tutorial/python-uv
[^10]: https://blog.stephenturner.us/p/uv-part-1-running-scripts-and-tools
[^11]: https://discuss.python.org/t/in-praise-of-pep-723/84039
[^12]: https://docs.astral.sh/uv/concepts/projects/dependencies/
[^13]: https://treyhunner.com/2024/12/lazy-self-installing-python-scripts-with-uv/
[^14]: https://pybit.es/articles/create-project-less-python-utilities-with-uv-and-inline-script-metadata/
[^15]: https://www.reddit.com/r/learnpython/comments/1jpgdki/uv_based_project_best_practice_question/
[^16]: https://www.reddit.com/r/Python/comments/1jmyip9/selfcontained_python_scripts_with_uv/
[^17]: https://news.ycombinator.com/item?id=43500124
[^18]: https://github.com/astral-sh/uv/issues/6692
[^19]: https://news.ycombinator.com/item?id=42855258
[^20]: https://flocode.substack.com/p/044-python-environments-again-uv
