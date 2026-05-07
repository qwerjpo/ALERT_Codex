# World Monitor - Personal OSINT Dashboard

Real-time collection and display of global military/security and political/diplomatic signals.
Uses **only free, public sources** - no API keys, no subscriptions required.

## Quick Start

### Windows (double-click setup)
1. Install [Python 3.12](https://www.python.org/downloads/windows/) - tick **"Add python.exe to PATH"**
2. Download this repo as ZIP and extract
3. Double-click **`scripts\setup.bat`** (first time only, takes a few minutes)
4. Double-click **`run.bat`** - browser opens automatically at http://127.0.0.1:8000

### macOS / Linux
```bash
git clone <this-repo> && cd world-monitor
./scripts/setup.sh run
```

## Free Online Hosting (Render.com)
1. Sign up at [render.com](https://render.com) (free)
2. New > Web Service > connect this GitHub repo
3. Build: `pip install -r requirements.txt` / Start: `python -m backend.main`
4. Deploy - get a public URL in ~2 minutes

## Data Sources (all free, no registration)
- **Military/Security**: ISW, Defense News, The War Zone, Bellingcat, Long War Journal, Naval News
- **Politics/Diplomacy**: Reuters, BBC, Al Jazeera, NHK World, France24, DW, UN News, NATO, State Dept
- **Cyber**: CISA, The Record, BleepingComputer, NVD CVE
- **Structured APIs**: GDELT 2.0, ReliefWeb (UN OCHA), USGS Earthquake feed
- **Regions**: Global / Europe / Russia-CIS / Middle East / Asia-Pacific / Americas / Africa

## License
MIT
