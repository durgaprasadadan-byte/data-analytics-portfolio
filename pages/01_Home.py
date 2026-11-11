"""Home: hero, portfolio overview, technology cards and featured projects."""
import streamlit as st

from settings import get_config
from utils import ui
from utils.project_registry import featured_projects

cfg = get_config()

ui.render_hero()
ui.render_hero_actions(cfg)
ui.render_placeholder_notice(cfg)

st.subheader("Portfolio overview")
ui.render_stats()
ui.render_category_grid()

st.subheader("Technology expertise")
ui.render_tool_grid()

st.subheader("Featured projects", anchor="featured-projects")
ui.render_project_cards(featured_projects(), per_row=3)

st.subheader("GitHub and contact")
ui.render_contact_card(cfg)
