"""Logic tests that need no running Streamlit server.  Run: python -m pytest"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import settings
from utils import project_registry as reg


def test_registry_has_22_projects_across_6_categories():
    assert len(reg.PROJECTS) == 22
    assert set(reg.CATEGORIES) == {p.category for p in reg.PROJECTS}


def test_each_technology_category_has_four_projects():
    for key, cat in reg.CATEGORIES.items():
        expected = 4 if cat.is_technology else 2
        assert len(reg.projects_by_category(key)) == expected, key


def test_stats_report_nothing_published_while_all_planned():
    s = reg.portfolio_stats()
    assert (s.total, s.live, s.datasets_live, s.ml_live) == (22, 0, 0, 0)
    assert s.categories == 5 and s.ml_total == 4


def test_stats_update_when_a_project_is_completed():
    done = reg.Project("x", "X", "machine_learning", "d", "Beginner", "t", ("Python",),
                       status=reg.Status.COMPLETED, dataset_name="demo")
    original = reg.PROJECTS
    try:
        reg.PROJECTS = original + (done,)
        s = reg.portfolio_stats()
        assert (s.live, s.datasets_live, s.ml_live) == (1, 1, 1)
        assert reg.tool_usage("Python")[1] == 1
    finally:
        reg.PROJECTS = original


def test_featured_projects_span_distinct_categories():
    cats = [p.category for p in reg.featured_projects()]
    assert len(cats) == len(set(cats)) == 6


def test_category_pages_exist_on_disk():
    root = Path(__file__).resolve().parents[1]
    for cat in reg.CATEGORIES.values():
        assert (root / cat.page_path).is_file(), cat.page_path


def test_settings_default_to_placeholders(monkeypatch):
    for key in settings.DEFAULTS:
        monkeypatch.delenv(key, raising=False)
    settings.get_config.cache_clear()
    cfg = settings.get_config()
    assert set(cfg.placeholders) == set(settings.DEFAULTS)
    assert not cfg.is_configured


def test_settings_reject_malformed_values_and_accept_valid(monkeypatch):
    monkeypatch.setenv("GITHUB_URL", "javascript:alert(1)")
    monkeypatch.setenv("CONTACT_EMAIL", "not-an-email")
    monkeypatch.setenv("PORTFOLIO_NAME", "Jane Doe")
    settings.get_config.cache_clear()
    cfg = settings.get_config()
    assert cfg.github_url == settings.DEFAULTS["GITHUB_URL"]
    assert cfg.email == settings.DEFAULTS["CONTACT_EMAIL"]
    assert cfg.name == "Jane Doe" and "PORTFOLIO_NAME" not in cfg.placeholders
    settings.get_config.cache_clear()


def test_resume_path_cannot_escape_project_folder(monkeypatch):
    monkeypatch.setenv("RESUME_PATH", "../../etc/passwd")
    settings.get_config.cache_clear()
    assert settings.get_config().resume_file is None
    settings.get_config.cache_clear()
