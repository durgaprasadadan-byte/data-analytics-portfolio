"""Entry point: page configuration, shared styling and navigation.

Run with:  streamlit run app.py
"""
import streamlit as st

from settings import get_config
from utils.project_registry import CATEGORIES
from utils.ui import inject_css, render_sidebar_footer

cfg = get_config()

st.set_page_config(
    page_title=f"{cfg.name} | Data Analytics & BI Portfolio",
    page_icon=":material/insights:",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()


def _category_page(key: str) -> st.Page:
    category = CATEGORIES[key]
    return st.Page(category.page_path, title=category.label, icon=category.icon)


navigation = st.navigation(
    {
        "": [st.Page("pages/01_Home.py", title="Home", icon=":material/home:", default=True)],
        "Business Intelligence": [_category_page(k) for k in ("tableau", "power_bi", "excel")],
        "Data Science": [_category_page(k) for k in ("python_analytics", "machine_learning", "end_to_end")],
        "Profile": [
            st.Page("pages/08_About.py", title="About", icon=":material/person:"),
            st.Page("pages/09_Contact.py", title="Contact", icon=":material/mail:"),
        ],
    }
)
render_sidebar_footer(cfg)
navigation.run()
