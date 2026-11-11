"""About: background, tools, education and resume."""
import streamlit as st

from settings import get_config
from utils import ui

cfg = get_config()

st.title("About")
ui.render_placeholder_notice(cfg)

st.subheader("Professional background")
st.write(cfg.about_summary)

st.subheader("Technical expertise")
ui.render_tool_grid()

st.subheader("Education")
st.write(cfg.education)

st.subheader("Resume")
ui.render_resume_button(cfg, key="about_resume")
