"""One-shot acceptance check for the mechanism-gap-hunting skill.
Verifies: (1) frontmatter parses, (2) execution==campaign, (3) no used-by,
(4) no tactics key, (5) every dependency resolves to a real dir in the DARE body."""
import sys, yaml
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent           # deep-insight repo
BODY = PKG.parent / "de-anthropocentric-research-engine"
SKILL = PKG / "skills" / "mechanism-gap-hunting" / "SKILL.md"
EXPECT = {
    "strategies": ["assumption-audit", "dialectical-reformulation", "failure-mode-analysis"],
    "sops": ["abstraction-laddering", "context-checkpoint", "context-init",
             "current-reality-tree", "deep-insight-assumption-surfacing",
             "failure-clustering", "five-whys-drilling"],
}

def main():
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---"), "no frontmatter"
    fm = yaml.safe_load(text.split("---", 2)[1])
    assert fm["name"] == "mechanism-gap-hunting", fm.get("name")
    assert fm["execution"] == "campaign", fm.get("execution")
    assert "used-by" not in fm, "used-by must be absent"
    deps = fm["dependencies"]
    assert "tactics" not in deps, "tactics key must be absent this version"
    assert deps["strategies"] == sorted(deps["strategies"]), "strategies not alphabetical"
    assert deps["sops"] == sorted(deps["sops"]), "sops not alphabetical"
    assert deps["strategies"] == EXPECT["strategies"], deps["strategies"]
    assert deps["sops"] == EXPECT["sops"], deps["sops"]
    missing = [d for grp in deps.values() for d in grp
               if not (BODY / "skills" / d).is_dir()]
    assert not missing, f"dependencies not resolvable in body: {missing}"
    print("check_mgh: OK — frontmatter valid, 10 deps resolve in body")

if __name__ == "__main__":
    sys.exit(main())
