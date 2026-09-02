#!/usr/bin/env python3
"""Shared plain-table renderer for figure scripts.

Extracted so the wrap-and-measure engine exists once. Column widths are in a 0–100 grid; the
canvas height is solved in two passes, so a table is exactly as tall as its content whatever the
copy says. Rows size to their tallest cell.
"""
import os
import matplotlib.pyplot as plt

INK, SOFT, FAINT, RULE = "#111111", "#4A4A4A", "#8A959F", "#C9D3DC"
HEAD_BG, HEAD_INK, EDGE = "#EFF3F7", "#3A4650", "#9AA7B2"


def draw_table(path, cols, rows, fig_w=17.0, fs=15, hs=12.5, cell_style=None,
               pad_inches=0.18, heavy_after=(), header=True):
    """cols: [(header, width)] · rows: [[cell, ...]] · cell_style(i, s) -> (colour, weight)."""
    def render(fig_h):
        fig = plt.figure(figsize=(fig_w, fig_h))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 100); ax.set_ylim(100, 0); ax.axis("off")
        fig.canvas.draw()
        rend = fig.canvas.get_renderer()
        u = lambda inches: inches * 100.0 / fig_h
        em = lambda f: u(f / 72.0)

        def tw(s, f, w="normal"):
            t = ax.text(0, 0, s, fontsize=f, fontweight=w, alpha=0)
            bb = t.get_window_extent(renderer=rend); t.remove()
            inv = ax.transData.inverted()
            return abs(inv.transform((bb.width, 0))[0] - inv.transform((0, 0))[0])

        def wrap(s, f, w, maxw):
            out, cur = [], ""
            for word in str(s).split(" "):
                trial = f"{cur} {word}".strip()
                if cur and tw(trial, f, w) > maxw:
                    out.append(cur); cur = word
                else:
                    cur = trial
            if cur:
                out.append(cur)
            return out

        def para(x, y, s, f, w, colour, maxw):
            for line in wrap(s, f, w, maxw):
                ax.text(x, y, line, fontsize=f, fontweight=w, color=colour,
                        va="baseline", zorder=3)
                y += em(f) * 1.32

        padx, pady = 1.1, u(0.15)
        X = [1.5]
        for _, w in cols:
            X.append(X[-1] + w)

        y = u(0.10)
        if header:
            nh = max(len(wrap(c, hs, "bold", w - 2 * padx)) for c, w in cols)
            hh = nh * em(hs) * 1.28 + 2 * pady
            ax.add_patch(plt.Rectangle((X[0], y), X[-1] - X[0], hh, facecolor=HEAD_BG,
                                       edgecolor="none", zorder=0))
            for i, (c, w) in enumerate(cols):
                para(X[i] + padx, y + pady + em(hs) * 0.80, c, hs, "bold", HEAD_INK,
                     w - 2 * padx)
            y += hh
            ax.plot([X[0], X[-1]], [y, y], color=EDGE, lw=1.6, zorder=2)

        for ri, cells in enumerate(rows):
            n = max(len(wrap(s, fs, "normal", cols[i][1] - 2 * padx))
                    for i, s in enumerate(cells))
            for i, s in enumerate(cells):
                colour, weight = (cell_style(i, s) if cell_style else (INK, "normal"))
                para(X[i] + padx, y + pady + em(fs) * 0.80, s, fs, weight, colour,
                     cols[i][1] - 2 * padx)
            y += n * em(fs) * 1.32 + 2 * pady
            hv = ri in heavy_after
            ax.plot([X[0], X[-1]], [y, y], color=EDGE if hv else RULE,
                    lw=1.6 if hv else 1.0, zorder=2)

        for xi in X:
            ax.plot([xi, xi], [u(0.10), y], color=RULE, lw=1.0, zorder=2)
        ax.plot([X[0], X[-1]], [u(0.10), u(0.10)], color=EDGE, lw=1.6, zorder=2)
        return fig, y * fig_h / 100.0

    probe, need = render(8.0)
    plt.close(probe)
    fig, _ = render(need + 0.10)
    fig.savefig(path, bbox_inches="tight", pad_inches=pad_inches)
    plt.close(fig)
    return path
