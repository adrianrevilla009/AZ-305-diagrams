#!/usr/bin/env python3
"""Build every .drawio file:  python build.py [section-prefix ...]   e.g. python build.py s04 s05"""
import importlib, os, sys, pkgutil, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))
import sections

wanted = sys.argv[1:]
outdir = os.path.join(HERE, "diagrams")
index, allwarn = [], []
for m in sorted(pkgutil.iter_modules(sections.__path__), key=lambda m: m.name):
    if wanted and not any(m.name.startswith(w) for w in wanted):
        continue
    mod = importlib.import_module("sections." + m.name)
    book = mod.build()
    path, warns = book.write(outdir)
    allwarn += warns
    for d in book.diagrams:
        index.append((book.filename, d.id, d.title, d.kind, d.summary))
    print(f"{book.filename}: {len(book.diagrams)} diagrams, {len(warns)} warnings")
for w in allwarn:
    print("WARN", w)
json.dump(index, open(os.path.join(HERE, "diagrams", "_index.json"), "w"), indent=1) if not wanted else None
