# SNoG Google Sheets Streamlit Dashboard

Read-only dashboard for the SNoG Google Forms response spreadsheet.

Source spreadsheet ID:
`1pPoRfEM6r6_ybbtneyAqfKt1epj9YcQWadpw2V944Ro`

The application:
- reads the Google Sheet as CSV;
- counts total responses;
- counts `oliGARCH` and `non-oliGARCH`;
- displays District 1 through District 9 separately;
- compares counts with 729, 47,795 and 48,524 targets;
- refreshes from Google Sheets;
- exports the current spreadsheet snapshot.

Run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

If the response worksheet is not the first worksheet, enter its `gid` in the sidebar.
