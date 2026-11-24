#!/usr/bin/env python3
"""Validate the skill and its packaging. Run from anywhere; uses only the standard library."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "arch-review"
errors = []


def err(message):
    errors.append(message)


def load_json(rel):
    path = ROOT / rel
    if not path.exists():
        err(f"{rel}: file is missing")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        err(f"{rel}: invalid JSON ({exc})")
        return None


# 1. Manifests parse and carry one consistent version.
versions = {}
plugin_claude = load_json(".claude-plugin/plugin.json")
market_claude = load_json(".claude-plugin/marketplace.json")
plugin_cursor = load_json(".cursor-plugin/plugin.json")
market_cursor = load_json(".cursor-plugin/marketplace.json")
gemini = load_json("gemini-extension.json")

if plugin_claude:
    versions[".claude-plugin/plugin.json"] = plugin_claude.get("version")
if plugin_cursor:
    versions[".cursor-plugin/plugin.json"] = plugin_cursor.get("version")
if gemini:
    versions["gemini-extension.json"] = gemini.get("version")
if market_claude:
    entries = market_claude.get("plugins") or []
    versions[".claude-plugin/marketplace.json"] = entries[0].get("version") if entries else None
    if not entries:
        err(".claude-plugin/marketplace.json: no plugins listed")
if market_cursor and not (market_cursor.get("plugins") or []):
    err(".cursor-plugin/marketplace.json: no plugins listed")

semver = re.compile(r"^\d+\.\d+\.\d+$")
for rel, value in versions.items():
    if not isinstance(value, str) or not semver.match(value):
        err(f"{rel}: version {value!r} is not MAJOR.MINOR.PATCH")
if len(set(versions.values())) > 1:
    err(f"manifest versions disagree: {versions}")

# 2. The newest CHANGELOG entry matches the manifest version.
changelog = ROOT / "CHANGELOG.md"
if changelog.exists():
    headings = re.findall(r"^## (\d+(?:\.\d+)*)\s*$", changelog.read_text(), re.M)
    if not headings:
        err("CHANGELOG.md: no version headings found")
    else:
        newest = headings[0]
        manifest_version = next((v for v in versions.values() if isinstance(v, str)), None)
        def pad(version):
            parts = version.split(".")
            return tuple(int(x) for x in parts + ["0"] * (3 - len(parts)))

        if manifest_version and semver.match(manifest_version) and pad(manifest_version) != pad(newest):
            err(f"CHANGELOG.md newest entry {newest} does not match manifest version {manifest_version}")
else:
    err("CHANGELOG.md: file is missing")

# 3. License is present and declared.
if not (ROOT / "LICENSE").exists():
    err("LICENSE: file is missing")
for name, data in (("plugin.json (Claude)", plugin_claude), ("plugin.json (Cursor)", plugin_cursor)):
    if data and data.get("license") != "MIT":
        err(f"{name}: license should be MIT")

# 4. SKILL.md has portable frontmatter: only name and description.
skill_md = SKILL_DIR / "SKILL.md"
if not skill_md.exists():
    err("skills/arch-review/SKILL.md: file is missing")
else:
    text = skill_md.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        err("SKILL.md: missing YAML frontmatter")
    else:
        keys = re.findall(r"^([A-Za-z_-]+):", match.group(1), re.M)
        if sorted(keys) != ["description", "name"]:
            err(f"SKILL.md: frontmatter keys must be exactly name and description, found {keys}")
        name = re.search(r"^name:\s*(.+)$", match.group(1), re.M)
        if name and name.group(1).strip() != SKILL_DIR.name:
            err(f"SKILL.md: name {name.group(1).strip()!r} does not match folder {SKILL_DIR.name!r}")
        desc = re.search(r"^description:\s*(.+)$", match.group(1), re.M)
        if not desc or not desc.group(1).strip():
            err("SKILL.md: description is empty")

# 5. Every referenced path inside the skill exists.
ref_pattern = re.compile(r"`(references/[A-Za-z0-9_./-]+)`")
for md in [skill_md, *sorted((SKILL_DIR / "references").rglob("*.md"))]:
    if not md.exists():
        continue
    for ref in ref_pattern.findall(md.read_text()):
        if not (SKILL_DIR / ref).exists():
            err(f"{md.relative_to(ROOT)}: references missing path {ref}")

# 6. The checklist index lists exactly the checklist files that exist.
checklist_dir = SKILL_DIR / "references" / "checklists"
index = checklist_dir / "README.md"
if index.exists():
    listed = set(re.findall(r"`([a-z0-9-]+\.md)`", index.read_text()))
    present = {p.name for p in checklist_dir.glob("*.md") if p.name != "README.md"}
    for missing in sorted(listed - present):
        err(f"checklists/README.md lists {missing}, which does not exist")
    for unlisted in sorted(present - listed):
        err(f"checklists/{unlisted} exists but is not in checklists/README.md")
else:
    err("references/checklists/README.md: file is missing")

if errors:
    print("Validation failed:")
    for message in errors:
        print(f"  - {message}")
    sys.exit(1)
print(f"Validation passed ({len(versions)} manifests, version {next(iter(set(versions.values())), '?')}).")
