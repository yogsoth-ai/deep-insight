import json, os, tempfile
from sync_from_dare import load_members, compute_diff

def _write(tmp, obj):
    p = os.path.join(tmp, "refactory_source.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f)
    return p

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
