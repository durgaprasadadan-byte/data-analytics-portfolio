"""Portfolio settings.

Each value is read, in order, from:
  1. an environment variable,
  2. Streamlit secrets (.streamlit/secrets.toml locally, the Secrets panel on
     Streamlit Community Cloud),
  3. the placeholder default below.

Nothing here is secret, but using the same mechanism keeps personal details out
of the code and lets later phases reuse it for external dashboard URLs.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

# Profile defaults can be overridden through secrets or environment variables.
DEFAULTS: dict[str, str] = {
    "PORTFOLIO_NAME": "Durga Prasad Jinna",
    "PORTFOLIO_ROLE": "Software Developer",
    "GITHUB_URL": "https://github.com/your-username",
    "LINKEDIN_URL": "https://www.linkedin.com/in/your-profile",
    "CONTACT_EMAIL": "durga.jinna@lindsey.edu",
    "ABOUT_SUMMARY": (
        "Software developer and data professional with experience in client-facing "
        "consulting, data engineering and analytics across financial services and "
        "healthcare. Based in Newark, Delaware."
    ),
    "EXPERIENCE": (
        "**Software Developer - Infosys (Full-time)**  \n"
        "Mar 2024 - Nov 2025 | Newark, Delaware (Hybrid) | Client-facing consulting engagement\n\n"
        "**Data Engineer - PNC (Contract)**  \n"
        "Jun 2023 - Feb 2024 | Remote\n\n"
        "**Data Analyst - Omnicom Health (Full-time)**  \n"
        "Oct 2020 - Jul 2021 | Hyderabad"
    ),
    "EDUCATION": (
        "**Lindsey Wilson University** | Mar 2026 - Dec 2029 (Expected)  \n"
        "Dual Master's Degree in Artificial Intelligence and Business Administration (MBA)\n\n"
        "**University of North Texas** | 2023  \n"
        "Master of Science in Data Science  \n"
        "Relevant coursework: Database Systems, Machine Learning, Data Mining and Statistics"
    ),
}
PLACEHOLDER_KEYS = frozenset({"GITHUB_URL", "LINKEDIN_URL"})
RESUME_PATH_DEFAULT = "assets/resume.pdf"


def _read_setting(key: str, default: str) -> str:
    value = os.environ.get(key)
    if not value:
        try:
            import streamlit as st

            value = st.secrets.get(key)
        except Exception:  # no secrets file, or running outside Streamlit
            value = None
    return str(value).strip() if value else default


def _is_http_url(value: str) -> bool:
    return value.lower().startswith(("http://", "https://"))


def _is_email(value: str) -> bool:
    local, _, domain = value.partition("@")
    return bool(local) and "." in domain


def _resolve_resume(raw_path: str) -> Path | None:
    """Return the resume file if it exists inside the project folder."""
    candidate = (ROOT_DIR / raw_path).resolve()
    try:
        candidate.relative_to(ROOT_DIR)
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


@dataclass(frozen=True)
class PortfolioConfig:
    name: str
    role: str
    github_url: str
    linkedin_url: str
    email: str
    about_summary: str
    experience: str
    education: str
    resume_file: Path | None
    placeholders: tuple[str, ...]  # setting keys still using placeholder values

    @property
    def is_configured(self) -> bool:
        return not self.placeholders


@lru_cache(maxsize=1)
def get_config() -> PortfolioConfig:
    values: dict[str, str] = {}
    placeholders: list[str] = []
    for key, default in DEFAULTS.items():
        value = _read_setting(key, default)
        if key.endswith("_URL") and not _is_http_url(value):
            value = default  # reject malformed links rather than render them
        if key == "CONTACT_EMAIL" and not _is_email(value):
            value = default
        if key in PLACEHOLDER_KEYS and value == default:
            placeholders.append(key)
        values[key] = value

    return PortfolioConfig(
        name=values["PORTFOLIO_NAME"],
        role=values["PORTFOLIO_ROLE"],
        github_url=values["GITHUB_URL"],
        linkedin_url=values["LINKEDIN_URL"],
        email=values["CONTACT_EMAIL"],
        about_summary=values["ABOUT_SUMMARY"],
        experience=values["EXPERIENCE"],
        education=values["EDUCATION"],
        resume_file=_resolve_resume(_read_setting("RESUME_PATH", RESUME_PATH_DEFAULT)),
        placeholders=tuple(placeholders),
    )
