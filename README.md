# 🌍 Visual Geography Intelligence

### *See the world's challenges. Understand the data. Drive change.*

An **open-source platform** for exploring and visualizing global crises—climate change, public health emergencies, and humanitarian disasters—using real, authoritative data from NASA, WHO, UN, and other official sources.

[**🚀 Launch App**](#quick-start) | [**📊 View Dashboards**](#dashboards) | [**🤝 Contribute**](#contributing) | [**💬 Discuss**](#community)

---

## Why This Exists

**The problem**: Global crises are complex. News headlines conflict. Statistics are hard to find. 

**The solution**: Interactive maps + official data + story-driven context = understanding.

This project makes it easy for:
- 📰 **Journalists** to tell data-driven stories about climate and crises
- 👨‍🎓 **Educators** to show students real-world data and patterns
- 🔬 **Researchers** to access clean, open datasets
- 🤲 **Activists** to visualize and share the urgency of global issues
- 🌍 **NGOs** to track impact and communicate need to donors

---

## Quick Start

### Browser Version (No Setup Required)

```bash
python3 main.py
```

Opens instantly at `http://localhost:8000`

**Features:**
- 🗺️ Interactive world map (Leaflet.js)
- 🌙 Dark mode
- 🔍 Search countries instantly
- 📊 Hover for quick stats
- 📱 Mobile responsive

### Desktop Version (GPU-Accelerated, Optional)

```bash
pip install -r requirements.txt
python3 main.py --desktop
```

- 60 FPS OpenGL canvas
- 2D/3D globe toggle
- Hardware-accelerated rendering
- Offline tile caching

---

## 📊 Current Dashboards

### 🌡️ **Climate Crisis**
Understand global warming and our progress (or lack thereof) toward net-zero.

- **Global Temperature Anomaly** (1880-2024) — See acceleration in real time
- **CO2 Emissions by Country** — Who's responsible? Historical vs current
- **Renewable Energy Progress** — Track the world's race to 2030
- **Deforestation Hotspots** — Amazon, Southeast Asia, Congo Basin at a glance
- **Sea Level Rise** — Impact on coastal populations
- **Carbon Footprint per Capita** — Developed vs developing countries

**Use Case:** *"The world has warmed 1.1°C since industrialization. Here's where and why."*

**Data Sources:** NASA GISS, IEA, Global Forest Watch, NOAA

---

### 🏥 **Public Health & Vaccination**
Track disease, health systems, and vaccination progress globally.

- **COVID-19 & Vaccination Progress** — Real-time global coverage
- **Routine Immunization Coverage** — Polio, measles, DTP by country
- **Healthcare Access Index** — Doctors, hospital beds, patient outcomes
- **Disease Hotspots** — Malaria, TB, HIV concentration
- **Life Expectancy Disparities** — 40+ year gap between richest and poorest countries
- **Maternal & Child Mortality** — Progress toward UN SDG #3

**Use Case:** *"Why does a child in Sub-Saharan Africa have 20x higher mortality risk?"*

**Data Sources:** WHO, CDC, UNICEF, Our World in Data

---

### 🤝 **Humanitarian & Development**
See where help is needed most.

- **Refugee & Displacement Flows** — Real-time movement of displaced populations
- **Extreme Poverty Map** — People living on < $2.15/day
- **Education Access** — School enrollment, literacy, gender gaps
- **Food Security** — Hunger hotspots and famine risk areas
- **Water & Sanitation** — 2 billion lack clean water
- **Active Conflicts** — Real-time crisis tracker
- **Natural Disaster Risk** — Earthquake zones, hurricane vulnerability

**Use Case:** *"Where are the world's 100 million displaced people, and where can donors help most?"*

**Data Sources:** UN OCHA, UNHCR, World Bank, FAO, GDACS

---

## 🎯 Core Features

### 📖 Story Mode
Not just data—**context-driven exploration**.

```
Step 1: "Global temperature has risen 1.1°C since 1880"
         → Shows world map with temperature change
         
Step 2: "Acceleration is dramatic in the last 50 years"
         → Zooms into recent data
         
Step 3: "CO2 is the culprit"
         → Overlay shows emissions by country
         
Step 4: "Here's what we can do about it"
         → Links to climate solutions and organizations
```

### 🔄 Compare Tool
*Select any two countries*—see side-by-side:
- CO2 total vs per capita
- Life expectancy vs healthcare spending
- Poverty rate vs education investment
- Understand disparities instantly

### 🎨 Interactive Overlays
- **Choropleth maps** — Color-coded by metric
- **Heatmaps** — Intensity visualization
- **Flow maps** — Refugee flows, trade routes
- **Bubbles** — Size = magnitude (population, GDP)
- **Graduated symbols** — Compare magnitudes

### 📊 Real-Time Data
- Data updates automatically
- Timestamps show when data was last updated
- Links to original sources for verification
- Data quality badges (⭐⭐⭐⭐⭐ = official UN data)

### 🌐 Responsive
- Desktop, tablet, mobile
- Touch-friendly controls
- Optimized for low bandwidth

---

## 📁 Project Structure

```
Interactive-World-Map/
├── web/                          # Browser app
│   ├── index.html               # Single-page dashboard
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── maps.js              # Leaflet integration
│   │   ├── dashboards.js        # Toggle between dashboards
│   │   ├── stories.js           # Story mode logic
│   │   └── data-loader.js       # Fetch & display data
│   └── data/
│       ├── countries.geojson    # World boundaries (258 countries)
│       ├── climate/
│       │   ├── temperature.json # NASA GISS data
│       │   ├── co2.json         # IEA emissions
│       │   └── renewable.json   # Renewable % by country
│       ├── health/
│       │   ├── vaccination.json # WHO data
│       │   ├── life_expectancy.json
│       │   └── healthcare_access.json
│       └── humanitarian/
│           ├── refugees.json    # UNHCR data
│           ├── poverty.json     # World Bank
│           └── conflicts.json   # UCDP
│
├── worldmap/                     # Desktop app (PyQt6 + OpenGL)
│   ├── map_widget.py
│   ├── data_manager.py
│   └── shaders/
│
├── scripts/                      # Data pipeline
│   ├── fetch_climate_data.py    # Fetch from NASA API
│   ├── fetch_health_data.py     # Fetch from WHO API
│   ├── fetch_humanitarian_data.py
│   └── update_data.sh           # Run monthly via cron
│
├── main.py                       # Entry point
├── browser_main.py              # Flask server for web app
├── requirements.txt             # Dependencies
│
└── docs/
    ├── README.md               # This file
    ├── CONTRIBUTING.md         # How to add data
    ├── DATA_SOURCES.md         # All sources + APIs
    ├── API.md                  # If we build API
    └── ROADMAP.md              # Future features
```

---

## 🔗 Data Sources & Attribution

All data is **open, official, and freely available**:

| Dashboard | Dataset | Source | Update Frequency |
|-----------|---------|--------|------------------|
| Climate | Temperature Anomaly | NASA GISS | Monthly |
| Climate | CO2 Emissions | IEA | Annual |
| Climate | Renewable Energy % | IEA | Annual |
| Health | Vaccination Coverage | WHO | Monthly |
| Health | Healthcare Access | WHO/World Bank | Annual |
| Humanitarian | Refugees | UNHCR | Real-time |
| Humanitarian | Poverty Rate | World Bank | Annual |
| Humanitarian | Conflicts | UCDP | Real-time |

**Full source documentation** → [DATA_SOURCES.md](docs/DATA_SOURCES.md)

---

## 🤝 Contributing

We need **your help** to grow this platform!

### 🎯 Where We Need Contributors

- **Data Researchers** — Find + integrate new datasets
  - Climate: Forest coverage, ocean acidification
  - Health: Pandemic preparedness index, disability adjusted life years
  - Humanitarian: Child labor, human trafficking

- **Frontend Developers** — Improve visualizations
  - Better charts (D3.js, Recharts)
  - Mobile optimization
  - Accessibility improvements
  - Dark/light theme toggle

- **Backend/Data Engineers** — Automate data pipelines
  - Set up API integrations
  - Data validation & quality checks
  - Automated monthly updates
  - Caching & performance

- **Designers** — Make stories more compelling
  - Infographics & icons
  - Color palette for accessibility
  - UI/UX improvements

- **Writers & Translators**
  - Context explanations ("Why does this matter?")
  - Translate stories to Spanish, Mandarin, French
  - Write blog posts about datasets

### Getting Started

1. **Fork the repo**
2. **Pick an issue** from [GitHub Issues](../../issues)
3. **Read** [CONTRIBUTING.md](docs/CONTRIBUTING.md)
4. **Make a PR**

### Ideas for New Dashboards

- 🌊 Ocean Health (temperature, acidification, overfishing)
- 📚 Education Crisis (enrollment, dropout rates, literacy)
- 💪 Gender Inequality (wage gap, leadership, violence)
- 🐝 Biodiversity Loss (species extinction, habitat loss)
- 🚗 Transportation & Emissions (EV adoption, fuel efficiency)

---

## 💬 Community & Support

- **Questions?** Open a [GitHub Discussion](../../discussions)
- **Found a bug?** [Report it](../../issues)
- **Have an idea?** [Start a discussion](../../discussions)
- **Email:** santoshgoteti9@gmail.com

---

## 🤲 Support This Project

This is free and always will be. But if you find it valuable, please consider:

### 💰 Donate
- **Patreon** (coming soon) — Monthly support tier
- **One-time donation** — OpenCollective or Buy Me a Coffee
- **Sponsor data sources** — Fund API access for next dataset

### ⭐ Spread the Word
- Share with educators, journalists, researchers
- Use in your articles, papers, presentations
- Star the repo and follow for updates

### 🏢 Institutional Support
- **Universities** — Use in classrooms, link to our dashboards
- **NGOs** — Partner with us, contribute data
- **News organizations** — Embed our maps in articles

---

## 📈 Roadmap

### Phase 1: Launch (Month 1-2) ✅
- [x] Climate dashboard
- [x] Health dashboard  
- [x] Humanitarian dashboard
- [x] Browser-based interface
- [ ] Story mode (in progress)

### Phase 2: Expand & Community (Month 3-4)
- [ ] 2 more datasets per dashboard
- [ ] Comparison tool (pick 2 countries)
- [ ] Export to image/PDF
- [ ] GitHub Discussions community
- [ ] First 5 contributor onboarding

### Phase 3: Growth (Month 5-6)
- [ ] Mobile app (native)
- [ ] API for developers
- [ ] Embed widget (add maps to websites)
- [ ] University partnerships
- [ ] Internationalization (Spanish, Mandarin)

### Phase 4: Sustainability (Month 7+)
- [ ] Donation program (Patreon)
- [ ] Enterprise API tier
- [ ] Academic partnerships
- [ ] 1,000+ GitHub stars
- [ ] 10+ active contributors

See [ROADMAP.md](docs/ROADMAP.md) for detailed plans.

---

## 🚀 Use Cases & Examples

### 📰 For Journalists
*Embed interactive climate map in climate article*
```html
<iframe src="https://visualgeog.com/embed/climate/temperature"></iframe>
```

### 👨‍🎓 For Educators
*Show 10th graders where climate change hits hardest*
- Display sea level rise by region
- Compare developed vs developing impact
- Discuss policy responses

### 🔬 For Researchers
*"What's the correlation between health spending and life expectancy?"*
- Download data as CSV
- Use API to fetch datasets
- Cite sources in academic papers

### 🤲 For Activists
*Share on social media with context*
- "100M people displaced globally. Here's where. Here's how to help."
- Embed in fundraising campaigns
- Track progress toward goals

---

## 📚 Learning & Resources

Each dashboard includes:
- **"Why this matters"** — Context for each metric
- **Key insights** — What the data reveals
- **Organizations fighting this issue** — How to help
- **Academic papers** — Deep dive into research
- **Policy resources** — What governments are doing

---

## 📜 License

MIT License — Free to use, modify, and distribute. See [LICENSE](LICENSE)

---

## 👤 Authors

- **Santosh Goteti** (Lead)
- **Built with AI** — Claude AI & GitHub Copilot
- **Contributors** — You! (We're just getting started)

---

## 🎉 Let's Make Data Matter

This project exists because **the world needs to see its challenges clearly**. Climate change, disease, inequality—they're not abstract statistics. They're real, measurable, and solvable if we understand them.

**Clone this repo. Build with us. Change minds. Drive action.**

---

### Quick Links
- 🔗 [Live Demo](http://localhost:8000) (run locally)
- 📖 [Full Documentation](docs/)
- 🐛 [Report Issues](../../issues)
- 💬 [Join Discussion](../../discussions)
- ⭐ [Star Us](../../)

**Questions?** Open a discussion or email santoshgoteti9@gmail.com

---

*Last updated: May 2026*