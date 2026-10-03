"""Generate src/ixraypy/resources/*.py from spec/openapi.json.

Run `python scripts/generate.py` after refreshing the spec. Models are produced
separately by datamodel-code-generator (see Makefile).
"""

from __future__ import annotations

import json
import keyword
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "spec" / "openapi.json").read_text())
OUT = ROOT / "src" / "ixraypy" / "resources"

# tag -> (module name, class name, client attribute)
TAGS = {
    "Admin": ("admin", "AdminResource", "admin"),
    "API Keys": ("api_keys", "ApiKeysResource", "api_keys"),
    "Admin Roles": ("admin_roles", "AdminRolesResource", "admin_roles"),
    "Setup": ("setup", "SetupResource", "setup"),
    "System": ("system", "SystemResource", "system"),
    "Settings": ("settings", "SettingsResource", "settings"),
    "Backups": ("backups", "BackupsResource", "backups"),
    "Groups": ("groups", "GroupsResource", "groups"),
    "Core": ("cores", "CoresResource", "cores"),
    "Client Template": ("client_templates", "ClientTemplatesResource", "client_templates"),
    "Host": ("hosts", "HostsResource", "hosts"),
    "Node": ("nodes", "NodesResource", "nodes"),
    "User": ("users", "UsersResource", "users"),
    "Subscription": ("subscription", "SubscriptionResource", "subscription"),
    "User Template": ("user_templates", "UserTemplatesResource", "user_templates"),
    "User HWID": ("hwids", "HwidsResource", "hwids"),
    "Push": ("push", "PushResource", "push"),
    "-": ("misc", "MiscResource", "misc"),
}

# Operations that need a hand-written body instead of the generic request.
SPECIAL = {
    "node_logs": "stream",
    "download_backup": "bytes",
}


def ref_name(ref: str) -> str:
    return ref.rsplit("/", 1)[-1]


def py_type(schema: dict, models: set[str]) -> str:
    if not schema:
        return "Any"
    if "$ref" in schema:
        n = ref_name(schema["$ref"])
        models.add(n)
        return f"models.{n}"
    if "anyOf" in schema or "oneOf" in schema:
        parts = [py_type(s, models) for s in schema.get("anyOf") or schema.get("oneOf")]
        parts = [p if p != "None" else "None" for p in parts]
        seen: list[str] = []
        for p in parts:
            if p not in seen:
                seen.append(p)
        return " | ".join(seen)
    t = schema.get("type")
    if t == "null":
        return "None"
    if t == "integer":
        return "int"
    if t == "number":
        return "float"
    if t == "boolean":
        return "bool"
    if t == "string":
        if schema.get("format") == "date-time":
            return "datetime"
        return "str"
    if t == "array":
        return f"list[{py_type(schema.get('items', {}), models)}]"
    if t == "object":
        return "dict[str, Any]"
    return "Any"


def snake(name: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", s).lower().strip("_")
    if keyword.iskeyword(s) or s in {"self", "json", "data"}:
        s += "_"
    return s


def response_type(op: dict, models: set[str]) -> tuple[str, str]:
    """Return (python type, kind) where kind is json|text|none."""
    for code in ("200", "201", "202"):
        r = op["responses"].get(code)
        if r is None:
            continue
        content = r.get("content") or {}
        if "application/json" in content:
            schema = content["application/json"].get("schema") or {}
            if not schema:
                return "Any", "any"
            return py_type(schema, models), "json"
        if content:
            return "str", "text"
        return "None", "none"
    if "204" in op["responses"]:
        return "None", "none"
    return "Any", "any"


def doc_block(op: dict, args: list[tuple[str, str, str]], ret: str, method: str, path: str) -> str:
    summary = (op.get("summary") or op["operationId"].replace("_", " ").title()).strip()
    desc = (op.get("description") or "").strip()
    lines = [summary + ("." if not summary.endswith(".") else "")]
    if desc and desc.rstrip(".") != summary.rstrip("."):
        lines += [""] + textwrap.dedent(desc).splitlines()
    lines += ["", f"``{method.upper()} {path}``"]
    if args:
        lines += ["", "Args:"]
        for name, _typ, help_ in args:
            lines.append(f"    {name}: {help_}" if help_ else f"    {name}:")
    lines += ["", "Returns:", f"    {ret}"]
    body = "\n".join(lines)
    body = body.replace("\\", "\\\\").replace('"""', "'''")
    return '"""' + body + '\n"""'


def gen_method(method: str, path: str, op: dict, models: set[str]) -> str:
    oid = op["operationId"]
    name = snake(oid)
    params = op.get("parameters", [])
    path_params = [p for p in params if p["in"] == "path"]
    query_params = [p for p in params if p["in"] == "query"]
    header_params = [p for p in params if p["in"] == "header"]

    sig: list[str] = ["self"]
    docs: list[tuple[str, str, str]] = []
    path_map: list[str] = []
    for p in path_params:
        pn = snake(p["name"])
        t = py_type(p["schema"], models)
        if t.startswith("models."):
            t += " | str"
        sig.append(f"{pn}: {t}")
        docs.append((pn, t, (p.get("description") or "").strip()))
        path_map.append(f'"{p["name"]}": {pn}')

    body_arg = None
    body_kind = None
    form_fields: list[tuple[str, str, bool]] = []
    rb = op.get("requestBody")
    if rb:
        content = rb["content"]
        if "application/json" in content:
            schema = content["application/json"]["schema"]
            t = py_type(schema, models)
            body_kind = "json"
            if t.startswith("models."):
                body_arg = ("body", f"{t} | dict[str, Any]")
            else:
                body_arg = ("body", t)
        elif "application/x-www-form-urlencoded" in content:
            schema = content["application/x-www-form-urlencoded"]["schema"]
            if "$ref" in schema:
                schema = SPEC["components"]["schemas"][ref_name(schema["$ref"])]
            body_kind = "form"
            req = set(schema.get("required", []))
            for fname, fschema in schema.get("properties", {}).items():
                form_fields.append((fname, py_type(fschema, models), fname in req))
        elif "multipart/form-data" in content:
            body_kind = "multipart"
            body_arg = ("files", "dict[str, Any]")
    if body_arg:
        sig.append("*")
        sig.append(f"{body_arg[0]}: {body_arg[1]}")
        docs.append((body_arg[0], body_arg[1], "Request payload (a model instance or a plain dict)."))
    kw_started = bool(body_arg)
    if form_fields:
        if not kw_started:
            sig.append("*")
            kw_started = True
        for fname, ftype, required in sorted(form_fields, key=lambda f: not f[2]):
            pn = snake(fname)
            if required:
                sig.append(f"{pn}: {ftype}")
            else:
                t2 = ftype if "None" in ftype.split(" | ") else f"{ftype} | None"
                sig.append(f"{pn}: {t2} = None")
            docs.append((pn, ftype, "Form field."))
    if query_params or header_params:
        if not kw_started:
            sig.append("*")
            kw_started = True
        for p in query_params + header_params:
            pn = snake(p["name"])
            t = py_type(p["schema"], models)
            if p.get("required"):
                sig.append(f"{pn}: {t}")
            else:
                t2 = t if "None" in t.split(" | ") else f"{t} | None"
                sig.append(f"{pn}: {t2} = None")
            where = "Query parameter." if p["in"] == "query" else f"Header ``{p['name']}``."
            d = (p.get("description") or "").strip()
            docs.append((pn, t, f"{d} {where}".strip()))

    ret_t, ret_kind = response_type(op, models)
    special = SPECIAL.get(oid)
    if special == "stream":
        ret_t = "AsyncIterator[str]"
    elif special == "bytes":
        ret_t = "bytes"

    lines = [f"    async def {name}({', '.join(sig)}) -> {ret_t}:"]
    lines.append(textwrap.indent(doc_block(op, docs, ret_t, method, path), "        "))
    if path_map:
        lines.append(f"        path = _fmt({path!r}, {{{', '.join(path_map)}}})")
    else:
        lines.append(f"        path = {path!r}")
    if query_params:
        q = ", ".join(f'"{p["name"]}": {snake(p["name"])}' for p in query_params)
        lines.append(f"        params = _clean({{{q}}})")
    else:
        lines.append("        params = None")
    if header_params:
        h = ", ".join(f'"{p["name"]}": {snake(p["name"])}' for p in header_params)
        lines.append(f"        headers = _clean({{{h}}})")
    else:
        lines.append("        headers = None")
    call_kwargs = ["params=params", "headers=headers"]
    if body_kind == "json":
        call_kwargs.append("json=_dump(body)")
    elif body_kind == "form":
        f = ", ".join(f'"{fn}": {snake(fn)}' for fn, _, _ in form_fields)
        call_kwargs.append(f"data=_clean({{{f}}})")
    elif body_kind == "multipart":
        call_kwargs.append("files=files")
    kw = ", ".join(call_kwargs)
    if special == "stream":
        lines.append(f"        async for line in self._http.stream_sse({method!r}, path, {kw}):")
        lines.append("            yield line")
    elif special == "bytes":
        lines.append(f"        return await self._http.request_bytes({method!r}, path, {kw})")
    elif ret_kind == "none":
        lines.append(f"        await self._http.request({method!r}, path, {kw})")
        lines.append("        return None")
    elif ret_kind == "json" and ret_t.startswith("models."):
        lines.append(f"        data = await self._http.request({method!r}, path, {kw})")
        lines.append(f"        return {ret_t}.model_validate(data)")
    elif ret_kind == "json" and ret_t.startswith("list[models."):
        inner = ret_t[len("list[") : -1]
        lines.append(f"        data = await self._http.request({method!r}, path, {kw})")
        lines.append(f"        return [{inner}.model_validate(x) for x in data]")
    else:
        lines.append(f"        return await self._http.request({method!r}, path, {kw})")
    return "\n".join(lines)


HEADER = '''"""{title} endpoints. Generated by scripts/generate.py; do not edit by hand."""

from __future__ import annotations

from collections.abc import AsyncIterator  # noqa: F401
from datetime import datetime  # noqa: F401
from typing import Any  # noqa: F401

from ixraypy import models  # noqa: F401
from ixraypy._http import HttpTransport, _clean, _dump, _fmt  # noqa: F401


class {cls}:
    """{title} endpoints."""

    def __init__(self, http: HttpTransport) -> None:
        self._http = http

'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    by_tag: dict[str, list[tuple[str, str, dict]]] = {t: [] for t in TAGS}
    for path, ops in SPEC["paths"].items():
        for method, op in ops.items():
            tag = (op.get("tags") or ["-"])[0]
            by_tag[tag].append((method, path, op))
    init_lines = ['"""Resource classes, one per API tag."""', ""]
    all_names = []
    summary: list[tuple[str, str, int]] = []
    for tag, ops in by_tag.items():
        mod, cls, attr = TAGS[tag]
        models: set[str] = set()
        methods = [gen_method(m, p, o, models) for m, p, o in ops]
        title = tag if tag != "-" else "Miscellaneous"
        src = HEADER.format(title=title, cls=cls) + "\n\n".join(methods) + "\n"
        (OUT / f"{mod}.py").write_text(src)
        init_lines.append(f"from ixraypy.resources.{mod} import {cls}")
        all_names.append(cls)
        summary.append((attr, cls, len(ops)))
    init_lines += ["", "__all__ = [", *(f'    "{n}",' for n in sorted(all_names)), "]", ""]
    (OUT / "__init__.py").write_text("\n".join(init_lines))
    (ROOT / "spec" / "resources.json").write_text(json.dumps(summary, indent=2))
    print(f"generated {sum(s[2] for s in summary)} methods in {len(summary)} resources")


if __name__ == "__main__":
    main()


# --- post-processing of models.py -------------------------------------------------------------
ROOT_RE = re.compile(
    r"^class (?P<name>\w+)\(RootModel\[(?P<type>[^\]]+(?:\[[^\]]*\])?)\]\):\n(?:[ \t].*\n|\n)*",
    re.MULTILINE,
)


def collapse_root_models() -> None:
    """Inline single-value RootModel wrappers so ``user.data_limit`` is an ``int``, not ``DataLimit(root=...)``.

    datamodel-codegen emits a RootModel for every ``anyOf`` member that carries a
    constraint (``minimum``, ``maxLength``...). The panel validates those anyway,
    so plain types are friendlier for callers.
    """
    path = ROOT / "src" / "ixraypy" / "models.py"
    src = path.read_text()
    mapping: dict[str, str] = {}
    for m in ROOT_RE.finditer(src):
        mapping[m.group("name")] = m.group("type").strip()
    src = ROOT_RE.sub("", src)
    # Resolve chains (a root model of a root model) before substituting.
    for name in list(mapping):
        t = mapping[name]
        while t in mapping:
            t = mapping[t]
        mapping[name] = t
    for name, t in mapping.items():
        src = re.sub(rf"(?<![\"'\w.]){name}(?![\"'\w])", t, src)
    path.write_text(src)
    print(f"collapsed {len(mapping)} root models")


if __name__ == "__main__":
    collapse_root_models()
