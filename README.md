# 🧬 Samflix

Vídeos e documentários (BioFlix) de estudo do Prof. Samuel Rocha (Biologia, Ciências, Química 9º ano e Direito/Fiscalização Ambiental), organizados por categoria a partir das playlists do canal **@leumasrock** no YouTube. Inspirado no material **Bioflix**.

Site: https://leumasrock-spec.github.io/samflix/

- `index.html` – site completo (dados embutidos)
- `data/samflix.json` – lista de categorias, vídeos e links de apoio
- `data/bioflix.json` + `assets/bioflix/` – documentários do BioFlix (https://bioflix.vercel.app/), gerados por `build_bioflix.py`
- Gerar: `python3 build_data.py` (precisa dos JSON do yt-dlp em /tmp) · `python3 build_bioflix.py` · `python3 build_site.py`
