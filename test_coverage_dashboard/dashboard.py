import streamlit as st
import pandas as pd
import os
from parse_coverage import parse_coverage
import matplotlib.pyplot as plt

st.title("📊 Test Coverage Dashboard")

# Run coverage automatically button
if st.button("Run Tests & Refresh Coverage"):
    os.system("./run_coverage.sh")

# Load coverage data
data = parse_coverage()
df = pd.DataFrame(data)

st.subheader("Coverage by File")
st.dataframe(df)

# Bar chart
fig, ax = plt.subplots()
ax.bar(df["file"], df["coverage"])
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# Highlight low coverage
threshold = st.slider("Coverage Threshold (%)", 0, 100, 70)
low = df[df["coverage"] < threshold]

if not low.empty:
    st.warning("Files below threshold:")
    st.dataframe(low)

st.success(f"Overall coverage: {df['coverage'].mean():.2f}%")
