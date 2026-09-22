"""
constants.py
============
All constant values, design tokens, content data, and raw SVG path data used
throughout the PIM-PAM Dash site. Mirrors the original Next.js project's
`tailwind.config.ts`, `app/globals.css`, and `content/*.ts` files 1:1.

Nothing in this file builds Dash components — see utils.py for that.
"""

# ──────────────────────────────────────────────────────────────────────────
# DESIGN TOKENS  (mirrors tailwind.config.ts + app/globals.css :root vars)
# ──────────────────────────────────────────────────────────────────────────
COLORS = {
    "bg": "#0A0E1A",
    "surface": "#121829",
    "surface_2": "#1A2237",
    "text": "#E6EAF2",
    "muted": "#8A93A8",
    "accent1": "#4345aa",   # blue/indigo
    "accent2": "#37b37f",   # green
    "accent3": "#64cbd6",   # teal/cyan
    "accent4": "#f26b23",   # orange
    "white": "#FFFFFF",
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_700": "#374151",
    "gray_900": "#111827",
}

FONT_SANS = "'Inter', system-ui, sans-serif"
FONT_HEADING = "'Fira Sans', system-ui, sans-serif"

GOOGLE_FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Fira+Sans:wght@700;800;900&family=Inter:wght@300;400;500;600;700&display=swap"
)

# Tailwind Play-CDN theme config, injected client-side so we can reuse the
# exact same utility className strings the original React components used
# (bg-bg, text-accent1, bg-surface-2, etc.)
TAILWIND_CONFIG_JS = """
tailwind.config = {
  theme: {
    extend: {
      colors: {
        bg: '#0A0E1A',
        surface: '#121829',
        'surface-2': '#1A2237',
        text: '#E6EAF2',
        muted: '#8A93A8',
        accent1: '#4345aa',
        accent2: '#37b37f',
        accent3: '#64cbd6',
        accent4: '#f26b23',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Fira Sans', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-brand': 'linear-gradient(135deg, #4345aa, #64cbd6)',
        'gradient-brand-r': 'linear-gradient(135deg, #64cbd6, #4345aa)',
        'gradient-hero': 'radial-gradient(ellipse 80% 60% at 50% -10%, rgba(67,69,170,0.35) 0%, transparent 70%), linear-gradient(180deg, #0A0E1A 0%, #0A0E1A 100%)',
        'gradient-card': 'linear-gradient(135deg, rgba(67,69,170,0.06), rgba(100,203,214,0.06))',
      },
      boxShadow: {
        glow: '0 0 40px rgba(67,69,170,0.25)',
        'glow-teal': '0 0 40px rgba(100,203,214,0.15)',
        'glow-green': '0 0 40px rgba(55,179,127,0.15)',
        card: '0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06)',
      },
      animation: {
        'fade-up': 'fadeUp 0.6s ease forwards',
        'fade-in': 'fadeIn 0.5s ease forwards',
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: 0, transform: 'translateY(24px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
      },
    },
  },
}
"""

# ──────────────────────────────────────────────────────────────────────────
# RAW SVG PATH DATA  (copied verbatim from the original .tsx source so the
# icons render pixel-identically). Fill-style icons: single/multi "d" path
# list, drawn with fill="currentColor" equivalent (explicit hex at render
# time, see utils.icon()). Stroke-style icons mimic lucide-react's default
# stroke rendering (fill="none", stroke=color, stroke-width=2, round caps).
# ──────────────────────────────────────────────────────────────────────────

ICONS_FILL = {
    # components/IconArrow.tsx
    "arrow": ["M16.0037 9.41421L7.39712 18.0208L5.98291 16.6066L14.5895 8H7.00373V6H18.0037V17H16.0037V9.41421Z"],
    # components/DimensionCarousel.tsx ChevLeft / ChevRight
    "chevron_left": ["M10.8284 12.0007L15.7782 16.9504L14.364 18.3646L8 12.0007L14.364 5.63672L15.7782 7.05093L10.8284 12.0007Z"],
    "chevron_right": ["M13.1717 12.0007L8.22192 7.05093L9.63614 5.63672L16.0001 12.0007L9.63614 18.3646L8.22192 16.9504L13.1717 12.0007Z"],
    # components/DimensionGrid.tsx — 8 Must-Have icons
    "guidance": ["M13 21V23H11V21H3C2.44772 21 2 20.5523 2 20V4C2 3.44772 2.44772 3 3 3H9C10.1947 3 11.2671 3.52375 12 4.35418C12.7329 3.52375 13.8053 3 15 3H21C21.5523 3 22 3.44772 22 4V20C22 20.5523 21.5523 21 21 21H13ZM20 19V5H15C13.8954 5 13 5.89543 13 7V19H20ZM11 19V7C11 5.89543 10.1046 5 9 5H4V19H11Z"],
    "appraisal": ["M4 2H20C20.5523 2 21 2.44772 21 3V21C21 21.5523 20.5523 22 20 22H4C3.44772 22 3 21.5523 3 21V3C3 2.44772 3.44772 2 4 2ZM5 4V20H19V4H5ZM7 6H17V10H7V6ZM7 12H9V14H7V12ZM7 16H9V18H7V16ZM11 12H13V14H11V12ZM11 16H13V18H11V16ZM15 12H17V18H15V12Z"],
    "review": ["M11 2C15.968 2 20 6.032 20 11C20 15.968 15.968 20 11 20C6.032 20 2 15.968 2 11C2 6.032 6.032 2 11 2ZM11 18C14.8675 18 18 14.8675 18 11C18 7.1325 14.8675 4 11 4C7.1325 4 4 7.1325 4 11C4 14.8675 7.1325 18 11 18ZM19.4853 18.0711L22.3137 20.8995L20.8995 22.3137L18.0711 19.4853L19.4853 18.0711Z"],
    "selection": ["M21 4V6H20L15 13.5V22H9V13.5L4 6H3V4H21ZM6.4037 6L11 12.8944V20H13V12.8944L17.5963 6H6.4037Z"],
    "implementation": ["M5 8V20H9V8H5ZM3 7L7 2L11 7V22H3V7ZM19 16V14H16V12H19V10H17V8H19V6H15V20H19V18H17V16H19ZM14 4H20C20.5523 4 21 4.44772 21 5V21C21 21.5523 20.5523 22 20 22H14C13.4477 22 13 21.5523 13 21V5C13 4.44772 13.4477 4 14 4Z"],
    "adjustment": ["M5.46257 4.43262C7.21556 2.91688 9.5007 2 12 2C17.5228 2 22 6.47715 22 12C22 14.1361 21.3302 16.1158 20.1892 17.7406L17 12H20C20 7.58172 16.4183 4 12 4C9.84982 4 7.89777 4.84827 6.46023 6.22842L5.46257 4.43262ZM18.5374 19.5674C16.7844 21.0831 14.4993 22 12 22C6.47715 22 2 17.5228 2 12C2 9.86386 2.66979 7.88416 3.8108 6.25944L7 12H4C4 16.4183 7.58172 20 12 20C14.1502 20 16.1022 19.1517 17.5398 17.7716L18.5374 19.5674Z"],
    "operation": ["M5.32943 3.27158C6.56252 2.8332 7.9923 3.10749 8.97927 4.09446C9.96652 5.08171 10.2407 6.51202 9.80178 7.74535L20.6465 18.5902L18.5252 20.7115L7.67936 9.86709C6.44627 10.3055 5.01649 10.0312 4.02952 9.04421C3.04227 8.05696 2.7681 6.62665 3.20701 5.39332L5.44373 7.63C6.02952 8.21578 6.97927 8.21578 7.56505 7.63C8.15084 7.04421 8.15084 6.09446 7.56505 5.50868L5.32943 3.27158ZM15.6968 5.15512L18.8788 3.38736L20.293 4.80157L18.5252 7.98355L16.7574 8.3371L14.6361 10.4584L13.2219 9.04421L15.3432 6.92289L15.6968 5.15512ZM8.62572 12.9333L10.747 15.0546L5.79729 20.0044C5.2115 20.5902 4.26175 20.5902 3.67597 20.0044C3.12464 19.453 3.09221 18.5793 3.57867 17.99L3.67597 17.883L8.62572 12.9333Z"],
    "evaluation": ["M3 3H21C21.5523 3 22 3.44772 22 4V20C22 20.5523 21.5523 21 21 21H3C2.44772 21 2 20.5523 2 20V4C2 3.44772 2.44772 3 3 3ZM4 5V19H20V5H4ZM7 13H9V17H7V13ZM11 7H13V17H11V7ZM15 10H17V17H15V10Z"],
    # components/ToolIcons.tsx
    "data_analytics": ["M11 19V9H4V19H11ZM11 7V4C11 3.44772 11.4477 3 12 3H21C21.5523 3 22 3.44772 22 4V20C22 20.5523 21.5523 21 21 21H3C2.44772 21 2 20.5523 2 20V8C2 7.44772 2.44772 7 3 7H11ZM13 5V19H20V5H13ZM5 16H10V18H5V16ZM14 16H19V18H14V16ZM14 13H19V15H14V13ZM14 10H19V12H14V10ZM5 13H10V15H5V13Z"],
    "geospatial": ["M16 16C17.6569 16 19 17.3431 19 19C19 20.6569 17.6569 22 16 22C14.3431 22 13 20.6569 13 19C13 17.3431 14.3431 16 16 16ZM6 12C8.20914 12 10 13.7909 10 16C10 18.2091 8.20914 20 6 20C3.79086 20 2 18.2091 2 16C2 13.7909 3.79086 12 6 12ZM16 18C15.4477 18 15 18.4477 15 19C15 19.5523 15.4477 20 16 20C16.5523 20 17 19.5523 17 19C17 18.4477 16.5523 18 16 18ZM6 14C4.89543 14 4 14.8954 4 16C4 17.1046 4.89543 18 6 18C7.10457 18 8 17.1046 8 16C8 14.8954 7.10457 14 6 14ZM14.5 2C17.5376 2 20 4.46243 20 7.5C20 10.5376 17.5376 13 14.5 13C11.4624 13 9 10.5376 9 7.5C9 4.46243 11.4624 2 14.5 2ZM14.5 4C12.567 4 11 5.567 11 7.5C11 9.433 12.567 11 14.5 11C16.433 11 18 9.433 18 7.5C18 5.567 16.433 4 14.5 4Z"],
    "generative_ai": ["M20.4668 8.69379L20.7134 8.12811C21.1529 7.11947 21.9445 6.31641 22.9323 5.87708L23.6919 5.53922C24.1027 5.35653 24.1027 4.75881 23.6919 4.57612L22.9748 4.25714C21.9616 3.80651 21.1558 2.97373 20.7238 1.93083L20.4706 1.31953C20.2942 0.893489 19.7058 0.893489 19.5293 1.31953L19.2761 1.93083C18.8442 2.97373 18.0384 3.80651 17.0252 4.25714L16.308 4.57612C15.8973 4.75881 15.8973 5.35653 16.308 5.53922L17.0677 5.87708C18.0555 6.31641 18.8471 7.11947 19.2866 8.12811L19.5331 8.69379C19.7136 9.10792 20.2864 9.10792 20.4668 8.69379ZM5.79993 16H7.95399L8.55399 14.5H11.4459L12.0459 16H14.1999L10.9999 8H8.99993L5.79993 16ZM9.99993 10.8852L10.6459 12.5H9.35399L9.99993 10.8852ZM15 16V8H17V16H15ZM3 3C2.44772 3 2 3.44772 2 4V20C2 20.5523 2.44772 21 3 21H21C21.5523 21 22 20.5523 22 20V11H20V19H4V5H14V3H3Z"],
    # components/FeedbackForm.tsx checkmark
    "checkmark": ["M10.0007 15.1709L19.1931 5.97852L20.6073 7.39273L10.0007 17.9993L3.63672 11.6354L5.05093 10.2212L10.0007 15.1709Z"],
    # app/resources/page.tsx
    "download": ["M13 10H18L12 16L6 10H11V3H13V10ZM4 19H20V12H22V20C22 20.5523 21.5523 21 21 21H3C2.44772 21 2 20.5523 2 20V12H4V19Z"],
    "pdf": ["M16 2L21 7V21C21 21.5523 20.5523 22 20 22H4C3.44772 22 3 21.5523 3 21V3C3 2.44772 3.44772 2 4 2H16ZM15 4H5V20H19V8H15V4ZM9 13V19H7V13H9ZM13 11V19H11V11H13ZM17 15V19H15V15H17Z"],
    # components/PimPamAiBanner.tsx
    "ai": ["M20.7134 8.12811L20.4668 8.69379C20.2864 9.10792 19.7136 9.10792 19.5331 8.69379L19.2866 8.12811C18.8471 7.11947 18.0555 6.31641 17.0677 5.87708L16.308 5.53922C15.8973 5.35653 15.8973 4.75881 16.308 4.57612L17.0252 4.25714C18.0384 3.80651 18.8442 2.97373 19.2761 1.93083L19.5293 1.31953C19.7058 0.893489 20.2942 0.893489 20.4706 1.31953L20.7238 1.93083C21.1558 2.97373 21.9616 3.80651 22.9748 4.25714L23.6919 4.57612C24.1027 4.75881 24.1027 5.35653 23.6919 5.53922L22.9323 5.87708C21.9445 6.31641 21.1529 7.11947 20.7134 8.12811ZM2 4C2 3.44772 2.44772 3 3 3H14V5H4V19H20V11H22V20C22 20.5523 21.5523 21 21 21H3C2.44772 21 2 20.5523 2 20V4ZM7 13H9V17H7V13ZM11 7H13V17H11V7ZM15 10H17V17H15V10Z"],
    # components/VideoCard.tsx PlayIcon (triangle)
    "play_triangle": ["M8 5v14l11-7z"],
    # app/greening-development/page.tsx — VDKC Engagement Framework cards
    "greening_legislative": ["M6 2H18C18.5523 2 19 2.44772 19 3V21C19 21.5523 18.5523 22 18 22H6C5.44772 22 5 21.5523 5 21V3C5 2.44772 5.44772 3 6 3ZM7 4V20H17V4H7ZM9 6H15V8H9V6ZM9 10H15V12H9V10ZM9 14H13V16H9V14Z"],
    "greening_institutional": ["M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11ZM12 13C8.13401 13 5 16.134 5 20H19C19 16.134 15.866 13 12 13Z"],
    "greening_digital": ["M3 3H21C21.5523 3 22 3.44772 22 4V20C22 20.5523 21.5523 21 21 21H3C2.44772 21 2 20.5523 2 20V4C2 3.44772 2.44772 3 3 3ZM4 5V19H20V5H4ZM7 9H9V15H7V9ZM11 7H13V15H11V7ZM15 11H17V15H15V11Z"],
    "greening_results": ["M12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2ZM12 4C7.58172 4 4 7.58172 4 12C4 16.4183 7.58172 20 12 20C16.4183 20 20 16.4183 20 12C20 7.58172 16.4183 4 12 4ZM11 7H13V11H17V13H11V7Z"],
}

ICONS_STROKE = {
    # lucide-react Menu
    "menu": '<line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="18" x2="20" y2="18"/>',
    # lucide-react X
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    # lucide-react ArrowUp
    "arrow_up": '<path d="M5 12l7-7 7 7"/><path d="M12 19V5"/>',
    # lucide-react ArrowLeft
    "arrow_left": '<path d="M12 19l-7-7 7-7"/><path d="M19 12H5"/>',
    # lucide-react ExternalLink
    "external_link": '<path d="M15 3h6v6"/><path d="M10 14L21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    # lucide-react Play
    "play": '<polygon points="6 3 20 12 6 21 6 3"/>',
    # lucide-react Calendar
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    # lucide-react MapPin
    "map_pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    # lucide-react ChevronDown  (AgendaAccordion.tsx)
    "chevron_down": '<path d="m6 9 6 6 6-6"/>',
    # lucide-react Clock  (MasterClassPage.tsx "At a Glance" tiles)
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    # lucide-react Users  (MasterClassPage.tsx "At a Glance" tiles)
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    # lucide-react GraduationCap  (MasterClassPage.tsx "At a Glance" tiles)
    "graduation_cap": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    # lucide-react Wrench  (MasterClassPage.tsx "At a Glance" tiles)
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94z"/>',
    # lucide-react MonitorSmartphone  (MasterClassPage.tsx "At a Glance" tiles)
    "monitor_smartphone": '<path d="M18 8V5c0-1-1-2-2-2H4C3 3 2 4 2 5v8c0 1 1 2 2 2h8"/><path d="M10 19v-3.96 3.15"/><path d="M7 19h5"/><rect x="16" y="12" width="6" height="10" rx="2"/>',
    # lucide-react Building2  (MasterClassPage.tsx "At a Glance" tiles)
    "building2": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
}

# ──────────────────────────────────────────────────────────────────────────
# NAVIGATION  (components/Nav.tsx)
#   Flat top-level nav links, no dropdown. "Feedback" isn't included —
#   it's still reachable from the footer only, same as the current live
#   site.
# ──────────────────────────────────────────────────────────────────────────
NAV_TOP_LINKS = [
    {"label": "Home", "href": "?page=home"},
    {"label": "Digital Tools", "href": "?page=digital-tools"},
    {"label": "InfraGov 2.0", "href": "?page=infragov", "badge": "New"},
    {"label": "Greening Development", "href": "?page=greening-development"},
    {"label": "Events", "href": "?page=events"},
    {"label": "Learning", "href": "?page=digital-academy"},
    {"label": "Resources", "href": "?page=downloads"},
]

# ──────────────────────────────────────────────────────────────────────────
# FOOTER  (components/Footer.tsx)
# ──────────────────────────────────────────────────────────────────────────
FOOTER_TOOL_LINKS = [
    {"label": "Country Benchmarking Dashboard", "href": "https://datanalytics.worldbank.org/country-benchmarking-dashboard/"},
    {"label": "eCBA Tool", "href": "https://www.gpbp-ecba.app/"},
    {"label": "Climate Change Screening", "href": "https://gpbp.adamplatform.eu/"},
    {"label": "Local Development Tracker", "href": "https://ldt.pim-pam.net"},
    {"label": "GoAT", "href": "https://datanalytics.worldbank.org/governance-operations-analytics-tool/"},
    {"label": "CLAD Database", "href": "https://design4climate.eu.pythonanywhere.com/"},
]

FOOTER_OTHER_LINKS = [
    {"label": "pim-pam.ai", "href": "https://pim-pam.ai", "external": True},
    {"label": "VDKC / PFM4CA", "href": "https://pfm4ca.com", "external": True},
    {"label": "Resources", "href": "?page=downloads", "external": False},
    {"label": "Feedback", "href": "?page=feedback", "external": False},
]

# ──────────────────────────────────────────────────────────────────────────
# HOME PAGE  (app/page.tsx)
# ──────────────────────────────────────────────────────────────────────────
BROUGHT_TO_YOU_BY = [
    {"src": "logos/brought-1.png", "alt": "Partner 1"},
    {"src": "logos/brought-2.png", "alt": "Partner 2"},
    {"src": "logos/brought-3.png", "alt": "Partner 3"},
]

SUPPORTED_BY_LOGOS = [
    {"src": "logos/bmf.svg", "alt": "BMF"},
    {"src": "logos/csf.png", "alt": "Climate Support Facility"},
    {"src": "logos/eu-flag.webp", "alt": "European Union"},
    {"src": "logos/qii.jpg", "alt": "Quality Infrastructure Investment"},
    {"src": "logos/fm.jpg", "alt": "Partner logo"},
]

DIMENSIONS_8 = [
    {"number": "01", "title": "Guidance", "description": "Clear policies, regulations, and mandates that define roles and responsibilities across the investment cycle.", "icon": "guidance"},
    {"number": "02", "title": "Appraisal", "description": "Rigorous cost-benefit analysis and feasibility assessment before projects enter the pipeline.", "icon": "appraisal"},
    {"number": "03", "title": "Independent Review", "description": "Third-party quality assurance to validate project design, cost estimates, and risk assessments.", "icon": "review"},
    {"number": "04", "title": "Selection", "description": "Prioritization and budget allocation based on strategic objectives and evidence of economic value.", "icon": "selection"},
    {"number": "05", "title": "Implementation", "description": "Active project management to keep delivery on time, on budget, and to specification.", "icon": "implementation"},
    {"number": "06", "title": "Adjustment", "description": "Adaptive management mechanisms that allow course correction when scope, cost, or schedule change.", "icon": "adjustment"},
    {"number": "07", "title": "Operation", "description": "Systematic asset management to maximize service delivery and extend infrastructure lifespan.", "icon": "operation"},
    {"number": "08", "title": "Evaluation", "description": "Post-completion review to assess outcomes, capture lessons, and improve future investment decisions.", "icon": "evaluation"},
]

TOOL_AREAS = [
    {
        "icon": "data_analytics",
        "title": "Data Analytics & Visualization",
        "description": "Interactive dashboards and benchmarking tools that transform complex PFM data into clear, country-specific insights for evidence-based policymaking.",
        "href": "/digital-tools#data",
    },
    {
        "icon": "geospatial",
        "title": "Geospatial Planning & Budgeting",
        "description": "Spatial tools for climate risk screening, economic cost-benefit analysis, and infrastructure access planning that connect maps with fiscal decisions.",
        "href": "/digital-tools#gpbp",
    },
    {
        "icon": "generative_ai",
        "title": "Generative AI",
        "description": "AI-powered applications that surface insights from legislative databases, climate thresholds, and World Bank operational documents at scale.",
        "href": "/digital-tools#ai",
    },
]

# ──────────────────────────────────────────────────────────────────────────
# INFRAGOV 2.0 PAGE  (app/infragov/page.tsx, components/DimensionCarousel.tsx,
# components/MaturityLadder.tsx)
# ──────────────────────────────────────────────────────────────────────────
INFRAGOV_WHY_LIST = [
    ("Structured and comparable", "standard benchmarks mean results hold up across countries and over time."),
    ("Modular and cost-effective", "assess everything, or just the areas that matter most right now."),
    ("From \u201cwhat\u201d to \u201chow\u201d", "every finding connects to practical reform guidance, not just a diagnosis."),
    ("A living framework", "designed to grow with new evidence, tools, and global priorities."),
]

CAROUSEL_AREAS = [
    {"id": 1, "badge": "Thematic Area 1", "label": "The 8 Must-Haves", "color": "#4345AA"},
    {"id": 2, "badge": "Thematic Area 2", "label": "Cross-Cutting Dimensions", "color": "#37b37f"},
    {"id": 3, "badge": "Thematic Area 3", "label": "Special Topics in PIM", "color": "#f26b23"},
]

CAROUSEL_DIMENSIONS = [
    {"num": "01", "title": "Guidance", "desc": "Clear policies, regulations, and mandates that define roles and responsibilities across the investment cycle.", "area": 1},
    {"num": "02", "title": "Appraisal", "desc": "Rigorous cost-benefit analysis and feasibility assessment before projects enter the pipeline.", "area": 1},
    {"num": "03", "title": "Independent Review", "desc": "Third-party quality assurance to validate project design, cost estimates, and risk assessments.", "area": 1},
    {"num": "04", "title": "Selection", "desc": "Prioritization and budget allocation based on strategic objectives and evidence of economic value.", "area": 1},
    {"num": "05", "title": "Implementation", "desc": "Active project management to keep delivery on time, on budget, and to specification.", "area": 1},
    {"num": "06", "title": "Adjustment", "desc": "Adaptive management mechanisms that allow course correction when scope, cost, or schedule change.", "area": 1},
    {"num": "07", "title": "Operation", "desc": "Systematic asset management to maximize service delivery and extend infrastructure lifespan.", "area": 1},
    {"num": "08", "title": "Evaluation", "desc": "Post-completion review to assess outcomes, capture lessons, and improve future investment decisions.", "area": 1},
    {"num": "09", "title": "Institutional & legal framework", "desc": "A sound legal hierarchy and a mandated PIM body at the centre of government.", "area": 2},
    {"num": "10", "title": "Integrity & anti-corruption", "desc": "Safeguards against misconduct across the whole project cycle.", "area": 2},
    {"num": "11", "title": "Information systems & digitalisation", "desc": "A single, digital PIM database that powers decisions.", "area": 2},
    {"num": "12", "title": "Climate-smart PIM", "desc": "Building climate mitigation and adaptation into every stage of investment.", "area": 3},
    {"num": "13", "title": "Public asset management", "desc": "Registering, maintaining and optimising public assets over their life.", "area": 3},
    {"num": "14", "title": "PIM for PPP governance", "desc": "Bringing public-private partnerships into one unified appraisal and selection system.", "area": 3},
    {"num": "15", "title": "PIM for SOE projects", "desc": "Aligning state-owned enterprise investment with national oversight.", "area": 3},
    {"num": "16", "title": "Subnational PIM governance", "desc": "Strengthening and coordinating public investment below the central level.", "area": 3},
]

MATURITY_LEVELS = [
    {"num": "01", "label": "Incipient", "desc": "The need is recognised, but systematic processes aren't yet in place.", "color": "#64CBD6"},
    {"num": "02", "label": "Nascent", "desc": "Foundational structures are emerging, applied unevenly across institutions.", "color": "#599EC7"},
    {"num": "03", "label": "Emerging", "desc": "Consistent processes and growing capacity, on a credible path forward.", "color": "#4E71B8"},
    {"num": "04", "label": "Advanced", "desc": "Leading practice: fully developed, consistently applied, routinely improved.", "color": "#4345AA"},
]

INFRAGOV_DASHBOARD_LIST = [
    "Assess one, several, or all 16 InfraGov 2.0 dimensions",
    "Run a specialized assessment, such as a PAG Functional Assessment",
    "Save, resume, and version each assessment by its cut-off date",
    "Work as a team with flexible read and write permissions",
    "Complete review and quality control, then publish a public version",
]

# ──────────────────────────────────────────────────────────────────────────
# DIGITAL TOOLS PAGE  (content/tools.ts)
# ──────────────────────────────────────────────────────────────────────────
TOOLS = [
    {
        "id": "cbd", "family": "data", "name": "Country Benchmarking Dashboard", "acronym": "CBD",
        "summary": "Benchmark PFM4CA performance across global and regional indicators.",
        "description": (
            "A map-driven dashboard for comparing how countries perform on climate, governance, and infrastructure measures. Hover over the maps to view country-specific indicators.\n\n"
            "CBD draws on two data streams: global datasets (Climate Change Institutional Indicators, GovTech Maturity Index, Infrastructure Efficiency, PEFA PI-11/12/16) and regional ECA datasets (CCIA, Infrastructure, PIIAG) \u2014 each traceable to its World Bank, IMF, or WBG source.\n\n"
            "The result: finance ministries can benchmark PFM4CA performance against peers at both a summary and indicator level."
        ),
        "href": "https://datanalytics.worldbank.org/country-benchmarking-dashboard/", "screenshot": "screenshots/cbd.png", "icon": "icons/cbd.png", "videoId": None,
    },
    {
        "id": "ecba", "family": "gpbp", "name": "Economic Cost Benefit Analysis Tool", "acronym": "eCBA",
        "summary": "Compare project strategies by modelling costs, benefits, and climate impacts.",
        "description": (
            "A guided tool for evaluating the financial and economic feasibility of public investment projects \u2014 no advanced expertise required.\n\n"
            "- **Assumption templates** \u2014 PIM units create official templates for faster, standardized calculations; users can build their own.\n"
            "- **Sensitivity analysis** \u2014 stress-test parameters across multiple scenarios.\n"
            "- **Sharing and collaboration** \u2014 share analyses with colleagues and evaluators in one click."
        ),
        "href": "https://www.gpbp-ecba.app/", "screenshot": "screenshots/ecba.png", "icon": "icons/ecba.png", "videoId": "1078016182/840a6546c2",
        "extraLinks": [{"label": "eCBA Methodology", "href": "?page=digital-tools&view=ecba-methodology"}],
    },
    {
        "id": "ccs", "family": "gpbp", "name": "Climate Change Screening Tool", "acronym": "CCS",
        "summary": "Screen public assets for climate risk using a traffic-light classification.",
        "description": (
            "A web platform that helps ministries of planning, finance, and project proponent agencies screen public infrastructure investments and assets against climate change risk using Earth Observation (EO) technology.\n\n"
            "Enter an asset type, its location, and a disruption level \u2014 the tool uses European Space Agency satellite data to assess which climate hazards the project is vulnerable to.\n\n"
            "Outputs include historical and future risk scenarios, analysis by climate parameter and risk trigger, disruption probabilities with assumed damages and losses, sensitivity analysis, and a downloadable PDF summary report."
        ),
        "href": "https://gpbp.adamplatform.eu/", "screenshot": "screenshots/ccs.png", "icon": "icons/ccs.png", "videoId": "953863570",
    },
    {
        "id": "ldt", "family": "gpbp", "name": "Local Development Tracker", "acronym": "LDT",
        "summary": "Generate prosperity and liability metrics for sub-national regions from big data.",
        "description": (
            "A public analytics platform for comparing local development conditions across municipalities in Nepal, Serbia, and Zambia (1,028 local government units, data through 2025).\n\n"
            "Built on the PIL framework, it links development diagnostics, planning evidence, and investment prioritization \u2014 offering municipality comparisons, interactive maps, evidence tracing, and AI-assisted plan synthesis to support evidence-based public investment decisions."
        ),
        "href": "https://ldt.pim-pam.net/", "screenshot": "screenshots/ldt.png", "icon": "icons/ldt.png", "videoId": None,
    },
    {
        "id": "pia", "family": "gpbp", "name": "Public Infrastructure Access Tool", "acronym": "PIA",
        "summary": "Optimize placement of new infrastructure to widen access to public services.",
        "description": (
            "PIA assists policymakers in identifying and planning key resources such as roads, bridges, and healthcare centres. It helps to optimise the placement of new infrastructure investments.\n\n"
            "Its goal is to increase access to public services, reduce expenses, and improve the quality of life in a region, starting with greater mapping transparency over existing infrastructure assets data."
        ),
        "href": "https://datanalytics.worldbank.org/public-infrastructure-access-tool/",
        "screenshot": "screenshots/pia.png", "icon": "icons/pia.png", "videoId": None,
    },
    {
        "id": "goat", "family": "ai", "name": "Governance Operations Analytics Tool", "acronym": "GoAT",
        "summary": "Search World Bank operations for PIM, PAM, and SOE-related themes.",
        "description": (
            "Allows for targeted searches across the World Bank's three operation types: Development Policy Operations (DPO), Investment Project Lending (IPL), and Program for Results (PfoR).\n\n"
            "Clusters of keywords can be mapped to a particular thematic area \u2014 for example, Public Investment Management (PIM), Public Asset Management (PAM), or State-Owned Enterprises (SOEs)."
        ),
        "href": "https://datanalytics.worldbank.org/governance-operations-analytics-tool/",
        "screenshot": "screenshots/goat.png", "icon": "icons/goat.png", "videoId": None,
    },
    {
        "id": "clad", "family": "ai", "name": "Climate Change Legislation and Actions Database", "acronym": "CLAD",
        "summary": "Derive climate-action insights from curated national legislative databases.",
        "description": (
            "Demonstrates how insights for climate action can be derived in an end-user centric manner from a curated set of strategies for each country.\n\n"
            "The tool also allows users to assess any significant legislative and policy changes made since the latest available Country Climate and Development Report (CCDR), as well as provide relevant updates to Climate Change Institutional Assessments (CCIA)."
        ),
        "href": "https://design4climate.eu.pythonanywhere.com/", "screenshot": "screenshots/clad.png", "icon": None, "videoId": None,
    },
    {
        "id": "rtd", "family": "ai", "name": "Climate Change Risk Threshold Database", "acronym": "RTD",
        "summary": "Identify climate thresholds that escalate damage and loss to public assets.",
        "description": (
            "Compiles climate parameters that, when exceeded, could escalate damages and losses (D&Ls) to assets, investments, or localities.\n\n"
            "It plays a key role in climate change screening processes and assists in the identification and planning of adaptation and mitigation measures."
        ),
        "href": "https://gpbprtd.eu.pythonanywhere.com/", "screenshot": "screenshots/rtd.png", "icon": None, "videoId": None,
    },
]

TOOL_FAMILIES = [
    {"id": "data", "label": "Data Analytics & Visualization", "description": "Dashboards and benchmarking tools that turn complex PFM data into clear, actionable insights.", "anchor": "#data"},
    {"id": "gpbp", "label": "Geospatial Planning & Budgeting Platform", "description": "Spatial tools for climate screening, cost-benefit analysis, and infrastructure access planning.", "anchor": "#gpbp"},
    {"id": "ai", "label": "Generative AI", "description": "AI-powered applications for governance analytics and climate-legislation intelligence.", "anchor": "#ai"},
]

# ──────────────────────────────────────────────────────────────────────────
# DIGITAL ACADEMY PAGE  (app/digital-academy/page.tsx)
# ──────────────────────────────────────────────────────────────────────────
ACADEMY_VIDEOS = [
    {"id": "1", "title": "PIM-PAM Introduction", "vimeoId": "742770564"},
    {"id": "2", "title": "Business Process Mapping (Part 1)", "vimeoId": "786864754"},
    {"id": "3", "title": "Business Process Mapping (Part 2)", "vimeoId": "786864937"},
    {"id": "4", "title": "Business Process Mapping (Part 3)", "vimeoId": "786881283"},
    {"id": "5", "title": "Design Thinking \u2013 Part 1", "vimeoId": "1094683175"},
    {"id": "6", "title": "Design Thinking \u2013 Part 2", "vimeoId": "1094683970"},
    {"id": "7", "title": "Cost-Benefit Analysis (Intro)", "vimeoId": "1097818664"},
    {"id": "8", "title": "Cost-Benefit Analysis (Part 2)", "vimeoId": "1097818525"},
    {"id": "9", "title": "Cost-Benefit Analysis (Part 3)", "vimeoId": "1097818585"},
]

# Icon (ICONS_STROKE key) shown for each "At a Glance" tile label on a
# Master Class detail page — mirrors MasterClassPage.tsx's glanceIcons map.
MASTER_CLASS_GLANCE_ICONS = {
    "Format": "clock",
    "Audience": "users",
    "Level": "graduation_cap",
    "Tools": "wrench",
    "Platform": "monitor_smartphone",
    "Sector": "building2",
}

# "How Deliveries Work" notes shown under the Master Class template grid on
# the Digital Academy page.
MASTER_CLASS_DELIVERY_NOTES = [
    "A regional Director or Practice Manager typically initiates a module; the task team then defines current client priorities and staff learning needs.",
    "Cohorts are ideally no more than 15–20 people, to keep engagement and exchange strong.",
    "Deliveries are ideally face-to-face, but can also run in a hybrid fashion (for example DC morning / regional afternoon slots).",
    "Regional teams identify specific country project pipelines and portfolio issues, which are then integrated into the delivery.",
    "Versions can be tailored to government counterparts or to national and sub-national trainer-of-trainers deliveries, customized to the relevant national PIM-PAM policy context (see the pim-pam.ai PIM Country Policy Profiles and AI Coach).",
    "Events can be delivered through Bank- or Recipient-executed activities.",
]

# Model Learning Templates (content/masterClasses.ts, app/digital-academy/[slug]/page.tsx).
# Each entry's "number" is the value used in the "?page=digital-academy&view=masterclass-<number>"
# detail-page route. "atAGlance" items are rendered with the icon from
# MASTER_CLASS_GLANCE_ICONS matching their "label". "agenda" rows follow the
# EVENTS agenda-row shape (time/title/focus/lead) used elsewhere on the site.
MASTER_CLASSES = [
    {
        "slug": "master-class-101",
        "number": "101",
        "title": "Public Investment & Asset Management (PIM-PAM): Foundations, Tools & Operations",
        "subtitle": "An integrated overview setting the stage for the four technical-level Master Classes.",
        "summary": "An integrated overview of public investment and asset management – why it matters, who is involved, the InfraGov 2.0 framework, and the pim-pam.net toolset.",
        "objective": "Provide an integrated overview of Public Investment and Asset Management (PIM-PAM): why it matters for development outcomes, the institutional actors involved, the InfraGov 2.0 modular approach, and the pim-pam.net/pim-pam.ai digital resources – setting the stage for the four technical-level Master Classes on Geospatial Planning and Budget (GPB) tools for Cost-Benefit Analysis (CBA).",
        "atAGlance": [
            {"label": "Format", "value": "3–4 Hours"},
            {"label": "Audience", "value": "Task Teams, Senior Officials, development partners"},
            {"label": "Level", "value": "Foundational – overview"},
            {"label": "Tools", "value": "pim-pam.net · GPB · GOAT · AI"},
        ],
        "agenda": [
            {"time": "08:45–09:00", "title": "Welcome & Framing", "focus": "Course objectives and link to the four technical Master Classes that follow.", "lead": "Chair"},
            {"time": "09:00–09:20", "title": "1. Key Concepts & Outcomes", "focus": "Scope of public infrastructure, land, and property; interplay between non-financial asset stocks (incl. digital data) and new investment flows.", "lead": "WBG Lead"},
            {"time": "09:20–09:35", "title": "2. Development Challenge", "focus": "How poor investment management impairs growth, structural change, fiscal space, and jobs creation.", "lead": "WBG Economist"},
            {"time": "09:35–09:50", "title": "3. The Who of PIM-PAM", "focus": "Central finance, planning & economy support/challenge function; roles of national MDAs, Sub-National Governments, and State-Owned Enterprises.", "lead": "WBG + Partner"},
            {"time": "09:50–10:00", "title": "4. InfraGov 2.0 Approach", "focus": "What better PIM-PAM outcomes require: the modular framework and how its pieces fit together.", "lead": "WBG Lead"},
            {"time": "10:00–10:25", "title": "The Project Cycle: Strong Preparation to Better Outcomes", "focus": "What are the methodologies/tools used during project preparation according to the proportionality concept (inc. economic analysis, climate risk analysis, etc,)"},
            {"time": "10:25–10:40", "title": "Coffee Break", "focus": "Networking and informal Q&A."},
            {"time": "10:40–11:05", "title": "5. Digitalization for PIM-PAM", "focus": "How digitalization supports better outcomes and what information is required at each stage of the cycle.", "lead": "Knowledge Partner"},
            {"time": "11:05–11:45", "title": "6. pim-pam.net Resources", "focus": "Data analytics & visualization platforms; Geospatial Planning & Budgeting (GPB) tools – CBA, CCS, LDT, PIA; and Generative AI.", "lead": "WBG + Partner"},
            {"time": "11:45–12:15", "title": "7. PIM-PAM in Operations", "focus": "Using the Governance Operations Analytics Tool (GOAT) to track IPF, PforR, and DPO operations.", "lead": "External Expert"},
            {"time": "12:15–12:35", "title": "8. Further Resources", "focus": "Roadmap of the four technical Master Classes and the Awareness / Application / Adoption digital decision-support engagements.", "lead": "Chair"},
            {"time": "12:35–12:45", "title": "Synthesis & Q&A", "focus": "Key takeaways and next steps for participants.", "lead": "Chair"},
        ],
        "outcomes": [
            "Frame PIM-PAM as a driver of growth, fiscal space, and jobs",
            "Map institutional roles across MDAs, SNGs, and SOEs",
            "Navigate pim-pam.net tools (GPB, GOAT, AI) and choose a follow-on Master Class",
        ],
        "deliveredBy": "World Bank Group staff, in collaboration with external experts and knowledge partners.",
        "showGpbSeries": True,
        "seriesIntro": "The Public Investment Management (PIM)/Public Asset Management (PAM) pim-pam.net Geospatial Planning and Budgeting (GPB) tools provide learning resources and implementation tools that can be replicated and scaled across different country contexts. The Master Classes are intended to assist Bank colleagues, country counterparts, and other development partners in advancing a journey of awareness, application to adoption of open-source methods and tools.",
        "references": [
            "World Bank. (2026b). Infrastructure Governance Assessment Framework: A Modular Approach for Better Outcomes (InfraGov 2.0). Washington, DC: Prosperity Vertical Governance Practice, April, pp. 52 + Summary.",
        ],
    },
    {
        "slug": "master-class-102",
        "number": "102",
        "title": "Public Investment Portfolio Rationalization",
        "summary": "Identify and tackle shortcomings in existing capital spending portfolios – weak project rationales, cost and time overruns, and climate risk exposure – and prioritise what to keep, restructure or stop.",
        "objective": "The master class helps participants identify and tackle shortcomings in existing capital expenditure/public investment portfolios. These include poor or outdated project rationales/viability, cost and time overruns, and exposure of climate change risks. Portfolio rationalization is often required in the context of fiscal consolidation, low public investment efficiency, and strategic program prioritization. Rationalization applies the same Project Readiness and cost-benefit tests to projects already in the portfolio.",
        "atAGlance": [
            {"label": "Format", "value": "3–4 Hours"},
            {"label": "Audience", "value": "Task Teams, Senior Officials, development partners"},
            {"label": "Level", "value": "Foundational – overview"},
            {"label": "Tools", "value": "pim-pam.net Portfolio Doctor, Project Readiness Gate, eCBA, AI tooling for Data Wrangling"},
        ],
        "agenda": [
            {"time": "08:45–09:00", "title": "Welcome & Framing", "focus": "Course objectives and link to the four technical Master Classes that follow.", "lead": "Chair"},
            {"time": "09:00–09:20", "title": "1. Key Concepts & Outcomes", "focus": "Define criteria by which public investment portfolio could be rationalized and more proactively managed for better public investment outcomes", "lead": "WBG Lead"},
            {"time": "09:20–09:35", "title": "2. Development Challenge", "focus": "How poor investment management impairs growth, structural change, fiscal space, and jobs creation. Existing public investment portfolios are often overcommitted with projects that are running over time and cost, without adequate clarity of expected development outcomes", "lead": "WBG Economist"},
            {"time": "09:35–09:50", "title": "3. The Who of PIM Portfolio Rationalization", "focus": "Central finance, planning & economy support/challenge function; roles of national MDAs, Sub-National Governments, and State-Owned Enterprises.", "lead": "WBG + Partner"},
            {"time": "09:50–10:00", "title": "4. Criteria for Program-Projects-Procurements Contract Rationalization", "focus": "Measures of time and cost overruns, procurement/contract commitments, ex post assessments of project rationales and viability under imperfect information, re-testing committed projects against Project Readiness criteria and eCBA results.", "lead": "WBG Lead"},
            {"time": "10:00–10:25", "title": "The Project Cycle: Strong Preparation to Better Outcomes", "focus": "What are the methodologies/tools used during project rationalization according to the proportionality concept (inc. size, economic analysis, climate risk analysis, etc,)"},
            {"time": "10:25–10:40", "title": "Coffee Break", "focus": "Networking and informal Q&A."},
            {"time": "10:40–11:05", "title": "5. Digitalization for PIM-PAM", "focus": "How digitalization supports better outcomes and what information is required for portfolio rationalization and further sustained proactive management. How to conduct required data wrangling for different data readiness/Financial-Public Information Management (PIMIS) contexts", "lead": "Knowledge Partner"},
            {"time": "11:05–11:45", "title": "6. pim-pam.net Resources", "focus": "Data analytics & visualization platforms; Model Portfolio Doctor, the Project Readiness Gate and eCBA, AI tools for data wrangling", "lead": "WBG + Partner"},
            {"time": "11:45–12:15", "title": "7. PIM Rationalization Operations", "focus": "Using the Portfolio Rationalization Approach in DPO, IPF, and PforR operations. Measuring benefits-value for money", "lead": "External Expert"},
            {"time": "12:15–12:35", "title": "8. Further Resources", "focus": "Roadmap Awareness / Application / Adoption digital decision-support engagements, leadership and ownership assessments of rationalization reforms", "lead": "Chair"},
            {"time": "12:35–12:45", "title": "Synthesis & Q&A", "focus": "Key takeaways and next steps for participants.", "lead": "Chair"},
        ],
        "outcomes": [
            "Frame PIM-PAM as a driver of growth, fiscal space, and jobs",
            "Develop and measure criteria for PIM portfolio rationalization",
            "Navigate pim-pam.net tools, and prioritize and sequence PIM Portfolio with the support of digital decision support deployments",
        ],
        "deliveredBy": "World Bank Group staff, in collaboration with external experts and knowledge partners.",
        "showGpbSeries": True,
        "seriesIntro": "The Public Investment Management (PIM)/Public Asset Management (PAM) pim-pam.net Geospatial Planning and Budgeting (GPB) tools provide learning resources and implementation tools that can be replicated and scaled across different country contexts. The Master Classes are intended to assist Bank colleagues, country counterparts, and other development partners in advancing a journey of awareness, application to adoption of open-source methods and tools.",
        "references": [
            "World Bank. (2026b). Infrastructure Governance Assessment Framework: A Modular Approach for Better Outcomes (InfraGov 2.0). Washington, DC: Prosperity Vertical Governance Practice, April, pp. 52 + Summary.",
            "Moon, Samuel, Kim, Jay-Hyung, Mroczka, Fabienne, & Fallov, Jonas Arp. (2026). Public Investment Portfolio Rationalization: Guidelines for overcommitted, Climate-exposed, and Emergency-Affected Portfolios. Washington, DC: World Bank Prosperity Insight Series, InfraGov 2.0 Application Guidance (forthcoming), May, pp. 53.",
        ],
    },
    {
        "slug": "master-class-201",
        "number": "201",
        "title": "Public Investment Project Preparation with Online Cost-Benefit Analysis (CBA)",
        "summary": "Lead with the Project Readiness application to strengthen and review concept notes at the pre-appraisal stage, then take projects further with eCBA – economic cost-benefit analysis, sensitivity testing and Reference Class Forecasting to counter cost and time biases.",
        "objective": "In good practice PIM systems, public investment projects move through a systematic process, from identification and appraisal to selection, implementation and evaluation. This Master Class focuses on the early stages of that process: using the Project Readiness application to prepare and review concept notes against national policy and quality criteria, then applying online Cost-Benefit Analysis through eCBA where fuller economic appraisal is required – across sectors, for both Bank-financed and country-systems projects.",
        "atAGlance": [
            {"label": "Format", "value": "3–4 Hours"},
            {"label": "Audience", "value": "Task Teams, PIM units, sector staff"},
            {"label": "Level", "value": "Intermediate – hands-on"},
            {"label": "Platform", "value": "pim-pam.net online tools"},
        ],
        "agenda": [
            {"time": "08:45–09:00", "title": "Welcome & Framing", "focus": "Registration, objectives of the Master Class, and introductions.", "lead": "Chair"},
            {"time": "09:00–09:20", "title": "1. InfraGov 2.0 Overview", "focus": "Modular framework design to support better public investment outcomes across sectors.", "lead": "WBG Lead"},
            {"time": "09:20–09:25", "title": "Short video on pim-pam.net GPB tools", "focus": "Why these tools, what do they cover, how can they be applied…"},
            {"time": "09:25–09:55", "title": "2. Role of CBA", "focus": "CBA in pipeline project preparation and active / ex-post portfolio analysis.", "lead": "WBG Economist"},
            {"time": "09:55–10:25", "title": "3. Mapping Prep. Requirements", "focus": "Using online AI tools to align national policy frameworks with WBG Economic & Finance Analysis (EFA) guidance.", "lead": "WBG + Partner"},
            {"time": "10:25–10:40", "title": "Coffee Break", "focus": "Networking and informal Q&A."},
            {"time": "10:40–11:30", "title": "4. Online CBA vs. Excel", "focus": "The case for online CBA relative to traditional Excel-based project preparation.", "lead": "Knowledge Partner"},
            {"time": "11:30–12:00", "title": "5. Sensitivity & RCF", "focus": "Sensitivity analysis and Reference Class Forecasting to address cost, time, and benefit biases.", "lead": "External Expert"},
            {"time": "12:00–12:25", "title": "6. Climate & D&L with GPB (Highlights with level 2 class available)", "focus": "Climate Change Screening (CCS) and Damage & Loss (D&L) analysis using pim-pam.net Geospatial Planning & Budgeting tools.", "lead": "WBG + Partner"},
            {"time": "12:25–12:45", "title": "Synthesis & Q&A", "focus": "Key takeaways, open discussion, and next steps for participants.", "lead": "Chair"},
        ],
        "outcomes": [
            "Apply online CBA to projects at pipeline and ex-post stages",
            "Run sensitivity analysis and RCF to counter preparation biases",
            "Assess implications and extent of time and cost overruns in public investment outcomes/impact evaluations",
            "Refer to CCS and D&L in the pim-pam.net GPB environment",
        ],
        "deliveredBy": "World Bank Group staff, in collaboration with external experts and knowledge partners.",
    },
    {
        "slug": "master-class-202",
        "number": "202",
        "title": "Project Preparation for a Changing Climate: Risks, Resilience & GHG Mitigation",
        "summary": "Screen projects for physical and transition climate risk, design adaptation and resilience measures, and bring GHG emissions into the appraisal.",
        "objective": "Use the Geospatial Planning and Budgeting (GPB) Climate Change Screening (CCS) and Cost-Benefit Analysis (CBA) tools to address climate risks, design Adaptation & Resilience (A&R) measures, and reduce Greenhouse Gas (GHG) emissions in a data-informed manner.",
        "atAGlance": [
            {"label": "Format", "value": "3–4 Hours"},
            {"label": "Audience", "value": "Task Teams, PIM units, climate focal points"},
            {"label": "Level", "value": "Intermediate – hands-on"},
            {"label": "Tools", "value": "pim-pam.net GPB · CCS · CBA"},
        ],
        "agenda": [
            {"time": "08:45–09:00", "title": "Welcome & Framing", "focus": "Why climate considerations belong in project preparation; objectives of the day.", "lead": "Chair"},
            {"time": "09:00–09:25", "title": "1. Climate & Public Investment", "focus": "How climate change reshapes project costs, benefits, and risk profiles across sectors.", "lead": "WBG Lead"},
            {"time": "09:25–09:55", "title": "2. Dimensions of Climate Risk", "focus": "Physical and transition risks, hazard categories, and exposure of public assets and services. EU climate change risk framework", "lead": "Climate Specialist"},
            {"time": "09:55–10:25", "title": "3. Adaptation & Resilience", "focus": "A&R measures: design options, cost-effectiveness, and integration into project scoping.", "lead": "WBG + Partner"},
            {"time": "10:25–10:40", "title": "Coffee Break", "focus": "Networking and informal Q&A."},
            {"time": "10:40–11:10", "title": "4. Mitigation & GHG Emissions", "focus": "Estimating project GHG footprints and identifying low-emission design alternatives.", "lead": "Knowledge Partner"},
            {"time": "11:10–11:45", "title": "5. CCS with GPB Tools", "focus": "Hands-on Climate Change Screening using pim-pam.net Geospatial Planning & Budgeting layers. Working with local uncertainty about climate change futures, GPB quantification", "lead": "External Expert"},
            {"time": "11:45–12:25", "title": "6. Climate-Informed CBA", "focus": "Embedding A&R benefits, residual climate damages, and GHG shadow pricing in online CBA.", "lead": "WBG + Partner"},
            {"time": "12:25–12:45", "title": "Synthesis & Q&A", "focus": "Key takeaways, open discussion, and how to apply CCS + CBA in your next project.", "lead": "Chair"},
        ],
        "outcomes": [
            "Identify physical and transition climate risks for a project",
            "Run CCS in the GPB environment and select A&R measures",
            "Integrate GHG accounting and resilience into online CBA",
        ],
        "deliveredBy": "World Bank Group staff, in collaboration with external climate experts and knowledge partners.",
        "references": [
            "World Bank. (2026a). InfraGov 2.0: Climate-Informed Project Preparation Supplementary Guidance. Washington, DC: Prosperity Vice Presidency, Global Governance Practice, April [final pre-publication draft], pp.",
            "World Bank. (2026b). Infrastructure Governance Assessment Framework: A Modular Approach for Better Outcomes (InfraGov 2.0). Washington, DC: Prosperity Vertical Governance Practice, April, pp. 52 + Summary.",
        ],
    },
    {
        "slug": "master-class-203",
        "number": "203",
        "title": "Local Development Tracking with Big Data and AI",
        "summary": "Build a prosperity, livability and infrastructure baseline for any sub-national geography, using big data and AI to surface local gaps and priorities.",
        "objective": "Assess how sub-national governments perform on Prosperity, Livability (including climate exposure), and Infrastructure (roads, rail, energy, water, health, education, digital). Use big data and AI to surface insights, gaps, and priorities for local jobs, revenue mobilization, market-based finance, and stronger public investment outcomes.",
        "atAGlance": [
            {"label": "Format", "value": "3–4 Hours"},
            {"label": "Audience", "value": "National & sub-national clients, Task Teams"},
            {"label": "Level", "value": "Intermediate – applied"},
            {"label": "Tools", "value": "pim-pam.net GPB · LDT · AI SWOT"},
        ],
        "agenda": [
            {"time": "08:45–09:00", "title": "Welcome & Framing", "focus": "Why local development tracking matters; objectives and structure of the day.", "lead": "Chair"},
            {"time": "09:00–09:15", "title": "1. Local Government Data Challenge", "focus": "Administrations of different sizes and shifting boundaries; gaps in traditional administrative and statistical series.", "lead": "WBG Lead"},
            {"time": "09:15–09:20", "title": "InfraGov 2.0 and the Special Challenge of Local Investments", "focus": "Highlight the interests of national Ministries of Finance versus Local Governments to improve investments, including with a line of sight to jobs creation"},
            {"time": "09:20–09:25", "title": "Short video on pim-pam.net GPB tools", "focus": "Why these tools, what do they cover, how can they be applied…"},
            {"time": "09:25–09:50", "title": "2. Local Strategy Challenge", "focus": "Variable quality and vintage of local development strategies; weak line-of-sight to jobs and outcomes.", "lead": "WBG Economist"},
            {"time": "09:50–10:25", "title": "3. GPB & the PIL Baseline", "focus": "Applying the pim-pam.net Geospatial Planning & Budgeting tool to build a Prosperity, Livability & Infrastructure baseline.", "lead": "WBG + Partner"},
            {"time": "10:25–10:40", "title": "Coffee Break", "focus": "Networking and informal Q&A."},
            {"time": "10:40–11:15", "title": "4. AI SWOT on Local Strategies", "focus": "AI processing of Local Development Strategy documents against the PIL baseline to yield national and local SWOT.", "lead": "Knowledge Partner"},
            {"time": "11:15–11:45", "title": "5. Local Jobs Trends", "focus": "Linking big data to administrative and statistical sources to generate jobs trends insights – ECA / Serbia illustration.", "lead": "WBG Poverty & Jobs Economist"},
            {"time": "11:45–12:25", "title": "6. Client Engagement with LDT", "focus": "Using GPB LDT tools with national and sub-national clients to shape ASA products and operational design.", "lead": "WBG + Partner"},
            {"time": "12:25–12:45", "title": "7. Synthesis & Q&A", "focus": "Key takeaways, open discussion, and pathways for follow-on engagement.", "lead": "Chair"},
        ],
        "outcomes": [
            "Build a PIL baseline for any sub-national geography in GPB",
            "Run an AI SWOT against local strategy documents",
            "Read local jobs trends from combined big-data and admin sources",
        ],
        "deliveredBy": "World Bank Group staff, in collaboration with external experts and knowledge partners.",
    },
    {
        "slug": "master-class-204",
        "number": "204",
        "title": "Public Infrastructure Access (PIA) Tool",
        "summary": "Map who can reach public services today, and simulate where new facilities would widen access the most – no GIS or coding skills required.",
        "objective": "Demonstrate how data-driven geospatial analytics can help governments identify gaps in public infrastructure access, prioritize new investments, and track progress toward equity-driven coverage targets – with no coding or GIS expertise required.",
        "atAGlance": [
            {"label": "Format", "value": "3–4 Hours"},
            {"label": "Audience", "value": "Task Teams, PIM units, health sector staff"},
            {"label": "Level", "value": "Intermediate – hands-on"},
            {"label": "Platform", "value": "pim-pam.net / Geospatial Hub"},
            {"label": "Sector", "value": "Health (expandable to education, water, roads)"},
        ],
        "agenda": [
            {"time": "08:45–09:00", "title": "Welcome & Framing", "focus": "Registration, objectives of the Master Class, and participant introductions.", "lead": "Chair"},
            {"time": "09:00–09:25", "title": "InfraGov 2.0 Overview", "focus": "Modular framework design to support better public investment outcomes across sectors.", "lead": "WBG Lead"},
            {"time": "09:25–09:30", "title": "GPB Digital Tools Overview Video (5-min video – to be recorded)", "focus": "A 5-minute visual overview of all PIM/MEGA digital tools: PIA, eCBA, CCS, LDT, GoAT, AI Knowledge Coach, PIM Policy Repository, Portfolio Doctor, CLAD, and Country Demos. Sets the scene for where PIA sits in the ecosystem.", "lead": "Video"},
            {"time": "09:30–10:25", "title": "1. The Access Problem – Why Geography Matters", "focus": "Healthcare access is geographic. Walking vs. driving time catchments. Why road-based analysis alone misses gaps. Country evidence from Timor-Leste and Zambia.", "lead": "Geospatial Lead"},
            {"time": "10:25–10:55", "title": "2. GPB/MEGA Ecosystem Context", "focus": "Where PIA sits within the broader suite of digital tools. Links to eCBA, CCS, LDT, and the Geospatial Hub.", "lead": "WBG Lead"},
            {"time": "10:55–11:25", "title": "3. Live Demo – Coverage Mapping", "focus": "Hands-on walkthrough: loading facility, generating coverage maps, and identifying underserved populations at national and sub-national level.", "lead": "WBG Economist / Facilitator"},
            {"time": "11:25–11:40", "title": "Coffee Break", "focus": "Networking and informal Q&A."},
            {"time": "11:40–12:10", "title": "4. Optimization – Where to Invest Next?", "focus": "Simulating thousands of potential facility locations. Visualizing incremental coverage gains and diminishing returns. Prioritizing investments across scales.", "lead": "WBG Economist / Facilitator"},
            {"time": "12:10–12:30", "title": "5. Existing Challenges in methodology", "focus": "Challenges in mapping geospatial data; existing methods (Euclidean, topography, raster-based calculation, isochrone / catchment area) Incorporating facility construction costs into placement optimization.", "lead": "Data Scientist"},
            {"time": "12:30–12:50", "title": "6. From Insight to Action", "focus": "How PIA outputs feed into budget proposals, capital investment plans, and WBG project preparation. Integration with eCBA and GPB tools for full investment appraisal.", "lead": "WBG Lead"},
            {"time": "12:50–13:10", "title": "7. Hands-On Exercise", "focus": "Participants run their own country scenario: define a coverage target, identify top facility placement candidates, and generate a decision-ready output.", "lead": "WBG Economist / Facilitator"},
            {"time": "13:10–13:30", "title": "Synthesis & Q&A", "focus": "Key takeaways, open discussion, and next steps for participants.", "lead": "Chair"},
        ],
        "outcomes": [
            "Interpret coverage maps showing who can access care by walking or driving time",
            "Identify underserved populations at national, regional, and facility-catchment level",
            "Simulate new facility placements and evaluate incremental coverage gains",
            "Understand diminishing returns and how to prioritize when resources are limited",
            "Connect PIA outputs to budget proposals and WBG project preparation processes",
            "Link PIA analysis to eCBA, CCS, and other GPB tools for end-to-end appraisal",
        ],
        "deliveredBy": "Governance staff along with the DIME team at DEC and the Innovation team, in collaboration with external experts and knowledge partners.",
        "about": {
            "heading": "About the pim-pam.net GPB PIA Tool",
            "body": "The Geospatial Planning and Budgeting (GPB) Public Infrastructure Access (PIA) tool supports governments in identifying where healthcare centers exist today, who they serve, and – most importantly – where new investment will have the greatest impact. First piloted in Timor-Leste in 2021 and scaled to much larger countries such as Zambia (nearly 50× bigger), PIA is now a living system hosted on the World Bank's Geospatial Hub under the MEGA initiative. At its core, PIA answers two questions: Who is currently served? And where should new facilities be placed to reach the most people? It models both walking and driving catchments, simulates thousands of potential placement scenarios, and translates complex geospatial analytics into decision-ready outputs – no GIS or coding skills required.",
        },
    },
]

# ──────────────────────────────────────────────────────────────────────────
# RESOURCES PAGE  (app/resources/page.tsx)
# ──────────────────────────────────────────────────────────────────────────
RESOURCE_DOCS = [
    {
        "id": "knowledge-framework",
        "title": "PIIAG Knowledge Framework",
        "description": "To better assist client countries, the World Bank is enhancing its stock of strategic and functional PIM training offerings through its Public Infrastructure Investment and Asset Governance (PIIAG) knowledge framework.",
        "href": "documents/piiag-knowledge-framework.pdf",
    },
    {
        "id": "digitalization-framework",
        "title": "PIIAG Digitalization Framework",
        "description": "Combined with the right public sector skills and competencies, fit-for-purpose digitalization of public infrastructure investment and asset governance function can generate massive returns relative to costs.",
        "href": "documents/piiag-digitalization-framework.pdf",
    },
]

# ──────────────────────────────────────────────────────────────────────────
# BLOGS  (content/blogs.ts)
# ──────────────────────────────────────────────────────────────────────────
BLOGS = [
    {
        "slug": "digitalization-transforms-public-infrastructure",
        "title": "How Digitalization Is Transforming Public Infrastructure Investment",
        "date": "2025-04-15",
        "excerpt": "From GIS mapping to AI-powered analytics, digital tools are reshaping how governments plan, appraise, and monitor public infrastructure investments.",
        "tag": "Innovation",
        "body": "Placeholder content for this blog post.",
    },
    {
        "slug": "climate-risk-screening-public-assets",
        "title": "Climate Risk Screening for Public Assets: A Practical Guide",
        "date": "2025-03-22",
        "excerpt": "The Climate Change Screening Tool provides a traffic-light classification system that helps officials assess climate vulnerabilities across roads, schools, and healthcare facilities.",
        "tag": "Climate",
        "body": "Placeholder content for this blog post.",
    },
    {
        "slug": "geospatial-planning-budget-decisions",
        "title": "Using Geospatial Data to Inform Budget Decisions",
        "date": "2025-02-10",
        "excerpt": "The GPBP suite connects spatial data with fiscal planning, enabling evidence-based decisions on where and how to invest in public infrastructure.",
        "tag": "Geospatial",
        "body": "Placeholder content for this blog post.",
    },
    {
        "slug": "ai-governance-operations-analytics",
        "title": "GoAT: AI-Powered Search Across World Bank Operations",
        "date": "2025-01-18",
        "excerpt": "The Governance Operations Analytics Tool maps keyword clusters to PIM, PAM, and SOE themes across DPO, IPL, and PfoR operation types.",
        "tag": "AI",
        "body": "Placeholder content for this blog post.",
    },
]

# ──────────────────────────────────────────────────────────────────────────
# EVENTS  (content/events.ts, app/events/page.tsx, app/events/[slug]/page.tsx)
#   Each event's "detail" dict mirrors the EventDetail TS interface:
#   aboutParagraphs / objectivesIntro / objectives / format / agenda /
#   summary / notes / links / references / organizers — all optional,
#   rendered conditionally by event_detail_page() exactly like the
#   original AgendaAccordion.tsx + app/events/[slug]/page.tsx did.
# ──────────────────────────────────────────────────────────────────────────
EVENTS = [
    {
        "slug": "public-sector-worth-sarajevo-2026",
        "title": "Public Sector Worth: Valuing Non-Financial Assets",
        "date": "2026-10-26",
        "dateLabel": "October 26, 2026",
        "location": "Sarajevo, Bosnia and Herzegovina",
        "format": "in-person",
        "description": "A half-day event demonstrating how countries across the region are gaining a better handle on the non-financial assets side of their public sector balance sheets \u2014 covering IPSAS standards, real asset management practices, AI, and emerging InfraGov 2.0 findings on Public Asset Governance.",
        "detail": {
            "aboutParagraphs": [
                "A critical first step in better managing the public sector balance sheet is knowing what you own and what it's worth. This half-day event will demonstrate how countries across the region are gaining a better handle on the non-financial assets side of their balance sheets, specifically land, property, and infrastructure, for decision-making and day-to-day management purposes.",
                "Participants will cover key concepts and perspectives from international accounting good practices (IPSAS 33/45, 44), real asset management practices, and the use of digital technologies, including Artificial Intelligence (AI), to generate better outcomes in the public sector, revenue, and public financial management (PFM).",
                "The event will disseminate emerging findings from the World Bank InfraGov 2.0 guidance on Public Asset Governance Functional Assessments (PAG-FA), as well as how Ministries of Finance can best spearhead tangible improvements in optimizing public sector worth across time for national, sub-national, and State-Owned Enterprise (SOE) levels, including addressing potential risks such as climate change.",
            ],
            "organizers": "Co-organized with the Public Expenditure Management Peer Assisted Learning (PEMPAL) network. Pre-event to the PEMPAL Treasury Community of Practice (CoP) Plenary.",
        },
    },
    {
        "slug": "public-sector-staffing-digitalization-2025",
        "title": "Public Sector Staffing and Digitalization for Public Infrastructure Investment Results",
        "date": "2025-12-03",
        "dateLabel": "December 3\u20135, 2025",
        "location": "Vienna, Austria",
        "format": "in-person",
        "description": "A workshop assessing strategies for addressing core PIM capacity challenges, showcasing elements of a core curriculum for PIM skills, and exploring how digitalization and AI can support improved public investment systems.",
        "detailsHref": "https://pfm4ca.com/public-sector-staffing-and-digitalization-for-public-infrastructure-investment-results-dec25/",
        "detail": {
            "aboutParagraphs": [
                "Effective Public Investment Management (PIM) requires purposeful leadership and specialized staffing, competencies, and skills in the public sector. Public sector staff need specific knowledge, skills, abilities, and behaviors to carry out their roles and responsibilities effectively. To generate good public investment outcomes, it is crucial to have the right personnel in the right positions, both in central PIM unit roles but also across various government levels (including Ministries, Departments and Agencies, Sub-National Governments, and State-Owned Enterprises).",
                "The World Bank's 8 Must-Haves identify the key PIM cycle functions that public sector personnel are expected to fulfill in improved infrastructure outcomes. While some PIM aspects can be outsourced, essential skills remain necessary to define, contract, and utilize these inputs effectively. Gaps in specific PIM skills echo some of the wider challenges in successful Public Administration Reform across the region.",
                "Learning results should be clear and sustainable. This calls for a systematic approach to skills development and capacity building, as training on PIM often occurs in ad hoc fashion with vague or limited impacts. Current examples of developing PIM curricula, training-of-trainers and partnering with public sector academies show promising results.",
                "PIM skills and results need to be assessed against clear outcome metrics. Key outcome indicators include the number and value of projects subject to PIM at minimum standards; cost and time overruns during implementation; the number and value of projects subject to climate change and environmental due diligence; and the efficiency of public investment spending. Digitalization and emerging technologies such as big data and AI are transforming the PIM landscape and necessitating relevant skills development.",
            ],
            "objectivesIntro": "This event assessed strategies for addressing core PIM capacity challenges, showcased elements of a core curriculum and resources for PIM skills, and set out ways these can be effectively leveraged for impact across the region. The workshop focused on central PIM authorities, public investment project owners from national agencies, sub-national governments and SOEs, and public sector academies expected to deliver continuous quality PIM training.",
            "objectives": [
                "Review strategies for addressing core PIM capacities, required roles, responsibilities, competencies and skills for country staffing related to PIM, including alignments to Single Project Pipeline (SPP) commitments.",
                "Identify challenges related to these gaps and design solutions to effectively address them, develop organisational enablers, and leverage PIM skills to drive impact across the region.",
                "Showcase and assess the potentials of new methods, tools, and technologies, with a focus on how digitalization, big data, and AI can support solutions for improving PIM-PAM systems.",
                "Foster peer exchange and develop competencies in key PIM cycle functions, digital transformation, problem-solving, and communication of proposals to the political level.",
            ],
            "format": "Face-to-face, two-and-a-half day workshop covering peer-learning presentation sessions, learning sprints, and field visits. Draft materials and the link for online access were circulated prior to the event.",
            "agenda": [
                {
                    "day": "Wednesday, December 3, 2025",
                    "venue": "Verwaltungsakademie, T-Center, Rennweg 97-99, 1030 Wien",
                    "sessions": [
                        {"time": "08:30\u201309:00", "title": "Registration", "description": ["Check in & Registration"]},
                        {
                            "time": "09:00\u201309:30", "title": "Welcome Remarks", "moderator": "Kai Kaiser, World Bank",
                            "speakers": [
                                "Fabian Seiderer \u2014 Practice Manager, World Bank",
                                "Emcet O. Tas \u2014 Program Manager, Vienna Development Knowledge Center",
                                "Christian Weise \u2014 DG ECFIN",
                                "Sandra Rauecker-Grillitsch \u2014 Federal Public Administration Academy (VAB)",
                                "Ursula Rosenbichler \u2014 Austrian School of Government (ASG)",
                            ],
                        },
                        {
                            "time": "09:30\u201311:00", "title": "Framing the Vision and Challenge", "moderator": "Jonas Arp, World Bank",
                            "description": [
                                "PIM Success Metrics: Ownership, Staffing, and Systems for Proportionality and Materiality \u2014 Jonas Arp and Kai Kaiser, World Bank",
                                "Public Investment Practices in the European Union \u2014 Christian Weise, European Commission, DG ECFIN",
                                "Principles of effective single project pipelines \u2014 Ferdinand Pot, OECD SIGMA",
                                "Q&A and discussion",
                            ],
                        },
                        {"time": "11:00\u201311:15", "title": "Break"},
                        {
                            "time": "11:15\u201312:45", "title": "Workshop 1: Country Staffing & Competencies for PIM Outcomes", "moderator": "Julia Piotrowska",
                            "description": [
                                "Who is needed in the Central Finance Agency and Line Agencies, SOE to make PIM a success?",
                                "What are the roles (personas) and responsibilities?",
                                "What are key competencies and skills?",
                                "What are the gaps between the current and the aimed situation?",
                                "Work in groups & presentations",
                            ],
                            "output": "Structured chart that maps key PIM competencies required across 8 Must Have Dimensions and gaps to current situation.",
                            "outcome": "Shared understanding and validation of competency gaps, enabling the creation of a prioritised action plan for skill development.",
                        },
                        {"time": "12:45\u201313:30", "title": "Lunch Break"},
                        {
                            "time": "13:30\u201315:15", "title": "Sharing Experiences from Peers: Organising for Better PIM", "moderator": "Aleksandra Drecun, World Bank",
                            "description": [
                                "PIM reform in Ukraine \u2014 Viktor Nestulia",
                                "Albania: Translating Training into better Projects \u2014 Renald Petriti",
                                "Lithuania: Integrated and Digital PIM \u2014 Linas Jasiukevi\u010dius",
                            ],
                        },
                        {
                            "time": "15:15\u201316:30", "title": "Workshop 2: Identification and Definition of Core Challenges in PIM", "moderator": "Climate Lab",
                            "description": [
                                "Introduction to the Human Centric Design Framework",
                                "Identify main challenges and bottlenecks in PIM-PAM",
                                "Prioritisation and selection of a challenge",
                                "Definition of challenge, stakeholders including organisational level (national, sub-national, SOEs)",
                                "Reasons for Action / Consequences of Inaction",
                            ],
                            "output": "Visualised problem map detailing key challenges and bottlenecks within the PIM-PAM ecosystem, linking issues to potential root causes.",
                            "outcome": "Capacity to perform a systemic analysis of complex problems and accurately identify core challenges and map key stakeholders.",
                        },
                    ],
                },
                {
                    "day": "Thursday, December 4, 2025",
                    "venue": "Climate Lab, Wien Energie Servicetreff, Spittelauer L\u00e4nde 45",
                    "sessions": [
                        {"time": "08:30\u201309:00", "title": "Registration"},
                        {"time": "09:00\u201309:30", "title": "Climate Lab Vienna", "description": ["Welcome and presentation of relevant showcases \u2014 Barbara Inmann and Florian W\u00fcrrer, Climate Lab Vienna"]},
                        {
                            "time": "09:30\u201310:30", "title": "Workshop 3: Solutions for Optimised PIM Results", "moderator": "Climate Lab",
                            "description": [
                                "Recap of Workshop 2 and Definition of 'How Might We?' Question",
                                "Ideation: Brainstorming on potential solutions for defined challenges",
                                "How can technology and AI support?",
                                "Prioritisation of ideas and defining first steps",
                            ],
                            "output": "List of prioritised opportunities to improve the PIM-PAM system.",
                            "outcome": "Potential approaches and solutions for specific country situations, including potential based on new technologies and AI.",
                        },
                        {
                            "time": "10:30\u201311:30", "title": "Potentials of Digitalization and AI", "moderator": "Kai Kaiser, World Bank",
                            "description": [
                                "Potentials of Digitalization and AI \u2014 Joao Ricardo Vasconcelos, World Bank",
                                "Country experience \u2014 Montenegro: Jelena Jovetić; Georgia: Giorgi Kakauridze; Ukraine: Viktor Nestulia",
                            ],
                        },
                        {"time": "11:30\u201311:45", "title": "Break"},
                        {
                            "time": "11:45\u201312:45", "title": "Workshop 4: Designing a PIM Solution Concept", "moderator": "Climate Lab",
                            "description": [
                                "Designing a Concept for the Top Idea",
                                "Impact Analysis based on SDGs: Benefits (positive SDGs), Risks and Mitigation Measures",
                                "Sketching a First Prototype",
                            ],
                            "output": "Concept for the implementation of a new approach in the client country's PIM-PAM systems.",
                            "outcome": "Enhanced capacity to develop, prioritise, and articulate innovative solutions for PIM-PAM challenges.",
                        },
                        {"time": "12:45\u201313:15", "title": "Lunch Break"},
                        {"time": "13:30\u201314:00", "title": "Bus Transfer to Field Visit"},
                        {
                            "time": "14:00\u201316:00", "title": "Field Visit: Vienna Flood Resilience Investments / Vienna Port Facilities",
                            "description": [
                                "Arrival at thinkport VIENNA \u2014 welcome, briefing",
                                "thinkport Vienna: Vienna Harbor logistics innovations hub \u2014 Henrike Bauer",
                                "River Management & Flood Protection: the viadonau State-owned Enterprise \u2014 Winfried F\u00fcrst",
                                "Site & Project Visit: Hafen Albern Flood Protection Infrastructure \u2014 Michael Pistracher, Harbour Master",
                            ],
                        },
                        {"time": "16:00\u201316:30", "title": "Bus Transfer"},
                        {"time": "16:30", "title": "Aligning PIM and SPPs: Priorities and Experiences", "description": ["Including for sectoral and local SPPs \u2014 practical feedback to operationalising principles and country activities \u2014 Round Table discussion"]},
                        {"time": "17:30", "title": "Dinner"},
                    ],
                },
                {
                    "day": "Friday, December 5, 2025",
                    "venue": "Verwaltungsakademie, T-Center, Rennweg 97-99, 1030 Wien",
                    "sessions": [
                        {
                            "time": "09:00\u201310:00", "title": "Key Principles and Competencies in Communication", "moderator": "Aleksandra Drecun",
                            "description": [
                                "Key principles: Transparency, Proportionality & Materiality, Execution \u2014 Kai Kaiser",
                                "Competencies in communication with political level \u2014 Ursula Rosenbichler, Austrian School of Government",
                                "Discussion and exchange of experiences between participants",
                            ],
                        },
                        {
                            "time": "10:00\u201311:00", "title": "Workshop 5: Communication & Lessons Learned", "moderator": "Gerhard Embacher-K\u00f6hle & Climate Lab",
                            "description": [
                                "Preparation of presentation of concepts created in previous workshops",
                                "Identification of lessons learned and takeaways",
                            ],
                        },
                        {"time": "11:00\u201311:15", "title": "Coffee Break"},
                        {
                            "time": "11:15\u201312:00", "title": "Presentation and Discussion", "moderator": "Gerhard Embacher-K\u00f6hle & Climate Lab",
                            "description": [
                                "Presentation of results and takeaways prepared in Workshop 5",
                                "Reflection and comments by experts",
                            ],
                        },
                        {"time": "12:00\u201312:30", "title": "Priorities, Next Steps and Farewells", "description": ["Emcet O. Tas \u2014 Program Manager, Vienna Development Knowledge Center"]},
                    ],
                },
            ],
            "notes": [
                "Participants should bring laptops or relevant devices to the workshops.",
                "Printed versions of suggested readings and presentations were not provided at the event.",
            ],
            "organizers": "This PFM4CA learning event was organised by the Austrian School of Government (ASG) and the World Bank. Supported by the Financial Management Umbrella Program (FMUP) and the European Union (EU), with technical assistance from the Western Balkans Enhancing Infrastructure Governance (EIG) programme.",
        },
    },
    {
        "slug": "public-sector-skills-pim-2025",
        "title": "Public Sector Skills for Public Investment Management Results",
        "date": "2025-06-25",
        "dateLabel": "June 25, 2025",
        "location": "Austrian School of Government (ASG) / Online",
        "format": "hybrid",
        "description": "A session defining a core curriculum of PIM skills for the public sector, generating consensus on the key skills and competencies needed to strengthen PIM in a scalable and sustainable way across the region.",
        "detailsHref": "https://pfm4ca.com/public-sector-skills-for-public-investment-management-results/",
        "detail": {
            "aboutParagraphs": [
                "Effective Public Investment Management (PIM) requires purposeful leadership and specialized competencies in the public sector. These competencies encompass specific knowledge, skills, abilities, and behaviors that professionals need to carry out their roles and responsibilities effectively. To generate good public investment outcomes, it is crucial to have the right personnel in the right positions, both in central PIM roles but also across various government levels.",
                "The World Bank's 8 Must-Haves identify the key PIM cycle functions that public sector personnel are expected to fulfill in improved infrastructure outcomes. Gaps in specific PIM skills echo some of the wider challenges in successful Public Administration Reform across the region. Skills deficits in key PFM functions impede daily technical operations as well as reform leadership amid efforts towards European Union accession.",
                "The relationship between PIM skills and results also needs to be framed against outcome metrics. Key outcome indicators include the number and value of projects subject to PIM at minimum standards; cost and time overruns during implementation; and the efficiency of public investment spending and perceived quality of public infrastructure.",
                "A systematic approach is needed to evaluate effective organisational structures, competency frameworks, and performance metrics for individuals and task teams. Emerging technologies such as big data and AI are transforming the PIM landscape and necessitating relevant skills for effective utilization.",
            ],
            "objectivesIntro": "The event defined a core curriculum of PIM skills for the public sector, focused on central PIM authorities, public investment project owners, and Public Sector Academies. It also engaged international development partners from agencies such as the EC, IMF, and OECD. The workshop formed part of the lead-up to a conference in Vienna in September 2025.",
            "objectives": [
                "Achieve a common understanding of key PIM delivery skills, regional capacity gaps, and issues.",
                "Crowdsource and prioritise capacity and skills issues and possible solutions to be refined at the September event in Vienna.",
                "Discuss the possible design of a PIM curriculum and competency framework.",
            ],
            "format": "Online/hybrid. Draft materials and connection link were circulated before the event. Further resources can be found at pim-pam.net.",
            "agenda": [
                {
                    "sessions": [
                        {
                            "time": "09:00", "title": "Welcome Remarks",
                            "speakers": [
                                "Ms. Sandra Rauecker-Grillitsch \u2014 Austrian Federal Public Administration Academy",
                                "Mr. Fabian Seiderer \u2014 Practice Manager, World Bank",
                            ],
                        },
                        {
                            "time": "09:15", "title": "Skills for Public Investment Results",
                            "description": [
                                "Achieving and sustaining good PIM outcomes is hampered by persistent capacity, skills and organisational gaps. This session explores data on the nature of these gaps and discusses their implications at the country level from the perspective of both PIM coordination and project management.",
                                "Successful PIM outcomes result from the effective alignment of people, processes, and technologies. The session outlines the key performance metrics essential for achieving successful PIM and focuses on identifying key organisational requirements and skills and proposing strategies for addressing them.",
                            ],
                            "speakers": [
                                "Mr. Kai-Alexander Kaiser \u2014 Senior Governance and Public Sector Specialist, World Bank",
                                "Mr. Klas Klaas \u2014 Senior Advisor / Policy Analyst, OECD SIGMA",
                                "Mr. Jonas Frank \u2014 Regional Advisor, PIM Transparency Standards, IMF",
                            ],
                            "moderator": "Ms. Mediha Agar \u2014 Senior Public Sector Specialist, World Bank",
                        },
                        {
                            "time": "10:45", "title": "Next Generation Public Sector Academies",
                            "description": [
                                "Public Sector Academies (PSAs) can contribute significantly to the continuous training of a broad spectrum of public officials, helping to ensure alignment with policy frameworks and practices. This section delves into the challenges faced by PSAs in the region and outlines strategies to make them more effective in supporting PIM.",
                            ],
                            "speakers": [
                                "Ms. Natia Gulua \u2014 Head of Budget Department, Ministry of Finance of Georgia (The ePIM Journey & Learning in Georgia)",
                                "Elda Baguca \u2014 Albanian School of Public Administration (PIM ToT and further roll out experience in Albania)",
                                "Aleksandra Lulkovska \u2014 Public Finance Academy, North Macedonia (PIM Training experience and further steps)",
                            ],
                            "moderator": "Mr. Jonas Arp Fallov \u2014 Senior Public Sector Specialist, World Bank",
                        },
                        {
                            "time": "11:45", "title": "Closing Remarks",
                            "description": ["Where do we want to be in September? Next steps and expectations regarding the functional strengthening of PIM and PAM across the regions, country priorities, and expectations for the Vienna conference."],
                            "moderator": "Mr. Fabian Seiderer \u2014 Practice Manager, World Bank",
                        },
                    ],
                },
            ],
        },
    },
    {
        "slug": "developing-kpis-soes-2025",
        "title": "Developing KPIs for SOEs: Peer Learning on Performance Metrics for State-Owned Enterprises in Europe and Central Asia",
        "date": "2025-06-17",
        "dateLabel": "June 17, 2025",
        "location": "Online",
        "format": "virtual",
        "description": "A peer-to-peer learning session on developing KPI systems to enhance performance, transparency, and accountability in state-owned enterprises across the Europe and Central Asia region.",
        "detailsHref": "https://pfm4ca.com/developing-kpis-for-soes-peer-learning-on-performance-metrics-for-state-owned-enterprises-in-europe-and-central-asia/",
        "detail": {
            "aboutParagraphs": [
                "State-Owned Enterprises (SOEs) are critical levers for public investment and service delivery. Yet, ensuring they deliver on both commercial and public mandates requires tools that can clearly translate ownership goals into measurable outcomes. At the heart of this challenge are Key Performance Indicators (KPIs).",
                "To address this, the World Bank convened a peer-to-peer learning session titled 'Setting Targets: Developing KPIs for SOEs \u2013 International Experiences and Lessons for ECA.' The event brought together around 45 SOE policymakers, practitioners, and international experts to discuss how strategic KPI systems can be designed to enhance performance, transparency, and accountability in SOEs. The session was the first event hosted under the recently established Community of Practice on SOE Governance for the Western Balkans and Eastern Partnership countries.",
            ],
            "summary": [
                {
                    "title": "Diverse Experiences, Shared Challenges",
                    "paragraphs": [
                        "In his opening remarks, Fabian Seiderer, Practice Manager at the World Bank, underscored that KPIs 'translate policy priorities into corporate priorities,' adding that 'SOEs are often catalysts for private investment and development \u2014 if we get governance right.' He cautioned against 'gaming' of indicators unless robust oversight mechanisms are in place.",
                        "Aakriti Chandihok, Director at Austria's \u00d6BAG, shared how KPIs are structured around three pillars: value creation for portfolio companies, long-term shareholder returns, and broader public value for Austria as a business location. Kazakhstan's Timur Onzhanov, Deputy Chairman of Baiterek Holding, illustrated how cascading KPIs are derived from national development strategies down to the enterprise level.",
                        "Yoon Q. Lee, Visiting Fellow from Korea's Institute of Public Finance, presented Korea's mature and institutionalised approach \u2014 embedded in law, combining standardised national guidelines with SOE-specific targets, linking KPI evaluations to financial incentives and sanctions.",
                    ],
                },
                {
                    "title": "Reformers Reflect",
                    "paragraphs": [
                        "Discussants from Croatia and Moldova shared how they are designing new KPI systems as part of broader SOE governance reforms. Leon \u017dulj, Director at Croatia's Ministry of Finance, emphasised the need to balance 'financial efficiency with fulfilment of public missions.' Maxim S\u00e2rbu, from Moldova's Public Property Agency, raised questions on data collection and accountability mechanisms when targets are missed.",
                        "In closing remarks, Minas Trubljanin, Director General at Montenegro's Ministry of Finance, reflected: 'In all the models we saw, KPIs are not peripheral \u2014 they are central to how state ownership is exercised. But it's equally clear that information systems and institutional capacity must keep pace.'",
                    ],
                },
                {
                    "title": "Looking Ahead",
                    "paragraphs": [
                        "This event marked the launch of the SOE Governance Community of Practice in ECA and fed into the World Bank's Vienna Development Knowledge Center agenda. Future sessions will continue to build a peer network of policymakers committed to making SOEs more transparent, efficient, and accountable.",
                    ],
                },
            ],
        },
    },
    {
        "slug": "greening-pfm-learning-event-2024",
        "title": "Greening Public Financial Management \u2014 Learning Event",
        "date": "2024-12-11",
        "dateLabel": "December 11\u201313, 2024",
        "location": "Vienna, Austria",
        "format": "in-person",
        "description": "A three-day learning event on greening public financial management, bringing together practitioners from across the Europe and Central Asia region to build capabilities for climate action through better public finance systems.",
        "detailsHref": "https://pfm4ca.com/greening-public-financial-management/",
        "detail": {
            "aboutParagraphs": [
                "The Public Financial Management for Climate Action (PFM4CA) for ECA is an integrated framework that supports country-level results by building country ownership and institutional capabilities for mitigation and adaptation results. The framework seeks to build on systematic and evidence-based diagnostics to prioritise better and sequence operational support in green PFM. Its primary focus is on the 'how', optimising promised results across different time horizons, and mitigating risks or pitfalls.",
                "The PFM4CA engagement framework takes a whole-of-government approach to achieving country-level results. National, sub-national, and SOE institutional sectors are all critical to delivering on climate actions across the ECA region. The PFM4CA is built on the premise that a combination of taxation, expenditure, and regulatory measures can help deliver climate action objectives.",
                "Given the long-term implications of inertia and green transition trajectories associated with public infrastructure investments and non-financial asset governance, this area of PFM receives particular attention. Climate action results will depend on the effectiveness of PFM-related policies and practices.",
                "The PFM4CA initiative also works to promote awareness, application, and adoption of online decision-support tools for better climate actions. Through an integrated people, process, and technology engagement framework, it aims to stimulate public sector modernisation for more inclusive and climate-smart development across the ECA region. Functional resources such as the Geospatial Planning and Budgeting Platform (GPBP) \u2014 which can be found on pim-pam.net \u2014 can help realise this opportunity.",
            ],
            "agenda": [
                {
                    "day": "Day 1 \u2014 Foundations of PFM for Climate Action",
                    "sessions": [
                        {
                            "time": "09:00", "title": "Welcome & Introduction",
                            "speakers": ["World Bank and Austrian School of Government (ASG) representatives", "Kai Kaiser", "Antonia Ida Grafl", "Jeremy Hills"],
                        },
                        {
                            "time": "09:30", "title": "Session 1: Climate Change and Our Response (1.5 Hours)",
                            "description": [
                                "An overview of the science behind climate change, along with a summary of anticipated global and regional changes specific to ECA countries. Explores the significance of IPCC assessments and their implications for future climate and socio-economic effects.",
                                "Covers the United Nations Framework Convention on Climate Change (UNFCCC), the Paris Accord and Nationally Determined Contributions (NDCs), and strategies for addressing climate change including mitigation and adaptation.",
                            ],
                            "speakers": ["Jeremy Hills"],
                        },
                        {
                            "time": "11:15", "title": "Session 2: The Economics of Climate Change (1.5 Hours)",
                            "description": ["Addresses the economic implications of climate change, exploring examples of climate-related impacts and their economic costs. Analyses the costs associated with responding to climate change and possible transition risks, and considers the role of government finance in supporting the national climate response."],
                            "speakers": ["Jeremy Hills"],
                        },
                        {
                            "time": "14:00", "title": "Session 3: The Interplay of Climate Change and Public Finances (1.5 Hours)",
                            "description": [
                                "Highlights the significant fiscal impact of climate change as a critical consideration in public financial management. Participants gain insight into climate change as a fiscal risk and the specific channels through which effects like loss and damage can be manifested.",
                                "Prompts participants to reconsider the role of finance ministries in climate governance, while offering a rationale for the climate-responsive management of public resources.",
                            ],
                            "speakers": ["Antonia Ida Grafl"],
                        },
                        {
                            "time": "15:45", "title": "Session 4: Climate-sensitive Public Financial Management (1.5 Hours)",
                            "description": [
                                "Introduces Green Public Financial Management as an innovative approach to managing public finances in a sustainable and climate-sensitive way. Participants explore specific entry points within the PFM cycle to integrate climate considerations into PFM practices, systems, and frameworks.",
                                "Demonstrates how diagnostic tools such as the CCIA and PEFA Climate can be leveraged to identify gaps, opportunities, and recommendations for climate governance reform.",
                            ],
                            "speakers": ["Antonia Ida Grafl"],
                        },
                        {
                            "time": "17:30", "title": "Fireside Chat: Green Budgeting in Austria",
                            "description": ["Explores the challenges and hurdles of implementing a Green Budgeting approach through a good-practice example. Participants are guided through the lessons learned by the Austrian Ministry of Finance when integrating climate considerations into the budget cycle."],
                        },
                    ],
                },
                {
                    "day": "Day 2 \u2014 Taking Agency: Practical Methods for Climate Action in PFM",
                    "sessions": [
                        {
                            "time": "09:15", "title": "Session 1: How to Design and Implement Solutions for Complex Problems (1.5 Hours)",
                            "description": [
                                "Equips participants with tools to take ownership and drive sustainable change in PFM. Provides an introduction to the core principles of problem- and stakeholder-oriented service design, including frameworks such as Problem-Driven Iterative Adaptation (PDIA) and Design Thinking.",
                                "Participants explore why these frameworks can be pivotal to efficient PFM and gain hands-on tools for creating solutions tailored to a specific country's context and the unique needs and challenges of its stakeholders.",
                            ],
                            "speakers": ["Gerhard Embacher-K\u00f6hle", "Fiona Hahn", "Du\u0161an Jankovi\u0107"],
                        },
                        {
                            "time": "11:00", "title": "Session 2: Workshop \u2014 Identification and Definition of Challenges (1.5 Hours)",
                            "description": [
                                "Participants identify specific challenges within their countries, drawing from the gaps, opportunities, and recommendations discussed on day one. Identified challenges are assessed based on criteria such as complexity, suitability, and cross-country relevance, and participants vote to select three key challenges.",
                                "Divided into three groups, participants refine the core problem and identify relevant stakeholders, their needs, pain points, and further relevant characteristics.",
                            ],
                        },
                        {
                            "time": "13:30", "title": "Session 3: Workshop \u2014 Ideation and Prototyping for Solutions (1.5 Hours)",
                            "description": [
                                "Participants apply various tools and methods to identify potential solutions for the defined problem, select one idea, outline a possible solution, and create a quick prototype. Participants then present the challenge, along with their ideas and solutions, to the group.",
                                "Having experienced a full cycle of problem definition, ideation, prototyping, and testing, participants reflect on the potential use of the practised frameworks in their own organisations.",
                            ],
                        },
                    ],
                },
                {
                    "day": "Day 3 \u2014 Regional Experiences and Future Directions",
                    "venue": "Galaxy Tower, Praterstra\u00dfe 31, 1020 Vienna (World Bank office, Room 21-5)",
                    "sessions": [
                        {"time": "09:30", "title": "Climate-informed PIM: Regional Survey Presentation"},
                        {
                            "time": "10:30", "title": "Regional Experience Highlights",
                            "description": [
                                "Albania: PIM Curriculum and Single Pipeline",
                                "Georgia: Green Budgeting and ePIM",
                                "Serbia: Real Property Valuation",
                                "North Macedonia: Public Investment Management and Performance Audit",
                            ],
                        },
                        {"time": "11:45", "title": "Priorities for 2025: Building a Community of Progress"},
                        {"time": "12:15", "title": "Next Steps"},
                    ],
                },
            ],
            "notes": [
                "Participants should bring laptops or relevant devices to the workshops.",
                "Printed versions of suggested readings and presentations were not provided at the event.",
            ],
            "organizers": "This PFM4CA learning event was organised by the Austrian School of Government (ASG) and the World Bank. Supported by the Financial Management Umbrella Program (FMUP) and the European Union (EU), with technical assistance from the Western Balkans Enhancing Infrastructure Governance (EIG) programme.",
        },
    },
    {
        "slug": "pfm4ca-launch-event-2024",
        "title": "Public Financial Management for Climate Action Network (PFM4CA) \u2014 Launch Event",
        "date": "2024-05-27",
        "dateLabel": "May 27, 2024",
        "location": "Online",
        "format": "virtual",
        "description": "The launch event for the Europe and Central Asia PFM4CA network \u2014 a collaborative platform for sharing insights and priorities for strengthening public financial management and advancing climate-smart policies.",
        "detailsHref": "https://pfm4ca.com/eca-pfm4ca-network-launch-event/",
        "detail": {
            "aboutParagraphs": [
                "This event marked the launch of the Europe and Central Asia (ECA) PFM4CA network, a collaborative platform for sharing insights, experiences and priorities for strengthening public financial management's core practices and advancing to climate-smart policies and practices.",
                "A core focus of the network and this event was public investment and asset management \u2014 recognising the critical role that infrastructure investment decisions play in green transition trajectories.",
                "The event convened senior government officials from the ECA region, alongside international development partners and experts. Policies and practices from the Western Balkans, Caucasus, and European Union countries were shared and discussed. It also presented the network's strategic objectives and planned activities, fostering a dialogue to align with the needs and expectations of World Bank counterparts.",
            ],
            "agenda": [
                {
                    "sessions": [
                        {"time": "08:45\u201309:00", "title": "Login / Registration"},
                        {"time": "09:00\u201310:15", "title": "Overview Session: Public Financial Management for Climate Action"},
                        {"time": "10:15\u201310:35", "title": "PIM in EU Member States"},
                        {"time": "10:35\u201311:20", "title": "Sharing Experiences"},
                        {"time": "11:20\u201312:05", "title": "Panel Discussion"},
                        {"time": "12:05\u201312:15", "title": "Wrap Up and Next Steps"},
                    ],
                },
            ],
        },
    },
]

# ──────────────────────────────────────────────────────────────────────────
# GREENING DEVELOPMENT PAGE  (app/greening-development/page.tsx)
# ──────────────────────────────────────────────────────────────────────────
GREENING_FRAMEWORK_CARDS = [
    {
        "icon": "greening_legislative",
        "title": "Legislative & Regulatory Alignment",
        "desc": "Supporting countries to design and implement legislation, regulations, and expenditure policies that drive greening development outcomes at national and sub-national levels.",
    },
    {
        "icon": "greening_institutional",
        "title": "Institutional Capacity Building",
        "desc": "Strengthening the capabilities of national, sub-national, and SOE institutions through targeted skills development, organisational reform, and peer-learning networks.",
    },
    {
        "icon": "greening_digital",
        "title": "Digital Systems & Innovation",
        "desc": "Modernising information management systems and harnessing big data, AI, and digital tools to support better climate planning, investment budgeting, and results reporting.",
    },
    {
        "icon": "greening_results",
        "title": "Results & Implementation",
        "desc": "Accelerating implementation and tracking progress against country-level greening development targets, with structured monitoring frameworks aligned to climate action goals.",
    },
]

# ──────────────────────────────────────────────────────────────────────────
# MISC
# ──────────────────────────────────────────────────────────────────────────
SITE_TITLE_DEFAULT = "PIM-PAM \u2014 Digital Tools for Public Investment Management"
SITE_DESCRIPTION = (
    "A World Bank initiative delivering digital tools, AI, and governance frameworks "
    "for smarter public investment management and asset governance across client countries."
)
CARD_SCROLL_STEP = 300  # px — matches CARD_STEP in DimensionCarousel.tsx