#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Validate PEP 723 inline script metadata

Checks Python scripts for:
- Valid PEP 723 metadata block
- Required fields (requires-python, dependencies)
- TOML syntax validity
- Shebang presence and format
- Security issues

Usage:
    python validate_script.py <script.py>
    python validate_script.py --strict <script.py>

Examples:
    # Basic validation
    python validate_script.py my_script.py

    # Strict mode (all best practices)
    python validate_script.py --strict my_script.py

    # Validate all scripts in directory
    find . -name '*.py' -exec python validate_script.py {} \;
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationResult:
    """Validation result"""
    valid: bool
    has_metadata: bool
    has_shebang: bool
    has_docstring: bool
    warnings: list[str]
    errors: list[str]


def extract_metadata_block(content: str) -> str | None:
    """Extract PEP 723 metadata block"""
    pattern = r'# /// script\n((?:# .*\n)+)# ///'
    match = re.search(pattern, content)

    if not match:
        return None

    # Extract TOML content (remove leading # from each line)
    toml_lines = match.group(1).split('\n')
    return '\n'.join(line[2:] if line.startswith('# ') else '' for line in toml_lines)


def validate_toml_syntax(toml_content: str) -> list[str]:
    """Validate TOML syntax (basic check)"""
    errors = []

    # Check for required sections
    if 'requires-python' not in toml_content:
        errors.append("Missing 'requires-python' field")

    if 'dependencies' not in toml_content:
        errors.append("Missing 'dependencies' field")

    # Check for common TOML syntax errors
    for line_num, line in enumerate(toml_content.split('\n'), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Check for unquoted strings in dependencies
        if 'dependencies' in toml_content and '=' not in line and '[' not in line and ']' not in line:
            if not line.startswith('"') and not line.startswith("'"):
                errors.append(f"Line {line_num}: Dependency should be quoted: {line}")

    return errors


def check_shebang(content: str) -> tuple[bool, list[str]]:
    """Check shebang line"""
    warnings = []
    lines = content.split('\n')

    if not lines:
        return False, ["Empty file"]

    first_line = lines[0]

    if not first_line.startswith('#!'):
        return False, []

    # Check for recommended shebangs
    recommended = [
        '#!/usr/bin/env -S uv run --script',
        '#!/usr/bin/env -S uv run --script --quiet',
    ]

    if first_line not in recommended:
        warnings.append(f"Shebang not recommended. Use: {recommended[0]}")

    return True, warnings


def check_security_issues(content: str) -> list[str]:
    """Check for common security issues"""
    warnings = []

    # Check for hardcoded secrets
    secret_patterns = [
        (r'password\s*=\s*["\']', "Possible hardcoded password"),
        (r'api[_-]?key\s*=\s*["\']', "Possible hardcoded API key"),
        (r'secret\s*=\s*["\']', "Possible hardcoded secret"),
        (r'token\s*=\s*["\']', "Possible hardcoded token"),
    ]

    for pattern, message in secret_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            warnings.append(f"Security: {message}")

    # Check for shell=True
    if re.search(r'shell\s*=\s*True', content):
        warnings.append("Security: subprocess.run with shell=True (command injection risk)")

    # Check for eval/exec
    if re.search(r'\b(eval|exec)\s*\(', content):
        warnings.append("Security: Use of eval() or exec() (code injection risk)")

    return warnings


def validate_script(script_path: Path, strict: bool = False) -> ValidationResult:
    """Validate Python script"""
    result = ValidationResult(
        valid=True,
        has_metadata=False,
        has_shebang=False,
        has_docstring=False,
        warnings=[],
        errors=[]
    )

    # Read file
    try:
        content = script_path.read_text()
    except (FileNotFoundError, PermissionError, OSError) as e:
        result.valid = False
        result.errors.append(f"Failed to read file: {e}")
        return result

    # Check shebang
    has_shebang, shebang_warnings = check_shebang(content)
    result.has_shebang = has_shebang
    result.warnings.extend(shebang_warnings)

    if strict and not has_shebang:
        result.errors.append("Missing shebang (required in strict mode)")

    # Check for metadata block
    metadata = extract_metadata_block(content)
    result.has_metadata = metadata is not None

    if not metadata:
        result.errors.append("No PEP 723 metadata block found")
        result.valid = False
        return result

    # Validate TOML syntax
    toml_errors = validate_toml_syntax(metadata)
    result.errors.extend(toml_errors)

    if toml_errors:
        result.valid = False

    # Check for docstring
    docstring_pattern = r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\''
    result.has_docstring = bool(re.search(docstring_pattern, content))

    if strict and not result.has_docstring:
        result.warnings.append("Missing module docstring (recommended in strict mode)")

    # Security checks
    security_warnings = check_security_issues(content)
    result.warnings.extend(security_warnings)

    if strict and security_warnings:
        result.valid = False
        result.errors.extend([f"Security issue: {w}" for w in security_warnings])

    return result


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate PEP 723 script metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('script', help='Python script to validate')
    parser.add_argument('--strict', action='store_true', help='Enable strict validation')

    args = parser.parse_args()

    script_path = Path(args.script)

    if not script_path.exists():
        print(f"Error: File not found: {script_path}", file=sys.stderr)
        sys.exit(1)

    if not script_path.suffix == '.py':
        print(f"Error: Not a Python file: {script_path}", file=sys.stderr)
        sys.exit(1)

    # Validate
    result = validate_script(script_path, strict=args.strict)

    # Print results
    print(f"Validating: {script_path}")
    print("=" * 60)

    if result.has_shebang:
        print("✓ Has shebang")
    else:
        print("✗ Missing shebang")

    if result.has_metadata:
        print("✓ Has PEP 723 metadata")
    else:
        print("✗ Missing PEP 723 metadata")

    if result.has_docstring:
        print("✓ Has docstring")
    else:
        print("○ No docstring")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  ⚠ {warning}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  ✗ {error}")

    print("\n" + "=" * 60)

    if result.valid:
        print("Status: ✓ VALID")
        sys.exit(0)
    else:
        print("Status: ✗ INVALID")
        sys.exit(1)


if __name__ == "__main__":
    main()
