import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="SEO Doctor AI")

st.title("🔍 SEO Doctor AI")
st.write("Analyze your website SEO easily")

url = st.text_input("Enter Website URL (with https://)")

def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else "No title"

    meta = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta["content"] if meta else "No meta description"

    content = soup.get_text()
    word_count = len(content.split())

    images = soup.find_all("img")

    return title, meta_desc, word_count, images


if st.button("Analyze"):

    if not url.startswith("http"):
        st.error("Enter valid URL (with http/https)")
    else:
        try:
            title, meta_desc, word_count, images = scrape(url)

            issues = []

            if len(title) < 50:
                issues.append("Title too short")

            if meta_desc == "No meta description":
                issues.append("Meta description missing")

            if word_count < 300:
                issues.append("Content too short")

            missing_alt = sum(1 for img in images if not img.get("alt"))
            if missing_alt > 0:
                issues.append(f"{missing_alt} images missing ALT tags")

            score = max(100 - len(issues)*10, 0)

            st.subheader("SEO Score")
            st.success(f"{score}/100")

            st.subheader("Issues")
            if issues:
                for i in issues:
                    st.write("❌", i)
            else:
                st.write("No issues found 🎉")

        except:
            st.error("Unable to fetch website. Try another URL.")
