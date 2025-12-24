import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

st.set_page_config(page_title="Domain Checker", layout="wide")

st.title("🔍 Domain Presence Checker in Page Source")

st.markdown("""
### Instructions
- Paste **URLs** in the left box (one per line)
- Paste **Domain name(s)** in the right box (one per line)
- Output will show **YES / NO**
""")

col1, col2 = st.columns(2)

with col1:
    urls_input = st.text_area(
        "📄 Paste All URLs",
        height=300,
        placeholder="https://example.com\nhttps://another-site.com"
    )

with col2:
    domains_input = st.text_area(
        "🌐 Paste Domain Name(s)",
        height=300,
        placeholder="example.com\nanotherdomain.com"
    )

if st.button("🚀 Check Domains"):

    urls = [u.strip() for u in urls_input.splitlines() if u.strip()]
    domains = [d.strip().lower() for d in domains_input.splitlines() if d.strip()]

    results = []

    for url in urls:
        try:
            response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            status_code = response.status_code

            if status_code != 200:
                for domain in domains:
                    results.append({
                        "URL": url,
                        "Domain": domain,
                        "Domain Found": "NO",
                        "URL Status": f"Not Working ({status_code})"
                    })
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            page_source = soup.prettify().lower()

            for domain in domains:
                found = "YES" if domain in page_source else "NO"
                results.append({
                    "URL": url,
                    "Domain": domain,
                    "Domain Found": found,
                    "URL Status": "Working"
                })

        except Exception as e:
            for domain in domains:
                results.append({
                    "URL": url,
                    "Domain": domain,
                    "Domain Found": "NO",
                    "URL Status": "Not Working"
                })

    df = pd.DataFrame(results)

    st.subheader("📊 Final Output (Copyable)")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="domain_check_results.csv",
        mime="text/csv"
    )
