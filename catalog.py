"""Structured civic problem catalog, zones, wards, and municipal service metadata.

Designed so citizens can register any municipal grievance entirely by selecting
from predefined categories, sub-problems, severity levels, durations, and
location tags without having to type a free-text description.
"""

ZONES = [
    {
        "id": "central-zone",
        "name": "Central Zone (Zone 1)",
        "name_hi": "मध्य जोन",
        "wards": [f"Ward {i} - Central Sector {((i - 1) % 5) + 1}" for i in range(1, 21)],
        "officer": "Sh. Rajendra Sharma (Zonal Commissioner)",
        "phone": "1800-180-4401",
    },
    {
        "id": "north-zone",
        "name": "North Zone (Zone 2)",
        "name_hi": "उत्तर जोन",
        "wards": [f"Ward {i} - North Enclave {((i - 21) % 5) + 1}" for i in range(21, 41)],
        "officer": "Smt. Meenakshi Verma (Zonal Commissioner)",
        "phone": "1800-180-4402",
    },
    {
        "id": "south-zone",
        "name": "South Zone (Zone 3)",
        "name_hi": "दक्षिण जोन",
        "wards": [f"Ward {i} - South Block {chr(65 + ((i - 41) % 5))}" for i in range(41, 61)],
        "officer": "Sh. Vikram Singh (Zonal Commissioner)",
        "phone": "1800-180-4403",
    },
    {
        "id": "east-zone",
        "name": "East Zone (Zone 4)",
        "name_hi": "पूर्व जोन",
        "wards": [f"Ward {i} - East Sector {((i - 61) % 8) + 1}" for i in range(61, 81)],
        "officer": "Sh. Pradeep Agarwal (Zonal Commissioner)",
        "phone": "1800-180-4404",
    },
    {
        "id": "west-zone",
        "name": "West Zone (Zone 5)",
        "name_hi": "पश्चिम जोन",
        "wards": [f"Ward {i} - West Colony {((i - 81) % 6) + 1}" for i in range(81, 101)],
        "officer": "Smt. Kavita Meena (Zonal Commissioner)",
        "phone": "1800-180-4405",
    },
    {
        "id": "industrial-zone",
        "name": "Industrial & Suburb Zone (Zone 6)",
        "name_hi": "औद्योगिक जोन",
        "wards": [f"Ward {i} - Industrial Area Phase {((i - 101) % 5) + 1}" for i in range(101, 126)],
        "officer": "Sh. Harish Nair (Zonal Commissioner)",
        "phone": "1800-180-4406",
    },
    {
        "id": "market-zone",
        "name": "Main Market & Civic Zone (Zone 7)",
        "name_hi": "मुख्य बाजार जोन",
        "wards": [f"Ward {i} - Market Circle {((i - 126) % 5) + 1}" for i in range(126, 151)],
        "officer": "Sh. Deepak Chaturvedi (Zonal Commissioner)",
        "phone": "1800-180-4407",
    },
]

PROBLEM_CATEGORIES = [
    {
        "id": "sanitation",
        "name": "Sanitation & Solid Waste",
        "name_hi": "स्वच्छता एवं कचरा प्रबंधन",
        "department": "Swachhata & Health Wing",
        "icon": "fa-solid fa-broom",
        "sla_hours": 24,
        "summary": "Garbage collection, street sweeping, open drains, public toilets, and dead animal removal.",
        "sub_problems": [
            {"id": "san-01", "title": "Door-to-door garbage collection van (Tipper) did not arrive", "sla_hours": 12},
            {"id": "san-02", "title": "Overflowing community dustbin / garbage point", "sla_hours": 12},
            {"id": "san-03", "title": "Street sweeping / road cleaning not done", "sla_hours": 24},
            {"id": "san-04", "title": "Open roadside drain (Nali) blocked or overflowing", "sla_hours": 24},
            {"id": "san-05", "title": "Illegal dumping of garbage or construction debris (Malba)", "sla_hours": 36},
            {"id": "san-06", "title": "Dead animal lying on street / public place", "sla_hours": 6},
            {"id": "san-07", "title": "Public toilet / Sulabh complex dirty or without water", "sla_hours": 12},
            {"id": "san-08", "title": "Open burning of garbage or dry leaves", "sla_hours": 6},
        ],
    },
    {
        "id": "water-sewer",
        "name": "Water Supply & Sewerage",
        "name_hi": "जल आपूर्ति एवं सीवरेज",
        "department": "Public Health & Sewerage Engineering",
        "icon": "fa-solid fa-droplet",
        "sla_hours": 24,
        "summary": "Choked sewer lines, broken manhole covers, waterlogging, and pipeline leaks.",
        "sub_problems": [
            {"id": "wat-01", "title": "Sewer line choked / sewage overflowing onto road", "sla_hours": 12},
            {"id": "wat-02", "title": "Broken, missing, or sunken manhole cover (Safety hazard)", "sla_hours": 6},
            {"id": "wat-03", "title": "Waterlogging / rainwater stagnation on street", "sla_hours": 12},
            {"id": "wat-04", "title": "Leaking municipal water supply pipeline", "sla_hours": 24},
            {"id": "wat-05", "title": "Low water pressure or irregular municipal supply", "sla_hours": 24},
            {"id": "wat-06", "title": "Contaminated / foul-smelling drinking water", "sla_hours": 12},
            {"id": "wat-07", "title": "Stormwater drain cover damaged or missing", "sla_hours": 18},
        ],
    },
    {
        "id": "streetlights",
        "name": "Street Lights & Electrical",
        "name_hi": "स्ट्रीट लाइट एवं विद्युत",
        "department": "Electrical & Street Light Cell",
        "icon": "fa-solid fa-lightbulb",
        "sla_hours": 48,
        "summary": "Fused LED street lights, exposed wires, damaged poles, and dark stretches.",
        "sub_problems": [
            {"id": "elc-01", "title": "Single street light not working / flickering", "sla_hours": 48},
            {"id": "elc-02", "title": "Entire stretch of colony street lights off (Phase fault)", "sla_hours": 24},
            {"id": "elc-03", "title": "Street lights remain ON during daytime", "sla_hours": 24},
            {"id": "elc-04", "title": "Loose, hanging, or exposed electrical wire on municipal pole", "sla_hours": 6},
            {"id": "elc-05", "title": "Damaged, rusted, or tilted street light pole", "sla_hours": 24},
            {"id": "elc-06", "title": "High-mast light or park lighting non-functional", "sla_hours": 48},
            {"id": "elc-07", "title": "Request for new street light installation in dark spot", "sla_hours": 120},
        ],
    },
    {
        "id": "roads-encroachment",
        "name": "Roads, Footpaths & Encroachment",
        "name_hi": "सड़क, फुटपाथ एवं अतिक्रमण",
        "department": "Civil Engineering & Vigilance Wing",
        "icon": "fa-solid fa-road",
        "sla_hours": 72,
        "summary": "Potholes, broken footpaths, illegal encroachments, hoardings, and speed breakers.",
        "sub_problems": [
            {"id": "rod-01", "title": "Deep potholes or damaged bitumen road surface", "sla_hours": 72},
            {"id": "rod-02", "title": "Broken footpath tiles / interlocking paver blocks", "sla_hours": 72},
            {"id": "rod-03", "title": "Road dug up for utility work and left unrepaired", "sla_hours": 48},
            {"id": "rod-04", "title": "Illegal encroachment / temporary stall blocking road or footpath", "sla_hours": 24},
            {"id": "rod-05", "title": "Damaged or unmarked speed breaker / road divider", "sla_hours": 48},
            {"id": "rod-06", "title": "Illegal flex banners, posters, or unapproved hoardings", "sla_hours": 24},
            {"id": "rod-07", "title": "Traffic island or road signage damaged", "sla_hours": 72},
        ],
    },
    {
        "id": "stray-animals",
        "name": "Stray Animals & Mosquito Control",
        "name_hi": "आवारा पशु एवं मच्छर नियंत्रण",
        "department": "Veterinary, Cattle Pound & Malaria Cell",
        "icon": "fa-solid fa-paw",
        "sla_hours": 24,
        "summary": "Stray cattle, aggressive dogs, injured animals, fogging, and pet licensing.",
        "sub_problems": [
            {"id": "ani-01", "title": "Stray cattle / cows blocking main road or market traffic", "sla_hours": 12},
            {"id": "ani-02", "title": "Aggressive stray dog pack / sterilization (ABC) request", "sla_hours": 24},
            {"id": "ani-03", "title": "Injured or sick stray animal needing rescue", "sla_hours": 6},
            {"id": "ani-04", "title": "Mosquito breeding / fogging & anti-larva spray needed", "sla_hours": 24},
            {"id": "ani-05", "title": "Monkey menace in residential colony", "sla_hours": 24},
            {"id": "ani-06", "title": "Illegal dairy / cattle shed operating in residential area", "sla_hours": 48},
            {"id": "ani-07", "title": "Rodent / rat infestation in public market or drain", "sla_hours": 48},
        ],
    },
    {
        "id": "parks-environment",
        "name": "Parks, Trees & Air Quality",
        "name_hi": "उद्यान, वृक्ष एवं पर्यावरण",
        "department": "Horticulture & NCAP Environment Cell",
        "icon": "fa-solid fa-tree",
        "sla_hours": 48,
        "summary": "Fallen trees, park upkeep, broken play equipment, and dust/air pollution.",
        "sub_problems": [
            {"id": "prk-01", "title": "Fallen tree or heavy broken branch blocking road/pathway", "sla_hours": 6},
            {"id": "prk-02", "title": "Overgrown grass, weeds, or uncleaned municipal park", "sla_hours": 48},
            {"id": "prk-03", "title": "Broken park benches, swings, or open-gym equipment", "sla_hours": 72},
            {"id": "prk-04", "title": "Tree pruning required (branches touching power lines/houses)", "sla_hours": 48},
            {"id": "prk-05", "title": "Illegal cutting of green trees", "sla_hours": 12},
            {"id": "prk-06", "title": "Severe construction dust / air pollution violation (NCAP)", "sla_hours": 24},
        ],
    },
    {
        "id": "building-tax",
        "name": "Building, Tax & Certificates",
        "name_hi": "भवन, कर एवं प्रमाण-पत्र",
        "department": "Revenue, Planning & Birth/Death Cell",
        "icon": "fa-solid fa-building-columns",
        "sla_hours": 72,
        "summary": "Unauthorized construction, property tax issues, trade/meat licenses, and certificates.",
        "sub_problems": [
            {"id": "bld-01", "title": "Unauthorized / illegal building construction in residential plot", "sla_hours": 48},
            {"id": "bld-02", "title": "Unsafe / dilapidated building structure posing collapse risk", "sla_hours": 12},
            {"id": "bld-03", "title": "Property / Urban Development (UD) Tax assessment mismatch", "sla_hours": 72},
            {"id": "bld-04", "title": "Birth or Death certificate correction / issuance delay", "sla_hours": 72},
            {"id": "bld-05", "title": "Unlicensed meat / commercial trade shop complaint", "sla_hours": 48},
            {"id": "bld-06", "title": "Dairy booth / municipal kiosk rent or maintenance issue", "sla_hours": 72},
            {"id": "bld-07", "title": "Commercial activity violating residential setback norms", "sla_hours": 72},
        ],
    },
    {
        "id": "public-health",
        "name": "Public Health & Safety",
        "name_hi": "जन स्वास्थ्य एवं सुरक्षा",
        "department": "Chief Medical & Health Officer (CMHO)",
        "icon": "fa-solid fa-kit-medical",
        "sla_hours": 24,
        "summary": "Unhygienic eateries, biomedical waste, noise nuisance, and fire safety hazards.",
        "sub_problems": [
            {"id": "hlt-01", "title": "Unhygienic street food stall or adulterated food concern", "sla_hours": 24},
            {"id": "hlt-02", "title": "Biomedical / hospital waste dumped in open municipal bin", "sla_hours": 6},
            {"id": "hlt-03", "title": "Excessive noise pollution from commercial event / DJ / generator", "sla_hours": 12},
            {"id": "hlt-04", "title": "Blocked fire brigade access lane in market / colony", "sla_hours": 12},
            {"id": "hlt-05", "title": "Open septic tank / hazardous pit in public area", "sla_hours": 12},
        ],
    },
]

SEVERITY_OPTIONS = [
    {"id": "Low", "label": "Low — Routine Maintenance", "color": "#198754"},
    {"id": "Medium", "label": "Medium — Needs Attention", "color": "#0d6efd"},
    {"id": "High", "label": "High — Urgent Disruption", "color": "#fd7e14"},
    {"id": "Emergency", "label": "Emergency — Immediate Public Hazard", "color": "#dc3545"},
]

DURATION_OPTIONS = [
    "Happened Today",
    "Since 2–3 Days",
    "More Than 1 Week",
    "Recurring / Frequent Problem",
]

LOCATION_TYPE_OPTIONS = [
    "Main Arterial Road",
    "Residential Colony / Lane",
    "Near School / College",
    "Near Hospital / Clinic",
    "Public Market / Bazaar",
    "Municipal Park / Ground",
    "Bus Stand / Public Chowk",
]

STATUS_FLOW = ["Registered", "Assigned to Ward Officer", "In Progress", "Resolved", "Closed"]

QUICK_SERVICE_TILES = [
    {"title": "Register Complaint", "subtitle": "Choose Problem (No Typing)", "url": "/register-complaint", "icon": "fa-solid fa-file-circle-plus", "accent": "#0d6efd"},
    {"title": "Track Grievance", "subtitle": "Live Status & SLA Timeline", "url": "/track-complaint", "icon": "fa-solid fa-magnifying-glass-location", "accent": "#0ea5e9"},
    {"title": "Pay Property Tax", "subtitle": "UD / House Tax & E-Receipt", "url": "/pay-tax", "icon": "fa-solid fa-indian-rupee-sign", "accent": "#10b981"},
    {"title": "Birth & Death", "subtitle": "Certificate Applications", "url": "/services/registration?type=Birth+Certificate", "icon": "fa-solid fa-certificate", "accent": "#6366f1"},
    {"title": "Trade & Dairy Booth", "subtitle": "Licenses & Kiosk Permits", "url": "/services/registration?type=Trade+License", "icon": "fa-solid fa-store", "accent": "#f59e0b"},
    {"title": "Pet Registration", "subtitle": "Dog & Cat Licensing", "url": "/services/registration?type=Pet+Registration", "icon": "fa-solid fa-dog", "accent": "#ec4899"},
    {"title": "Tenders & e-Auction", "subtitle": "Active Municipal Bids", "url": "/tenders", "icon": "fa-solid fa-gavel", "accent": "#8b5cf6"},
    {"title": "Ward & Zone Map", "subtitle": "150 Wards Directory", "url": "/wards", "icon": "fa-solid fa-map-location-dot", "accent": "#14b8a6"},
    {"title": "Air Quality (AQI)", "subtitle": "CAAQMS Live Stations", "url": "/aqi", "icon": "fa-solid fa-wind", "accent": "#0284c7"},
    {"title": "Public Notices", "subtitle": "Orders, Circulars & News", "url": "/notices", "icon": "fa-solid fa-bullhorn", "accent": "#ef4444"},
    {"title": "Helplines & Contact", "subtitle": "Zonal Control Rooms", "url": "/contact", "icon": "fa-solid fa-phone-volume", "accent": "#0f766e"},
    {"title": "Officer Portal", "subtitle": "Department Resolution Desk", "url": "/officer/login", "icon": "fa-solid fa-user-shield", "accent": "#1e293b"},
]


def get_category_by_id(category_id: str):
    for cat in PROBLEM_CATEGORIES:
        if cat["id"] == category_id:
            return cat
    return None


def get_sub_problem(category_id: str, sub_problem_id: str):
    cat = get_category_by_id(category_id)
    if not cat:
        return None, None
    for sub in cat["sub_problems"]:
        if sub["id"] == sub_problem_id:
            return cat, sub
    return cat, None


def get_zone_by_id(zone_id: str):
    for zone in ZONES:
        if zone["id"] == zone_id:
            return zone
    return None
