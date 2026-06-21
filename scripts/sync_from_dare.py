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
