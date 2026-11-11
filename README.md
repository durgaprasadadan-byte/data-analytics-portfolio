# Data Analytics & Business Intelligence Portfolio

A multi-page Streamlit portfolio covering Tableau, Power BI, Excel, Python analytics and
machine learning. It is built in phases; this repository is currently at **Phase 1**
(homepage and navigation).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Configure your details

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in your name,
GitHub, LinkedIn, email, summary and education. Environment variables with the same names
also work. Anything missing shows a placeholder and a warning on the page.

For a resume download, put the file at `assets/resume.pdf` (or set `RESUME_PATH`). It is
served from the repository, so only commit a version you are happy to publish.

## Structure

| Path | Purpose |
|---|---|
| `app.py` | Page config, shared CSS, navigation |
| `settings.py` | Profile configuration (env vars, secrets, placeholders) |
| `pages/` | One script per navigation entry |
| `utils/project_registry.py` | All projects, categories, tools and derived statistics |
| `utils/ui.py` | Reusable UI components |
| `assets/styles/main.css` | Custom styling |
| `tests/` | Logic tests (`python -m pytest` after `pip install pytest`) |

## Adding or promoting a project

Edit its entry in `utils/project_registry.py`: set `status` to `Status.COMPLETED` and, if it
uses a real dataset, `dataset_name`. Homepage statistics update automatically and count only
completed projects.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub (`.streamlit/secrets.toml` is git-ignored).
2. Sign in at https://share.streamlit.io with GitHub and choose **Create app**.
3. Select the repository, branch `main`, and main file `app.py`.
4. Under **Advanced settings**, paste your secrets (same keys as `secrets.toml.example`).
5. Deploy. Later phases add dependencies to `requirements.txt`; the app redeploys on each push.

## Roadmap

| Phase | Scope | Status |
|---|---|---|
| 1 | Homepage and navigation | Done |
| 2 | Searchable catalog, technology and domain filters | Next |
| 3 | Reusable project page template | Planned |
| 4 | Python analytics projects | Planned |
| 5 | Scikit-learn projects | Planned |
| 6 | Excel, Tableau and Power BI integrations | Planned |
| 7 | End-to-end platforms | Planned |
| 8 | GitHub links, documentation, deployment polish | Planned |
