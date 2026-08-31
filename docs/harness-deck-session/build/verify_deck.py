# -*- coding: utf-8 -*-
import re, json, sys

path = "/Users/kurtshen/Desktop/Harness 心智圖＋課程.html"
html = open(path, encoding="utf-8").read()

m = re.search(r"var SLIDES\s*=\s*(\{.*?\});", html, re.S)
if not m:
    print("FAILED TO FIND SLIDES BLOB")
    sys.exit(1)
data = json.loads(m.group(1))

errors = []
warnings = []
slide_count = 0
diagram_count = 0

def cjk_width(s, size):
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E7F:
            w += size
        else:
            w += size * 0.55
    return w

for cluster_id, slides in data.items():
    for slide in slides:
        slide_count += 1
        sid = slide.get("id", "?")
        diagram = slide.get("diagram")
        if not diagram:
            continue
        diagram_count += 1
        svg_m = re.search(r'viewBox="([\d\.\-]+) ([\d\.\-]+) ([\d\.\-]+) ([\d\.\-]+)"', diagram)
        if not svg_m:
            continue
        vx, vy, vw, vh = map(float, svg_m.groups())

        marker_ids = set(re.findall(r'<marker id="([^"]+)"', diagram))
        marker_refs = set(re.findall(r'marker-end="url\(#([^"]+)\)"', diagram))
        for ref in marker_refs:
            if ref not in marker_ids:
                errors.append(f"{sid}: marker-end #{ref} not defined")

        rects = re.findall(r'<rect class="([^"]*)" x="(-?[\d\.]+)" y="(-?[\d\.]+)" width="([\d\.]+)" height="([\d\.]+)"', diagram)
        boxes = []
        for cls, x, y, w, h in rects:
            x, y, w, h = float(x), float(y), float(w), float(h)
            boxes.append((x, y, w, h))
            if x < vx - 0.5 or y < vy - 0.5 or x + w > vx + vw + 0.5 or y + h > vy + vh + 0.5:
                errors.append(f"{sid}: box at ({x},{y},{w},{h}) out of viewBox {diagram[:0]}{vx},{vy},{vw},{vh}")

        for i in range(len(boxes)):
            for j in range(i+1, len(boxes)):
                x1,y1,w1,h1 = boxes[i]
                x2,y2,w2,h2 = boxes[j]
                if x1 < x2+w2 and x2 < x1+w1 and y1 < y2+h2 and y2 < y1+h1:
                    errors.append(f"{sid}: box overlap {boxes[i]} vs {boxes[j]}")

        texts = re.findall(r'<text class="([^"]*)" x="(-?[\d\.]+)" y="(-?[\d\.]+)"(?: text-anchor="([^"]*)")? font-size="(\d+)"(?: text-anchor="([^"]*)")?>([^<]*)</text>', diagram)
        for cls, x, y, anchor1, size, anchor2, label in texts:
            x, y, size = float(x), float(y), float(size)
            anchor = anchor1 or anchor2
            w = cjk_width(label, size)
            if anchor == "middle":
                left = x - w/2
                right = x + w/2
            elif anchor == "end":
                left = x - w
                right = x
            else:
                left = x
                right = x + w
            if left < vx - 2 or right > vx + vw + 2:
                warnings.append(f"{sid}: text '{label}' overflow [{left:.0f},{right:.0f}] vs viewBox width {vw}")

print(f"Slides: {slide_count}, diagrams: {diagram_count}")
print(f"Errors: {len(errors)}")
for e in errors:
    print("  ERR:", e)
print(f"Warnings (possible text overflow): {len(warnings)}")
for w in warnings:
    print("  WARN:", w)
