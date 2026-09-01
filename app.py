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
import re
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
    SupportedByCarousel, EventCard, AgendaAccordion, EcbaMethodologyNav,
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
    <style>
        /* AgendaAccordion.tsx — strip the native <details> marker so our
           own chevron icon is the only expand/collapse indicator, and
           rotate that chevron when a session is open. */
        details > summary {{ list-style: none; }}
        details > summary::-webkit-details-marker {{ display: none; }}
        details > summary::marker {{ content: ""; }}
        details[open] > summary .agenda-chevron {{ transform: rotate(180deg); }}
    </style>
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

        function initResourcesDropdown() {{
            // Desktop: click to open a floating panel; closes on an
            // outside click, an Escape press, or picking a link inside.
            // Mobile: click expands an inline sub-list within the mobile
            // menu instead of a floating panel. Mirrors Nav.tsx's
            // useState-driven "Resources" dropdown with plain JS, same
            // pattern as initMobileNav() above.
            var dBtn = document.getElementById('nav-resources-btn');
            var dMenu = document.getElementById('nav-resources-menu');
            if (dBtn && dMenu && !dBtn.__init) {{
                dBtn.__init = true;
                var chevron = dBtn.querySelector('img');
                function closeDesktop() {{
                    dMenu.classList.add('hidden');
                    dBtn.setAttribute('aria-expanded', 'false');
                    if (chevron) chevron.style.transform = '';
                }}
                function openDesktop() {{
                    dMenu.classList.remove('hidden');
                    dBtn.setAttribute('aria-expanded', 'true');
                    if (chevron) chevron.style.transform = 'rotate(180deg)';
                }}
                dBtn.addEventListener('click', function (e) {{
                    e.stopPropagation();
                    if (dMenu.classList.contains('hidden')) openDesktop(); else closeDesktop();
                }});
                dMenu.querySelectorAll('a').forEach(function (a) {{ a.addEventListener('click', closeDesktop); }});
                document.addEventListener('click', function (e) {{
                    if (!dMenu.classList.contains('hidden') && !dMenu.contains(e.target) && e.target !== dBtn) closeDesktop();
                }});
                document.addEventListener('keydown', function (e) {{ if (e.key === 'Escape') closeDesktop(); }});
            }}

            var mBtn = document.getElementById('nav-mobile-resources-btn');
            var mMenu = document.getElementById('nav-mobile-resources-menu');
            if (mBtn && mMenu && !mBtn.__init) {{
                mBtn.__init = true;
                var mChevron = mBtn.querySelector('img');
                mBtn.addEventListener('click', function () {{
                    var isHidden = mMenu.classList.contains('hidden');
                    mMenu.classList.toggle('hidden');
                    mMenu.classList.toggle('flex', isHidden);
                    mBtn.setAttribute('aria-expanded', isHidden ? 'true' : 'false');
                    if (mChevron) mChevron.style.transform = isHidden ? 'rotate(180deg)' : '';
                }});
                mMenu.querySelectorAll('a').forEach(function (a) {{
                    a.addEventListener('click', function () {{
                        var mobileMenu = document.getElementById('nav-mobile-menu');
                        if (mobileMenu) mobileMenu.classList.add('hidden');
                    }});
                }});
            }}
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

        function initAgendaAccordions() {{
            // AgendaAccordion.tsx — only one session row should be open at
            // a time within a given event's agenda. Native <details> fires
            // a real "toggle" event when it opens/closes; when one in a
            // data-accordion-group opens, close its siblings in that same
            // group. (See the AgendaAccordion() docstring in utils.py.)
            document.querySelectorAll('details[data-accordion-group]').forEach(function (el) {{
                if (el.__init) return;
                el.__init = true;
                el.addEventListener('toggle', function () {{
                    if (!el.open) return;
                    var group = el.getAttribute('data-accordion-group');
                    document.querySelectorAll('details[data-accordion-group="' + group + '"]').forEach(function (other) {{
                        if (other !== el && other.open) other.open = false;
                    }});
                }});
            }});
        }}

        function initEcbaMethodologyNav() {{
            // EcbaMethodologyNav.tsx — highlight the sidebar nav item for
            // whichever section is currently in view, same rootMargin as
            // the original's per-item IntersectionObserver.
            var nav = document.getElementById('ecba-methodology-nav');
            if (!nav || nav.__init) return;
            nav.__init = true;
            var links = nav.querySelectorAll('a[data-nav-target]');
            if (!links.length) return;
            function setActive(id) {{
                links.forEach(function (a) {{
                    var isActive = a.getAttribute('data-nav-target') === id;
                    a.classList.toggle('text-accent1', isActive);
                    a.classList.toggle('font-semibold', isActive);
                    a.classList.toggle('text-gray-500', !isActive);
                    a.classList.toggle('hover:text-accent1', !isActive);
                }});
            }}
            var observer = new IntersectionObserver(function (entries) {{
                entries.forEach(function (entry) {{
                    if (entry.isIntersecting) setActive(entry.target.id);
                }});
            }}, {{ rootMargin: '-20% 0px -70% 0px', threshold: 0 }});
            links.forEach(function (a) {{
                var el = document.getElementById(a.getAttribute('data-nav-target'));
                if (el) observer.observe(el);
            }});
        }}

        function initAll() {{
            initNavScroll();
            initMobileNav();
            initResourcesDropdown();
            initCarousel();
            initRevealOnScroll();
            initAgendaAccordions();
            initEcbaMethodologyNav();
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
                                dcc.Link(["Explore Tools ", IconArrow(size=80, color=C.COLORS["accent1"])], href="?page=digital-tools",
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

        # ── Events ────────────────────────────────────────────────────
        html.Section(
            className="py-14 lg:py-20 bg-surface border-b border-white/10",
            children=html.Div(
                className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                children=[
                    html.Div(
                        className="flex items-end justify-between mb-10",
                        children=[
                            SectionHeading(
                                eyebrow="Events", heading="Explore Events",
                                subheading="Workshops, training sessions, and conferences on public investment management and public asset management.",
                                light_badge=True,
                            ),
                            dcc.Link(["View all events ", IconArrow(size=14, color="#FFFFFF")], href="?page=events",
                                     className="hidden sm:inline-flex items-center gap-2 text-sm text-white/60 hover:text-white transition-colors flex-shrink-0 pb-1"),
                        ],
                    ),
                    html.Div([EventCard(e, compact=True) for e in C.EVENTS[:3]], className="grid grid-cols-1 md:grid-cols-3 gap-5"),
                    html.Div(
                        dcc.Link(["View all events ", IconArrow(size=14, color="#FFFFFF")], href="?page=events",
                                 className="inline-flex items-center gap-2 text-sm text-white/60 hover:text-white transition-colors"),
                        className="mt-8 sm:hidden text-center",
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


def _ecba_section(section_id, title, children):
    """One <section id="..."> block of the eCBA Methodology article, with
    the shared heading style used throughout page.tsx."""
    return html.Section(
        id=section_id,
        className="mb-16",
        children=[
            html.H2(title, className="text-2xl font-bold text-gray-900 mb-6 pb-3 border-b border-gray-100"),
            *children,
        ],
    )


def _ecba_bullets(items, tight=False):
    return html.Ul(
        [
            html.Li([html.Span("•", className="text-accent1 flex-shrink-0 mt-0.5"), html.Span(item)],
                    className="flex gap-2 text-sm text-gray-500 leading-relaxed")
            for item in items
        ],
        className="space-y-1.5" if tight else "space-y-1.5 pl-4",
    )


def ecba_methodology_page():
    hero = _hero_section(
        "ecba-methodology-hero",
        "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(67,69,170,0.22) 0%, transparent 65%)",
        "eCBA", "eCBA Methodology",
        "The methodology behind the Economic Cost-Benefit Analysis Tool — how financial and economic indicators are estimated, the underlying calculations, and the assumptions that drive them.",
    )

    # ── Introduction ────────────────────────────────────────────────────
    introduction = _ecba_section("introduction", "Introduction", [
        html.Div([
            html.P("The eCBA tool is an online module that enables users to assess financial and economic feasibility of investment projects by utilizing aggregated primary input data series such as capital expenditures, operational costs, and revenue streams. As a result, users do not need expertise in financial modelling or proficiency in Excel to use the tool. By providing a standardized approach to appraisal and evaluation procedures, the tool can serve as a foundation for various applications — for example, supporting online public investment management (PIM) platforms or functioning as a repository, reporting, and record-management system for completed projects, rejected project concepts, and potential future undertakings."),
            html.P("To ensure global applicability and relevance across diverse project types, the calculations have been standardized and streamlined to a certain degree. Project proponents are expected to provide financial and economic streams as input data in line with specific PIM process requirements. These include financial costs and revenues series, as well as economic benefits, costs, externalities, and non-market impacts. A general challenge in public investment CBA lies in identifying and monetizing appropriate data series. For example, a CBA may require estimating the monetized value of time savings, accident reduction, or reduced CO₂ emissions. Developing these series depends on various data sources and methods, particularly within the ‘without-the-project’ scenario and ‘with-the-project’ scenario framework. The eCBA tool does not resolve these methodological challenges but provides a more structured way to distil and present these valuations."),
            html.P("The eCBA tool allows proponents to upload documentation explaining how different summary series were created (e.g., PDFs, Word, or Excel spreadsheets). While Excel provides greater flexibility for experienced users, it can be less transparent and less accessible for general users with limited time and capacity. The eCBA tool is not intended to replace all key steps or inputs for a cost-benefit analysis. Users remain responsible for generating the required input data based on calculations done outside the module (e.g. demand analyses used to project revenues or estimate economic benefits). Particularly larger complex projects may require bespoke tools and methods, and hence the eCBA tool could simply be used to record key aggregate values."),
            html.P("A prerequisite for using the eCBA tool is transparent documentation of project components and their associated cost and benefit flows. The tool helps standardize the CBA process and clearly document assumptions and results. However, estimating actual benefits and costs must be done separately, and the basis for those calculations must be explained by the project proponent in the relevant input fields or supporting attachments. The eCBA module is not designed for conducting demand analyses or calculating economic benefits, costs, externalities and non-market impacts from scratch. Therefore, input data for financial and economic analyses must be prepared externally — often in Excel — before the aggregated annual values are entered into the eCBA tool. At this early stage of development, it is not feasible to provide a uniform framework for detailed, project-specific calculations without inadvertently favouring certain project types or requiring extensive sector- and country-specific data. Future releases may introduce additional modules allowing more calculations to be performed within the tool, potentially supported by databases of economic values (e.g., value of time, value of statistical life, shadow price of carbon) tailored to different country and sector contexts."),
            html.P("The eCBA tool is designed to balance ease of use with the need to capture essential project details. A core objective is to ensure that all critical financial and economic data series are made explicit over the project’s life. However, the tool does not require users to enter every intermediate calculation step; these can be documented in supporting files. For financial analysis, the current eCBA requires users to separately enter BAU (variant 0) and with-project (variant 1) series (e.g., current and projected costs, current and future revenues where applicable). Economic costs, benefits, externalities, and non-market impacts are recorded only as incremental values (i.e., variant 1 only), primarily to keep the process simple. A future module could require users to enter both BAU and with-project economic series explicitly, thereby making incremental values more transparent."),
            html.P("The tool is fully functional and continuously being improved, offering a flexible framework that can be used both for training purposes and as a source of inspiration for developing project assessment practices. Its underlying code is publicly available and can serve as a foundation for building national or country-specific project appraisal systems. While the tool enables rapid project validation by ministries of finance, it is most effective when integrated into a broader public investment management or budgeting system, as demonstrated in the case of Georgia."),
            html.P([
                "This document describes in detail the methodology behind the eCBA tool, including how the financial and economic indicators are estimated and the underlying calculations. The following sections reflect the structure of the eCBA module. The methodology behind the calculations in the eCBA tool is inspired by EU appraisal guidelines and other international documentation pertaining to the subject, such as ",
                html.Em("Guide to Cost-Benefit Analysis of Investment Projects for Cohesion Policy 2014–2020"),
                " and ",
                html.Em("Economic Appraisal Vademecum 2021–2027"),
                ".",
            ]),
        ], className="space-y-4 text-gray-600 leading-relaxed text-sm"),
    ])

    # ── Project Details ─────────────────────────────────────────────────
    project_details = _ecba_section("project-details", "Project Details", [
        html.Div([
            html.P("This section captures the general administrative information about the project, including its name or title, a brief description, the sector in which the project will operate, and the time horizon of the analysis."),
            html.P([html.Strong("Reference period", className="text-gray-800"), " indicates the overall lifespan of the project and includes both the investment as well as the operational phase. In other words, this is the period over which the financial and economic analyses are performed. The length of the reference period defines the time frame for which data must be entered, counted from the first year of the investment period (see ", html.Em("Start of investment period"), " below)."]),
            html.P([html.Strong("Base year", className="text-gray-800"), " specifies in which year the analysis is conducted and directly affects the discounting calculations. The tool treats the selected base year as the current year and does not discount cash flows up to and including that year. This allows the tool to accommodate both historical projects and projects planned to start in the future. Base year should always be greater or equal to the Start of investment period."]),
            html.P([html.Strong("Start of investment period", className="text-gray-800"), " indicates the first year in which costs related to project implementation are incurred. This year also marks the beginning of the project’s Reference period."]),
            html.P([html.Strong("End of investment period", className="text-gray-800"), " identifies the last year in which capital expenditures are incurred before the project becomes operational, while ", html.Strong("Start of operation period", className="text-gray-800"), " marks the first year of the project’s operational phase and determines the first year in which depreciation begins to accumulate. The first year of the operation period should always be equal to or greater than the End of investment period."]),
        ], className="space-y-4 text-gray-600 leading-relaxed text-sm"),
    ])

    # ── General Assumptions ─────────────────────────────────────────────
    ga_intro = html.Div([
        html.P("General assumptions define the setting, the environment in which a project is to take place. These include:"),
        _ecba_bullets([
            "Analysis assumptions (financial and social discount rates)",
            "Fiscal adjustment coefficients (VAT and employment tax rates)",
            "Depreciation factors for estimating residual value",
            "Data types (Input and Output data types, Constant or Current prices)",
            "Macroeconomic assumptions (inflation, projected real wage growth and projected nominal wage growth rates)",
        ]),
    ], className="space-y-4 text-gray-600 leading-relaxed text-sm mb-8")

    ga_2_1 = html.Div([
        html.H3("2.1. Analysis assumptions", className="text-base font-bold text-gray-900 mb-3"),
        html.Div([
            html.P("Financial and social discount rates provided in Analysis assumptions are used to discount the cash flows in financial and economic analyses, respectively, and ultimately to calculate the values of Financial Net Present Value (FNPV) as well as Economic Net Present Value (ENPV) of a project. The first year in which the discounting occurs is always ‘Base year +1’ (e.g. if base year is set to 2026, then 2027 is the first year in which the cash flows are discounted). The following formula is used:"),
            html.Div(
                html.Div([
                    html.Div(["PV = FV / (1 + r)", html.Sup("t")], className="text-lg font-semibold text-gray-800 mb-1"),
                    html.Div([
                        html.Div([html.Span("PV", className="font-semibold"), " — present value"]),
                        html.Div([html.Span("FV", className="font-semibold"), " — future value"]),
                        html.Div([html.Span("r", className="font-semibold"), " — discount rate"]),
                        html.Div([html.Span("t", className="font-semibold"), " — time period"]),
                    ], className="text-xs text-gray-500 mt-3 text-left space-y-0.5"),
                ], className="inline-block bg-gray-50 border border-gray-200 rounded-xl px-8 py-5 font-mono text-center"),
                className="my-6 flex justify-center",
            ),
            html.P("As such, when calculating PV of cash flows in the base year, ‘t’ always equals 0."),
        ], className="space-y-4 text-gray-600 leading-relaxed text-sm"),
    ], className="mb-8")

    ga_2_2 = html.Div([
        html.H3("2.2. Fiscal adjustment coefficients", className="text-base font-bold text-gray-900 mb-3"),
        html.Div([
            html.P("Data provided in this section can be divided into two categories, each having a different impact on calculations in the later stages of the analysis:"),
            html.Ol([html.Li("VAT rate(s)"), html.Li("Employment tax")], className="space-y-1 pl-4 list-decimal list-inside"),
            html.P("All of the fiscal adjustment coefficients are automatically applied in the calculations in the tool."),
        ], className="space-y-4 text-gray-600 leading-relaxed text-sm mb-4"),
        html.Div([
            html.H4("2.2.1. VAT rates", className="text-sm font-bold text-gray-800 mb-2"),
            html.P("Different rates of VAT can be applied to each category of capital expenditures, each category of operating expenditures (except Wages and salaries cost category), and all revenue streams in a project. Their impact on the calculations can be multifactorial depending on provided information concerning Data types and VAT recoverability. Additionally, the aforementioned choices also have an effect on the Residual value calculations.",
                   className="text-sm text-gray-600 leading-relaxed"),
        ], className="mb-6"),
        html.Div([
            html.H4("2.2.2. Employment tax", className="text-sm font-bold text-gray-800 mb-2"),
            html.P("Employment tax is a coefficient that only applies to the Wages and salaries category in the OPEX section of the analysis.",
                   className="text-sm text-gray-600 leading-relaxed"),
        ]),
    ], className="mb-8")

    ga_2_3 = html.Div([
        html.H3("2.3. Depreciation factors for estimating residual value", className="text-base font-bold text-gray-900 mb-3"),
        html.P("Residual value of a project is calculated automatically using the asset-based approach, which determines the net asset value at the end of the reference period. This amount is included as a positive cash flow in the final year of the analysis. Annual asset depreciation is calculated using the straight-line method, which reduces the asset’s value by an equal amount each year, starting from the first year of the operation period.",
               className="text-sm text-gray-600 leading-relaxed"),
    ], className="mb-8")

    ga_2_4_table = html.Div([
        html.Div([
            html.P("Analysis based on net values", className="font-semibold text-gray-800 mb-1"),
            _ecba_bullets([
                "Costs in financial analysis are based on net values unless VAT is not recoverable for the implementing or operating entity",
                "Economic analysis is based on net values regardless of VAT recoverability; wages and salaries are excluded from deductions (assuming a well-functioning labour market)",
            ], tight=True),
        ]),
        html.Div([
            html.P("Analysis based on gross values", className="font-semibold text-gray-800 mb-1"),
            _ecba_bullets([
                "Gross values are used in the financial analysis, and VAT recoverability is not an issue",
                "Economic analysis is still based on net values regardless of the chosen option or VAT recoverability",
            ], tight=True),
        ]),
    ], className="bg-gray-50 rounded-xl p-5 space-y-3")

    ga_2_4 = html.Div([
        html.H3("2.4. Data types — Input and Output data types; Constant and Current prices", className="text-base font-bold text-gray-900 mb-3"),
        html.Div([
            html.P("As the tool offers its users an option to convert uploaded data from net to gross values and vice versa, it is necessary to establish these parameters for each analysis."),
            html.P([html.Strong("Input data type", className="text-gray-800"), " determines whether the values uploaded in the tool are net values (i.e. void of any taxes) or gross values, meaning that they include taxes based on rates provided in fiscal adjustment coefficients."]),
            html.P([html.Strong("Output data type", className="text-gray-800"), " determines what kind of information the analysis should be based on."]),
            ga_2_4_table,
            html.P([html.Strong("Current prices or constant prices", className="text-gray-800"), " determines whether the analysis should incorporate the effects of inflation. If Current prices are selected, the tool will automatically adjust the input data throughout the reference period based on the information provided in the Macroeconomic assumptions table (excluding Wages and salaries category in OPEX)."]),
            html.P("The Macroeconomic assumptions table includes inflation, projected real wage growth, and projected nominal wage growth, and displays cumulative values over the entire reference period. For the base year these values should always be set to 0%, meaning that regardless of chosen pricing option, data entered for the base year will not be adjusted for inflation or wage growth. Data should be entered either for each year of the reference period or, alternatively, only for the first 5 years if the tool is to assume that the rates are constant afterwards."),
        ], className="space-y-4 text-sm text-gray-600 leading-relaxed"),
    ])

    general_assumptions = _ecba_section("general-assumptions", "General Assumptions", [ga_intro, ga_2_1, ga_2_2, ga_2_3, ga_2_4])

    # ── Financial Analysis ───────────────────────────────────────────────
    fa_intro = html.Div([
        html.P("The financial analysis methodology used in the tool is the Discounted Cash Flow (DCF) method. The calculations aggregate all positive and negative cash flows for each project variant, and then subtract the cash flows of the baseline scenario (i.e. Variant 0 or ‘business-as-usual’ scenario) from each investment alternative (i.e. Variant 1, Variant 2, and so on). Only actual cash inflows and outflows are considered in the analysis; therefore, depreciation, reserves, price and technical contingencies and other accounting items which do not correspond to real cash flows should be excluded. The key financial indicators — Financial Net Present Value (FNPV) and Internal Rate of Return (IRR) — are calculated based on these differential cash flows for each investment variant."),
        html.P([html.Strong("Variant 0", className="text-gray-800"), " represents a situation that would occur if the project is not implemented, covering both financial and economic conditions. This scenario does not always correspond to a strict ‘do-nothing’ option. In some cases, it may represent a ‘do-the-minimum’ scenario, which could include capital expenditures such as rehabilitation costs to reestablish the performance of the degraded asset if the proposed project is not undertaken. In such cases, the relevant capital expenditures (as well as any operational expenditures and revenues) should be entered in the appropriate tables."]),
        html.P("The financial analysis and the calculations of project viability indicators rely on four categories of cash flows, each of which must be specified separately for every project variant:"),
        html.Ol([
            html.Li("Capital expenditures and Replacement costs (negative cash flows, i.e. expenses)"),
            html.Li("Operational expenditures (negative cash flows, i.e. expenses)"),
            html.Li("Revenues (positive cash flows)"),
            html.Li("Residual value (positive cash flow in the last year of the reference period)"),
        ], className="space-y-1 pl-4 list-decimal list-inside"),
    ], className="space-y-4 text-sm text-gray-600 leading-relaxed mb-8")

    fa_3_1 = html.Div([
        html.H3("3.1. Capital expenditures and Replacement costs", className="text-base font-bold text-gray-900 mb-3"),
        html.Div([
            html.P("The Capital expenditures section covers all expenditures related to the acquisition or major improvements of fixed assets required to set up or establish a project. These may include tangible assets (e.g. buildings, structures, machinery or equipment) and intangible assets (e.g. information, communication, IT systems). Data entered into the tool should be grouped and categorized based on shared parameters regarding VAT recoverability, Tax rate, and Depreciation rate. Annual expenditure values must be provided for each year of the Investment period."),
            html.P([
                "Any expenditure entered for years after the End of investment period will be treated by the tool as a ",
                html.Strong("Replacement cost", className="text-gray-800"),
                ", i.e. an expenditure required to maintain the status quo or to rehabilitate the degraded assets. In principle, these costs must be incurred to ensure that assets remain functional. Replacement costs differ from Maintenance and repair costs within Operational expenditures, as the latter cover only minor renovation works that are not essential for the continued operation of the infrastructure.",
            ]),
            html.P("Additionally, the tool will apply depreciation to all capital and replacement costs entered in the Capital expenditures section and will calculate the investment’s residual value based on these inputs. It is important to note that in a situation where parts of a project become operational before the overall investment is completed (e.g. project begins operations in 2030, while some investment costs continue to be incurred in 2031 and 2032), then the tool will still technically classify these expenditures as Replacement costs and apply the corresponding depreciation and residual value calculation rules accordingly."),
        ], className="space-y-4 text-sm text-gray-600 leading-relaxed"),
    ], className="mb-8")

    fa_3_2 = html.Div([
        html.H3("3.2. Operational expenditures", className="text-base font-bold text-gray-900 mb-3"),
        html.Div(
            html.P("Operational expenditures include all costs related to operation and maintenance of the service throughout the project’s lifetime. These costs must not include depreciation, interest, and loan repayments. Data entered into the tool should be grouped and categorized based on shared parameters regarding VAT recoverability and Tax rate. Special attention should be given to the Wages and salaries category as these costs follow a different set of rules in the calculations compared to other operational expenditures."),
            className="space-y-4 text-sm text-gray-600 leading-relaxed",
        ),
        html.Div([
            html.H4("3.2.1. Wages and salaries", className="text-sm font-bold text-gray-800 mb-2"),
            html.Div([
                html.P("Wages and salaries used in the financial analysis must always be presented as the full employer cost, i.e. it should include all social-security-related taxes, as well as overheads or surcharges. Regardless of the selected Input and Output data types, the tool consistently uses gross values of wages and salaries in the calculation of both financial and economic indicators."),
                html.P("Additionally, wages and salaries are adjusted separately from other cost categories using Projected real wage growth rate or the Projected nominal wage growth rate, depending on whether the analysis is conducted in constant or current prices:"),
                _ecba_bullets([
                    [html.Span("If the analysis is performed in "), html.Strong("Constant prices", className="text-gray-800"), html.Span(", the tool automatically adjusts wages and salaries using Projected real wage growth rate throughout the whole reference period.")],
                    [html.Span("If the analysis is performed in "), html.Strong("Current prices", className="text-gray-800"), html.Span(", the tool applies the Projected nominal wage growth rate to the annual wages and salaries values.")],
                ]),
                html.P("The projected nominal wage growth is calculated by combining inflation rate and real wage growth rate for a given year."),
            ], className="space-y-3 text-sm text-gray-600 leading-relaxed"),
        ], className="mt-4"),
    ], className="mb-8")

    fa_3_3 = html.Div([
        html.H3("3.3. Revenues", className="text-base font-bold text-gray-900 mb-3"),
        html.P("Operational Revenues include all cash inflows generated from the provision of goods and services or from monetizing usage and/or availability. Users are expected to estimate these inflows based on current demand (where applicable) and projected future demand, taking into account the existing infrastructure’s current capacity. Revenues used in the calculations of financial profitability must exclude transfers, subsidies, and other financial income, as these do not arise from project operations. Data entered into the tool should be grouped and categorized according to shared Tax rate parameters.",
               className="text-sm text-gray-600 leading-relaxed"),
    ], className="mb-8")

    residual_value_rows = [
        ("net→net", "No adjustments are made unless VAT is non-recoverable for one or more cost categories (in such cases gross values for those categories are used in residual value calculations)"),
        ("net→gross", "All capital expenditures and replacement costs are converted into gross values, which are then used to calculate the residual value"),
        ("gross→net", "All costs are converted into net values and the residual value is calculated using the net values unless VAT is non-recoverable for specific categories (for those categories gross values are used instead)"),
        ("gross→gross", "No adjustments are made; residual value is calculated directly from the entered inputs"),
    ]
    fa_3_4_table = html.Div(
        [html.P("Input and Output data type combinations", className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-3")]
        + [
            html.Div([
                html.Span(rtype, className="font-mono font-semibold text-accent1 flex-shrink-0 w-24"),
                html.Span(desc, className="text-gray-600"),
            ], className="flex gap-3 text-sm")
            for rtype, desc in residual_value_rows
        ]
        + [
            html.Div([
                html.Span("Current prices", className="font-semibold text-gray-800 flex-shrink-0 w-24"),
                html.Span("If Current prices are selected, the tool automatically adjusts input values for inflation before performing the calculations", className="text-gray-600"),
            ], className="flex gap-3 text-sm pt-1 border-t border-gray-200 mt-2"),
        ],
        className="bg-gray-50 rounded-xl p-5 space-y-2",
    )
    fa_3_4 = html.Div([
        html.H3("3.4. Residual value", className="text-base font-bold text-gray-900 mb-3"),
        html.Div([
            html.P("Residual value of each investment variant is calculated separately based on the inputs provided in the Capital expenditures and Replacement costs tables. All capital expenditures incurred during the investment phase (i.e. between Start of investment period and End of investment period) are aggregated within each CAPEX category defined by the user and depreciated annually using the applicable depreciation rate for that category. Depreciation for these costs begins in the first year of the operational period and continues until the end of the reference period or until the asset category is fully depreciated, whichever occurs first."),
            html.P("For replacement costs incurred during any year of the operational phase, depreciation begins in the following year of the analysis, using the same approach and depreciation rate applied to the corresponding cost category in capital expenditures. If the reference period ends before a replacement cost is fully depreciated, the net value of the asset (i.e. the original cost reduced by the accumulated depreciation) is added to the project variant’s residual value."),
            html.P("In the financial analysis, the values of capital expenditures and replacement costs used to calculate depreciation and residual value may be adjusted automatically by the tool depending on the user’s selections in Data types and based on VAT recoverability:"),
            fa_3_4_table,
            html.P("In the economic analysis, all capital expenditures and replacement costs are converted into net values and the residual value calculations are performed using these values (regardless of chosen Input and Output data types or VAT recoverability settings; however, if Current prices are selected, inflation adjustments may still affect the calculations)."),
        ], className="space-y-4 text-sm text-gray-600 leading-relaxed"),
    ], className="mb-8")

    fa_3_5_steps = [
        "General assumptions are established and financial data is entered.",
        "Inflation adjustments — if Current prices are selected, the tool adjusts all relevant input values for inflation.",
        "Input and Output data types adjustments — if the analysis requires a net→gross or gross→net conversion, the tool applies the appropriate adjustment. Wages and salaries are always converted to gross values when necessary.",
        "VAT recoverability — if the implementing entity is unable to recover VAT for any cost category, gross values for these expenditures are used in all financial calculations, regardless of the selected Input and Output data type.",
        "Cash flow aggregation — all positive and negative cash flows are summed separately for each variant, including Variant 0.",
        "Differential cash flow calculation and financial indicators — cash flows of the baseline scenario (Variant 0) are subtracted from each investment variant. The financial indicators are then calculated using these differential cash flows (e.g. Variant 1 — Variant 0; Variant 2 — Variant 0, etc.).",
    ]
    fa_3_5 = html.Div([
        html.H3("3.5. Summary of calculation steps in the financial analysis", className="text-base font-bold text-gray-900 mb-3"),
        html.Div([
            html.P("Applying the rules outlined in previous sections, the financial analysis follows these calculation steps:"),
            html.Ol([
                html.Li([
                    html.Span(str(i + 1), className="flex-shrink-0 w-6 h-6 rounded-full bg-accent1/10 text-accent1 text-xs font-bold flex items-center justify-center mt-0.5"),
                    html.Span(step),
                ], className="flex gap-3")
                for i, step in enumerate(fa_3_5_steps)
            ], className="space-y-3 pl-4"),
        ], className="space-y-4 text-sm text-gray-600 leading-relaxed"),
    ])

    financial_analysis = _ecba_section("financial-analysis", "Financial Analysis", [fa_intro, fa_3_1, fa_3_2, fa_3_3, fa_3_4, fa_3_5])

    # ── Economic Analysis ────────────────────────────────────────────────
    ea_intro = html.Div([
        html.P("Evaluating economic costs, benefits, non-market impacts, and externalities in the context of cost-benefit analysis is a complex and data-intensive process. Such analyses are typically intricate and require extensive data collection and research before aggregated values can be incorporated into decision-making tools. Sector-specific variability, unique project characteristics, and the need for comprehensive data across sectors and regions make standardization particularly challenging. These calculations fall outside the scope of what the eCBA tool currently accommodates. However, this does not mean that they should be omitted, as project proposers are expected to conduct these assessments and document them appropriately in the background materials accompanying the eCBA inputs."),
        html.P("The current release of the eCBA tool does not request a BAU economic value stream, but instead asks only for the incremental valuation of economic costs and benefits. This approach was chosen to avoid excessive complexity and potential confusion for users conducting foundational CBA. In a full breakdown, these series would typically be presented in detailed economic benefit modelling worksheets. However, in many cases, calculation methods produce only incremental values, and requiring BAU and project values to be separated would have necessitated an additional workflow."),
        html.P("Future releases of the eCBA are considering the introduction of a user workflow that allows both series — BAU and with-project — to be entered separately, with the tool then calculating the resulting incremental values. This functionality is intended primarily for more advanced users, including those working with detailed valuation of climate change adaptation and resilience measures."),
    ], className="space-y-4 text-sm text-gray-600 leading-relaxed mb-8")

    ea_4_1 = html.Div([
        html.H3("4.1. General approach", className="text-base font-bold text-gray-900 mb-3"),
        html.Div([
            html.P("As the eCBA tool is intended to function as a universal instrument applicable globally across diverse project types and sectors, it is not feasible to provide a uniform framework for the detailed and often project-specific calculations required, e.g. related to demand estimation or valuation of economic benefits, costs, externalities or non-market impacts. Therefore, a simplified and more flexible approach was chosen."),
            html.P("The economic analysis in the tool builds upon the financial analysis by automatically converting or adjusting the financial cash flows generated from the user’s inputs. The tool also provides space for users to add monetized benefits, costs, non-market impacts and externalities arising from project implementation. These entries are treated as additional positive or negative cash flows and are incorporated into the adjusted or converted financial cash flows."),
            html.P("Economic indicators are then calculated based on the resulting differential cash flows, using the same methodology applied in the financial analysis."),
        ], className="space-y-4 text-sm text-gray-600 leading-relaxed"),
    ], className="mb-8")

    ea_4_2_items = [
        ("Removal of taxes", "All taxes are removed from capital expenditures, replacement costs, operational expenditures, and revenues — regardless of the choices made in Input and Output data types or VAT recoverability settings."),
        ("Exception for wages and salaries", "Wages and salaries are exempt from tax removal — the full employer cost is always retained."),
        ("Residual value adjustments", "Residual value is recalculated using the adjusted (tax-removed) or converted (net) capital expenditures and replacement costs."),
        ("Integration of additional economic items", "All identified benefits, costs, non-market impacts and externalities are added to the positive or negative cash flows, depending on their nature."),
        ("Application of general rules", "The same rules used in the financial analysis apply regarding general assumptions, Constant or Current prices option, residual value calculations, and the differential cash flows method."),
        ("Calculation of economic indicators", "Economic indicators are calculated based on the newly derived differential cash flows."),
    ]
    ea_4_2 = html.Div([
        html.H3("4.2. From financial to economic analysis", className="text-base font-bold text-gray-900 mb-3"),
        html.Div([
            html.P("The tool applies several rules when converting or adjusting data provided in the financial analysis. These rules are as follows:"),
            html.Ul([
                html.Li([
                    html.Span("•", className="text-accent1 flex-shrink-0 mt-0.5"),
                    html.Span([html.Strong(f"{title}:", className="text-gray-800"), f" {desc}"]),
                ], className="flex gap-2")
                for title, desc in ea_4_2_items
            ], className="space-y-3 pl-4"),
        ], className="space-y-4 text-sm text-gray-600 leading-relaxed"),
    ])

    economic_analysis = _ecba_section("economic-analysis", "Economic Analysis", [ea_intro, ea_4_1, ea_4_2])

    # ── Summary ──────────────────────────────────────────────────────────
    summary = _ecba_section("summary", "Summary", [
        html.Div([
            html.P("Completing a foundational project CBA is a prerequisite for addressing advanced climate change considerations, particularly those related to damage and loss risks (D&L). Climate change mitigation can be assessed by applying a shadow price for carbon; however, it is equally important to understand how differential calculations are conducted between the BAU scenario and Variant 1 (e.g. comparing diesel versus an electric train scenario)."),
            html.P("Within the project appraisal framework, users may also be asked to provide a qualitative assessment of potential climate-related risks and possible mitigation options, including their implications for financial series. The Climate Change Screening and the detailed CBA guidance offer further support for this more quantitative approach and are documented in accompanying manuals."),
            html.P("Ultimately, completing the basic project profile within the online CBA tool is a necessary precondition for undertaking any climate-informed CBA exercises."),
        ], className="space-y-4 text-sm text-gray-600 leading-relaxed"),
        html.Div([
            html.P("Ready to try the eCBA tool?", className="text-sm text-gray-700 mb-4"),
            html.A(
                ["Launch eCBA Tool", Icon("external_link", size=16, color="#FFFFFF")],
                href="https://www.gpbp-ecba.app/", target="_blank", rel="noopener noreferrer",
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded bg-accent1 text-white text-sm font-semibold hover:bg-accent1/90 transition-colors",
            ),
        ], className="mt-10 p-6 rounded-xl bg-accent1/5 border border-accent1/20"),
    ])

    article = html.Article(
        [introduction, project_details, general_assumptions, financial_analysis, economic_analysis, summary],
        className="flex-1 min-w-0 prose-headings:scroll-mt-32",
    )

    return html.Div([
        hero,
        html.Div(
            className="bg-white py-16",
            children=html.Div(
                html.Div([EcbaMethodologyNav(), article], className="flex gap-16 items-start"),
                className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            ),
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


def _greening_label(text):
    """SectionLabel component from app/greening-development/page.tsx —
    a small uppercase kicker distinct from the shared SectionHeading."""
    return html.Span(text, className="inline-block text-xs font-bold tracking-widest uppercase text-accent2 mb-4")


def greening_development_page():
    hero = html.Section(
        id="greening-hero", className="pt-44 pb-16 relative overflow-hidden",
        style={"background": "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(55,179,127,0.18) 0%, transparent 65%), #0A0E1A"},
        children=[
            GridOverlay(),
            html.Div(
                className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                children=html.Div(
                    className="max-w-3xl",
                    children=[
                        _greening_label("Greening Development"),
                        html.H1("Public Finances & State Owned Enterprises (SOEs) For Greening Development",
                                className="text-4xl sm:text-5xl font-bold text-white leading-tight mb-6"),
                        html.P("Implementing a whole-of-public-sector approach to deliver greater prosperity and sustainable development through the design and implementation of better expenditure, regulatory, and taxation policies and practices.",
                               className="text-lg text-white/70 leading-relaxed mb-10"),
                        html.Div(className="flex flex-wrap gap-4", children=[
                            dcc.Link("Upcoming Events", href="?page=events",
                                     className="inline-flex items-center gap-2 px-6 py-3 rounded bg-accent2 text-white font-semibold hover:bg-accent2/90 transition-colors"),
                            html.A("Why Greening Development?", href="#why-greening",
                                   className="inline-flex items-center gap-2 px-6 py-3 rounded border border-white/30 text-white font-semibold hover:bg-white/10 transition-colors"),
                        ]),
                    ],
                ),
            ),
        ],
    )

    why_greening = html.Section(
        id="why-greening", className="py-20 bg-surface",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=html.Div(
                className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center",
                children=[
                    html.Div([
                        _greening_label("Why"),
                        html.H2("Why Greening Development?", className="text-3xl sm:text-4xl font-bold text-white mb-6"),
                        html.Div([
                            html.P("Advancing climate action and achieving green growth \u2014 what we refer to as 'greening development' \u2014 are global priorities that require tailored interventions and holistic approaches."),
                            html.P("Green growth enables economic development that is resource efficient, low-carbon, and socially inclusive. Investing in clean energy, resilient infrastructure, and sustainable land use can reduce greenhouse gas emissions, boost local competitiveness, and generate new economic opportunities."),
                            html.P("At the same time, effective climate action safeguards long-term economic productivity by minimising the risks and costs of climate-related shocks."),
                        ], className="space-y-4 text-white/70 leading-relaxed"),
                    ]),
                    html.Div(
                        html.Img(src=asset("images/greening/vdkc-2.png"), alt="", className="w-full h-full object-contain"),
                        className="rounded-xl overflow-hidden aspect-[4/3] relative",
                    ),
                ],
            ),
        ),
    )

    whole_of_gov = html.Section(
        className="py-20 bg-gray-50",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=html.Div(
                className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center",
                children=[
                    html.Div(
                        html.Img(src=asset("images/greening/vdkc-3.png"), alt="", className="w-full h-full object-contain"),
                        className="rounded-xl overflow-hidden aspect-[4/3] relative order-2 lg:order-1",
                    ),
                    html.Div([
                        _greening_label("Approach"),
                        html.H2("Why a whole-of-government approach?", className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6"),
                        html.Div([
                            html.P("Tackling greening development challenges and unlocking opportunities for green growth and climate action requires individual countries to design and implement policies that align with their unique development contexts."),
                            html.P("Beyond central government, sub-national authorities and state-owned enterprises (SOEs) also need to be engaged. Their participation is essential for scaling climate action from policy design through to on-the-ground implementation."),
                            html.P("Three factors are critical for success: country demand and ownership; strong organisational capabilities and skilled public sector staff; and modernised, digital information systems \u2014 harnessing innovations like big data and artificial intelligence."),
                        ], className="space-y-4 text-gray-500 leading-relaxed"),
                        html.Div(
                            html.A("Engagement Framework", href="#framework",
                                   className="inline-flex items-center gap-2 px-6 py-3 rounded border border-accent1 text-accent1 font-semibold hover:bg-accent1 hover:text-white transition-colors"),
                            className="mt-8",
                        ),
                    ], className="order-1 lg:order-2"),
                ],
            ),
        ),
    )

    vdkc_callout = html.Section(
        className="py-10 bg-gray-50",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=html.Div(
                className="rounded-xl border border-accent1/20 bg-accent1/5 p-8 flex flex-col sm:flex-row items-start sm:items-center gap-6 justify-between",
                children=[
                    html.P([
                        "The Vienna Development Knowledge Centre (VDKC) also promotes awareness, application, and the adoption of online decision-support tools for better climate actions. Operational tools such as the Geospatial Planning and Budgeting Platform (GPBP) \u2014 which can be found on ",
                        html.Span("pim-pam.net", className="font-semibold text-accent1"),
                        " \u2014 can help countries maximise opportunities through user-friendly, openly disseminated methods and tools.",
                    ], className="text-gray-700 leading-relaxed max-w-3xl"),
                    dcc.Link("Explore Tools", href="?page=digital-tools",
                             className="flex-shrink-0 inline-flex items-center gap-2 px-5 py-2.5 rounded bg-accent1 text-white text-sm font-semibold hover:bg-accent1/90 transition-colors"),
                ],
            ),
        ),
    )

    framework_cards = html.Div(
        [
            html.Div([
                html.Div(Icon(card["icon"], size=24, color=C.COLORS["accent1"]),
                          className="w-12 h-12 rounded-lg bg-accent1/10 flex items-center justify-center text-accent1 flex-shrink-0"),
                html.Div([
                    html.H3(card["title"], className="text-base font-bold text-gray-900 mb-2"),
                    html.P(card["desc"], className="text-sm text-gray-500 leading-relaxed"),
                ]),
            ], className="flex flex-col gap-4 p-6 rounded-xl border border-gray-200 bg-white hover:border-accent1/30 transition-colors")
            for card in C.GREENING_FRAMEWORK_CARDS
        ],
        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6",
    )
    framework_section = html.Section(
        id="framework", className="py-20 bg-white",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=[
                html.Div([
                    _greening_label("Framework"),
                    html.H2("The Vienna Development Knowledge Centre Public Finance and SOEs Engagement Framework",
                            className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4"),
                    html.P("The VDKC Public Finance and SOEs Engagement Framework applies the whole-of-government approach to achieving country-level results for greening development. It offers a structure and pathway for governments and development practitioners to translate policy into action.",
                           className="text-gray-500 leading-relaxed"),
                ], className="max-w-3xl mb-12"),
                framework_cards,
            ],
        ),
    )

    how_it_works = html.Section(
        className="greening-how-it-works relative overflow-hidden border-y border-white/10",
        style={
            "backgroundImage": f"url('{asset('images/greening/how-it-works-bg.jpg')}')",
            "backgroundSize": "cover",
            "backgroundPosition": "center center",
            "backgroundRepeat": "no-repeat",
            "paddingTop": "96px",
            "paddingBottom": "96px",
            "minHeight": "560px",
        },
        children=[
            html.Div(className="absolute inset-0", style={"background": "rgba(5, 12, 18, 0.28)"}),
            html.Div(
                className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-center",
                children=html.Div(
                    className="greening-how-it-works-card w-full max-w-3xl border border-white/30 px-10 py-10 sm:px-14 sm:py-12",
                    style={
                        "background": "rgba(239, 244, 241, 0.84)",
                        "backdropFilter": "blur(8px)",
                        "WebkitBackdropFilter": "blur(8px)",
                        "borderRadius": "12px",
                        "paddingLeft": "40px",
                        "paddingRight": "40px",
                    },
                    children=[
                        _greening_label("How It Works"),
                        html.H2(
                            "How does it work?",
                            className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6",
                        ),
                        html.Div(
                            [
                                html.P(
                                    "The foundational departure point of the VDKC Engagement Framework is that national, sub-national, and SOE institutional sectors are all critical to delivering on greening development across the ECA region.",
                                    className="text-gray-700 leading-relaxed text-base sm:text-lg text-left",
                                ),
                                html.P(
                                    "The outcome framework builds on the premise that a combination of taxation, expenditure, and regulatory measures can help deliver climate action and green growth objectives. The public sector depends on adequate policies, but above all the capabilities to deliver on those policies.",
                                    className="text-gray-700 leading-relaxed text-base sm:text-lg text-left",
                                ),
                            ],
                            className="space-y-5 text-gray-700 leading-relaxed",
                        ),
                    ],
                ),
            ),
        ],
    )

    results_framework = html.Section(
        className="py-20 bg-white",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=[
                html.Div([
                    _greening_label("Results"),
                    html.H2("Results Framework", className="text-3xl sm:text-4xl font-bold text-gray-900"),
                ], className="max-w-2xl mb-10"),
                html.Div(
                    html.Img(src=asset("images/greening/results-framework.png"), alt="Results Framework", className="w-full h-full object-contain"),
                    className="w-full rounded-xl overflow-hidden border border-gray-200 relative aspect-[16/7]",
                ),
            ],
        ),
    )

    public_infra = html.Section(
        className="py-20 bg-gray-50",
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=html.Div(
                className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center",
                children=[
                    html.Div(
                        html.Img(src=asset("images/greening/vdkc-4.png"), alt="", className="w-full h-full object-contain"),
                        className="rounded-xl overflow-hidden aspect-[4/3] relative",
                    ),
                    html.Div([
                        html.H2("Public infrastructure investment and non-financial asset governance are critical in green transition trajectories.",
                                className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6"),
                        html.Div([
                            html.P("Infrastructure investment decisions carry long-term implications. Failing to account for climate risk in planning and budgeting cycles leads to stranded assets, increased fiscal exposure, and missed opportunities for sustainable development."),
                            html.P("The VDKC approach integrates people, processes, and technology to embed climate considerations into public investment management \u2014 from project appraisal through to asset lifecycle management and performance reporting."),
                        ], className="space-y-4 text-gray-500 leading-relaxed"),
                    ]),
                ],
            ),
        ),
    )

    soes_section = html.Section(
        className="py-20",
        style={"background": "radial-gradient(ellipse 80% 80% at 20% 50%, rgba(55,179,127,0.15) 0%, transparent 60%), #0A0E1A"},
        children=html.Div(
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            children=html.Div([
                html.H2("State-owned enterprises (SOEs) play a critical role in mitigating climate change and advancing green economies due to their scale, strategic sectors, and public mandates.",
                        className="text-3xl sm:text-4xl font-bold text-white mb-6"),
                html.Div([
                    html.P("Operating in key areas like energy, transport, and water, SOEs control significant emissions and infrastructure investments, positioning them as essential drivers of sustainable economic transformation \u2014 provided they have the right governance structures, incentives, and capabilities in place."),
                    html.P("The VDKC activity has special emphasis on building SOE Community of Practice in Report 2025 for the European Europe and Central Asia (ECA) region to better address the challenges and opportunities."),
                ], className="space-y-4 text-white/70 leading-relaxed"),
            ], className="max-w-3xl"),
        ),
    )

    return html.Div([
        hero, why_greening, whole_of_gov, vdkc_callout, framework_section,
        how_it_works, results_framework, public_infra, soes_section,
    ])


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


EVENT_FORMAT_LABELS = {"in-person": "In-Person", "virtual": "Virtual", "hybrid": "Hybrid"}
EVENT_FORMAT_COLORS = {"in-person": "bg-accent2/15 text-accent2", "virtual": "bg-accent1/15 text-accent1", "hybrid": "bg-accent4/15 text-accent4"}


def events_page():
    hero = _hero_section(
        "events-hero",
        "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(55,179,127,0.18) 0%, transparent 65%)",
        "Events", "Upcoming events",
        "Workshops, training sessions, and conferences on public investment management, public asset management, and greening development.",
    )
    cards = html.Div([EventCard(e) for e in C.EVENTS], className="grid grid-cols-1 md:grid-cols-2 gap-6")
    return html.Div([
        hero,
        html.Div(
            className="py-16 bg-white",
            children=html.Div(cards, className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"),
        ),
    ])


def event_detail_page(slug):
    event = next((e for e in C.EVENTS if e["slug"] == slug), None)
    if not event:
        logger.warning("event_detail_page: no event found for slug=%r — rendering 404.", slug)
        return not_found_page()

    detail = event.get("detail")

    format_badge = None
    if event.get("format"):
        format_badge = html.Div(
            html.Span(
                EVENT_FORMAT_LABELS.get(event["format"], event["format"]),
                className=f"inline-block text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full {EVENT_FORMAT_COLORS.get(event['format'], 'bg-white/10 text-white/70')}",
            ),
            className="mb-6",
        )

    meta_row = html.Div(
        className="flex flex-wrap gap-5 text-sm text-white/60",
        children=[
            html.Div([Icon("calendar", size=15, color=C.COLORS["accent2"]), html.Span(event.get("dateLabel") or event["date"])],
                     className="flex items-center gap-2"),
        ] + ([html.Div([Icon("map_pin", size=15, color=C.COLORS["accent2"]), html.Span(event["location"])],
                       className="flex items-center gap-2")] if event.get("location") else []),
    )

    hero = html.Section(
        className="relative overflow-hidden bg-bg",
        style={"paddingTop": "160px", "paddingBottom": "56px"},  # pt-40 / pb-14
        children=[
            html.Div(
                className="absolute inset-0",
                style={
                    "backgroundImage": f"url('{asset('images/events/' + event['slug'] + '.jpg')}')",
                    "backgroundColor": "#0A0E1A",
                    "backgroundSize": "cover",
                    "backgroundPosition": "center center",
                    "backgroundRepeat": "no-repeat",
                    "transform": "scale(1.08)",
                },
            ),
            html.Div(className="absolute inset-0", style={
                "background": "linear-gradient(180deg, rgba(8, 12, 19, 0.80) 95%, rgba(8, 12, 19, 0.62) 95%, rgba(8, 12, 19, 0.86) 95%)"
            }),
            GridOverlay(),
            html.Div(
                className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8",
                children=[
                    dcc.Link([Icon("arrow_left", size=14, color=C.COLORS["muted"]), " All Events"], href="?page=events",
                             className="inline-flex items-center gap-2 text-sm text-muted hover:text-text transition-colors mb-5"),
                    format_badge,
                    html.H1(event["title"], className="text-3xl sm:text-4xl font-bold text-white leading-tight mb-6"),
                    meta_row,
                ],
            ),
        ],
    )

    if not detail:
        body = html.Div(
            html.Div(html.P(event["description"], className="text-gray-500"),
                      className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8"),
            className="bg-white py-20",
        )
        return html.Div([hero, body])

    sections = []

    sections.append(html.Section([
        html.H2("About the Event", className="text-xs font-bold uppercase tracking-widest text-accent2 mb-5"),
        html.Div([html.P(p) for p in detail.get("aboutParagraphs", [])], className="space-y-4 text-gray-500 leading-relaxed"),
    ]))

    if detail.get("objectivesIntro") or detail.get("objectives"):
        obj_children = [html.H2("Objectives & Target Audience", className="text-xs font-bold uppercase tracking-widest text-accent2 mb-5")]
        if detail.get("objectivesIntro"):
            obj_children.append(html.P(detail["objectivesIntro"], className="text-gray-500 leading-relaxed mb-5"))
        if detail.get("objectives"):
            obj_children.append(html.Ul([
                html.Li([html.Span(className="mt-1.5 flex-shrink-0 w-1.5 h-1.5 rounded-full bg-accent2"), obj],
                        className="flex gap-3 text-gray-500 leading-relaxed")
                for obj in detail["objectives"]
            ], className="space-y-3"))
        sections.append(html.Section(obj_children))

    if detail.get("format"):
        sections.append(html.Section([
            html.H2("Format", className="text-xs font-bold uppercase tracking-widest text-accent2 mb-5"),
            html.P(detail["format"], className="text-gray-500 leading-relaxed"),
        ]))

    if detail.get("summary"):
        summary_children = [html.H2("Event Summary", className="text-xs font-bold uppercase tracking-widest text-accent2")]
        for sec in detail["summary"]:
            summary_children.append(html.Div([
                html.H3(sec["title"], className="text-lg font-bold text-gray-900 mb-3"),
                html.Div([html.P(p) for p in sec["paragraphs"]], className="space-y-3 text-gray-500 leading-relaxed"),
            ]))
        sections.append(html.Section(summary_children, className="space-y-8"))

    if detail.get("agenda"):
        sections.append(html.Section([
            html.H2("Event Agenda", className="text-xs font-bold uppercase tracking-widest text-accent2 mb-6"),
            AgendaAccordion(detail["agenda"], group_name=f"agenda-{slug}"),
        ]))

    if detail.get("links"):
        sections.append(html.Section([
            html.H2("Key Resources", className="text-xs font-bold uppercase tracking-widest text-accent2 mb-5"),
            html.Div([
                html.A([link["label"], Icon("arrow", size=14, color=C.COLORS["accent1"])],
                       href=link["href"], target="_blank", rel="noopener noreferrer",
                       className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-200 bg-white text-sm font-medium text-accent1 hover:border-accent1/40 hover:bg-accent1/5 transition-colors")
                for link in detail["links"]
            ], className="flex flex-wrap gap-3"),
        ]))

    if detail.get("notes"):
        sections.append(html.Section([
            html.H2("Please Note", className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4"),
            html.Ul([
                html.Li([html.Span(className="mt-1.5 flex-shrink-0 w-1.5 h-1.5 rounded-full bg-gray-400"), note],
                        className="flex gap-3 text-sm text-gray-500")
                for note in detail["notes"]
            ], className="space-y-2"),
        ], className="rounded-lg bg-gray-50 border border-gray-200 p-6"))

    if detail.get("references"):
        ref_items = []
        for ref in detail["references"]:
            m = re.search(r"(https?://\S+)", ref)
            url = m.group(1) if m else None
            text = ref.replace(url, "").strip() if url else ref
            ref_items.append(html.Li([
                html.Span(className="mt-2 flex-shrink-0 w-1 h-1 rounded-full bg-gray-300"),
                html.Span([text, html.A(url, href=url, target="_blank", rel="noopener noreferrer",
                                          className="ml-1 text-accent1 hover:underline break-all") if url else None]),
            ], className="flex gap-3 text-sm text-gray-500 leading-relaxed"))
        sections.append(html.Section([
            html.H2("Selected References", className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4"),
            html.Ul(ref_items, className="space-y-3"),
        ]))

    if detail.get("organizers"):
        sections.append(html.Section([
            html.H2("Organisers & Supporters", className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-3"),
            html.P(detail["organizers"], className="text-sm text-gray-500 leading-relaxed"),
        ], className="border-t border-gray-100 pt-10"))

    body = html.Div(
        html.Div(sections, className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-14"),
        className="bg-white",
    )
    return html.Div([hero, body])


def downloads_page():
    hero = _hero_section(
        "downloads-hero",
        "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(67,69,170,0.2) 0%, transparent 65%)",
        "Downloads", "Knowledge resources",
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
        view = (query.get("view", [None])[0] or "").strip().lower()
        if view == "ecba-methodology":
            logger.info("Routing to eCBA Methodology page.")
            return ecba_methodology_page()
        return digital_tools_page()
    if page == "infragov":
        return infragov_page()
    if page == "greening-development":
        return greening_development_page()
    if page == "digital-academy":
        return digital_academy_page()
    if page == "events":
        slug = query.get("slug", [None])[0]
        if slug:
            logger.info("Routing to event detail, slug=%r", slug)
            return event_detail_page(slug)
        return events_page()
    if page in ("downloads", "resources"):
        # "resources" kept as a backward-compatible alias — the footer
        # and old bookmarks still use "?page=resources"; the nav dropdown
        # itself links to "?page=downloads" (Nav.tsx's Resources > Downloads).
        return downloads_page()
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