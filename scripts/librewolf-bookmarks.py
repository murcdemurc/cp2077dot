#!/usr/bin/env python3
"""Exportiert die LibreWolf-Lesezeichen aus places.sqlite nach JSON.

Liest die Datenbank read-only, schreibt also nichts ins Live-Profil.
Optional (mit --prefs) wird prefs.js als librewolf-prefs.js kopiert.
"""
import datetime
import json
import os
import shutil
import sqlite3
import sys
from configparser import ConfigParser

BOOKMARK_TYPES = {1: "bookmark", 2: "folder", 3: "separator"}


def find_profile_dir():
    home = os.path.expanduser("~")
    lw_dir = os.path.join(home, ".librewolf")
    ini = os.path.join(lw_dir, "profiles.ini")
    if not os.path.isfile(ini):
        sys.exit("Keine ~/.librewolf/profiles.ini gefunden – LibreWolf ist nicht installiert.")
    cp = ConfigParser()
    cp.read(ini)
    default = first = None
    for section in cp.sections():
        if section.lower().startswith("profile"):
            if first is None:
                first = section
            if cp[section].get("default") == "1":
                default = section
    section = default or first
    if section is None:
        sys.exit("Kein Profil in profiles.ini gefunden.")
    path = cp[section]["path"]
    return lw_dir if os.path.isabs(path) else os.path.join(lw_dir, path)


def export(db, profile_name, out_path, with_prefs):
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT b.id, b.parent, b.type, b.title, b.position, p.url AS url
        FROM moz_bookmarks b
        LEFT JOIN moz_places p ON b.fk = p.id
        ORDER BY b.parent, b.position
        """
    ).fetchall()
    conn.close()

    by_id = {r["id"]: r for r in rows}
    children = {}
    for r in rows:
        children.setdefault(r["parent"], []).append(r["id"])

    def build(node_id):
        r = by_id[node_id]
        node = {
            "type": BOOKMARK_TYPES.get(r["type"], str(r["type"])),
            "title": r["title"] or "",
        }
        if r["type"] == 1 and r["url"]:
            node["url"] = r["url"]
        kids = [build(cid) for cid in children.get(node_id, [])]
        if kids:
            node["children"] = kids
        return node

    payload = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "profile": profile_name,
        "bookmarks": build(1)["children"],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print(f"{len(rows)} Lesezeichen-Einträge exportiert nach {out_path}")

    if with_prefs:
        prefs = os.path.join(os.path.dirname(db), "prefs.js")
        if os.path.isfile(prefs):
            shutil.copy2(prefs, os.path.join(os.path.dirname(out_path), "librewolf-prefs.js"))
            print("prefs.js als librewolf-prefs.js kopiert")


def main(argv):
    out_path = argv[0] if argv else os.path.expanduser(
        "~/.local/share/chezmoi/librewolf-bookmarks.json")
    with_prefs = "--prefs" in argv
    profile = find_profile_dir()
    db = os.path.join(profile, "places.sqlite")
    if not os.path.isfile(db):
        sys.exit("places.sqlite nicht gefunden – LibreWolf einmal starten, dann erneut sichern.")
    export(db, os.path.basename(profile), out_path, with_prefs)


if __name__ == "__main__":
    main(sys.argv[1:])
