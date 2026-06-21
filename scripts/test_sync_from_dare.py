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

def test_verify_detects_nested_subdir_content_diff():
    """Test that verify recurses into subdirs and detects content changes."""
    with tempfile.TemporaryDirectory() as tmp:
        dare = Path(tmp) / "dare"; pkg = Path(tmp) / "pkg"
        dare.mkdir(); pkg.mkdir()
        _mkskill(dare, "skill1", body="X")
        (dare / "skill1" / "scripts").mkdir()
        (dare / "skill1" / "scripts" / "helper.py").write_text("DARE_CONTENT", encoding="utf-8")
        rebuild(dare, pkg, {"skill1"})
        # Now modify the nested file in pkg
        (pkg / "skill1" / "scripts" / "helper.py").write_text("PKG_CONTENT", encoding="utf-8")
        # verify should detect this difference
        problems = verify(dare, pkg, {"skill1"})
        assert len(problems) > 0, "verify should detect nested content diff"
        assert "skill1" in problems[0], f"problem should name skill1: {problems}"

def test_verify_detects_same_size_different_content():
    """Test that verify uses content compare (shallow=False) not just size."""
    with tempfile.TemporaryDirectory() as tmp:
        dare = Path(tmp) / "dare"; pkg = Path(tmp) / "pkg"
        dare.mkdir(); pkg.mkdir()
        _mkskill(dare, "skill2", body="AAA")
        rebuild(dare, pkg, {"skill2"})
        # Overwrite top-level SKILL.md with same-length different content
        (pkg / "skill2" / "SKILL.md").write_text("BBB", encoding="utf-8")
        # verify should detect this despite identical file size
        problems = verify(dare, pkg, {"skill2"})
        assert len(problems) > 0, "verify should detect same-size different-content"
        assert "skill2" in problems[0], f"problem should name skill2: {problems}"

def test_rebuild_is_dir_guard():
    """Test that rebuild treats same-named non-dir files as new, not as prior copy."""
    with tempfile.TemporaryDirectory() as tmp:
        dare = Path(tmp) / "dare"; pkg = Path(tmp) / "pkg"
        dare.mkdir(); pkg.mkdir()
        _mkskill(dare, "skill3", body="X")
        _mkskill(dare, "stray_skill", body="S")
        # Create a stray file (not dir) with the same name in pkg before rebuild
        stray_file = pkg / "stray_file"
        stray_file.write_text("stray", encoding="utf-8")
        # Rebuild should treat stray_file as a stray (not a dir, not removed)
        stats = rebuild(dare, pkg, {"skill3", "stray_skill"})
        assert "stray_file" in stats["strays"], "stray_file should be reported as stray"
        assert (pkg / "skill3").is_dir(), "skill3 should be created"
        assert (pkg / "stray_skill").is_dir(), "stray_skill should be created"
