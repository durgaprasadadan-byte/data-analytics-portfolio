"""Reusable Streamlit UI components. No business logic lives here."""
from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from settings import ROOT_DIR, PortfolioConfig
from utils.project_registry import (
    CATEGORIES,
    TOOLS,
    Project,
    Status,
    portfolio_stats,
    projects_by_category,
    tool_usage,
)

_CSS_PATH = ROOT_DIR / "assets" / "styles" / "main.css"
_RESUME_MIME = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
WORKFLOW_STEPS = (
    "Data collection",
    "Validation",
    "Cleaning",
    "Transformation",
    "Feature engineering",
    "Analysis and modelling",
    "Results",
)


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


def _html(*parts: str) -> str:
    # Joined without newlines: blank lines or 4-space indents would make
    # Streamlit's markdown parser treat the HTML as a code block.
    return "".join(parts)


@st.cache_data(show_spinner=False)
def _read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


@st.cache_data(show_spinner=False)
def _read_bytes(path: str, modified: float) -> bytes:
    # `modified` is part of the cache key so a replaced resume is picked up.
    return Path(path).read_bytes()


def _grid(count: int, per_row: int) -> list:
    """Return one column slot per item, laid out in rows of `per_row`."""
    slots: list = []
    for start in range(0, count, per_row):
        row = st.columns(per_row)
        slots.extend(row[: min(per_row, count - start)])
    return slots


def inject_css() -> None:
    try:
        css = _read_text(str(_CSS_PATH))
    except OSError:
        st.warning("Stylesheet assets/styles/main.css could not be loaded; using default styling.")
        return
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def status_badge(status: Status) -> str:
    css = {Status.PLANNED: "planned", Status.IN_PROGRESS: "progress", Status.COMPLETED: "done"}[status]
    return f'<span class="badge badge-{css}">{_esc(status.value)}</span>'


def _chips(values, css_class: str = "chip") -> str:
    return "".join(f'<span class="{css_class}">{_esc(v)}</span>' for v in values)


def render_placeholder_notice(cfg: PortfolioConfig) -> None:
    if cfg.placeholders:
        keys = ", ".join(f"`{k}`" for k in cfg.placeholders)
        st.warning(
            f"Placeholder profile details are in use for {keys}. Set them in "
            "`.streamlit/secrets.toml` (see `secrets.toml.example`). This notice disappears "
            "once every value is set."
        )


def render_sidebar_footer(cfg: PortfolioConfig) -> None:
    with st.sidebar:
        st.markdown(
            _html(
                '<div class="sidebar-brand">',
                f'<div class="sidebar-name">{_esc(cfg.name)}</div>',
                f'<div class="sidebar-role">{_esc(cfg.role)}</div>',
                "</div>",
            ),
            unsafe_allow_html=True,
        )
        st.link_button("GitHub", cfg.github_url)
        st.link_button("LinkedIn", cfg.linkedin_url)


def render_hero() -> None:
    steps = "".join(f'<span class="flow-step">{_esc(s)}</span>' for s in WORKFLOW_STEPS)
    st.markdown(
        _html(
            '<div class="hero">',
            '<h1 class="hero-title">Data Analytics &amp; Business Intelligence Portfolio</h1>',
            '<p class="hero-sub">Transforming Data into Insights, Intelligence, and Business Value.</p>',
            '<p class="hero-desc">Explore practical projects across Business Intelligence, '
            "Data Analytics, Python, and Machine Learning.</p>",
            f'<div class="flow" aria-label="Typical project workflow">{steps}</div>',
            "</div>",
        ),
        unsafe_allow_html=True,
    )


def render_resume_button(cfg: PortfolioConfig, key: str) -> None:
    label = "Download Resume"
    path = cfg.resume_file
    if path is None:
        st.button(label, key=key, disabled=True,
                  help="Add your resume at assets/resume.pdf or set RESUME_PATH.")
        return
    try:
        data = _read_bytes(str(path), path.stat().st_mtime)
    except OSError:
        st.button(label, key=key, disabled=True, help="The resume file could not be read.")
        return
    st.download_button(label, data=data, file_name=path.name, key=key,
                       mime=_RESUME_MIME.get(path.suffix.lower(), "application/octet-stream"))


def render_hero_actions(cfg: PortfolioConfig) -> None:
    explore, github, resume, _ = st.columns([1.2, 1, 1.2, 3])
    with explore:
        st.markdown('<a class="btn-link" href="#featured-projects">Explore Projects</a>',
                    unsafe_allow_html=True)
    with github:
        st.link_button("View GitHub", cfg.github_url)
    with resume:
        render_resume_button(cfg, key="hero_resume")


def render_stats() -> None:
    s = portfolio_stats()
    items = [
        ("Total projects", s.total, f"{s.live} published, {s.total - s.live} not yet published"),
        ("Technology categories", s.categories, "Business intelligence, Python and ML"),
        ("Datasets analyzed", s.datasets_live, "Counted from published projects only"),
        ("Machine learning models", s.ml_live, f"Published of {s.ml_total} planned"),
    ]
    for col, (label, value, caption) in zip(st.columns(4), items):
        with col, st.container(border=True):
            st.metric(label, value)
            st.caption(caption)


def render_category_grid() -> None:
    cats = list(CATEGORIES.values())
    for slot, cat in zip(_grid(len(cats), 3), cats):
        projects = projects_by_category(cat.key)
        live = sum(1 for p in projects if p.status is Status.COMPLETED)
        with slot, st.container(border=True):
            st.markdown(
                _html(f'<div class="card-title">{_esc(cat.label)}</div>',
                      f'<p class="card-text">{_esc(cat.summary)}</p>',
                      f'<div class="card-meta">{len(projects)} projects, {live} published</div>'),
                unsafe_allow_html=True,
            )
            st.page_link(cat.page_path, label=f"Open {cat.label}", icon=cat.icon)


def render_tool_grid() -> None:
    for slot, tool in zip(_grid(len(TOOLS), 3), TOOLS):
        total, live = tool_usage(tool.key)
        if total == 0:
            usage = "Not used in a listed project yet"
        else:
            usage = f"{total} planned project{'s' if total != 1 else ''}"
            if live:
                usage += f", {live} published"
        with slot:
            st.markdown(
                _html('<div class="tool-card">',
                      f'<div class="card-title">{_esc(tool.label)}</div>',
                      f'<p class="card-text">{_esc(tool.blurb)}</p>',
                      f'<div class="card-meta">{_esc(usage)}</div>',
                      "</div>"),
                unsafe_allow_html=True,
            )


def render_project_card(project: Project, *, show_link: bool = True) -> None:
    category = CATEGORIES[project.category]
    with st.container(border=True):
        st.markdown(
            _html(
                '<div class="chip-row">', status_badge(project.status),
                _chips([category.label, project.domain]), "</div>",
                f'<div class="card-title">{_esc(project.title)}</div>',
                f'<p class="card-text">{_esc(project.description)}</p>',
                f'<div class="card-meta">Difficulty: {_esc(project.difficulty)}</div>',
                '<div class="chip-row">', _chips(project.tools, "chip chip-tool"), "</div>",
            ),
            unsafe_allow_html=True,
        )
        if show_link:
            st.page_link(category.page_path, label="Explore project")


def render_project_cards(projects: list[Project], per_row: int = 3, *, show_link: bool = True) -> None:
    for slot, project in zip(_grid(len(projects), per_row), projects):
        with slot:
            render_project_card(project, show_link=show_link)


def render_contact_card(cfg: PortfolioConfig) -> None:
    left, right = st.columns(2)
    with left, st.container(border=True):
        st.markdown('<div class="card-title">GitHub</div>', unsafe_allow_html=True)
        st.write("Source code, notebooks and documentation for each project.")
        st.link_button("View GitHub profile", cfg.github_url)
    with right, st.container(border=True):
        st.markdown('<div class="card-title">Get in touch</div>', unsafe_allow_html=True)
        st.markdown(f"Email: [{cfg.email}](mailto:{cfg.email})")
        st.link_button("Connect on LinkedIn", cfg.linkedin_url)


def render_category_page(key: str) -> None:
    category = CATEGORIES[key]
    projects = projects_by_category(key)
    live = sum(1 for p in projects if p.status is Status.COMPLETED)
    st.title(category.label)
    st.write(category.summary)
    published = f"{live} of {len(projects)} projects are published" if live else "No projects are published yet"
    st.info(f"{published}. Interactive project pages for this section are scheduled for Phase {category.phase}.")
    render_project_cards(projects, per_row=2, show_link=False)
