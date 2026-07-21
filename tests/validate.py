#!/usr/bin/env python3
"""Validate the portable skill package and its fixed regression contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "valorant-cn-performance"
CASES = ROOT / "evals" / "cases"
FIXTURES = ROOT / "evals" / "fixtures"


class Checks:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.passed: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if condition:
            self.passed.append(message)
        else:
            self.errors.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not match:
        return {}, text
    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, match.group(2)


def validate_skill(checks: Checks) -> None:
    skill_file = SKILL / "SKILL.md"
    checks.require(skill_file.is_file(), "SKILL.md exists")
    if not skill_file.is_file():
        return

    text = read(skill_file)
    metadata, body = parse_frontmatter(text)
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    checks.require(name == SKILL.name, "frontmatter name matches parent directory")
    checks.require(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)), "name follows Agent Skills rules")
    checks.require(1 <= len(description) <= 1024, "description length is 1..1024")
    trigger_terms = ("VALORANT", "无畏契约", "low FPS", "stutter", "ACE", "Vanguard")
    checks.require(all(term in description for term in trigger_terms), "description includes trigger vocabulary")
    checks.require(len(text.splitlines()) < 500, "SKILL.md stays under 500 lines")

    referenced = re.findall(r"`((?:references|scripts)/[^`]+)`", body)
    checks.require(bool(referenced), "SKILL.md declares progressive resources")
    for relative in sorted(set(referenced)):
        checks.require((SKILL / relative).is_file(), f"referenced resource exists: {relative}")

    required_boundaries = [
        "不修改、停用、欺骗或绕过 ACE/Vanguard",
        "没有改动前后数据时",
        "2026-07-22",
    ]
    for phrase in required_boundaries:
        checks.require(phrase in text, f"skill contains boundary: {phrase}")


def validate_script(checks: Checks) -> None:
    path = SKILL / "scripts" / "diagnose.ps1"
    checks.require(path.is_file(), "read-only diagnostic script exists")
    if not path.is_file():
        return
    text = read(path)
    banned_patterns = {
        r"\bSet-ItemProperty\b": "registry writes",
        r"\bNew-ItemProperty\b": "registry creation",
        r"\bRemove-Item\b": "file or registry deletion",
        r"\bStop-(?:Service|Process)\b": "service/process termination",
        r"\bSet-Service\b": "service mutation",
        r"\bbcdedit\b": "boot configuration mutation",
        r"\bCheckpoint-Computer\b": "restore-point write",
        r"\bSet-ExecutionPolicy\b": "execution-policy mutation",
        r"\bInvoke-WebRequest\b|\bcurl\b|\bwget\b": "network access",
    }
    for pattern, label in banned_patterns.items():
        checks.require(not re.search(pattern, text, re.I), f"diagnostic contains no {label}")
    checks.require("ConvertTo-Json" in text, "diagnostic emits structured JSON")
    checks.require("collectsPublicIp = $false" in text, "diagnostic declares no public-IP collection")
    checks.require("readOnly = $true" in text, "diagnostic marks output read-only")


def load_cases(checks: Checks) -> list[dict]:
    paths = sorted(CASES.glob("*.json"))
    checks.require(len(paths) == 6, "exactly 6 fixed evaluation cases exist")
    cases: list[dict] = []
    ids: set[str] = set()
    for path in paths:
        try:
            case = json.loads(read(path))
        except (OSError, json.JSONDecodeError) as exc:
            checks.errors.append(f"valid JSON: {path.name}: {exc}")
            continue
        required_keys = {"id", "title", "prompt", "expected_route", "required", "forbidden"}
        checks.require(required_keys.issubset(case), f"case schema complete: {path.name}")
        checks.require(case.get("id") == path.stem, f"case id matches filename: {path.name}")
        checks.require(case.get("id") not in ids, f"case id unique: {path.name}")
        ids.add(case.get("id", ""))
        checks.require(bool(case.get("required")), f"case has required assertions: {path.name}")
        checks.require(bool(case.get("forbidden")), f"case has forbidden assertions: {path.name}")
        for alternatives in case.get("required_any", []):
            checks.require(
                isinstance(alternatives, list) and len(alternatives) >= 2 and all(isinstance(x, str) for x in alternatives),
                f"case required_any alternatives valid: {path.name}",
            )
        cases.append(case)
    return cases


def validate_outputs(checks: Checks, cases: list[dict], output_dir: Path, label: str) -> None:
    for case in cases:
        path = output_dir / f"{case['id']}.md"
        checks.require(path.is_file(), f"{label} exists: {path.name}")
        if not path.is_file():
            continue
        output = read(path)
        for phrase in case["required"]:
            checks.require(phrase in output, f"{label} {path.name} includes: {phrase}")
        for alternatives in case.get("required_any", []):
            checks.require(
                any(phrase in output for phrase in alternatives),
                f"{label} {path.name} includes one of: {' | '.join(alternatives)}",
            )
        for phrase in case["forbidden"]:
            checks.require(phrase not in output, f"{label} {path.name} excludes: {phrase}")


def validate_docs(checks: Checks) -> None:
    sources = read(SKILL / "references" / "sources.md")
    for domain in ("gamesafe.qq.com", "riotgames.com", "playvalorant.com", "microsoft.com", "agentskills.io", "okx.ai"):
        checks.require(domain in sources, f"source inventory includes {domain}")
    draft = read(ROOT / "docs" / "okx-a2a-listing-draft.md")
    checks.require("DRAFT_ONLY" in draft and "未登记" in draft, "OKX listing is explicitly draft-only")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", type=Path, help="Directory containing real Agent outputs named after case ids")
    args = parser.parse_args()

    checks = Checks()
    validate_skill(checks)
    validate_script(checks)
    cases = load_cases(checks)
    validate_outputs(checks, cases, FIXTURES, "fixture")
    validate_docs(checks)
    if args.outputs:
        validate_outputs(checks, cases, args.outputs.resolve(), "agent output")

    print(f"PASS: {len(checks.passed)}")
    if checks.errors:
        print(f"FAIL: {len(checks.errors)}")
        for error in checks.errors:
            print(f"- {error}")
        return 1
    print("FAIL: 0")
    print("Skill package, read-only script contract, 6 eval cases, and fixture assertions validated.")
    if not args.outputs:
        print("Live Agent outputs were not supplied; no model-quality score is claimed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
