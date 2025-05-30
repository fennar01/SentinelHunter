#!/usr/bin/env python3
"""
CLI utility to update ROADMAP.md based on commit messages.
Scans for 'Closes <Epic>-<number>' and updates the Status to '✅ Done'.
"""
import re
import sys
from pathlib import Path

ROADMAP = Path(__file__).parent.parent / "ROADMAP.md"


def update_roadmap(epic_key):
    lines = ROADMAP.read_text().splitlines()
    new_lines = []
    for line in lines:
        if epic_key in line and "⏳ Planned" in line:
            line = line.replace("⏳ Planned", "✅ Done")
        new_lines.append(line)
    ROADMAP.write_text("\n".join(new_lines) + "\n")


def main():
    # Simulate reading commit messages from stdin or a file
    commit_msgs = sys.stdin.read()
    matches = re.findall(r"Closes ([\w-]+-\d+)", commit_msgs)
    for epic_key in matches:
        update_roadmap(epic_key)
    # Optionally: git add, commit, and push
    # os.system('git add ROADMAP.md && git commit -m "Update roadmap" && git push')

if __name__ == "__main__":
    main()
