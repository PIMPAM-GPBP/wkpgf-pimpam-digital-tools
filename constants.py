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
}

# ──────────────────────────────────────────────────────────────────────────
# NAVIGATION  (components/Nav.tsx)
# ──────────────────────────────────────────────────────────────────────────
NAV_LINKS = [
    {"label": "Home", "href": "/"},
    {"label": "Digital Tools", "href": "/digital-tools"},
    {"label": "InfraGov 2.0", "href": "/infragov", "badge": "New"},
    {"label": "Digital Academy", "href": "/digital-academy"},
    {"label": "Resources", "href": "/resources"},
    {"label": "Feedback", "href": "/feedback"},
]

# ──────────────────────────────────────────────────────────────────────────
# FOOTER  (components/Footer.tsx)
# ──────────────────────────────────────────────────────────────────────────
FOOTER_TOOL_LINKS = [
    {"label": "Country Benchmarking Dashboard", "href": "https://cbd.pim-pam.net/"},
    {"label": "eCBA Tool", "href": "https://www.gpbp-ecba.app/"},
    {"label": "Climate Change Screening", "href": "https://gpbp.adamplatform.eu/"},
    {"label": "Local Development Tracker", "href": "https://ldt.pim-pam.net"},
    {"label": "GoAT", "href": "https://pimpam-goat-i2plk.ondigitalocean.app/"},
    {"label": "CLAD Database", "href": "https://design4climate.eu.pythonanywhere.com/"},
]

FOOTER_OTHER_LINKS = [
    {"label": "pim-pam.ai", "href": "https://pim-pam.ai", "external": True},
    {"label": "VDKC / PFM4CA", "href": "https://pfm4ca.com", "external": True},
    {"label": "Resources", "href": "/resources", "external": False},
    {"label": "Feedback", "href": "/feedback", "external": False},
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
        "href": "https://cbd.pim-pam.net/", "screenshot": "screenshots/cbd.png", "icon": "icons/cbd.png", "videoId": None,
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
        "href": "https://www.figma.com/proto/MRIuLeqyVOFGJQwVi0sVAg/PIA-final?node-id=14101-76623&p=f&t=wMUuiwyzr7W56K36-0&scaling=min-zoom&content-scaling=fixed&page-id=14101%3A64991&starting-point-node-id=14101%3A76623",
        "screenshot": "screenshots/pia.png", "icon": "icons/pia.png", "videoId": None,
    },
    {
        "id": "goat", "family": "ai", "name": "Governance Operations Analytics Tool", "acronym": "GoAT",
        "summary": "Search World Bank operations for PIM, PAM, and SOE-related themes.",
        "description": (
            "Allows for targeted searches across the World Bank's three operation types: Development Policy Operations (DPO), Investment Project Lending (IPL), and Program for Results (PfoR).\n\n"
            "Clusters of keywords can be mapped to a particular thematic area \u2014 for example, Public Investment Management (PIM), Public Asset Management (PAM), or State-Owned Enterprises (SOEs)."
        ),
        "href": "https://datanalytics.worldbank.org/content/5e009cdd-7b07-4567-8f45-eb3a3f476abc/",
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
# MISC
# ──────────────────────────────────────────────────────────────────────────
SITE_TITLE_DEFAULT = "PIM-PAM \u2014 Digital Tools for Public Investment Management"
SITE_DESCRIPTION = (
    "A World Bank initiative delivering digital tools, AI, and governance frameworks "
    "for smarter public investment management and asset governance across client countries."
)
CARD_SCROLL_STEP = 300  # px — matches CARD_STEP in DimensionCarousel.tsx