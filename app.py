"""
app.py
======
Main structure, routing, and callbacks for the PIM-PAM Dash replica of
https://pim-pam.net/.

Run with:
    python app.py
Then open http://127.0.0.1:8050
"""

import logging
import os
import time
import urllib.parse
from functools import lru_cache

import requests
from dash import Dash, html, dcc, Input, Output, State, ALL, MATCH, ctx, no_update

import constants as C
import utils
from utils import (
    register_app, asset, Icon, IconArrow, GridOverlay, SectionHeading, NavBar,
    Footer, PimPamAiBanner, DimensionGrid, DimensionCarousel, MaturityLadder,
    ToolListSection, ToolDrawerContent, vimeo_embed_url, BlogCard,
    format_date_long, VideoCard, VideoIframe, FeedbackFormFields,
    FeedbackThankYou, ResourceCard, ToolAreaCard, BroughtToYouByStrip,
    SupportedByCarousel,
)

# ──────────────────────────────────────────────────────────────────────────
# LOGGING
#   A plain stdlib logging setup (no extra dependencies). Level is
#   controllable via the PIMPAM_LOG_LEVEL env var (INFO by default; set to
#   DEBUG for verbose per-callback tracing). Every route change and every
#   data-driven callback (tool drawer, video lightbox, academy video embeds,
#   feedback submission) logs a line, plus warnings for anything unexpected
#   (unknown tool ids, missing blog slugs, failed thumbnail fetches, invalid
#   feedback submissions).
# ──────────────────────────────────────────────────────────────────────────
LOG_LEVEL = os.environ.get("PIMPAM_LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("pimpam.app")
logger.info("Logging initialized at level %s", LOG_LEVEL)

# ──────────────────────────────────────────────────────────────────────────
# APP INSTANTIATION
# ──────────────────────────────────────────────────────────────────────────
app = Dash(
    __name__,
    title=C.SITE_TITLE_DEFAULT,
    update_title=None,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
register_app(app)  # lets utils.py resolve get_asset_url()
logger.info("Dash app '%s' created; asset resolver registered.", C.SITE_TITLE_DEFAULT)

# ──────────────────────────────────────────────────────────────────────────
# CUSTOM INDEX STRING
#   - Google Fonts (Fira Sans / Inter) — same @import as the original
#     app/globals.css
#   - Tailwind CDN (Play CDN) configured with the exact design tokens from
#     tailwind.config.ts, so every component below can reuse the original
#     React components' className strings verbatim.
#   - A small vanilla-JS layer that reproduces the purely cosmetic
#     client-side behaviors the original React components handled with
#     hooks (useState/useEffect/IntersectionObserver): nav scroll shadow,
#     mobile menu toggle, dimension-carousel autoplay/drag, scroll-reveal
#     fade-up, and smooth-scroll to `#hash` anchors. All data-driven
#     interactivity (routing, tool drawer, video embeds, the feedback form)
#     is handled by real Dash callbacks further down this file.
# ──────────────────────────────────────────────────────────────────────────
app.index_string = f"""<!DOCTYPE html>
<html lang="en">
<head>
    {{%metas%}}
    <title>{{%title%}}</title>
    <link rel="icon" type="image/x-icon" href="{app.get_asset_url('pimpam.ico')}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="{C.GOOGLE_FONTS_URL}" rel="stylesheet">
    {{%css%}}
</head>
<body class="bg-bg text-text antialiased">
    {{%app_entry%}}
    <footer>
        {{%config%}}
        {{%scripts%}}
        {{%renderer%}}
    </footer>
    <script>
    (function () {{
        function initNavScroll() {{
            var nav = document.getElementById('site-nav');
            if (!nav || nav.__navInit) return;
            nav.__navInit = true;
            function onScroll() {{
                if (window.scrollY > 16) {{ nav.classList.add('nav-scrolled'); }}
                else {{ nav.classList.remove('nav-scrolled'); }}
            }}
            window.addEventListener('scroll', onScroll, {{ passive: true }});
            onScroll();
        }}

        function initMobileNav() {{
            var btn = document.getElementById('nav-mobile-btn');
            var menu = document.getElementById('nav-mobile-menu');
            var iconMenu = document.getElementById('nav-icon-menu');
            var iconClose = document.getElementById('nav-icon-close');
            if (!btn || !menu || btn.__init) return;
            btn.__init = true;
            function closeMenu() {{
                menu.classList.add('hidden');
                if (iconMenu) iconMenu.classList.remove('hidden');
                if (iconClose) iconClose.classList.add('hidden');
                btn.setAttribute('aria-label', 'Open menu');
            }}
            function openMenu() {{
                menu.classList.remove('hidden');
                if (iconMenu) iconMenu.classList.add('hidden');
                if (iconClose) iconClose.classList.remove('hidden');
                btn.setAttribute('aria-label', 'Close menu');
            }}
            btn.addEventListener('click', function () {{
                if (menu.classList.contains('hidden')) openMenu(); else closeMenu();
            }});
            menu.querySelectorAll('a').forEach(function (a) {{
                a.addEventListener('click', closeMenu);
            }});
        }}

        function initCarousel() {{
            var track = document.getElementById('dimension-carousel-track');
            if (!track || track.__init) return;
            track.__init = true;
            var isDragging = false, isHovered = false, userTookControl = false;
            var dragStartX = 0, dragScrollLeft = 0;

            function step() {{
                if (!isHovered && !isDragging && !userTookControl) {{ track.scrollLeft += 0.8; }}
                requestAnimationFrame(step);
            }}
            requestAnimationFrame(step);

            track.addEventListener('mouseenter', function () {{ isHovered = true; }});
            track.addEventListener('mouseleave', function () {{ isHovered = false; stopDrag(); }});
            track.addEventListener('mousedown', function (e) {{
                isDragging = true;
                dragStartX = e.pageX - track.offsetLeft;
                dragScrollLeft = track.scrollLeft;
                track.classList.add('dragging');
            }});
            track.addEventListener('mousemove', function (e) {{
                if (!isDragging) return;
                e.preventDefault();
                var x = e.pageX - track.offsetLeft;
                track.scrollLeft = dragScrollLeft - (x - dragStartX);
            }});
            function stopDrag() {{ isDragging = false; track.classList.remove('dragging'); }}
            track.addEventListener('mouseup', stopDrag);

            function updateFades() {{
                var left = document.getElementById('carousel-fade-left');
                var right = document.getElementById('carousel-fade-right');
                if (left) left.style.opacity = track.scrollLeft > 4 ? '1' : '0';
                if (right) right.style.opacity = (track.scrollLeft < track.scrollWidth - track.clientWidth - 4) ? '1' : '0';
            }}
            track.addEventListener('scroll', updateFades, {{ passive: true }});
            updateFades();

            var prev = document.getElementById('carousel-prev-btn');
            var next = document.getElementById('carousel-next-btn');
            if (prev) prev.addEventListener('click', function () {{
                userTookControl = true;
                track.scrollBy({{ left: -{C.CARD_SCROLL_STEP}, behavior: 'smooth' }});
            }});
            if (next) next.addEventListener('click', function () {{
                userTookControl = true;
                track.scrollBy({{ left: {C.CARD_SCROLL_STEP}, behavior: 'smooth' }});
            }});
        }}

        function initRevealOnScroll() {{
            var els = document.querySelectorAll('.reveal-on-scroll:not(.observed)');
            if (!els.length) return;
            var observer = new IntersectionObserver(function (entries) {{
                entries.forEach(function (entry) {{
                    if (entry.isIntersecting) entry.target.classList.add('is-visible');
                }});
            }}, {{ threshold: 0.1, rootMargin: '0px 0px -40px 0px' }});
            els.forEach(function (el) {{ el.classList.add('observed'); observer.observe(el); }});
        }}

        function initAll() {{
            initNavScroll();
            initMobileNav();
            initCarousel();
            initRevealOnScroll();
        }}

        function scrollToHash() {{
            if (window.location.hash) {{
                setTimeout(function () {{
                    var el = document.querySelector(window.location.hash);
                    if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}, 300);
            }}
        }}

        document.addEventListener('DOMContentLoaded', function () {{
            initAll();
            scrollToHash();
            var target = document.getElementById('react-entry-point') || document.body;
            var mo = new MutationObserver(function () {{ initAll(); }});
            mo.observe(target, {{ childList: true, subtree: true }});
            window.addEventListener('hashchange', scrollToHash);
        }});
    }})();
    </script>
</body>
</html>"""


# ──────────────────────────────────────────────────────────────────────────
# PAGE LAYOUTS  (one function ~ one app/**/page.tsx)
# ──────────────────────────────────────────────────────────────────────────

def _hero_section(section_id, gradient, eyebrow, heading, subheading, extra_top_pad="pt-44"):
    """Shared dark hero block used by every inner page (matches the
    `style={{ background: 'radial-gradient(...), #0A0E1A' }}` pattern
    repeated across app/**/page.tsx)."""
    return html.Section(
        id=section_id,
        className=f"{extra_top_pad} pb-10 relative overflow-hidden",
        style={"background": f"{gradient}, #0A0E1A"},
        children=[
            GridOverlay(),
            html.Div(
                SectionHeading(eyebrow=eyebrow, heading=heading, subheading=subheading),
                className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            ),
        ],
    )


def home_page():
    return html.Div([
        # ── Hero ──────────────────────────────────────────────────────
        html.Section(
            id="top",
            className="relative flex items-center pt-16 overflow-hidden",
            style={"background": (
                "radial-gradient(ellipse 100% 80% at 50% -5%, rgba(67,69,170,0.28) 0%, transparent 65%), "
                "radial-gradient(ellipse 60% 40% at 80% 20%, rgba(100,203,214,0.12) 0%, transparent 60%), #0A0E1A"
            )},
            children=[
                GridOverlay(),
                html.Div(
                    className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28 w-full",
                    children=html.Div(
                        className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center",
                        children=[
                            html.Div([
                                html.H1("Public Infrastructure Investment & Asset Governance",
                                        className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white leading-[1.1] mb-6",
                                        style={"letterSpacing": "0"}),
                                html.P("Digital tools for smarter public investment and asset management built around the 16 dimensions of InfraGov 2.0.",
                                       className="text-lg sm:text-xl text-muted leading-relaxed mb-10"),
                                html.Div(
                                    className="flex flex-col sm:flex-row gap-4",
                                    children=[
                                        dcc.Link(
                                            ["View Digital Tools", IconArrow(size=18, color="#FFFFFF")],
                                            href="?page=digital-tools",
                                            className="inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded bg-accent1 text-white font-semibold text-base hover:bg-accent1/90 transition-colors",
                                        ),
                                        dcc.Link(
                                            ["InfraGov 2.0 Info",
                                             html.Span("New", className="bg-accent4 text-white text-xs font-bold px-1.5 py-0.5 rounded leading-none")],
                                            href="?page=infragov",
                                            className="inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded border border-white/10 bg-surface text-white font-semibold text-base hover:bg-surface-2 transition-colors",
                                        ),
                                    ],
                                ),
                            ]),
                            html.Div(
                                className="relative flex items-center justify-center lg:justify-end",
                                children=html.Div(
                                    html.Img(src=asset("PIM-PAM-Hero.png"), alt="PIM-PAM digital tools platform",
                                             className="w-full h-auto object-contain drop-shadow-2xl"),
                                    className="relative w-full max-w-lg lg:max-w-none",
                                ),
                            ),
                        ],
                    ),
                ),
                html.Div(className="absolute bottom-0 left-0 right-0 h-40 bg-gradient-to-t from-bg to-transparent"),
            ],
        ),

        # ── Brought to you by ────────────────────────────────────────
        html.Section(
            className="py-8 bg-white border-y border-gray-100",
            children=html.Div(BroughtToYouByStrip(C.BROUGHT_TO_YOU_BY), className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8"),
        ),

        # ── Why PIM-PAM ───────────────────────────────────────────────
        html.Section(
            className="pt-14 lg:pt-20 pb-8 lg:pb-12 bg-white",
            children=html.Div(
                className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                children=html.Div(
                    className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center",
                    children=[
                        html.Div(
                            html.Img(src=asset("pim-pam-why.png"), alt="Why PIM-PAM \u2014 digitalization in public infrastructure",
                                     className="w-full h-auto object-contain rounded"),
                            className="relative",
                        ),
                        html.Div([
                            SectionHeading(eyebrow="Why PIM-PAM?", heading="Digitalization is transforming public infrastructure", light=True),
                            html.Div([
                                html.P("Digitalization can transform public infrastructure investment and asset management by enabling smarter investment decisions and leveraging relevant, real-time data to improve service delivery and fiscal sustainability across infrastructure, property, and land owned and operated by national and subnational governments, as well as state-owned enterprises.",
                                       className="text-base text-gray-500 leading-relaxed"),
                                html.P("With digital tools such as Geographic Information Systems (GIS), Earth Observation (EO) satellite data, Internet of Things (IoT) sensors, and a range of Artificial Intelligence (AI) analytics, governments can optimize asset lifecycles, reduce costs, and strengthen service delivery. In the context of InfraGov 2.0, these capabilities also support better transparency, data-driven strategic planning, and more resilient investment decisions across the 16 dimensions of infrastructure governance and asset management, especially where land, property, and infrastructure are exposed to climate, environmental, and urban development pressures.",
                                       className="text-base text-gray-500 leading-relaxed"),
                            ], className="mt-6 space-y-5"),
                            html.Div(
                                dcc.Link(["Explore Tools ", IconArrow(size=18, color=C.COLORS["accent1"])], href="?page=digital-tools",
                                         className="inline-flex items-center gap-2 px-6 py-3 rounded border border-accent1 text-accent1 text-base font-semibold hover:bg-accent1 hover:text-white transition-colors"),
                                className="mt-8",
                            ),
                        ]),
                    ],
                ),
            ),
        ),

        # ── What We Do ────────────────────────────────────────────────
        html.Section(
            className="pt-14 lg:pt-20 pb-14 lg:pb-20 bg-white border-t border-gray-100",
            children=html.Div(
                className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                children=html.Div(
                    className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center",
                    children=[
                        html.Div([
                            SectionHeading(eyebrow="What is PIM-PAM?", heading="Digital tools for smarter public investment and asset management", light=True),
                            html.Div([
                                html.P("The use of digital technologies is both a catalyst and a test of effective public infrastructure and asset management. Tools such as big data analytics, data visualization, and AI can improve planning, monitoring, and maintenance while also signaling a government's commitment to evidence-based decision-making, transparency, and long-term value creation. When these tools are adopted, they demonstrate institutional readiness to modernize and strengthen the performance of public investment flows and asset stocks, turning technology from a technical upgrade into a benchmark of good governance.",
                                       className="text-base text-gray-500 leading-relaxed"),
                                html.P("To better support client countries, the World Bank is developing end-user-friendly online tools that can quickly improve insights for smarter public investment and asset management across countries. These tools are designed to support a learning-by-doing journey, moving users from awareness to application and adoption across the public sector.",
                                       className="text-base text-gray-500 leading-relaxed"),
                            ], className="mt-6 space-y-5"),
                            html.Div(
                                dcc.Link(["Explore Tools ", IconArrow(size=18, color=C.COLORS["accent1"])], href="?page=digital-tools",
                                         className="inline-flex items-center gap-2 px-6 py-3 rounded border border-accent1 text-accent1 text-base font-semibold hover:bg-accent1 hover:text-white transition-colors"),
                                className="mt-8",
                            ),
                        ]),
                        html.Div(
                            html.Img(src=asset("about-pim-pam.png"), alt="About PIM-PAM", className="w-full h-auto object-contain rounded"),
                            className="relative",
                        ),
                    ],
                ),
            ),
        ),

        # ── Supported By carousel ─────────────────────────────────────
        html.Section(
            className="py-10 bg-white border-t border-gray-100",
            children=[
                html.P("Supported By", className="text-center text-xs font-semibold uppercase tracking-widest text-gray-400 mb-6"),
                html.Div(SupportedByCarousel(C.SUPPORTED_BY_LOGOS), className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8"),
            ],
        ),

        # ── 8 Dimensions ──────────────────────────────────────────────
        html.Section(
            className="py-14 lg:py-20",
            children=html.Div(
                className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                children=[
                    html.Div(
                        SectionHeading(
                            eyebrow="Framework", heading="8 Must-Have Dimensions for Project Delivery",
                            subheading="A comprehensive framework covering every stage of the public investment lifecycle \u2014 from policy guidance through to ex-post evaluation.",
                            centered=True, light_badge=True,
                        ),
                        className="text-center mb-12",
                    ),
                    DimensionGrid(),
                ],
            ),
        ),

        # ── Three Tool Areas ──────────────────────────────────────────
        html.Section(
            className="py-14 lg:py-20 bg-gray-50 border-t border-gray-100",
            children=html.Div(
                className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                children=[
                    html.Div([
                        html.P("Digital Tools", className="inline-block text-xs font-semibold uppercase tracking-widest text-accent1 bg-accent1/10 rounded-full px-3 py-1 mb-3"),
                        html.H2("Three areas of digital innovation", className="text-3xl sm:text-4xl font-bold leading-tight mb-4 text-gray-900"),
                        html.P("Each tool family targets a distinct dimension of the investment and asset management challenge.",
                               className="text-base sm:text-lg leading-relaxed max-w-2xl mx-auto text-gray-500"),
                    ], className="text-center mb-12"),
                    html.Div([ToolAreaCard(a) for a in C.TOOL_AREAS], className="grid grid-cols-1 md:grid-cols-3 gap-4"),
                    html.Div(
                        dcc.Link(["Explore Tools ", IconArrow(size=18, color="#FFFFFF")], href="?page=digital-tools",
                                 className="inline-flex items-center gap-2 px-7 py-3.5 rounded bg-accent1 text-white font-semibold text-base hover:bg-accent1/90 transition-colors"),
                        className="text-center mt-10",
                    ),
                ],
            ),
        ),
    ])


def digital_tools_page():
    hero = _hero_section(
        "digital-tools-hero",
        "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(67,69,170,0.2) 0%, transparent 65%)",
        "Digital Tools", "A full suite of tools for smarter governance",
        "Eight open-source platforms spanning data analytics, geospatial planning, and generative AI \u2014 built for government practitioners.",
    )
    return html.Div([
        hero,
        html.Section(
            className="pt-14 pb-24 bg-white",
            children=html.Div(ToolListSection(C.TOOL_FAMILIES, C.TOOLS), className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8"),
        ),
    ])


def infragov_page():
    hero = _hero_section(
        "infragov-hero",
        "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(55,179,127,0.18) 0%, transparent 65%)",
        "InfraGov 2.0 is here!", "Better infrastructure starts with better governance",
        "InfraGov 2.0 is the World Bank Group's framework for assessing how well a country manages public investment \u2014 across 16 dimensions and 119 indicators, module by module, from a project's first idea to its final review.",
    )

    what_section = html.Section(
        className="py-20 bg-white",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=html.Div(
                className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center",
                children=[
                    html.Div([
                        SectionHeading(eyebrow="Overview", heading="What is InfraGov 2.0?", light=True),
                        html.Div([
                            html.P("Public investment management \u2014 PIM for short \u2014 is how governments choose, deliver, and look after the infrastructure their citizens rely on: roads, schools, power, water. When it's done well, money goes further and projects deliver. When it's done poorly, costs spiral and benefits never arrive.",
                                   className="text-base text-gray-500 leading-relaxed"),
                            html.P("InfraGov 2.0 is a structured way to see where a country stands. It brings together the best of the tools that came before it \u2014 the World Bank's 8 Must-Haves and InfraGov 1.0, the IMF's PIMA, PEFA, and the OECD's infrastructure toolkit \u2014 into one modular, problem-driven framework. It assesses the maturity of a country's PIM system across 16 dimensions, scores each against clear benchmarks, and points the way toward practical reform.",
                                   className="text-base text-gray-500 leading-relaxed"),
                        ], className="mt-6 space-y-5"),
                    ]),
                    html.Div(html.Img(src=asset("pim-pam-why.png"), alt="InfraGov 2.0 framework", className="w-full h-auto object-contain rounded"), className="relative"),
                ],
            ),
        ),
    )

    why_bullets = html.Ul(
        [
            html.Li([
                html.Span("\u2022", className="text-accent1 flex-shrink-0 mt-1"),
                html.Span([html.Strong(bold, className="font-semibold text-gray-700"), f" \u2014 {rest}"]),
            ], className="flex gap-2 text-base text-gray-500 leading-relaxed")
            for bold, rest in C.INFRAGOV_WHY_LIST
        ],
        className="space-y-3",
    )
    why_section = html.Section(
        className="py-20 bg-gray-50 border-t border-gray-100",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=html.Div(
                className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center",
                children=[
                    html.Div(html.Img(src=asset("about-pim-pam.png"), alt="Why InfraGov 2.0 matters", className="w-full h-auto object-contain rounded"), className="relative"),
                    html.Div([
                        SectionHeading(eyebrow="WHY", heading="Why it matters", light=True),
                        html.Div([
                            html.P("Strong infrastructure governance is a fiscal and developmental imperative, not a technical nicety. Yet for years, assessment tools struggled with the same gaps: results that couldn't be compared across countries, advice that named problems without showing how to fix them, little evidence of real impact, and a scope that lagged behind new priorities like climate and decentralisation.",
                                   className="text-base text-gray-500 leading-relaxed"),
                            html.P("InfraGov 2.0 was built to close those gaps.", className="text-base text-gray-500 leading-relaxed"),
                            why_bullets,
                        ], className="mt-6 space-y-5"),
                    ]),
                ],
            ),
        ),
    )

    dims_section = html.Section(
        className="py-20",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=[
                html.Div([
                    SectionHeading(eyebrow="Framework", heading="16 dimensions, three thematic areas"),
                    html.P("The framework spans 16 dimensions, grouped into three areas. The first eight are the 8 Must-Haves \u2014 the essential, non-negotiable functions every well-run public investment system performs, following a project from its first idea to its final review. Three cross-cutting dimensions cover the foundations that hold the whole system together, and five optional special topics tackle today's fast-moving priorities. Countries apply whichever areas fit their needs.",
                           className="text-base text-muted leading-relaxed max-w-3xl mt-4"),
                ], className="mb-10"),
                DimensionCarousel(),
            ],
        ),
    )

    maturity_section = html.Section(
        className="py-20 bg-gray-50 border-t border-gray-100",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=[
                html.Div([
                    SectionHeading(eyebrow="Maturity Levels", heading="A maturity ladder, not a scoreboard", light=True),
                    html.P("Every dimension is benchmarked on the same four-point scale. It describes a journey of progress \u2014 where a country sits in a sequence of development stages \u2014 rather than a pass or fail.",
                           className="text-base text-gray-500 leading-relaxed mt-4 max-w-2xl"),
                ], className="mb-10"),
                MaturityLadder(),
            ],
        ),
    )

    dashboard_list = html.Ul(
        [html.Li([html.Span("\u2022", className="text-accent1 flex-shrink-0"), html.Span(item)],
                 className="flex items-center gap-2.5 text-base text-gray-500 leading-relaxed")
         for item in C.INFRAGOV_DASHBOARD_LIST],
        className="mt-5 space-y-2.5",
    )
    dashboard_section = html.Section(
        className="py-20 bg-white border-t border-gray-100",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=html.Div(
                className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center",
                children=[
                    html.Div(
                        html.Img(src=asset("screenshots/ig-dashboard.jpg"), alt="InfraGov Benchmarking Dashboard", className="w-full h-auto object-cover rounded"),
                        className="relative w-full rounded overflow-hidden border border-gray-200",
                    ),
                    html.Div([
                        SectionHeading(eyebrow="Put the framework to work", heading="The InfraGov Dashboard", light=True),
                        html.P("The InfraGov Benchmarking Dashboard lets country teams self-assess infrastructure governance against the InfraGov 2.0 framework, module by module and share validated results once review and quality control are complete.",
                               className="text-base text-gray-500 leading-relaxed mt-6"),
                        dashboard_list,
                        html.Div(html.Span("Coming Soon...", className="text-sm font-medium text-gray-400 italic"), className="mt-8"),
                    ]),
                ],
            ),
        ),
    )

    return html.Div([hero, what_section, why_section, dims_section, maturity_section, dashboard_section])


def digital_academy_page():
    hero = _hero_section(
        "academy-hero",
        "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(67,69,170,0.22) 0%, transparent 65%)",
        "Digital Academy", "Learning resources for better infrastructure governance",
        "Video guides, tutorials, and expert sessions to help your team get the most from the InfraGov 2.0 framework and PIM-PAM digital tools.",
    )
    cards = []
    for v in C.ACADEMY_VIDEOS:
        thumb = get_vimeo_thumbnail(v["vimeoId"])
        cards.append(VideoCard(v["title"], v["vimeoId"], thumbnail_url=thumb))
    logger.debug("digital_academy_page: rendered %d video cards.", len(cards))

    return html.Div([
        hero,
        html.Section(
            className="py-20 bg-white",
            children=html.Div(html.Div(cards, className="grid grid-cols-1 md:grid-cols-2 gap-10"),
                               className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"),
        ),
    ])


def resources_page():
    hero = _hero_section(
        "resources-hero",
        "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(67,69,170,0.2) 0%, transparent 65%)",
        "Resources", "Knowledge resources",
        "Download frameworks, guides, and reference documents for public infrastructure investment and asset governance.",
    )
    return html.Div([
        hero,
        html.Section(
            className="py-16 bg-white",
            children=html.Div(
                html.Div([ResourceCard(doc) for doc in C.RESOURCE_DOCS], className="grid grid-cols-1 md:grid-cols-2 gap-6"),
                className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            ),
        ),
    ])


def feedback_page():
    hero = _hero_section(
        "feedback-hero",
        "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(67,69,170,0.2) 0%, transparent 65%)",
        "Feedback", "Share your thoughts",
        "We'd love to hear how you're using PIM-PAM tools and how we can help improve them.",
    )
    return html.Div([
        hero,
        html.Section(
            className="py-16 bg-white",
            children=html.Div(
                html.Form(FeedbackFormFields(), id="feedback-form-container", className="space-y-6"),
                className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8",
            ),
        ),
    ])


def blogs_page():
    hero = html.Section(
        className="pt-32 pb-20 relative overflow-hidden",
        style={"background": "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(67,69,170,0.15) 0%, transparent 65%), #0A0E1A"},
        children=[
            GridOverlay(),
            html.Div(
                SectionHeading(eyebrow="Blog", heading="Insights on digital governance",
                                subheading="Analysis, case studies, and practitioner perspectives on public investment management and asset governance."),
                className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            ),
        ],
    )
    grid = html.Section(
        className="pb-24",
        children=html.Div(
            html.Div([BlogCard(post) for post in C.BLOGS], className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"),
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
    )
    return html.Div([hero, grid])


def blog_detail_page(slug):
    post = next((p for p in C.BLOGS if p["slug"] == slug), None)
    if post is None:
        logger.warning("blog_detail_page: no blog post found for slug=%r — rendering 404.", slug)
        return not_found_page()
    tag_el = None
    if post.get("tag"):
        tag_el = html.Span(post["tag"], className="inline-block text-xs font-semibold uppercase tracking-wider text-accent2 bg-accent2/10 px-2.5 py-1 rounded-full mb-4")
    return html.Article(
        className="pt-32 pb-24",
        children=html.Div(
            className="max-w-3xl mx-auto px-4 sm:px-6",
            children=[
                dcc.Link([Icon("arrow_left", size=14, color=C.COLORS["muted"]), " Back to Blogs"], href="?page=blogs",
                         className="inline-flex items-center gap-2 text-sm text-muted hover:text-accent2 transition-colors mb-8"),
                tag_el,
                html.H1(post["title"], className="text-3xl sm:text-4xl font-extrabold text-text leading-tight mb-4"),
                html.P(format_date_long(post["date"]), className="text-sm text-muted mb-10 pb-10 border-b border-white/5"),
                html.P(post["body"], className="text-muted leading-relaxed"),
            ],
        ),
    )


def not_found_page():
    return html.Div(
        className="min-h-[60vh] flex flex-col items-center justify-center text-center px-4 py-32",
        children=[
            html.P("404", className="text-sm font-semibold uppercase tracking-widest text-accent1 mb-3"),
            html.H1("Page not found", className="text-3xl font-bold text-text mb-4"),
            html.P("The page you're looking for doesn't exist or has moved.", className="text-muted mb-8"),
            dcc.Link(["Back to Home", IconArrow(size=16, color="#FFFFFF")],
                     href="?page=home", className="inline-flex items-center gap-2 px-6 py-3 rounded bg-accent1 text-white font-semibold hover:bg-accent1/90 transition-colors"),
        ],
    )


# ──────────────────────────────────────────────────────────────────────────
# VIMEO THUMBNAIL LOOKUP  (Digital Academy)
# ──────────────────────────────────────────────────────────────────────────

@lru_cache(maxsize=64)
def get_vimeo_thumbnail(vimeo_id):
    """Mirrors VideoCard.tsx's oEmbed fetch. Cached + fails soft (returns
    None -> a plain dark placeholder is shown, same fallback as the
    original before the thumbnail loads)."""
    try:
        resp = requests.get(
            "https://vimeo.com/api/oembed.json",
            params={"url": f"https://vimeo.com/{vimeo_id}", "width": 1280},
            timeout=3,
        )
        if resp.ok:
            thumb = resp.json().get("thumbnail_url")
            logger.debug("Fetched Vimeo thumbnail for %r: %s", vimeo_id, thumb)
            return thumb
        logger.warning("Vimeo oEmbed returned HTTP %s for video %r.", resp.status_code, vimeo_id)
    except requests.RequestException as exc:
        logger.warning("Vimeo oEmbed fetch failed for video %r: %s", vimeo_id, exc)
    return None


# ──────────────────────────────────────────────────────────────────────────
# APP-LEVEL LAYOUT
#   Nav / PimPamAiBanner / Footer are persistent across routes (mirrors
#   app/layout.tsx wrapping <main>{children}</main>). The tool drawer,
#   its backdrop, and the video lightbox are likewise persistent overlay
#   elements, toggled purely by Dash Store-driven callbacks below.
#
#   Open/closed state is reflected through BOTH a Tailwind className AND an
#   explicit inline `style` (transform/opacity/display/pointerEvents). The
#   className gives us the animated transition; the inline style is a
#   belt-and-suspenders guarantee that the element visibly opens/closes even
#   in an environment where the Tailwind Play CDN hasn't yet JIT-compiled a
#   class that first appears via a callback-patched attribute rather than
#   the initial page load.
# ──────────────────────────────────────────────────────────────────────────

DRAWER_BASE_CLASS = "fixed top-0 right-0 h-full w-full sm:w-[520px] bg-white z-50 shadow-2xl flex flex-col transition-transform duration-300 ease-out"
BACKDROP_BASE_CLASS = "fixed inset-0 bg-black/40 z-40 transition-opacity duration-300"
LIGHTBOX_BASE_CLASS = "fixed inset-0 z-[60] items-center justify-center bg-black/90 p-4"


def _drawer_style(is_open):
    return {"transform": "translateX(0)" if is_open else "translateX(100%)"}


def _backdrop_style(is_open):
    return {"opacity": "1" if is_open else "0", "pointerEvents": "auto" if is_open else "none"}


def _lightbox_style(is_open):
    return {"display": "flex" if is_open else "none"}


app.layout = html.Div([
    dcc.Location(id="url", refresh=False),

    dcc.Store(id="selected-tool-id", data=None),
    dcc.Store(id="drawer-open", data=False),
    dcc.Store(id="lightbox-video", data=None),
    dcc.Store(id="lightbox-open", data=False),

    NavBar(),

    html.Div(id="page-content"),

    PimPamAiBanner(),
    Footer(),

    # ── Tool detail drawer (ToolList.tsx) ──────────────────────────────
    # The close ("X") button lives here — statically, created exactly once
    # — rather than inside the dynamically-swapped `tool-drawer-content`.
    # See the comment on close_tool_drawer() below for why: a button
    # rebuilt every time the drawer opens would "phantom click" itself
    # closed the instant it was first inserted into the DOM.
    html.Div(id="tool-drawer-backdrop", n_clicks=0,
              className=f"{BACKDROP_BASE_CLASS} opacity-0 pointer-events-none",
              style=_backdrop_style(False)),
    html.Div(
        id="tool-drawer",
        className=f"{DRAWER_BASE_CLASS} translate-x-full",
        style=_drawer_style(False),
        children=[
            html.Button(
                Icon("x", size=20, color="#9CA3AF"),
                id="tool-drawer-close-btn", n_clicks=0,
                className="absolute top-5 right-5 z-10 p-1.5 rounded hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors bg-white/80",
                **{"aria-label": "Close"},
            ),
            html.Div(id="tool-drawer-content", className="flex-1 min-h-0 flex flex-col"),
        ],
    ),

    # ── Video lightbox (ToolList.tsx "Watch Video") ────────────────────
    html.Div(
        id="lightbox-container",
        className=f"{LIGHTBOX_BASE_CLASS} hidden",
        style=_lightbox_style(False),
        children=[
            html.Button(Icon("x", size=22, color="#FFFFFF"), id="lightbox-close-btn", n_clicks=0,
                        className="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors",
                        **{"aria-label": "Close video"}),
            html.Div(id="lightbox-iframe-wrapper", className="w-full max-w-4xl aspect-video mx-auto"),
        ],
    ),
], id="react-entry-point")

logger.info("app.layout constructed (%d top-level children).", len(app.layout.children))


# ──────────────────────────────────────────────────────────────────────────
# CALLBACKS
# ──────────────────────────────────────────────────────────────────────────

# ── URL normalization: make "/" explicit as "/?page=home" ────────────────
# On a bare page load (no query string at all — e.g. someone hits the raw
# Connect URL or bookmarks the root), rewrite the address bar to
# "?page=home" via history.replaceState. This doesn't reload the page or
# add a back-button entry; it just makes the URL an accurate, shareable
# reflection of what's on screen, matching every other page's convention.
app.clientside_callback(
    """
    function(pathname) {
        if (!window.location.search) {
            var newUrl = window.location.pathname + "?page=home" + window.location.hash;
            window.history.replaceState(null, "", newUrl);
        }
        return false;
    }
    """,
    Output("url", "refresh"),
    Input("url", "pathname"),
)


# ── Routing ────────────────────────────────────────────────────────────
# Query-string based routing: /?page=digital-tools, /?page=blogs&slug=..., etc.
# Everything lives at "/" and only the "page" param changes, so this is a
# single lightweight GET each time (no full-page path resolution), and it
# sidesteps Posit Connect's /content/<guid> path-prefixing entirely — the
# query string is untouched by whatever path prefix Connect serves the app
# under, so no prefix-stripping hack is needed here anymore.
@app.callback(Output("page-content", "children"), Input("url", "search"))
def route(search):
    query = urllib.parse.parse_qs((search or "").lstrip("?"))
    page = (query.get("page", ["home"])[0] or "home").strip().lower()
    logger.info("Routing request for page=%r", page)
    if page == "home":
        return home_page()
    if page == "digital-tools":
        return digital_tools_page()
    if page == "infragov":
        return infragov_page()
    if page == "digital-academy":
        return digital_academy_page()
    if page == "resources":
        return resources_page()
    if page == "feedback":
        return feedback_page()
    if page == "blogs":
        slug = query.get("slug", [None])[0]
        if slug:
            logger.info("Routing to blog detail, slug=%r", slug)
            return blog_detail_page(slug)
        return blogs_page()
    logger.warning("No page matched page=%r — rendering 404.", page)
    return not_found_page()


# ── Tool drawer: open on row click ───────────────────────────────────────
@app.callback(
    Output("selected-tool-id", "data"),
    Output("drawer-open", "data"),
    Output("tool-drawer-content", "children"),
    Input({"type": "tool-row-btn", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def open_tool_drawer(_n_clicks):
    triggered = ctx.triggered_id
    if not triggered or not any(_n_clicks):
        logger.debug("open_tool_drawer fired with no real click (triggered_id=%r) — ignoring.", triggered)
        return no_update, no_update, no_update
    tool_id = triggered["index"]
    tool = next((t for t in C.TOOLS if t["id"] == tool_id), None)
    if tool is None:
        logger.warning("open_tool_drawer: unknown tool id %r clicked.", tool_id)
        return no_update, no_update, no_update
    logger.info("Opening tool drawer for tool_id=%r (%s)", tool_id, tool.get("name"))
    return tool_id, True, ToolDrawerContent(tool)


# ── Tool drawer: close (X button or backdrop click) ──────────────────────
@app.callback(
    Output("drawer-open", "data", allow_duplicate=True),
    Input("tool-drawer-close-btn", "n_clicks"),
    Input("tool-drawer-backdrop", "n_clicks"),
    prevent_initial_call=True,
)
def close_tool_drawer(_close, _backdrop):
    # `tool-drawer-close-btn` only comes into existence the first time
    # ToolDrawerContent() is rendered (i.e. as a side effect of
    # open_tool_drawer's own output). Dash fires a callback once when a
    # component it depends on is newly inserted into the layout, REGARDLESS
    # of prevent_initial_call — that "phantom" first call arrives with
    # n_clicks still at its initial value (0), immediately after the drawer
    # opens, which is exactly the bug reported: open + close logged back to
    # back. Guarding on a real (truthy) n_clicks value fixes it.
    if not _close and not _backdrop:
        logger.debug("close_tool_drawer fired with no real click (close=%r, backdrop=%r) — ignoring.", _close, _backdrop)
        return no_update
    logger.info("Closing tool drawer (triggered by %r).", ctx.triggered_id)
    return False


# ── Tool drawer: reflect open/closed state in the DOM ────────────────────
@app.callback(
    Output("tool-drawer", "className"),
    Output("tool-drawer", "style"),
    Output("tool-drawer-backdrop", "className"),
    Output("tool-drawer-backdrop", "style"),
    Input("drawer-open", "data"),
)
def render_drawer_state(is_open):
    logger.debug("render_drawer_state: is_open=%s", is_open)
    if is_open:
        drawer_cls = f"{DRAWER_BASE_CLASS} translate-x-0"
        backdrop_cls = f"{BACKDROP_BASE_CLASS} opacity-100"
    else:
        drawer_cls = f"{DRAWER_BASE_CLASS} translate-x-full"
        backdrop_cls = f"{BACKDROP_BASE_CLASS} opacity-0 pointer-events-none"
    return drawer_cls, _drawer_style(is_open), backdrop_cls, _backdrop_style(is_open)


# ── Watch Video button inside the drawer -> opens the lightbox ───────────
@app.callback(
    Output("lightbox-video", "data"),
    Output("lightbox-open", "data"),
    Input("tool-drawer-watch-btn", "n_clicks"),
    State("selected-tool-id", "data"),
    prevent_initial_call=True,
)
def open_lightbox(_n_clicks, tool_id):
    # Same phantom-first-mount hazard as close_tool_drawer: this button only
    # exists once a tool WITH a video is opened, so its first appearance
    # would otherwise auto-open the lightbox without any real click.
    if not _n_clicks:
        logger.debug("open_lightbox fired with no real click (n_clicks=%r) — ignoring.", _n_clicks)
        return no_update, no_update
    tool = next((t for t in C.TOOLS if t["id"] == tool_id), None)
    if not tool or not tool.get("videoId"):
        logger.warning("open_lightbox: tool_id=%r has no video — ignoring Watch Video click.", tool_id)
        return no_update, no_update
    logger.info("Opening video lightbox for tool_id=%r, videoId=%r", tool_id, tool["videoId"])
    return tool["videoId"], True


# ── Lightbox close ─────────────────────────────────────────────────────
@app.callback(
    Output("lightbox-open", "data", allow_duplicate=True),
    Input("lightbox-close-btn", "n_clicks"),
    prevent_initial_call=True,
)
def close_lightbox(_n_clicks):
    if not _n_clicks:
        return no_update
    logger.info("Closing video lightbox.")
    return False


# ── Lightbox: reflect open/closed state + mount/unmount the iframe ───────
@app.callback(
    Output("lightbox-container", "className"),
    Output("lightbox-container", "style"),
    Output("lightbox-iframe-wrapper", "children"),
    Input("lightbox-open", "data"),
    State("lightbox-video", "data"),
)
def render_lightbox_state(is_open, video_id):
    logger.debug("render_lightbox_state: is_open=%s, video_id=%r", is_open, video_id)
    if is_open and video_id:
        iframe = html.Iframe(
            src=vimeo_embed_url(video_id, autoplay=True),
            className="w-full h-full rounded",
            style={"border": "0"},
            allow="autoplay; fullscreen; picture-in-picture",
        )
        return f"{LIGHTBOX_BASE_CLASS} flex", _lightbox_style(True), iframe
    return f"{LIGHTBOX_BASE_CLASS} hidden", _lightbox_style(False), None


# ── Digital Academy: play button swaps thumbnail for a live embed ────────
@app.callback(
    Output({"type": "video-container", "index": MATCH}, "children"),
    Input({"type": "video-play-btn", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def play_academy_video(n_clicks):
    if not n_clicks:
        return no_update
    vimeo_id = ctx.triggered_id["index"]
    title = next((v["title"] for v in C.ACADEMY_VIDEOS if v["vimeoId"] == vimeo_id), "")
    logger.info("Playing academy video vimeoId=%r (%s)", vimeo_id, title)
    return VideoIframe(vimeo_id, title=title)


# ── Feedback form submission ──────────────────────────────────────────────
@app.callback(
    Output("feedback-form-container", "children"),
    Input("fb-submit-btn", "n_clicks"),
    State("fb-name", "value"),
    State("fb-email", "value"),
    State("fb-org", "value"),
    State("fb-feedback", "value"),
    prevent_initial_call=True,
)
def submit_feedback(_n_clicks, name, email, org, feedback):
    # `fb-submit-btn` is rebuilt from scratch by feedback_page() every time
    # the user navigates to /feedback (routing swaps page-content entirely).
    # Without this guard, Dash's "fire once when a new Input appears"
    # behavior would show validation errors on a completely untouched form
    # the instant the page loads — this was almost certainly the source of
    # the earlier "Feedback tab looks broken" report.
    if not _n_clicks:
        logger.debug("submit_feedback fired with no real click (n_clicks=%r) — ignoring.", _n_clicks)
        return no_update

    name = (name or "").strip()
    email = (email or "").strip()
    org = (org or "").strip()
    feedback = (feedback or "").strip()

    errors = set()
    if not name:
        errors.add("name")
    if not email or "@" not in email:
        errors.add("email")
    if not feedback:
        errors.add("feedback")

    if errors:
        logger.warning("Feedback submission rejected — missing/invalid fields: %s", sorted(errors))
        values = {"name": name, "email": email, "organization": org, "feedback": feedback}
        return html.Div(FeedbackFormFields(values=values, errors=errors), className="space-y-6")

    # brief pause to mirror the original's simulated network delay / "Sending…" state
    time.sleep(0.5)
    logger.info("Feedback submitted successfully from %r (org=%r, message length=%d).", email, org, len(feedback))
    return html.Div(FeedbackThankYou())


# ──────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Starting PIM-PAM Dash server on http://127.0.0.1:8050 ...")
    app.run(debug=True, host="127.0.0.1", port=8050)