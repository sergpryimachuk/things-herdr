#!/usr/bin/env python3
"""Install Things while preserving all non-theme config values and comments."""
import argparse
from datetime import datetime
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib


def merge(original: str, overlay: str) -> str:
    before = tomllib.loads(original)
    theme = tomllib.loads(overlay)
    assert set(theme) == {"theme"}
    # Remove only complete theme tables. Validate semantic preservation below,
    # which also rejects unusual inline/dotted theme definitions before writing.
    lines = original.splitlines(keepends=True)
    kept = []
    removing = False
    for line in lines:
        header = re.match(r'^\s*\[\[?\s*([^\]]+?)\s*\]\]?\s*(?:#.*)?$', line.rstrip())
        if header:
            table = header.group(1).strip()
            removing = table == "theme" or table.startswith("theme.")
        if not removing:
            kept.append(line)
    output = ''.join(kept).rstrip() + '\n\n' + overlay
    after = tomllib.loads(output)
    if {k: v for k, v in before.items() if k != "theme"} != {k: v for k, v in after.items() if k != "theme"}:
        raise ValueError("Refusing to change non-theme configuration. Merge theme.toml manually.")
    if after["theme"] != theme["theme"]:
        raise ValueError("Theme could not be replaced safely. Merge theme.toml manually.")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path(os.environ.get('HERDR_CONFIG_PATH', '~/.config/herdr/config.toml')).expanduser())
    parser.add_argument('--reload', action='store_true', help='Reload the current Herdr session after installing; requires HERDR_ENV=1')
    args = parser.parse_args()
    if args.reload and os.environ.get('HERDR_ENV') != '1':
        parser.error('--reload must run inside Herdr with HERDR_ENV=1')
    config = args.config.expanduser()
    overlay = Path(__file__).with_name('theme.toml').read_text()
    original = config.read_text() if config.exists() else ''
    output = merge(original, overlay)
    if output != original:
        config.parent.mkdir(parents=True, exist_ok=True)
        if config.exists():
            backup = config.with_name(config.name + '.things-backup-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
            shutil.copy2(config, backup)
            print(f'Backup: {backup}')
        mode = config.stat().st_mode & 0o777 if config.exists() else 0o600
        with tempfile.NamedTemporaryFile(mode='w', dir=config.parent, delete=False) as tmp:
            tmp.write(output)
            temporary = Path(tmp.name)
        try:
            temporary.chmod(mode)
            temporary.replace(config)
        finally:
            temporary.unlink(missing_ok=True)
        print(f'Installed: {config}')
    else:
        print(f'Already installed: {config}')
    if args.reload:
        subprocess.run(['herdr', 'server', 'reload-config'], check=True)


if __name__ == '__main__':
    main()
