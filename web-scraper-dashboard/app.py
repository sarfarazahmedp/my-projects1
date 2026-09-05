"""Run with: streamlit run app.py"""
from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(page_title="Quote Scout", page_icon="📊", layout="wide")
st.title("Quote Scout")
st.caption("A small web-scraping and data-visualization project")

@st.cache_data(ttl=3600)
def fetch_quotes():
    response = requests.get("https://quotes.toscrape.com/", timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    rows = []
    for quote in soup.select(".quote"):
        rows.append({
            "quote": quote.select_one(".text").get_text(strip=True),
            "author": quote.select_one(".author").get_text(strip=True),
            "tags": ", ".join(tag.get_text(strip=True) for tag in quote.select(".tag")),
        })
    return pd.DataFrame(rows)

try:
    data = fetch_quotes()
except requests.RequestException as error:
    st.error(f"Could not fetch demo data: {error}")
    st.stop()

authors = st.multiselect("Filter by author", sorted(data.author.unique()))
filtered = data[data.author.isin(authors)] if authors else data
left, right, export = st.columns(3)
left.metric("Quotes", len(filtered))
right.metric("Authors", filtered.author.nunique())
export.download_button("Download CSV", filtered.to_csv(index=False), "quotes.csv", "text/csv")

st.subheader("Quotes by author")
counts = filtered.author.value_counts().sort_values()
fig, ax = plt.subplots()
counts.plot.barh(ax=ax, color="#e65426")
ax.set_xlabel("Number of quotes")
ax.set_ylabel("")
st.pyplot(fig, clear_figure=True)
st.subheader("Scraped records")
st.dataframe(filtered, use_container_width=True, hide_index=True)
