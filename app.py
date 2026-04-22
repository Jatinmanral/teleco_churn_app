import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Churn Simulator", layout="wide")

# --- Header ---
st.markdown("""
# 📊 Churn Strategy Simulator  
### Optimize retention spend & maximize ROI
""")

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("results1.csv")

results = load_data()

# --- Sort customers ---
results = results.sort_values(by='Priority_Score', ascending=False)

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Strategy Controls")

discount = st.sidebar.slider("💸 Discount per Customer (₹)", 0, 500, 50)
retention_rate = st.sidebar.slider("🔁 Retention Rate", 0.0, 1.0, 0.6)
target_pct = st.sidebar.slider("🎯 Target % of Customers", 0.01, 0.5, 0.1)

# --- Select customers ---
top_n = int(target_pct * len(results))
target = results.head(top_n)

# --- Calculations ---
total_cost = discount * len(target)
revenue_saved = (target['Customer_Value'] * retention_rate).sum()
profit = revenue_saved - total_cost
roi = profit / total_cost if total_cost != 0 else 0

# --- Metrics ---
st.subheader("📈 Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("👥 Customers", len(target))
col2.metric("💸 Cost", f"₹{total_cost:,.0f}")
col3.metric("💰 Revenue Saved", f"₹{revenue_saved:,.0f}")

col4, col5 = st.columns(2)
col4.metric("📈 Profit", f"₹{profit:,.0f}")
col5.metric("📊 ROI", f"{roi:.2f}")

# --- Profit Indicator ---
if profit > 0:
    st.success("✅ Profitable Strategy")
else:
    st.error("❌ Loss-making Strategy")

# --- Profit vs Target Chart ---
st.subheader("📊 Profit vs Target Size")

percentages = [5, 10, 15, 20, 25, 30]
profits = []

for pct in percentages:
    n = int(len(results) * pct / 100)
    temp = results.head(n)

    cost = discount * len(temp)
    revenue = (temp['Customer_Value'] * retention_rate).sum()
    profits.append(revenue - cost)

fig, ax = plt.subplots()
ax.plot(percentages, profits)
ax.set_xlabel("Target %")
ax.set_ylabel("Profit")
ax.set_title("Profit vs Target Size")

st.pyplot(fig)

