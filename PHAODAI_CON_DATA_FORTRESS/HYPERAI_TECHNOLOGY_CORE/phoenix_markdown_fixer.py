#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
"""
Phoenix Markdown Formatter
Auto-fix all markdown formatting issues
"""
import re


def fix_markdown_formatting():
    """Fix markdown formatting issues in HYPERAI_MASTER_TODO.md"""
    file_path = r'c:\Users\pc\.vscode\extensions\aidev\core_system\HYPERAI_MASTER_TODO.md'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("🔧 Phoenix Markdown Formatter - Starting...")

    # Fix 1: Add blank lines around headings (MD022)
    # Add blank line before headings that don't have one
    content = re.sub(r'(?<!\n)\n(###? )', r'\n\n\1', content)

    # Add blank line after headings that don't have one
    content = re.sub(r'(###? [^\n]*)\n(?!\n)', r'\1\n\n', content)

    # Fix 2: Add blank lines around lists (MD032)
    # Add blank line before lists
    content = re.sub(r'(?<!\n)\n(- \[)', r'\n\n\1', content)
    content = re.sub(r'(?<!\n)\n(\d+\. )', r'\n\n\1', content)

    # Add blank line after lists
    content = re.sub(r'(- [^\n]*)\n(?!\n)(?!- )(?!\d+\. )', r'\1\n\n', content)
    content = re.sub(r'(\d+\. [^\n]*)\n(?!\n)(?!- )(?!\d+\. )', r'\1\n\n', content)

    # Fix 3: Clean up excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Save the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Phoenix Markdown Formatter - Complete!")
    print("📄 Fixed markdown formatting issues in HYPERAI_MASTER_TODO.md")


if __name__ == "__main__":
    fix_markdown_formatting()
