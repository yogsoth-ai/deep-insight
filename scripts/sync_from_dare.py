"""Sync this repo's skills/ to its subset of the DARE flat body.

Source of truth: <dare>/scripts/refactory_source.json (field `package` ==
this PKG, field `name` == the DARE flat dir name). DARE is read-only; we only
write under this repo's skills/. Idempotent: safe to re-run.
"""
import argparse, json, os, shutil, sys, filecmp
from pathlib import Path

PKG = "deep-insight"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DARE = REPO_ROOT.parent / "de-anthropocentric-research-engine"


def load_members(refactory_json_path, pkg):
    with open(refactory_json_path, encoding="utf-8") as f:
        data = json.load(f)
    return {n["name"] for n in data["nodes"] if n.get("package") == pkg}


def compute_diff(target, current):
    to_add = sorted(target - current)
    to_del = sorted(current - target)
    common = sorted(target & current)
    return to_add, to_del, common


def resolve_target(dare_root):
    dare_skills = Path(dare_root) / "skills"
    rs = Path(dare_root) / "scripts" / "refactory_source.json"
    target = load_members(str(rs), PKG)
    missing = [n for n in sorted(target) if not (dare_skills / n).is_dir()]
    if missing:
        raise SystemExit(f"FATAL: {len(missing)} members missing in DARE: {missing}")
    return target


def rebuild(dare_skills, pkg_skills, target):
    dare_skills, pkg_skills = Path(dare_skills), Path(pkg_skills)
    pkg_skills.mkdir(parents=True, exist_ok=True)
    existing_dirs = {p.name for p in pkg_skills.iterdir() if p.is_dir()}
    strays = sorted(p.name for p in pkg_skills.iterdir() if not p.is_dir())
    added, overwritten = [], []
    for name in sorted(target):
        dst = pkg_skills / name
        if dst.is_dir():
            shutil.rmtree(dst); overwritten.append(name)
        else:
            added.append(name)
        shutil.copytree(dare_skills / name, dst)
    deleted = sorted(existing_dirs - target)
    for name in deleted:
        shutil.rmtree(pkg_skills / name)
    return {"added": added, "deleted": deleted,
            "overwritten": overwritten, "strays": strays}


def _dircmp_problems(name, cmp, dare_skills, pkg_skills):
    """Recursively check for dircmp problems, including content (shallow=False)."""
    issues = []
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        issues.append(f"{name}: left_only={cmp.left_only} right_only={cmp.right_only} "
                      f"diff={cmp.diff_files} funny={cmp.funny_files}")
    # Content check: for common files, verify byte-equality (shallow=False)
    for fname in cmp.common_files:
        left_path = dare_skills / name / fname
        right_path = pkg_skills / name / fname
        if not filecmp.cmp(left_path, right_path, shallow=False):
            issues.append(f"{name}: content differs in {fname}")
    # Recurse into subdirs
    for sub, subcmp in cmp.subdirs.items():
        sub_name = f"{name}/{sub}"
        issues.extend(_dircmp_problems(sub_name, subcmp, dare_skills, pkg_skills))
    return issues


def verify(dare_skills, pkg_skills, target):
    dare_skills, pkg_skills = Path(dare_skills), Path(pkg_skills)
    problems = []
    actual = {p.name for p in pkg_skills.iterdir() if p.is_dir()}
    if actual != target:
        problems.append(f"membership: extra={sorted(actual-target)} "
                        f"missing={sorted(target-actual)}")
    for name in sorted(target & actual):
        cmp = filecmp.dircmp(dare_skills / name, pkg_skills / name)
        problems.extend(_dircmp_problems(name, cmp, dare_skills, pkg_skills))
    return problems
