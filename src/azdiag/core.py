"""azdiag - tiny DSL that generates draw.io (.drawio) pages using draw.io's built-in Azure icon library.

Nothing is bundled from Microsoft: icons are referenced by draw.io's own path (img/lib/azure2/...),
which draw.io resolves itself. Every icon name is validated against icon_index.txt at build time.
"""
import math, os, re
from html import escape as _esc
from xml.sax.saxutils import quoteattr

HERE = os.path.dirname(os.path.abspath(__file__))
_INDEX = [l.strip() for l in open(os.path.join(HERE, "icon_index.txt"), encoding="utf-8") if l.strip()]
_BY_STEM = {}
for _p in _INDEX:
    _BY_STEM.setdefault(_p.split("/")[-1].lower(), []).append(_p)
# when a stem exists in several categories prefer these first
_CAT_PRIORITY = ["compute", "networking", "databases", "storage", "security", "identity", "integration", "analytics",
                 "app_services", "management_governance", "containers", "ai_machine_learning", "iot", "devops",
                 "general", "migrate", "other", "web", "power_platform", "hybrid_multicloud", "azure_stack"]


def resolve_icon(name):
    """name = 'Front_Doors' or 'networking/Front_Doors'. Returns the draw.io relative path (no extension)."""
    if "/" in name:
        if name not in _INDEX:
            raise KeyError(f"unknown icon path {name}")
        return name
    hits = _BY_STEM.get(name.lower())
    if not hits:
        raise KeyError(f"unknown icon '{name}'")
    hits.sort(key=lambda p: _CAT_PRIORITY.index(p.split("/")[0]) if p.split("/")[0] in _CAT_PRIORITY else 99)
    return hits[0]


# ----------------------------------------------------------------------------- geometry constants
CW, RH = 210, 152          # grid cell width / height
X0, Y0 = 40, 104           # grid origin
ICON = 48
ICON_TOP = 34              # icon offset inside a grid row (room for group titles)
LINE_H = 14.2
CHAR_B, CHAR_N = 6.5, 5.9  # approx px per char (bold / normal) at 11px

COLORS = {  # fill, stroke
    "blue": ("#EEF5FC", "#0078D4"), "green": ("#F1F8E9", "#6FA800"), "orange": ("#FDF3E7", "#C55A11"),
    "gray": ("#F5F5F5", "#8A8A8A"), "purple": ("#F3EFFA", "#7B4FB2"), "red": ("#FCEDED", "#C00000"),
    "yellow": ("#FFF9DB", "#B8860B"), "teal": ("#E8F7F6", "#0F8B8D"), "white": ("#FFFFFF", "#8A8A8A"),
}
KIND_BADGE = {"A": ("Architecture", "#0078D4"), "D": ("Decision map", "#C55A11"), "C": ("Concept / cheat sheet", "#6B6B6B")}
EDGE = {  # color, dashed, width
    "data": ("#0078D4", False, 2), "ctrl": ("#7F7F7F", True, 1.5), "private": ("#C55A11", False, 2.5),
    "ok": ("#5B9A00", False, 2), "bad": ("#C00000", True, 2), "async": ("#7B4FB2", True, 2),
}


def wrap(text, width):
    """greedy word wrap on spaces (also after '/'), returns list of lines"""
    out = []
    for para in str(text).split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            cand = (cur + " " + w).strip() if cur else w
            if len(cand) <= width or not cur:
                cur = cand
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out


def tw(s, bold=False):
    return len(s) * (CHAR_B if bold else CHAR_N)


class _Block:
    __slots__ = ("key", "x", "y", "w", "h", "kind")

    def __init__(self, key, x, y, w, h, kind):
        self.key, self.x, self.y, self.w, self.h, self.kind = key, x, y, w, h, kind


class Diagram:
    def __init__(self, id, title, kind, summary, rule=None, domain=""):
        assert kind in KIND_BADGE
        self.id, self.title, self.kind, self.summary, self.rule, self.domain = id, title, kind, summary, rule or [], domain
        self.nodes, self.groups, self.edges, self.tables, self.texts = {}, {}, [], [], []
        self.warnings = []

    # ------------------------------------------------------------------ element constructors
    def _pos(self, c, r):
        return X0 + c * CW, Y0 + r * RH

    def icon(self, key, icon, az, aws=None, c=0, r=0, tag=None, side="below"):
        path = resolve_icon(icon)
        lines = wrap(az, 22)
        aws_lines = []
        if aws == "!":
            aws_lines = ["(no direct AWS equivalent)"]
        elif aws and aws != "-":
            aws_lines = wrap("(AWS: " + aws + ")", 26)
        tag_lines = [tag] if tag else []
        x, y = self._pos(c, r)
        cx = x + CW / 2
        maxc = max([len(l) * CHAR_B for l in lines] + [len(l) * CHAR_N for l in aws_lines + tag_lines] + [ICON])
        n = len(lines) + len(aws_lines) + len(tag_lines)
        w = min(maxc, CW - 10)
        h = ICON + 4 + n * LINE_H
        val = "<b>" + "<br>".join(_esc(l) for l in lines) + "</b>"
        if aws_lines:
            val += '<br><font color="#C55A11">' + "<br>".join(_esc(l) for l in aws_lines) + "</font>"
        if tag_lines:
            val += '<br><font color="#B8860B">' + "<br>".join(_esc(l) for l in tag_lines) + "</font>"
        if side == "right":
            self.nodes[key] = dict(type="icon", path=path, value=val, x=cx - ICON / 2, y=y + ICON_TOP, w=ICON + 8 + min(maxc, 150), h=max(ICON, n * LINE_H + 4), cx=cx, icon_y=y + ICON_TOP, side="right")
        else:
            self.nodes[key] = dict(type="icon", path=path, value=val, x=cx - w / 2, y=y + ICON_TOP, w=w, h=h, cx=cx, icon_y=y + ICON_TOP, side="below")
        return key

    def box(self, key, text, c=0, r=0, w=150, h=None, color="gray", bold=True, dx=0, dy=0, size=11):
        fill, stroke = COLORS[color]
        lines = wrap(text, max(8, int((w - 14) / (CHAR_B if bold else CHAR_N))))
        hh = h or max(40, len(lines) * (LINE_H + 1) + 18)
        x, y = self._pos(c, r)
        bx = x + CW / 2 - w / 2 + dx
        by = y + ICON_TOP + dy
        val = "<br>".join(_esc(l) for l in lines)
        if bold:
            val = "<b>" + val + "</b>"
        self.nodes[key] = dict(type="box", value=val, x=bx, y=by, w=w, h=hh, fill=fill, stroke=stroke, size=size)
        return key

    def note(self, key, text, c=0, r=0, w=190, color="#444444", size=11, bold=False, dx=0, dy=0, align="left"):
        lines = wrap(text, max(8, int((w - 6) / (CHAR_B if bold else CHAR_N))))
        hh = len(lines) * (LINE_H + 0.5) + 6
        x, y = self._pos(c, r)
        val = "<br>".join(_esc(l) for l in lines)
        if bold:
            val = "<b>" + val + "</b>"
        self.nodes[key] = dict(type="note", value=val, x=x + dx + (CW - w) / 2, y=y + ICON_TOP + dy, w=w, h=hh, color=color, size=size, align=align)
        return key

    def row(self, r, specs, c0=0, step=1.0):
        """specs: (key, icon, az, aws[, tag]) placed left to right on grid row r; returns the keys"""
        keys = []
        for i, sp in enumerate(specs):
            self.icon(sp[0], sp[1], sp[2], sp[3], c0 + i * step, r, tag=sp[4] if len(sp) > 4 else None)
            keys.append(sp[0])
        return keys

    def tree(self, parent, children, kind="data"):
        for ch in children:
            self.edge(parent, ch, "", kind, src="b", dst="t")

    def chain(self, keys, labels=None, kind="data"):
        for i in range(len(keys) - 1):
            self.edge(keys[i], keys[i + 1], labels[i] if labels and i < len(labels) else "", kind)

    def group(self, key, title, members, color="blue", dashed=True, pad=(26, 40, 26, 24), min_w=0):
        self.groups[key] = dict(title=title, members=list(members), color=color, dashed=dashed, pad=pad, min_w=min_w)
        return key

    def edge(self, a, b, label="", kind="data", both=False, src=None, dst=None, via=None, dashed=None):
        self.edges.append(dict(a=a, b=b, label=label, kind=kind, both=both, src=src, dst=dst, via=via or [], dashed=dashed))

    def table(self, c, r, cols, rows, label_w=140, hdr_color="#0078D4", dx=0, dy=0, row_label_header="", sub_header=None):
        """cols: list of dict(title, icon=None, aws=None, w=180). rows: list of (row_label, [cell,...]).
        cell prefixes: '✓ ' green, '✗ ' red, '⚠ ' amber, '★ ' blue highlight."""
        x, y = self._pos(c, r)
        x += dx
        y += dy
        self.tables.append(dict(x=x, y=y, cols=cols, rows=rows, label_w=label_w, hdr_color=hdr_color, rlh=row_label_header))

    # ------------------------------------------------------------------ layout
    def _bbox(self, key, memo):
        if key in memo:
            return memo[key]
        if key in self.nodes:
            n = self.nodes[key]
            bb = (n["x"], n["y"], n["x"] + n["w"], n["y"] + n["h"])
        else:
            g = self.groups[key]
            xs = [self._bbox(m, memo) for m in g["members"]]
            padl, padt, padr, padb = g["pad"]
            x1 = min(b[0] for b in xs) - padl
            y1 = min(b[1] for b in xs) - padt
            x2 = max(b[2] for b in xs) + padr
            y2 = max(b[3] for b in xs) + padb
            need = max(tw(g["title"], True) + 28, g["min_w"])
            if x2 - x1 < need:
                x2 = x1 + need
            bb = (x1, y1, x2, y2)
        memo[key] = bb
        return bb

    def _table_layout(self, t):
        cols, rows = t["cols"], t["rows"]
        has_icon = any(c.get("icon") for c in cols)
        hdr_h = 0
        hcells = []
        for c in cols:
            lines = wrap(c["title"], max(8, int((c.get("w", 180) - 10) / CHAR_B)))
            al = wrap("(AWS: " + c["aws"] + ")", max(8, int((c.get("w", 180) - 10) / CHAR_N))) if c.get("aws") and c["aws"] != "-" else []
            h = (46 if c.get("icon") else 8) + (len(lines) + len(al)) * LINE_H + 12
            hdr_h = max(hdr_h, h)
            hcells.append((lines, al))
        out = dict(hdr_h=hdr_h, hcells=hcells, rows=[])
        for rl, cells in rows:
            rh = 0
            ls = []
            for ci, cell in enumerate(cells):
                w = cols[ci].get("w", 180)
                txt = str(cell)
                lines = wrap(txt, max(6, int((w - 14) / CHAR_N)))
                ls.append(lines)
                rh = max(rh, len(lines) * LINE_H + 12)
            rll = wrap(rl, max(6, int((t["label_w"] - 14) / CHAR_B)))
            rh = max(rh, len(rll) * LINE_H + 12, 28)
            out["rows"].append((rll, ls, rh))
        tot_w = t["label_w"] + sum(c.get("w", 180) for c in cols)
        tot_h = hdr_h + sum(r[2] for r in out["rows"])
        out["w"], out["h"] = tot_w, tot_h
        return out

    # ------------------------------------------------------------------ XML build
    def _normalize(self):
        """shift everything so the content starts at the top-left margin (removes empty rows/cols)"""
        if getattr(self, "_normalized", False):
            return
        memo = {}
        xs, ys = [], []
        for k, n in self.nodes.items():
            xs.append(n["x"]); ys.append(n["y"])
        for t in self.tables:
            xs.append(t["x"]); ys.append(t["y"])
        for k in self.groups:
            bb = self._bbox(k, memo)
            xs.append(bb[0]); ys.append(bb[1])
        dx = X0 - min(xs) if xs else 0
        dy = (Y0 - 4) - min(ys) if ys else 0
        for n in self.nodes.values():
            n["x"] += dx; n["y"] += dy
            if "cx" in n:
                n["cx"] += dx; n["icon_y"] += dy
        for t in self.tables:
            t["x"] += dx; t["y"] += dy
        self._sx, self._sy = dx, dy
        self._normalized = True

    def build(self):
        self.warnings = []
        self._normalize()
        memo = {}
        # blocks for bounds/overlap checks
        blocks = []
        for k, n in self.nodes.items():
            blocks.append(_Block(k, n["x"], n["y"], n["w"], n["h"], "node"))
        tlay = []
        for ti, t in enumerate(self.tables):
            lay = self._table_layout(t)
            tlay.append(lay)
            blocks.append(_Block(f"table{ti}", t["x"], t["y"], lay["w"], lay["h"], "table"))
        gb = {k: self._bbox(k, memo) for k in self.groups}
        for k, b in gb.items():
            blocks.append(_Block(k, b[0], b[1], b[2] - b[0], b[3] - b[1], "group"))

        minx = min(b.x for b in blocks) if blocks else X0
        maxx = max(b.x + b.w for b in blocks) if blocks else 900
        maxy = max(b.y + b.h for b in blocks) if blocks else 400
        width = max(maxx - X0, 900)

        # ---- cells
        cells = []
        self._n = 1

        def nid():
            self._n += 1
            return f"c{self._n}"

        ids = {}
        # parent mapping by declared membership (smallest enclosing group wins)
        parent = {}
        order = sorted(self.groups, key=lambda k: (gb[k][2] - gb[k][0]) * (gb[k][3] - gb[k][1]))
        for gk in order:
            for m in self.groups[gk]["members"]:
                if m not in parent:
                    parent[m] = gk
        for gk in self.groups:
            ids[gk] = nid()
        for k in self.nodes:
            ids[k] = nid()
        abspos = {}

        def rel(x, y, p):
            if p:
                px, py = abspos[p]
                return x - px, y - py
            return x, y

        def add(cid, value, style, x, y, w, h, p=None):
            gx, gy = rel(x, y, p)
            cells.append(f'<mxCell id="{cid}" value={quoteattr(value)} style={quoteattr(style)} vertex="1" parent="{ids[p] if p else "1"}">'
                         f'<mxGeometry x="{gx:.0f}" y="{gy:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>')

        # title area
        tid = nid()
        titletxt = f"{self.id}  {self.title}"
        cells.append(f'<mxCell id="{tid}" value={quoteattr(f"<b>{_esc(titletxt)}</b>")} style="text;html=1;align=left;verticalAlign=middle;fontSize=20;" vertex="1" parent="1">'
                     f'<mxGeometry x="{X0}" y="14" width="{max(len(titletxt) * 11.6, 260):.0f}" height="30" as="geometry"/></mxCell>')
        bl, bc = KIND_BADGE[self.kind]
        bx = X0 + max(len(titletxt) * 11.6, 260) + 10
        cells.append(f'<mxCell id="{nid()}" value={quoteattr(_esc(bl))} style="rounded=1;whiteSpace=wrap;html=1;fillColor={bc};strokeColor=none;fontColor=#FFFFFF;fontSize=11;fontStyle=1;arcSize=50;" vertex="1" parent="1">'
                     f'<mxGeometry x="{bx:.0f}" y="19" width="{tw(bl, True) + 24:.0f}" height="22" as="geometry"/></mxCell>')
        if self.domain:
            cells.append(f'<mxCell id="{nid()}" value={quoteattr("AZ-305 domain: " + _esc(self.domain))} style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#8A8A8A;" vertex="1" parent="1">'
                         f'<mxGeometry x="{bx + tw(bl, True) + 36:.0f}" y="19" width="420" height="22" as="geometry"/></mxCell>')
        sl = wrap(self.summary, int(min(width, 1500) / CHAR_N))
        sh = len(sl) * (LINE_H + 1) + 6
        cells.append(f'<mxCell id="{nid()}" value={quoteattr("<br>".join(_esc(l) for l in sl))} style="text;html=1;align=left;verticalAlign=top;fontSize=12;fontColor=#555555;whiteSpace=wrap;" vertex="1" parent="1">'
                     f'<mxGeometry x="{X0}" y="48" width="{min(width, 1500):.0f}" height="{sh:.0f}" as="geometry"/></mxCell>')
        if 48 + sh > Y0 - 6:
            self.warnings.append("summary too long (overlaps content)")

        # groups (largest first so nested ones draw above)
        for gk in sorted(self.groups, key=lambda k: -(gb[k][2] - gb[k][0]) * (gb[k][3] - gb[k][1])):
            g = self.groups[gk]
            b = gb[gk]
            fill, stroke = COLORS[g["color"]]
            abspos[gk] = (b[0], b[1])
            style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};{'dashed=1;' if g['dashed'] else ''}"
                     f"verticalAlign=top;align=left;spacingLeft=10;spacingTop=6;fontStyle=1;fontSize=12;fontColor={stroke};arcSize=3;container=0;")
            add(ids[gk], g["title"], style, b[0], b[1], b[2] - b[0], b[3] - b[1], parent.get(gk))
        # tables
        for ti, t in enumerate(self.tables):
            lay = tlay[ti]
            x, y = t["x"], t["y"]
            cur = x
            if t["rlh"]:
                add(nid(), f"<b>{_esc(t['rlh'])}</b>", f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=none;fontSize=11;align=left;spacingLeft=6;", x, y, t["label_w"], lay["hdr_h"])
            cx = x + t["label_w"]
            for ci, c in enumerate(t["cols"]):
                w = c.get("w", 180)
                lines, al = lay["hcells"][ci]
                val = "<b>" + "<br>".join(_esc(l) for l in lines) + "</b>"
                if al:
                    val += '<br><font color="#C55A11">' + "<br>".join(_esc(l) for l in al) + "</font>"
                if c.get("icon"):
                    st = (f"shape=label;whiteSpace=wrap;html=1;fillColor=#EEF5FC;strokeColor={t['hdr_color']};fontSize=11;"
                          f"image=img/lib/azure2/{resolve_icon(c['icon'])}.svg;imageWidth=40;imageHeight=40;imageAlign=center;imageVerticalAlign=top;"
                          f"verticalAlign=bottom;spacingBottom=4;imageBorder=none;")
                else:
                    st = f"rounded=0;whiteSpace=wrap;html=1;fillColor=#EEF5FC;strokeColor={t['hdr_color']};fontSize=11;"
                add(nid(), val, st, cx, y, w, lay["hdr_h"])
                cx += w
            cy = y + lay["hdr_h"]
            for ri, (rll, ls, rh) in enumerate(lay["rows"]):
                add(nid(), "<b>" + "<br>".join(_esc(l) for l in rll) + "</b>",
                    "rounded=0;whiteSpace=wrap;html=1;fillColor=#F2F2F2;strokeColor=#BFBFBF;fontSize=11;align=left;verticalAlign=middle;spacingLeft=6;", x, cy, t["label_w"], rh)
                cx = x + t["label_w"]
                for ci, lines in enumerate(ls):
                    raw = str(t["rows"][ri][1][ci])
                    fill = "#FFFFFF"
                    fc = "#000000"
                    if raw.startswith("✓"):
                        fill = "#E8F5E0"
                    elif raw.startswith("✗"):
                        fill = "#FBE5E5"
                    elif raw.startswith("⚠"):
                        fill = "#FFF4CC"
                    elif raw.startswith("★"):
                        fill = "#DCEBFA"
                    add(nid(), "<br>".join(_esc(l) for l in lines),
                        f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=#BFBFBF;fontSize=11;align=left;verticalAlign=middle;spacingLeft=6;fontColor={fc};",
                        cx, cy, t["cols"][ci].get("w", 180), rh)
                    cx += t["cols"][ci].get("w", 180)
                cy += rh
        # edges before nodes (so lines never cover icons)
        ecells = []
        for e in self.edges:
            if e["a"] not in self.nodes or e["b"] not in self.nodes:
                raise KeyError(f"{self.id}: edge references unknown node {e['a']}->{e['b']}")
            col, dsh, wd = EDGE[e["kind"]]
            if e["dashed"] is not None:
                dsh = e["dashed"]
            sides = {"l": (0, 0.5), "r": (1, 0.5), "t": (0.5, 0), "b": (0.5, 1)}
            extra = ""
            if not e["src"] and not e["dst"] and not e["via"]:
                A, B = self.nodes[e["a"]], self.nodes[e["b"]]
                dx = (B["x"] + B["w"] / 2) - (A["x"] + A["w"] / 2)
                dy = (B["y"] + B["h"] / 2) - (A["y"] + A["h"] / 2)
                if abs(dx) >= 20:
                    e["src"], e["dst"] = ("r", "l") if dx > 0 else ("l", "r")
                else:
                    e["src"], e["dst"] = ("b", "t") if dy > 0 else ("t", "b")
            if e["src"]:
                extra += f"exitX={sides[e['src']][0]};exitY={sides[e['src']][1]};exitDx=0;exitDy=0;"
            if e["dst"]:
                extra += f"entryX={sides[e['dst']][0]};entryY={sides[e['dst']][1]};entryDx=0;entryDy=0;"
            style = (f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;{'startArrow=block;startFill=1;' if e['both'] else ''}"
                     f"strokeWidth={wd};strokeColor={col};{'dashed=1;' if dsh else ''}fontSize=10;labelBackgroundColor=#FFFFFF;{extra}")
            pts = ""
            if e["via"]:
                pts = '<Array as="points">' + "".join(
                    f'<mxPoint x="{X0 + c * CW + CW / 2 + self._sx:.0f}" y="{Y0 + r * RH + ICON_TOP + ICON / 2 + self._sy:.0f}"/>' for c, r in e["via"]) + "</Array>"
            ecells.append(f'<mxCell id="{nid()}" value={quoteattr(_esc(e["label"]))} style={quoteattr(style)} edge="1" parent="1" '
                          f'source="{ids[e["a"]]}" target="{ids[e["b"]]}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>')
        cells.extend(ecells)
        # nodes
        for k, n in self.nodes.items():
            p = parent.get(k)
            if n["type"] == "icon":
                abspos[k] = (n["x"], n["y"])
                # draw as a vertex of icon size, label below; geometry = icon square centered
                gx, gy = rel(n["cx"] - ICON / 2, n["icon_y"], p)
                if n.get("side") == "right":
                    st = (f"image;aspect=fixed;html=1;points=[];fontSize=11;labelPosition=right;verticalLabelPosition=middle;align=left;verticalAlign=middle;spacingLeft=4;"
                          f"image=img/lib/azure2/{n['path']}.svg;")
                else:
                    st = (f"image;aspect=fixed;html=1;points=[];align=center;fontSize=11;verticalLabelPosition=bottom;verticalAlign=top;"
                          f"image=img/lib/azure2/{n['path']}.svg;")
                cells.append(f'<mxCell id="{ids[k]}" value={quoteattr(n["value"])} style={quoteattr(st)} vertex="1" parent="{ids[p] if p else "1"}">'
                             f'<mxGeometry x="{gx:.0f}" y="{gy:.0f}" width="{ICON}" height="{ICON}" as="geometry"/></mxCell>')
            elif n["type"] == "box":
                abspos[k] = (n["x"], n["y"])
                st = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={n['fill']};strokeColor={n['stroke']};fontSize={n['size']};arcSize=12;")
                add(ids[k], n["value"], st, n["x"], n["y"], n["w"], n["h"], p)
            else:
                abspos[k] = (n["x"], n["y"])
                st = f"text;html=1;whiteSpace=wrap;align={n['align']};verticalAlign=top;fontSize={n['size']};fontColor={n['color']};"
                add(ids[k], n["value"], st, n["x"], n["y"], n["w"], n["h"], p)

        # exam rule callout
        if self.rule:
            y = maxy + 34
            items = [f"<b>{_esc(c)}</b> → {_esc(a)}" for c, a in self.rule]
            cols_n = 2 if len(items) > 5 and width >= 1000 else 1
            colw = (width - 24) / cols_n
            per = math.ceil(len(items) / cols_n)
            heights = []
            chunks = [items[i * per:(i + 1) * per] for i in range(cols_n)]
            for ch in chunks:
                hh = 0
                for it in ch:
                    plain = re.sub(r"<[^>]+>", "", it)
                    hh += len(wrap(plain, int((colw - 8) / CHAR_N))) * LINE_H + 2
                heights.append(hh)
            box_h = max(heights) + 32
            cells.append(f'<mxCell id="{nid()}" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF9DB;strokeColor=#B8860B;arcSize=4;" vertex="1" parent="1">'
                         f'<mxGeometry x="{X0}" y="{y:.0f}" width="{width:.0f}" height="{box_h:.0f}" as="geometry"/></mxCell>')
            cells.append(f'<mxCell id="{nid()}" value="&lt;b&gt;EXAM RULES&lt;/b&gt;" style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#B8860B;" vertex="1" parent="1">'
                         f'<mxGeometry x="{X0 + 10}" y="{y + 4:.0f}" width="200" height="20" as="geometry"/></mxCell>')
            for ci, ch in enumerate(chunks):
                cells.append(f'<mxCell id="{nid()}" value={quoteattr("<br>".join(ch))} style="text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fontSize=11;" vertex="1" parent="1">'
                             f'<mxGeometry x="{X0 + 10 + ci * colw:.0f}" y="{y + 26:.0f}" width="{colw - 10:.0f}" height="{heights[ci]:.0f}" as="geometry"/></mxCell>')
            maxy = y + box_h

        self._check(blocks, gb, parent)
        pw, ph = int(X0 + width + 60), int(maxy + 60)
        return (f'<diagram id="d{self.id.replace(".", "_")}" name={quoteattr(self.id + " " + self.title)}>'
                f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" '
                f'pageScale="1" pageWidth="{pw}" pageHeight="{ph}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
                + "".join(cells) + "</root></mxGraphModel></diagram>")

    # ------------------------------------------------------------------ QA heuristics
    def _check(self, blocks, gb, parent):
        w = self.warnings
        leafs = [b for b in blocks if b.kind in ("node", "table")]
        for i, a in enumerate(leafs):
            for b in leafs[i + 1:]:
                if a.x < b.x + b.w - 2 and b.x < a.x + a.w - 2 and a.y < b.y + b.h - 2 and b.y < a.y + a.h - 2:
                    w.append(f"overlap: {a.key} x {b.key}")
        # leaf vs unrelated group (leaf inside a group it isn't a member of)
        for g, bb in gb.items():
            members = set(self._all_members(g))
            for a in leafs:
                if a.key in members:
                    continue
                if a.x < bb[2] and bb[0] < a.x + a.w and a.y < bb[3] and bb[1] < a.y + a.h:
                    w.append(f"{a.key} intrudes into group '{self.groups[g]['title'][:25]}'")
        # sibling groups overlapping (neither contains the other)
        gks = list(self.groups)
        for i, a in enumerate(gks):
            for b in gks[i + 1:]:
                A, B = gb[a], gb[b]
                inter = A[0] < B[2] and B[0] < A[2] and A[1] < B[3] and B[1] < A[3]
                a_in_b = A[0] >= B[0] and A[1] >= B[1] and A[2] <= B[2] and A[3] <= B[3]
                b_in_a = B[0] >= A[0] and B[1] >= A[1] and B[2] <= A[2] and B[3] <= A[3]
                if inter and not a_in_b and not b_in_a:
                    w.append(f"groups overlap: '{self.groups[a]['title'][:20]}' x '{self.groups[b]['title'][:20]}'")
        # text overflow in boxes
        for k, n in self.nodes.items():
            if n["type"] == "box":
                lines = re.sub(r"<br>", "\n", re.sub(r"</?b>", "", n["value"])).split("\n")
                if len(lines) * (LINE_H + 1) + 6 > n["h"]:
                    w.append(f"box text overflow: {k}")
        # edges crossing unrelated nodes (straight/elbow approximation)
        for e in self.edges:
            A, B = self.nodes[e["a"]], self.nodes[e["b"]]
            ax, ay = A["x"] + A["w"] / 2, (A["icon_y"] + ICON / 2) if A["type"] == "icon" else A["y"] + A["h"] / 2
            bx, by = B["x"] + B["w"] / 2, (B["icon_y"] + ICON / 2) if B["type"] == "icon" else B["y"] + B["h"] / 2
            pts = [(ax, ay)] + [(X0 + c * CW + CW / 2 + self._sx, Y0 + r * RH + ICON_TOP + ICON / 2 + self._sy) for c, r in e["via"]] + [(bx, by)]
            if len(pts) == 2 and abs(ax - bx) > 4 and abs(ay - by) > 4:
                mx = (ax + bx) / 2
                pts = [(ax, ay), (mx, ay), (mx, by), (bx, by)]
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                for k, n in self.nodes.items():
                    if k in (e["a"], e["b"]):
                        continue
                    ry1 = n["icon_y"] if n["type"] == "icon" else n["y"]
                    ry2 = (n["icon_y"] + ICON) if n["type"] == "icon" else n["y"] + n["h"]
                    rx1, rx2 = (n["cx"] - ICON / 2, n["cx"] + ICON / 2) if n["type"] == "icon" else (n["x"], n["x"] + n["w"])
                    if n["type"] == "note":
                        continue
                    if max(min(x1, x2), rx1) < min(max(x1, x2), rx2) and max(min(y1, y2), ry1) < min(max(y1, y2), ry2):
                        w.append(f"edge {e['a']}->{e['b']} crosses {k}")
                        break

    def _all_members(self, g):
        out = []
        for m in self.groups[g]["members"]:
            out.append(m)
            if m in self.groups:
                out.extend(self._all_members(m))
        return out


def legend_diagram(file_title, domain):
    """First page of every file: explains icons, colours and line styles."""
    d = Diagram("0", "Legend - " + file_title, "C",
                "How to read the diagrams in this file. Icons are draw.io's built-in Azure icon set; the orange text under each icon is the closest AWS equivalent.",
                domain=domain)
    d.icon("a", "Virtual_Machine", "Azure service name", "closest AWS equivalent", 0, 0)
    d.icon("b", "Storage_Accounts", "Another service", "S3", 1, 0, tag="⚠ verify")
    d.note("n1", "Bold text = Azure service. Orange text = closest AWS equivalent (taken from your study document where it gives one). Amber '⚠ verify' = your document flags the detail as to be verified (dates, SKUs, limits). Amber '+ added' = a service I added that is not in your document.", 0, 1, w=420, dx=105, dy=-20)
    d.edge("a", "b", "data flow", "data")
    d.icon("c", "Key_Vaults", "Control / telemetry", None, 2.2, 0)
    d.icon("d", "Monitor", "Observer", None, 3.2, 0)
    d.edge("c", "d", "dashed = management / telemetry", "ctrl")
    d.icon("e", "Private_Endpoint", "Private path", None, 4.4, 0)
    d.icon("f", "SQL_Database", "PaaS target", None, 5.4, 0)
    d.edge("e", "f", "orange = private / dedicated link", "private")
    d.box("kA", "A = Architecture: how pieces connect", 0.2, 2.2, w=250, color="blue")
    d.box("kD", "D = Decision map: which service when (table)", 1.5, 2.2, w=280, color="orange")
    d.box("kC", "C = Concept / cheat sheet", 3.0, 2.2, w=230, color="gray")
    d.box("g1", "Dashed blue/green boxes = scope or boundary (VNet, subnet, region, subscription...)", 4.3, 2.2, w=300, color="green")
    d.rule = [("Table colours", "green = yes / supported, red = not supported, amber = caution, blue = key point"),
              ("Exam rules", "each page ends with the 'Regla del examen' pairs from the study document, translated to English")]
    return d
