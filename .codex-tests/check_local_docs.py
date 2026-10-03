"""Local Markdown data checks; no imports from source code and no network."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re

root = Path.cwd().resolve()
paths = ['.github/AI.md', 'README.md', 'README-DE.md', 'README-EN.md', 'README-ES.md']
pattern = re.compile(r'!?\[[^\]]*\]\(\s*(<[^>]*>|[^\s)]+)(?:\s+[^)]*)?\)')
local = 0
external = 0
failed = 0
for name in paths:
    path = root / name
    try:
        text = path.read_text(encoding='utf-8')
        if not text.strip():
            failed += 1
        for match in pattern.finditer(text):
            target = match.group(1).strip('<>')
            if not target or target.startswith('#'):
                continue
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                external += 1
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            local += 1
            if not destination.is_relative_to(root) or not destination.exists():
                failed += 1
    except (UnicodeError, OSError, ValueError):
        failed += 1
print(json.dumps({'markdown_files': len(paths), 'local_targets': local,
                  'external_targets_not_requested': external, 'failures': failed}))
raise SystemExit(1 if failed else 0)
