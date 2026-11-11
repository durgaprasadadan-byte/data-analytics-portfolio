"""Contact: email, LinkedIn and GitHub."""
import streamlit as st

from settings import get_config
from utils import ui

cfg = get_config()

st.title("Contact")
ui.render_placeholder_notice(cfg)
st.write("Reach out about analytics roles, projects or collaboration.")
ui.render_contact_card(cfg)
