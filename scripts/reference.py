"""Write docs/reference.md from the generated resource classes.

uv run python scripts/reference.py
"""

import importlib.util
import inspect
import re
from pathlib import Path

import ixraypy.resources as resources

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("generate", ROOT / "scripts" / "generate.py")
generate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate)

HEAD = """# API reference

Every method is `async`. Names follow the panel's OpenAPI operation ids, so the
Swagger page of your panel (`/docs` when `DOCS=1`) and this list line up one to one.

Methods that take a `body` accept either the pydantic model from `ixraypy.models`
or a plain `dict` with the same fields. Query parameters are keyword-only.

| Client attribute | Class | Methods |
|---|---|---|
"""


def methods(cls):
    for name, fn in inspect.getmembers(cls, inspect.iscoroutinefunction):
        if not name.startswith("_"):
            yield name, fn


def main() -> None:
    entries = sorted((attr, cls) for _, cls, attr in generate.TAGS.values() if hasattr(resources, cls))
    out = [HEAD]
    for attr, cls_name in entries:
        out.append(f"| `ix.{attr}` | `{cls_name}` | {len(list(methods(getattr(resources, cls_name))))} |\n")
    for attr, cls_name in entries:
        out.append(f"\n## `ix.{attr}` — {cls_name}\n")
        for name, fn in methods(getattr(resources, cls_name)):
            sig = str(inspect.signature(fn)).replace("(self, ", "(").replace("(self)", "()")
            doc = inspect.getdoc(fn) or ""
            title = doc.split("\n", 1)[0].rstrip(".")
            route = re.search(r"``([A-Z]+ [^`]+)``", doc)
            out.append(f"\n### `{name}{sig}`\n\n")
            out.append(f"`{route.group(1)}` — {title}\n" if route else f"{title}\n")
    (ROOT / "docs" / "reference.md").write_text("".join(out))


main()
