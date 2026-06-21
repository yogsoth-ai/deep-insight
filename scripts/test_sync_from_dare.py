import json, os, tempfile, shutil
from pathlib import Path
from sync_from_dare import load_members, compute_diff, rebuild, verify

def _write(tmp, obj):
    p = os.path.join(tmp, "refactory_source.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f)
    return p

def _mkskill(root, name, body="x", prompt=None):
    d = Path(root) / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(body, encoding="utf-8")
    if prompt is not None:
        (d / "prompt.md").write_text(prompt, encoding="utf-8")

def test_load_members_filters_by_package():
    with tempfile.TemporaryDirectory() as tmp:
        p = _write(tmp, {"nodes": [
            {"name": "a", "package": "deep-insight"},
            {"name": "b", "package": "deep-insight"},
            {"name": "c", "package": "stress-test"},
        ]})
        assert load_members(p, "deep-insight") == {"a", "b"}

def test_compute_diff_partitions():
    add, dele, common = compute_diff({"a", "b", "x"}, {"b", "c"})
    assert add == ["a", "x"]
    assert dele == ["c"]
    assert common == ["b"]

def test_rebuild_adds_overwrites_deletes_and_verifies():
    with tempfile.TemporaryDirectory() as tmp:
        dare = Path(tmp) / "dare"; pkg = Path(tmp) / "pkg"
        dare.mkdir(); pkg.mkdir()
        _mkskill(dare, "keep", body="NEW", prompt="P")   # overwrite
        _mkskill(dare, "added", body="A")                # add
        _mkskill(pkg, "keep", body="OLD")                # stale content, no prompt
        _mkskill(pkg, "gone", body="Z")                  # delete
        target = {"keep", "added"}
        stats = rebuild(dare, pkg, target)
        assert stats["added"] == ["added"]
        assert stats["deleted"] == ["gone"]
        assert stats["overwritten"] == ["keep"]
        assert set(p.name for p in pkg.iterdir()) == {"keep", "added"}
        assert (pkg / "keep" / "SKILL.md").read_text(encoding="utf-8") == "NEW"
        assert (pkg / "keep" / "prompt.md").read_text(encoding="utf-8") == "P"
        assert verify(dare, pkg, target) == []
