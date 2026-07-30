"""
utils.py
========
Reusable component-building "toolkit" for the PIM-PAM Dash replica.
Every function here returns Dash html/dcc components — no callbacks live
here (those are registered in app.py), just pure layout builders, mirroring
the original React components/ folder 1:1 (one builder function ~ one .tsx
component).
"""

import logging
import os
import urllib.parse
from datetime import datetime

from dash import html, dcc

from constants import (
    COLORS, ICONS_FILL, ICONS_STROKE, NAV_LINKS, FOOTER_TOOL_LINKS,
    FOOTER_OTHER_LINKS, DIMENSIONS_8, CAROUSEL_AREAS, CAROUSEL_DIMENSIONS,
    MATURITY_LEVELS, CARD_SCROLL_STEP,
)

logger = logging.getLogger("pimpam.utils")

# ──────────────────────────────────────────────────────────────────────────
# APP / ASSET REGISTRATION
# every image, icon, and PDF in this file is resolved through Dash's
# `app.get_asset_url()` — per the project requirement, nothing is ever
# hardcoded as a raw "/assets/..." string.
# ──────────────────────────────────────────────────────────────────────────
_app = None


def register_app(app):
    """Called once from app.py right after the Dash app is created, so this
    module can resolve asset URLs via app.get_asset_url()."""
    global _app
    _app = app
    logger.info("utils.register_app(): asset resolver bound to Dash app instance.")


def asset(path):
    if _app is None:
        logger.error("utils.asset(%r) called before register_app() — assets will 404.", path)
        raise RuntimeError("utils.register_app(app) must be called before building layouts.")
    return _app.get_asset_url(path)


# ──────────────────────────────────────────────────────────────────────────
# ICON HELPERS  (SVG -> data-URI <img>, since dash.html has no <svg> tags)
# ──────────────────────────────────────────────────────────────────────────

def _svg_markup(inner, view_box="0 0 24 24", color="#E6EAF2", stroke=False, stroke_width=2):
    if stroke:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" '
            f'fill="none" stroke="{color}" stroke-width="{stroke_width}" '
            f'stroke-linecap="round" stroke-linejoin="round">{inner}</svg>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" '
        f'fill="{color}">{inner}</svg>'
    )


def icon_uri(name, color="#E6EAF2", view_box="0 0 24 24"):
    """Build a data: URI for a named icon (fill or stroke set)."""
    if name in ICONS_FILL:
        inner = "".join(f'<path d="{d}"/>' for d in ICONS_FILL[name])
        svg = _svg_markup(inner, view_box=view_box, color=color, stroke=False)
    elif name in ICONS_STROKE:
        svg = _svg_markup(ICONS_STROKE[name], view_box=view_box, color=color, stroke=True)
    else:
        raise KeyError(f"Unknown icon: {name}")
    return "data:image/svg+xml," + urllib.parse.quote(svg)


def Icon(name, size=20, color="#E6EAF2", className="", style=None, view_box="0 0 24 24"):
    """Return an <img> rendering of an icon. Analogous to the inline <svg>
    icon components used throughout the original .tsx files."""
    base_style = {
        "width": f"{size}px",
        "height": f"{size}px",
        "display": "inline-block",
        "flexShrink": "0",
        "verticalAlign": "middle",
    }
    if style:
        base_style.update(style)
    return html.Img(
        src=icon_uri(name, color=color, view_box=view_box),
        className=className,
        style=base_style,
        alt="",
    )


# ──────────────────────────────────────────────────────────────────────────
# GridOverlay.tsx
# ──────────────────────────────────────────────────────────────────────────

def GridOverlay():
    return html.Div(
        className="absolute inset-0 pointer-events-none",
        style={
            "backgroundImage": (
                "linear-gradient(rgba(255,255,255,0.055) 1px, transparent 1px), "
                "linear-gradient(90deg, rgba(255,255,255,0.055) 1px, transparent 1px)"
            ),
            "backgroundSize": "60px 60px",
        },
    )


# ──────────────────────────────────────────────────────────────────────────
# IconArrow.tsx
# ──────────────────────────────────────────────────────────────────────────

def IconArrow(size=16, color="#FFFFFF"):
    return Icon("arrow", size=size, color=color)


# ──────────────────────────────────────────────────────────────────────────
# SectionHeading.tsx
# ──────────────────────────────────────────────────────────────────────────

def SectionHeading(heading, eyebrow=None, subheading=None, centered=False,
                    light=False, light_badge=False):
    children = []
    if eyebrow:
        badge_bg = "bg-white" if light_badge else "bg-accent1/10"
        children.append(
            html.P(eyebrow, className=(
                f"inline-block text-xs font-semibold uppercase tracking-widest "
                f"text-accent1 rounded-full px-3 py-1 mb-3 {badge_bg}"
            ))
        )
    heading_color = "text-gray-900" if light else "text-text"
    children.append(
        html.H2(heading, className=f"text-3xl sm:text-4xl font-bold leading-tight mb-4 {heading_color}")
    )
    if subheading:
        sub_color = "text-gray-500" if light else "text-muted"
        mx = "mx-auto" if centered else ""
        children.append(
            html.P(subheading, className=f"text-base sm:text-lg leading-relaxed max-w-2xl {mx} {sub_color}")
        )
    return html.Div(children, className="text-center" if centered else "")


# ──────────────────────────────────────────────────────────────────────────
# Nav.tsx
# ──────────────────────────────────────────────────────────────────────────

def NavBar():
    desktop_links = []
    mobile_links = []
    for link in NAV_LINKS:
        badge = None
        if link.get("badge"):
            badge = html.Span(
                link["badge"],
                className="inline-block text-[10px] font-bold uppercase tracking-wide bg-accent4 text-white px-1.5 py-0.5 rounded-full leading-none",
            )
        desktop_links.append(
            dcc.Link(
                [link["label"], badge] if badge else link["label"],
                href=link["href"],
                className="relative flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-muted hover:text-text transition-colors duration-200 rounded hover:bg-white/5",
            )
        )
        mobile_links.append(
            dcc.Link(
                [link["label"], badge] if badge else link["label"],
                href=link["href"],
                className="flex items-center gap-2 px-4 py-3 text-sm font-medium text-muted hover:text-text rounded hover:bg-white/5 transition-colors",
            )
        )

    return html.Header(
        id="site-nav",
        className="fixed top-0 left-0 right-0 z-50 transition-all duration-300 bg-transparent",
        children=[
            html.Div(
                className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                children=html.Div(
                    className="flex items-center justify-between h-16",
                    children=[
                        dcc.Link(
                            html.Img(
                                src=asset("PIM-PAM-Logo.png"),
                                alt="PIM-PAM",
                                className="h-14 w-auto object-contain",
                            ),
                            href="/",
                            className="flex items-center",
                        ),
                        html.Nav(desktop_links, className="hidden lg:flex items-center gap-1"),
                        html.Button(
                            Icon("menu", size=20, color="#8A93A8"),
                            id="nav-mobile-btn",
                            n_clicks=0,
                            className="lg:hidden p-2 rounded text-muted hover:text-text hover:bg-white/5 transition-colors",
                            **{"aria-label": "Open menu"},
                        ),
                    ],
                ),
            ),
            html.Div(
                id="nav-mobile-menu",
                className="lg:hidden bg-surface/95 backdrop-blur-md border-b border-white/5 hidden",
                children=html.Nav(mobile_links, className="max-w-7xl mx-auto px-4 py-4 flex flex-col gap-1"),
            ),
        ],
    )


# ──────────────────────────────────────────────────────────────────────────
# PimPamAiBanner.tsx
# ──────────────────────────────────────────────────────────────────────────

def PimPamAiBanner():
    return html.Section(
        className="relative overflow-hidden",
        style={
            "background": (
                "radial-gradient(ellipse 80% 120% at 80% 50%, rgba(55,179,127,0.12) 0%, transparent 60%), #0d1120"
            )
        },
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 flex flex-col md:flex-row items-center justify-between gap-8",
            children=[
                html.Div(
                    className="flex items-start gap-5",
                    children=[
                        html.Div(Icon("ai", size=36, color=COLORS["accent2"]), className="flex-shrink-0 mt-1 text-accent2"),
                        html.Div([
                            html.H2("AI for smarter public investment and asset governance",
                                    className="text-2xl sm:text-3xl font-bold text-white leading-snug mb-2"),
                            html.P("Open-source AI tools and curated data for ministries of finance, PIM practitioners, and peer-learning networks.",
                                   className="text-sm text-white/60 max-w-xl leading-relaxed"),
                        ]),
                    ],
                ),
                html.Div(
                    html.A(
                        ["Visit pim-pam.ai", Icon("external_link", size=15, color="#FFFFFF")],
                        href="https://pim-pam.ai", target="_blank", rel="noopener noreferrer",
                        className="inline-flex items-center gap-2 px-6 py-3 rounded bg-accent2 text-white text-sm font-semibold hover:bg-accent2/90 transition-colors whitespace-nowrap",
                    ),
                    className="flex-shrink-0",
                ),
            ],
        ),
    )


# ──────────────────────────────────────────────────────────────────────────
# Footer.tsx
# ──────────────────────────────────────────────────────────────────────────

def Footer():
    tool_items = [
        html.Li(html.A(link["label"], href=link["href"], target="_blank", rel="noopener noreferrer",
                        className="text-sm text-muted hover:text-text transition-colors"))
        for link in FOOTER_TOOL_LINKS
    ]
    other_items = []
    for link in FOOTER_OTHER_LINKS:
        if link.get("external"):
            other_items.append(html.Li(html.A(link["label"], href=link["href"], target="_blank", rel="noopener noreferrer",
                                               className="text-sm text-muted hover:text-text transition-colors")))
        else:
            other_items.append(html.Li(dcc.Link(link["label"], href=link["href"],
                                                  className="text-sm text-muted hover:text-text transition-colors")))

    return html.Footer(
        className="relative bg-surface border-t border-white/5 overflow-hidden",
        children=[
            GridOverlay(),
            html.Div(
                className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16",
                children=html.Div(
                    className="grid grid-cols-1 md:grid-cols-3 gap-16",
                    children=[
                        html.Div([
                            dcc.Link(
                                html.Img(src=asset("PIM-PAM-Logo.png"), alt="PIM-PAM",
                                         className="h-12 w-auto object-contain"),
                                href="/", className="inline-block mb-4",
                            ),
                            html.P(
                                "A World Bank initiative promoting digital tools for smarter public investment "
                                "and asset management, in collaboration with the Vienna Development Knowledge Center.",
                                className="text-muted text-sm leading-relaxed",
                            ),
                        ]),
                        html.Div([
                            html.H3("Digital Tools", className="text-sm font-semibold text-text uppercase tracking-wider mb-4"),
                            html.Ul(tool_items, className="space-y-2"),
                        ]),
                        html.Div([
                            html.H3("Other Links", className="text-sm font-semibold text-text uppercase tracking-wider mb-4"),
                            html.Ul(other_items, className="space-y-2"),
                        ]),
                    ],
                ),
            ),
            html.Div(
                className="relative z-10",
                style={"backgroundColor": "#06090f"},
                children=html.Div(
                    className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5 flex flex-col sm:flex-row items-center justify-between gap-4",
                    children=[
                        html.P(f"\u00a9 {datetime.now().year} PIM-PAM / PIIAG \u2014 World Bank Initiative. All rights reserved.",
                               className="text-xs text-muted"),
                        html.A(
                            ["Back to top", Icon("arrow_up", size=14, color="#8A93A8")],
                            href="#top",
                            className="inline-flex items-center gap-2 text-xs text-muted hover:text-accent3 transition-colors group",
                        ),
                    ],
                ),
            ),
        ],
    )


# ──────────────────────────────────────────────────────────────────────────
# DimensionGrid.tsx  (home page "8 Must-Have Dimensions" grid)
# ──────────────────────────────────────────────────────────────────────────

def DimensionGrid():
    cards = []
    for dim in DIMENSIONS_8:
        cards.append(
            html.Div(
                className="group relative bg-surface border border-white/5 rounded overflow-hidden hover:bg-surface-2 transition-colors flex flex-col p-6 min-h-[200px]",
                children=[
                    html.Div(className="absolute top-0 left-0 right-0 h-[3px] bg-accent1"),
                    html.H3(dim["title"], className="text-base font-bold text-text mb-2 leading-snug mt-8"),
                    html.P(dim["description"], className="text-sm text-muted leading-relaxed"),
                    html.Span(
                        dim["number"],
                        className="absolute bottom-2 right-3 text-7xl font-black leading-none select-none pointer-events-none origin-bottom-right transition-transform duration-500 ease-out group-hover:scale-150",
                        style={"color": "rgba(255,255,255,0.04)"},
                    ),
                ],
            )
        )
    return html.Div(cards, className="grid grid-cols-2 lg:grid-cols-4 gap-4")


# ──────────────────────────────────────────────────────────────────────────
# DimensionCarousel.tsx  (InfraGov 2.0 — 16 dimensions horizontal scroller)
# ──────────────────────────────────────────────────────────────────────────

def DimensionCarousel():
    legend = html.Div(
        className="flex items-center gap-4 mb-5 flex-wrap",
        children=[
            html.Div(
                className="flex items-center gap-2",
                children=[
                    html.Span(className="inline-block w-3 h-3 rounded-sm flex-shrink-0", style={"backgroundColor": a["color"]}),
                    html.Span(f'{a["badge"]}: {a["label"]}', className="text-xs text-muted font-medium"),
                ],
            )
            for a in CAROUSEL_AREAS
        ],
    )

    track_children = []
    for area in CAROUSEL_AREAS:
        track_children.append(
            html.Div(
                className="flex-shrink-0 w-16 rounded flex flex-col items-center justify-center gap-3 p-3",
                style={"backgroundColor": area["color"], "minHeight": "300px"},
                children=[
                    html.Span(area["badge"], className="text-[9px] font-bold tracking-widest uppercase text-white/60 leading-tight text-center",
                              style={"writingMode": "vertical-rl", "transform": "rotate(180deg)"}),
                    html.Div(className="w-px flex-1", style={"backgroundColor": "rgba(255,255,255,0.2)"}),
                    html.Span(area["label"], className="text-[9px] font-bold tracking-widest uppercase text-white/60 leading-tight text-center",
                              style={"writingMode": "vertical-rl", "transform": "rotate(180deg)"}),
                ],
            )
        )
        for dim in [d for d in CAROUSEL_DIMENSIONS if d["area"] == area["id"]]:
            track_children.append(
                html.Div(
                    className="group flex-shrink-0 w-72 relative bg-surface border border-white/5 rounded overflow-hidden flex flex-col hover:bg-surface-2 transition-colors",
                    style={"minHeight": "300px"},
                    children=[
                        html.Div(className="h-[3px] flex-shrink-0", style={"backgroundColor": area["color"]}),
                        html.Div(
                            className="flex flex-col flex-1 p-6",
                            children=[
                                html.Span(dim["num"], className="text-xs font-bold tracking-widest mb-4", style={"color": area["color"]}),
                                html.H3(dim["title"], className="text-base font-bold text-text leading-snug mb-3"),
                                html.P(dim["desc"], className="text-sm text-muted leading-relaxed"),
                                html.Div(
                                    html.Span(area["badge"], className="text-[10px] font-semibold uppercase tracking-widest rounded-full px-2.5 py-1",
                                              style={"color": area["color"], "backgroundColor": area["color"] + "18"}),
                                    className="mt-auto pt-6",
                                ),
                            ],
                        ),
                        html.Span(dim["num"],
                                  className="absolute bottom-2 right-3 text-7xl font-black leading-none select-none pointer-events-none origin-bottom-right transition-transform duration-500 ease-out group-hover:scale-150",
                                  style={"color": "rgba(255,255,255,0.04)"}),
                    ],
                )
            )

    return html.Div(
        className="relative",
        children=[
            legend,
            html.Div(id="carousel-fade-left", className="absolute left-0 top-0 bottom-0 w-16 z-10 pointer-events-none transition-opacity duration-200 opacity-0",
                     style={"background": "linear-gradient(to right, #0A0E1A, transparent)"}),
            html.Div(id="carousel-fade-right", className="absolute right-0 top-0 bottom-0 w-16 z-10 pointer-events-none transition-opacity duration-200 opacity-100",
                     style={"background": "linear-gradient(to left, #0A0E1A, transparent)"}),
            html.Button(
                Icon("chevron_left", size=20, color="#E6EAF2"),
                id="carousel-prev-btn",
                n_clicks=0,
                className="absolute left-2 top-1/2 -translate-y-1/2 z-20 w-9 h-9 rounded-full bg-surface border border-white/10 flex items-center justify-center text-text hover:bg-surface-2 transition-all shadow-lg",
                **{"aria-label": "Scroll left"},
            ),
            html.Button(
                Icon("chevron_right", size=20, color="#E6EAF2"),
                id="carousel-next-btn",
                n_clicks=0,
                className="absolute right-2 top-1/2 -translate-y-1/2 z-20 w-9 h-9 rounded-full bg-surface border border-white/10 flex items-center justify-center text-text hover:bg-surface-2 transition-all shadow-lg",
                **{"aria-label": "Scroll right"},
            ),
            html.Div(
                track_children,
                id="dimension-carousel-track",
                className="flex gap-3 overflow-x-auto pb-2 no-scrollbar",
                style={"cursor": "grab"},
            ),
        ],
    )


# ──────────────────────────────────────────────────────────────────────────
# MaturityLadder.tsx
# ──────────────────────────────────────────────────────────────────────────

def MaturityLadder():
    items = []
    n = len(MATURITY_LEVELS)
    for i, level in enumerate(MATURITY_LEVELS):
        card = html.Div(
            className="flex-1 reveal-on-scroll",
            style={"transitionDelay": f"{i * 120}ms"},
            children=html.Div(
                className="relative rounded overflow-hidden p-6 h-full",
                style={"backgroundColor": level["color"]},
                children=[
                    html.Div(html.Span(level["num"], className="text-xs font-bold tracking-widest text-white/60"),
                              className="flex items-baseline gap-2 mb-3"),
                    html.H4(level["label"], className="text-base font-bold mb-2 text-white"),
                    html.P(level["desc"], className="text-sm text-white/80 leading-relaxed"),
                ],
            ),
        )
        row = [card]
        if i < n - 1:
            row.append(
                html.Div(
                    className="flex-shrink-0 flex items-center text-gray-300 px-1",
                    children=[
                        html.Div(className="w-6 h-px bg-gray-300"),
                        Icon("chevron_right", size=14, color="#D1D5DB"),
                    ],
                )
            )
        items.append(html.Div(row, className="flex items-center flex-1"))
    return html.Div(items, className="flex items-stretch")


# ──────────────────────────────────────────────────────────────────────────
# ToolList.tsx  (Digital Tools page — grouped list rows + slide-over drawer)
# ──────────────────────────────────────────────────────────────────────────

def _render_inline_bold(text):
    """Very small **bold** markdown renderer used inside tool descriptions."""
    parts = text.split("**")
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append(html.Strong(part, className="font-semibold text-gray-700"))
        else:
            out.append(part)
    return out


def render_tool_description_blocks(description):
    """Mirrors ToolList.tsx's block/bullet parsing of the description field."""
    blocks = []
    for i, block in enumerate(description.split("\n\n")):
        lines = block.split("\n")
        bullet_lines = [l for l in lines if l.startswith("- ")]
        label_line = next((l for l in lines if not l.startswith("- ")), None)
        if bullet_lines:
            content = []
            if label_line:
                content.append(html.P(label_line, className="text-sm font-semibold text-gray-700 mb-2"))
            content.append(
                html.Ul([
                    html.Li(
                        [html.Span("\u2022", className="text-accent1 flex-shrink-0 mt-0.5"),
                         html.Span(_render_inline_bold(item[2:]))],
                        className="flex gap-2 text-sm text-gray-500 leading-relaxed",
                    )
                    for item in bullet_lines
                ], className="space-y-1.5")
            )
            blocks.append(html.Div(content, key=str(i)))
        else:
            blocks.append(html.P(_render_inline_bold(block), className="text-sm text-gray-500 leading-relaxed", key=str(i)))
    return blocks


def ToolListSection(families, tools):
    sections = []
    for family in families:
        family_tools = [t for t in tools if t["family"] == family["id"]]
        rows = []
        for tool in family_tools:
            icon_el = (
                html.Img(src=asset(tool["icon"]), alt="", className="w-14 h-14 object-contain")
                if tool.get("icon") else
                html.Div(html.Span(tool.get("acronym", ""), className="text-accent1 text-sm font-bold"),
                          className="w-14 h-14 rounded-xl bg-accent1/10 flex items-center justify-center")
            )
            rows.append(
                html.Button(
                    className="w-full flex items-center gap-5 py-4 px-5 text-left border-b border-gray-200 hover:bg-gray-50 transition-colors group",
                    id={"type": "tool-row-btn", "index": tool["id"]},
                    n_clicks=0,
                    children=[
                        html.Div(icon_el, className="flex-shrink-0 w-14 h-14 flex items-center justify-center"),
                        html.Div([
                            html.P(tool["name"], className="text-base font-semibold text-gray-900 leading-snug"),
                            html.P(tool.get("summary") or tool["description"], className="text-sm text-gray-500 mt-0.5 truncate"),
                        ], className="flex-1 min-w-0"),
                        html.Div(
                            [html.Span("More details", className="text-xs font-medium"),
                             Icon("chevron_right", size=20, color="#9CA3AF")],
                            className="flex-shrink-0 flex items-center gap-1 text-gray-400 group-hover:text-accent1 transition-colors",
                        ),
                    ],
                )
            )
        sections.append(
            html.Div(
                id=family["id"],
                children=[
                    html.Div([
                        html.H2(family["label"], className="text-2xl font-bold text-gray-900"),
                        html.Span(f'{len(family_tools)} tool{"s" if len(family_tools) != 1 else ""}',
                                  className="text-sm text-gray-400 mb-0.5"),
                    ], className="flex items-end gap-4 mb-2"),
                    html.P(family["description"], className="text-gray-500 text-sm mb-4"),
                    html.Div(rows),
                ],
            )
        )
    return html.Div(sections, className="space-y-16")


def ToolDrawerContent(tool):
    """Content shown inside the slide-over drawer for a given tool dict.
    Always returns a single Component (never a bare list) since this is
    used directly as a scalar callback Output's `children` value.

    Note: the drawer's close ("X") button is intentionally NOT built here.
    It lives once, statically, in app.py's app.layout instead — see the
    comment there for why (rebuilding it on every open caused a real bug:
    Dash fires a callback once when its Input component is newly inserted
    into the layout, so a close button freshly created here would
    immediately "phantom click" itself shut the instant the drawer opened)."""
    if tool is None:
        return html.Div()
    buttons = []
    if tool.get("videoId"):
        buttons.append(
            html.Button(
                [Icon("play", size=18, color=COLORS["accent1"]), " Watch Video"],
                id="tool-drawer-watch-btn",
                n_clicks=0,
                className="inline-flex items-center justify-center gap-2 w-full px-6 py-3.5 rounded border border-accent1 text-accent1 text-base font-semibold hover:bg-accent1/5 transition-colors",
            )
        )
    buttons.append(
        html.A(
            ["Launch Tool", Icon("external_link", size=18, color="#FFFFFF")],
            href=tool["href"], target="_blank", rel="noopener noreferrer",
            className="inline-flex items-center justify-center gap-2 w-full px-6 py-3.5 rounded bg-accent1 text-white text-base font-semibold hover:bg-accent1/90 transition-colors",
        )
    )
    return html.Div(
        className="flex flex-col h-full",
        children=[
            html.Div(
                html.Img(src=asset(tool["screenshot"]), alt=f"{tool['name']} screenshot",
                         className="w-full h-full object-cover object-top"),
                className="relative w-full aspect-[40/19] bg-gray-100 flex-shrink-0 overflow-hidden",
            ),
            html.Div(
                className="flex flex-col flex-1 overflow-y-auto p-6",
                children=[
                    html.Div([
                        html.Span(tool.get("acronym", ""), className="inline-block text-xs font-bold text-accent1 tracking-wider uppercase mb-1") if tool.get("acronym") else None,
                        html.H2(tool["name"], className="text-2xl font-bold text-gray-900 leading-snug pr-8"),
                    ], className="mb-4"),
                    html.Div(render_tool_description_blocks(tool["description"]), className="space-y-4"),
                    html.Div(buttons, className="mt-auto pt-8 flex flex-col gap-3"),
                ],
            ),
        ],
    )


def vimeo_embed_url(video_id_field, autoplay=True):
    """Replicates the id/hash splitting logic from ToolList.tsx / VideoCard.tsx."""
    parts = video_id_field.split("/")
    vid = parts[0]
    vhash = parts[1] if len(parts) > 1 else None
    params = "autoplay=1&title=0&byline=0&portrait=0&badge=0" if autoplay else "title=0&byline=0&portrait=0&badge=0"
    if vhash:
        params += f"&h={vhash}"
    return f"https://player.vimeo.com/video/{vid}?{params}"


# ──────────────────────────────────────────────────────────────────────────
# BlogCard.tsx
# ──────────────────────────────────────────────────────────────────────────

def format_date_long(iso_date, fmt="en-GB-day-month-short"):
    d = datetime.strptime(iso_date, "%Y-%m-%d")
    return f'{d.day} {d.strftime("%b")} {d.year}'


def BlogCard(post):
    tag_el = None
    if post.get("tag"):
        tag_el = html.Span(post["tag"], className="inline-block text-xs font-semibold uppercase tracking-wider text-accent2 bg-accent2/10 px-2.5 py-1 rounded-full w-fit")
    return dcc.Link(
        [
            tag_el,
            html.H3(post["title"], className="text-base font-semibold text-text leading-snug group-hover:text-accent3 transition-colors duration-200"),
            html.P(post["excerpt"], className="text-sm text-muted leading-relaxed line-clamp-3"),
            html.Div([
                html.Span(format_date_long(post["date"]), className="text-xs text-muted"),
                html.Span(["Read more ", IconArrow(size=12, color=COLORS["accent2"])], className="text-xs text-accent2 flex items-center gap-1 group-hover:gap-2 transition-all"),
            ], className="flex items-center justify-between mt-auto pt-2 border-t border-white/5"),
        ],
        href=f'/?page=blogs&slug={post["slug"]}',
        className="gradient-border rounded bg-surface p-6 flex flex-col gap-3 hover:bg-surface-2 transition-colors group",
    )


# ──────────────────────────────────────────────────────────────────────────
# VideoCard.tsx  (Digital Academy)
# ──────────────────────────────────────────────────────────────────────────

def VideoCard(title, vimeo_id, thumbnail_url=None):
    if thumbnail_url:
        overlay_bg = html.Img(src=thumbnail_url, alt="", className="w-full h-full object-cover")
    else:
        overlay_bg = None
    play_button = html.Button(
        [
            overlay_bg,
            html.Div(
                html.Div(Icon("play_triangle", size=28, color="#111111"), className="w-20 h-20 rounded-full bg-white shadow-xl flex items-center justify-center pl-1 group-hover:scale-110 transition-all duration-200"),
                className="absolute inset-0 flex items-center justify-center bg-black/10 group-hover:bg-black/20 transition-colors duration-200",
            ),
        ],
        id={"type": "video-play-btn", "index": vimeo_id},
        n_clicks=0,
        className="absolute inset-0 w-full h-full group",
        **{"aria-label": f"Play {title}"},
    )
    return html.Div([
        html.H3(title, className="text-base font-semibold text-gray-900 mb-3"),
        html.Div(
            play_button,
            id={"type": "video-container", "index": vimeo_id},
            className="aspect-video w-full rounded overflow-hidden bg-gray-900 border border-gray-200 relative",
        ),
    ])


def VideoIframe(vimeo_id, title=""):
    return html.Iframe(
        src=f"https://player.vimeo.com/video/{vimeo_id}?autoplay=1&title=0&byline=0&portrait=0&badge=0&sidedock=0",
        className="absolute inset-0 w-full h-full",
        style={"width": "100%", "height": "100%", "border": "0"},
        allow="autoplay; fullscreen; picture-in-picture",
        title=title,
    )


# ──────────────────────────────────────────────────────────────────────────
# FeedbackForm.tsx
# ──────────────────────────────────────────────────────────────────────────

_INPUT_CLASS = ("w-full px-3 py-2 rounded border text-gray-900 text-base "
                "placeholder:text-gray-400 focus:outline-none focus:border-accent1 "
                "focus:ring-1 focus:ring-accent1 transition-colors box-border")
_LABEL_CLASS = "text-sm font-semibold text-gray-700"


def FeedbackFormFields(values=None, errors=None, submitting=False):
    """Builds the <form> body. `values` pre-fills fields after a failed
    submit; `errors` is a set of field names ('name','email','feedback') to
    highlight in red, mirroring the `required` HTML validation in the
    original React form.

    Each label+input pair is wrapped in an explicit `flex flex-col gap-1.5`
    container (rather than relying on default block stacking + a margin on
    the label) so spacing is correct regardless of any default styling
    `dcc.Input`/`dcc.Textarea` ship with."""
    values = values or {}
    errors = errors or set()

    def field_class(name):
        base = _INPUT_CLASS
        border = "border-red-400" if name in errors else "border-gray-200"
        return f"{base} {border}"

    def error_note(name):
        if name in errors:
            return html.P("This field is required.", className="text-xs text-red-500")
        return None

    return [
        html.Div(
            className="grid grid-cols-1 sm:grid-cols-2 gap-6",
            children=[
                html.Div(
                    className="flex flex-col gap-1.5",
                    children=[
                        html.Label("Name", htmlFor="fb-name", className=_LABEL_CLASS),
                        dcc.Input(id="fb-name", type="text", placeholder="Your full name",
                                  value=values.get("name", ""), className=field_class("name"),
                                  style={"width": "100%", "margin": 0}),
                        error_note("name"),
                    ],
                ),
                html.Div(
                    className="flex flex-col gap-1.5",
                    children=[
                        html.Label("Email", htmlFor="fb-email", className=_LABEL_CLASS),
                        dcc.Input(id="fb-email", type="email", placeholder="you@example.com",
                                  value=values.get("email", ""), className=field_class("email"),
                                  style={"width": "100%", "margin": 0}),
                        error_note("email"),
                    ],
                ),
            ],
        ),
        html.Div(
            className="flex flex-col gap-1.5",
            children=[
                html.Label("Organization", htmlFor="fb-org", className=_LABEL_CLASS),
                dcc.Input(id="fb-org", type="text", placeholder="Your organization or institution",
                          value=values.get("organization", ""), className=_INPUT_CLASS,
                          style={"width": "100%", "margin": 0}),
            ],
        ),
        html.Div(
            className="flex flex-col gap-1.5",
            children=[
                html.Label("Feedback", htmlFor="fb-feedback", className=_LABEL_CLASS),
                dcc.Textarea(id="fb-feedback", placeholder="Share your thoughts, suggestions, or questions about PIM-PAM tools...",
                             value=values.get("feedback", ""), className=field_class("feedback") + " resize-none",
                             style={"width": "100%", "margin": 0}, rows=6),
                error_note("feedback"),
            ],
        ),
        html.Button(
            ["Sending\u2026" if submitting else "Submit Feedback",
             None if submitting else IconArrow(size=18, color="#FFFFFF")],
            id="fb-submit-btn", n_clicks=0, disabled=submitting,
            className="inline-flex items-center gap-2 px-7 py-3.5 rounded bg-accent1 text-white font-semibold text-base hover:bg-accent1/90 transition-colors disabled:opacity-60 self-start",
        ),
    ]


def FeedbackThankYou():
    return html.Div(
        className="text-center py-16",
        children=[
            html.Div(Icon("checkmark", size=28, color=COLORS["accent1"]),
                     className="w-14 h-14 rounded-full bg-accent1/10 flex items-center justify-center mx-auto mb-5"),
            html.H2("Thank you for your feedback!", className="text-2xl font-bold text-gray-900 mb-3"),
            html.P("We appreciate you taking the time to share your thoughts. We'll review your feedback carefully.",
                   className="text-gray-500 text-base"),
        ],
    )


# ──────────────────────────────────────────────────────────────────────────
# app/resources/page.tsx — document download card
# ──────────────────────────────────────────────────────────────────────────

def ResourceCard(doc):
    filename = os.path.basename(doc["href"])
    return html.Div(
        className="flex flex-col gap-5 p-7 rounded border border-gray-200 bg-white hover:border-accent1/30 transition-colors",
        children=[
            html.Div(Icon("pdf", size=24, color=COLORS["accent1"]),
                     className="w-12 h-12 rounded bg-accent1/10 flex items-center justify-center flex-shrink-0"),
            html.Div([
                html.H2(doc["title"], className="text-lg font-bold text-gray-900 mb-1.5"),
                html.P(doc["description"], className="text-base text-gray-500 leading-relaxed"),
            ], className="flex-1"),
            html.A(
                ["Download PDF", Icon("download", size=18, color="#FFFFFF")],
                href=asset(doc["href"]), download=filename,
                className="inline-flex items-center gap-2 px-6 py-3 rounded bg-accent1 text-white text-base font-semibold hover:bg-accent1/90 transition-colors self-start",
            ),
        ],
    )


# ──────────────────────────────────────────────────────────────────────────
# app/page.tsx — "Three areas of digital innovation" cards
# ──────────────────────────────────────────────────────────────────────────

def ToolAreaCard(area):
    return html.Div(
        className="relative bg-white border border-gray-200 rounded overflow-hidden flex flex-col p-6 min-h-[220px]",
        children=[
            Icon(area["icon"], size=40, color=COLORS["accent1"]),
            html.H3(area["title"], className="text-xl font-bold text-accent1 mb-2 leading-snug mt-[100px]"),
            html.P(area["description"], className="text-base leading-relaxed text-gray-500"),
        ],
    )


# ──────────────────────────────────────────────────────────────────────────
# app/page.tsx — "Brought to you by" and "Supported By" logo strips
# ──────────────────────────────────────────────────────────────────────────

def BroughtToYouByStrip(logos):
    return html.Div(
        className="flex items-center justify-center gap-8",
        children=[
            html.Span("Brought to you by:", className="text-xs font-semibold uppercase tracking-widest text-gray-400 whitespace-nowrap"),
        ] + [
            html.Img(src=asset(logo["src"]), alt=logo["alt"], className="h-24 w-auto object-contain")
            for logo in logos
        ],
    )


def SupportedByCarousel(logos):
    def _pass(prefix):
        return [
            html.Div(
                html.Img(src=asset(logo["src"]), alt=logo["alt"], className="h-16 w-auto object-contain"),
                className="mx-8 flex-shrink-0 flex items-center justify-center",
                key=f"{prefix}-{i}",
            )
            for i, logo in enumerate(logos)
        ]

    return html.Div(
        className="overflow-hidden",
        style={
            "maskImage": "linear-gradient(to right, transparent 0%, black 15%, black 85%, transparent 100%)",
            "WebkitMaskImage": "linear-gradient(to right, transparent 0%, black 15%, black 85%, transparent 100%)",
        },
        children=html.Div(_pass("p0") + _pass("p1"), className="flex items-center animate-scroll-logos", style={"width": "max-content"}),
    )