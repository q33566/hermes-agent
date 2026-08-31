# -*- coding: utf-8 -*-
# Shared SVG diagram builder. Fixes the marker-id bug from the previous build
# (defs id and marker-end reference were generated independently and never matched).
_counter = [0]

class Diagram:
    def __init__(self, vb, aria_label, caption):
        self.vb = vb
        self.aria = aria_label
        self.cap = caption
        _counter[0] += 1
        self.mid = 'arrow%d' % _counter[0]
        self.body = []

    def defs(self):
        return ('<defs><marker id="%s" markerWidth="8" markerHeight="8" refX="6" refY="3" '
                'orient="auto"><polygon points="0,0 6,3 0,6" fill="currentColor"/></marker></defs>') % self.mid

    def box(self, x, y, w, h, label, sub=None, accent=False):
        cls = 'dg-box accent' if accent else 'dg-box'
        s = '<rect class="%s" x="%d" y="%d" width="%d" height="%d" rx="8"/>' % (cls, x, y, w, h)
        ty = y + (h/2 - 6 if sub else h/2 + 4)
        s += '<text class="dg-text" x="%d" y="%d" text-anchor="middle" font-size="12">%s</text>' % (x+w/2, ty, label)
        if sub:
            s += '<text class="dg-mono" x="%d" y="%d" text-anchor="middle" font-size="9">%s</text>' % (x+w/2, ty+15, sub)
        self.body.append(s)
        return self

    def arrow(self, x1, y1, x2, y2, label=None, lx=None, ly=None):
        s = '<path class="dg-line" d="M%d %d L%d %d" marker-end="url(#%s)"/>' % (x1, y1, x2, y2, self.mid)
        if label:
            s += '<text class="dg-mono" x="%d" y="%d" font-size="10">%s</text>' % (lx if lx is not None else x1+8, ly if ly is not None else y1-6, label)
        self.body.append(s)
        return self

    def line_plain(self, x1, y1, x2, y2):
        self.body.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="dg-line"/>' % (x1,y1,x2,y2))
        return self

    def text(self, x, y, label, size=12, anchor=None, mono=False):
        cls = 'dg-mono' if mono else 'dg-text'
        a = ' text-anchor="%s"' % anchor if anchor else ''
        self.body.append('<text class="%s" x="%d" y="%d" font-size="%d"%s>%s</text>' % (cls, x, y, size, a, label))
        return self

    def raw(self, s):
        self.body.append(s)
        return self

    def render(self):
        svg = '<svg viewBox="%s" role="img" aria-label="%s">%s%s</svg>' % (
            self.vb, self.aria, self.defs(), ''.join(self.body))
        return '<div class="diagram"><figure>%s<figcaption>%s</figcaption></figure></div>' % (svg, self.cap)
