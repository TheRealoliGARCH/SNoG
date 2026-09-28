import io
import re
import pandas as pd
import requests
import streamlit as st

SPREADSHEET_ID = "1pPoRfEM6r6_ybbtneyAqfKt1epj9YcQWadpw2V944Ro"
TARGET_TOTAL = 48524
TARGET_OLIGARCH = 729
TARGET_NON_OLIGARCH = 47795
DISTRICTS = [f"District {i}" for i in range(1, 10)]

st.set_page_config(page_title="SNoG Enumeration Dashboard", page_icon="🔢", layout="wide")

def csv_url(sheet_id, gid):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

def norm(x):
    return re.sub(r"[^a-z0-9]+", "_", str(x).strip().lower()).strip("_")

def find_col(columns, candidates):
    ncols = {norm(c): c for c in columns}
    for c in candidates:
        if norm(c) in ncols:
            return ncols[norm(c)]
    for n, original in ncols.items():
        if any(norm(c) in n for c in candidates):
            return original
    return None

@st.cache_data(ttl=60)
def load_sheet(sheet_id, gid):
    url = csv_url(sheet_id, gid)
    r = requests.get(url, timeout=30, headers={"User-Agent": "SNoG-Streamlit/1.0"})
    r.raise_for_status()
    return pd.read_csv(io.BytesIO(r.content)), url

def clean_profession(s):
    return s.astype(str).str.strip().str.lower().replace({
        "oligarch": "oliGARCH",
        "oli garch": "oliGARCH",
        "oli_garch": "oliGARCH",
        "non-oligarch": "non-oliGARCH",
        "non oligarch": "non-oliGARCH",
        "non_oligarch": "non-oliGARCH",
    })

def clean_district(s):
    vals = s.astype(str).str.strip()
    nums = vals.str.extract(r"(\d+)", expand=False)
    def f(x):
        try:
            n = int(x)
            return f"District {n}" if 1 <= n <= 9 else str(x)
        except (TypeError, ValueError):
            return str(x)
    return nums.map(f).fillna(vals)

with st.sidebar:
    st.header("Google Sheets")
    gid = st.text_input("Response worksheet gid", "0")
    if st.button("Refresh now", type="primary"):
        st.cache_data.clear()
        st.rerun()

st.title("Standard Nuclear oliGARCHy")
st.subheader("Google Sheets Enumeration Dashboard")
st.caption("Read-only dashboard. Google Sheets is the source of truth.")

try:
    df, source = load_sheet(SPREADSHEET_ID, gid)
except Exception as e:
    st.error("Could not read the Google Sheets response worksheet.")
    st.code(str(e))
    st.info("The worksheet must be readable through Google's CSV export, or the application must be adapted to use authenticated Google Sheets API credentials.")
    st.stop()

profession_col = find_col(df.columns, ["Your Profession", "Profession", "profession"])
district_col = find_col(df.columns, ["Your District", "District", "district"])
timestamp_col = find_col(df.columns, ["Timestamp", "timestamp", "submitted_at"])

if profession_col is None or district_col is None:
    st.error("Could not identify the profession and district columns.")
    st.write("Columns returned by the spreadsheet:", list(df.columns))
    st.stop()

profession = clean_profession(df[profession_col])
district = clean_district(df[district_col])

oli_total = int((profession == "oliGARCH").sum())
non_total = int((profession == "non-oliGARCH").sum())
total = len(df)
unclassified = total - oli_total - non_total
remaining = max(TARGET_TOTAL - total, 0)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Registered entries", f"{total:,}", f"{100*total/TARGET_TOTAL:.2f}% of 48,524")
m2.metric("oliGARCH", f"{oli_total:,}", f"{100*oli_total/TARGET_OLIGARCH:.2f}% of 729")
m3.metric("non-oliGARCH", f"{non_total:,}", f"{100*non_total/TARGET_NON_OLIGARCH:.2f}% of 47,795")
m4.metric("Remaining", f"{remaining:,}", "to 48,524")
st.progress(min(total / TARGET_TOTAL, 1.0))

if unclassified:
    st.warning(f"{unclassified:,} row(s) have an unrecognized profession value.")

table = pd.crosstab(district, profession)
for c in ["oliGARCH", "non-oliGARCH"]:
    if c not in table.columns:
        table[c] = 0
table = table[["oliGARCH", "non-oliGARCH"]].reindex(DISTRICTS, fill_value=0)
table["Total"] = table["oliGARCH"] + table["non-oliGARCH"]

st.header("District-wise enumeration")
shown = table.copy()
shown.loc["Total"] = shown.sum()
st.dataframe(shown.style.format("{:,.0f}"), use_container_width=True)

st.header("District distribution")
st.bar_chart(table[["oliGARCH", "non-oliGARCH"]], height=420)

if timestamp_col is not None and total:
    ts = pd.to_datetime(df[timestamp_col], errors="coerce")
    if ts.notna().any():
        st.caption(f"Latest response: {ts.max()}")

with st.expander("Raw Google Sheets data"):
    st.dataframe(df, use_container_width=True, hide_index=True)

st.download_button(
    "Download current spreadsheet snapshot",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="snog_google_sheets_snapshot.csv",
    mime="text/csv",
)

st.caption(f"Source CSV endpoint: {source}")
