<pre align="center">
██████╗ ███████╗██████╗  ██████╗ ███████╗██╗███╗   ██╗
██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔════╝██║████╗  ██║
██████╔╝█████╗  ██████╔╝██║   ██║███████╗██║██╔██╗ ██║
██╔══██╗██╔══╝  ██╔══██╗██║   ██║╚════██║██║██║╚██╗██║
██████╔╝███████╗██║  ██║╚██████╔╝███████║██║██║ ╚████║
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝
</pre>

<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&multiline=true&repeat=true&width=780&height=70&lines=Full-stack+developer+building+practical+products;across+AI%2C+Web3%2C+and+cloud-native+systems.)](https://git.io/typing-svg)

<a href="https://github.com/Berosin"><img src="https://img.shields.io/github/followers/Berosin?label=Follow&style=social" /></a>
<a href="https://linkedin.com/in/berosin"><img src="https://img.shields.io/badge/LinkedIn-Berosin-0A66C2?style=flat&logo=linkedin&logoColor=white" /></a>
<img src="https://komarev.com/ghpvc/?username=Berosin&label=Profile+Views&color=58A6FF&style=flat" />

</div>

<br/>

<div align="center">

<img src="avi-ascii.svg" width="460" alt="ASCII portrait, rendered as a terminal session" />

<br/><br/>

<img src="info-card.svg" width="460" alt="neofetch-style info card" />

</div>

<br/>

## 🛠️ Tech Stack

<div align="center">

<sub>**Languages**</sub>
<br/>
<img src="https://skillicons.dev/icons?i=js,ts,py,java,dart,php,html,css,c&theme=dark" />

<br/><br/>

<sub>**Frontend & Frameworks**</sub>
<br/>
<img src="https://skillicons.dev/icons?i=react,nextjs,vite,nodejs,spring,fastapi&theme=dark" />

<br/><br/>

<sub>**Data & Cloud**</sub>
<br/>
<img src="https://skillicons.dev/icons?i=mongodb,mysql,firebase,supabase&theme=dark" />

<br/><br/>

<sub>**AI & Web3**</sub>
<br/>
<img src="https://skillicons.dev/icons?i=solidity&theme=dark" />
<br/>
<sub><i>+ RAG pipelines &amp; IBM Watsonx for applied AI &nbsp;·&nbsp; Foundry &amp; wagmi/viem for on-chain dev</i></sub>

<br/><br/>

<sub>**Tools**</sub>
<br/>
<img src="https://skillicons.dev/icons?i=git,github,figma&theme=dark" />

</div>

<br/>

## 📊 GitHub Stats

<div align="center">

<img height="165" src="https://github-readme-stats.vercel.app/api?username=Berosin&show_icons=true&theme=tokyonight&hide_border=true&count_private=true" />
<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Berosin&layout=compact&theme=tokyonight&hide_border=true" />

<img src="https://streak-stats.demolab.com/?user=Berosin&theme=tokyonight&hide_border=true" />

<img src="https://github-profile-trophy.vercel.app/?username=Berosin&theme=tokyonight&no-frame=true&row=1&column=6" />

</div>

<br/>

<details>
<summary><b>🧪 How the portrait &amp; info card are built (click to expand)</b></summary>
<br/>

Two hand-rolled Python scripts turn a plain photo into the self-typing SVG art above — no external ASCII-art service involved.

**Setup** — `scripts/requirements.txt` lists everything needed. The daily automation only needs `requests` + `beautifulsoup4`; the portrait libraries (`pillow`, `numpy`, `opencv-python-headless`, `onnxruntime`, `rembg`) only matter when you swap in a new photo:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
```

**Step 1 — Prep the photo** (`scripts/prep_photo.py`). A flatly-lit face converts to a dark, unreadable blob, so this script: removes the background with `rembg`, boosts local contrast with OpenCV's CLAHE, then composites onto pure white so the background maps to blank space in the ASCII ramp.

```bash
python scripts/prep_photo.py source-photo.jpg
```

**Step 2 — Convert to a self-typing, terminal-framed SVG** (`scripts/make_ascii_svg.py`). The prepped image is downsampled to an ~80-column character grid (rows auto-computed from the photo's aspect ratio so nothing gets stretched); each pixel's brightness picks a glyph from a density ramp (`" .`:-=+*cs#%@"`, bright → sparse, dark → dense). It's rendered **monochrome** — one light-gray fill, no per-character rainbow — wrapped in a terminal-window card (title bar, traffic-light dots, a closing `whoami` prompt line), and each row wipes in left-to-right with a small cursor block, staggered top-to-bottom, printing once and freezing (SMIL, no loop).

```bash
python scripts/make_ascii_svg.py source-photo-prepped.png -o avi-ascii.svg --whoami-name "Berosin BF"
```

**Step 3 — Build the neofetch-style info card** (`scripts/make_info_card.py`). A small hand-authored SVG with a title bar and `Role` / `Interests` / `Stack` / `Highlights` rows that fade + slide in on a stagger — the story the stats widgets above can't tell. Set `STATIC=1` for a frozen frame (handy for local previews).

```bash
python scripts/make_info_card.py -o info-card.svg
```

Commit `avi-ascii.svg` and `info-card.svg` to the repo root and the README picks them up automatically.

**Prefer it fully automatic?** `.github/workflows/portrait.yml` runs this same pipeline weekly (and on-demand from the Actions tab), pulling your avatar directly from `https://github.com/<username>.png` — GitHub's live avatar URL — via `scripts/fetch_avatar.py`. Change your profile picture on GitHub and the portrait updates itself on the next run, no manual re-upload needed.

</details>

<br/>

## 🐍 Contribution Snake

<div align="center">

<img src="https://raw.githubusercontent.com/Berosin/Berosin/output/github-contribution-grid-snake.svg" />

<sub>Animated snake eating my contribution graph — powered by a GitHub Action (setup below ⬇️)</sub>

</div>

<br/>

## 📈 Activity Graph

<div align="center">

<img src="https://github-readme-activity-graph.vercel.app/graph?username=Berosin&theme=tokyo-night&hide_border=true&days=61" width="100%"/>

</div>

<br/>

<div align="center">

## 🤝 Connect With Me

<a href="https://linkedin.com/in/berosin"><img src="https://skillicons.dev/icons?i=linkedin&theme=dark" height="50"/></a>
&nbsp;
<a href="https://github.com/Berosin"><img src="https://skillicons.dev/icons?i=github&theme=dark" height="50"/></a>

<br/><br/>

### 💭 Random dev wisdom, refreshed every visit

![Quote](https://quotes-github-readme.vercel.app/api?type=horizontal&theme=tokyonight)

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:8E2DE2,50:4A00E0,100:00C6FF&height=120&section=footer"/>

</div>