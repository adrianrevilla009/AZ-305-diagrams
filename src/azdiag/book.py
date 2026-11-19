import os
from .core import Diagram, legend_diagram


class Book:
    """One .drawio file = one section of the study document = many pages (one per diagram)."""

    def __init__(self, filename, title, domain=""):
        self.filename, self.title, self.domain = filename, title, domain
        self.diagrams = []

    def add(self, d):
        d.domain = d.domain or self.domain
        self.diagrams.append(d)
        return d

    def D(self, id, title, kind, summary, rule=None):
        return self.add(Diagram(id, title, kind, summary, rule, self.domain))

    def write(self, outdir):
        os.makedirs(outdir, exist_ok=True)
        pages, warns = [], []
        leg = legend_diagram(self.title, self.domain)
        for d in [leg] + self.diagrams:
            pages.append(d.build())
            for w in d.warnings:
                warns.append(f"[{self.filename}] {d.id} {d.title}: {w}")
        xml = '<mxfile host="app.diagrams.net" type="device">' + "".join(pages) + "</mxfile>"
        path = os.path.join(outdir, self.filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml)
        return path, warns
