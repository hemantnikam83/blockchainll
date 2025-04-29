import streamlit as st
import pandas as pd
import hashlib

st.set_page_config(page_title="Store Sales Ledger", layout="wide")

st.title("🧾 Store Sales Ledger with Hashing")

# Ledger data
data = {
    "Date": ["2025-04-25", "2025-04-25", "2025-04-26", "2025-04-26", "2025-04-27", "2025-04-27"],
    "Item": ["T-shirt", "Mug", "Notebook", "Water Bottle", "Cap", "Hoodie"],
    "Quantity": [2, 1, 3, 2, 1, 1],
    "Unit Price": [15.00, 8.00, 5.00, 12.50, 10.00, 35.00],
    "Payment Method": ["Credit Card", "Cash", "Debit Card", "Mobile Payment", "Cash", "Credit Card"]
}

# Calculate total sale
data["Total Sale"] = [q * p for q, p in zip(data["Quantity"], data["Unit Price"])]

# Create DataFrame
ledger_df = pd.DataFrame(data)

# Hashing function
def hash_block(data_str, prev_hash):
    to_hash = data_str + prev_hash
    return hashlib.sha256(to_hash.encode()).hexdigest()

# Add hash columns
ledger_df["Prev Hash"] = ""
ledger_df["Hash"] = ""

# Genesis block
prev_hash = "0"

# Compute hashes
for i in ledger_df.index:
    block_data = f"{ledger_df.at[i, 'Date']}{ledger_df.at[i, 'Item']}{ledger_df.at[i, 'Quantity']}{ledger_df.at[i, 'Unit Price']}{ledger_df.at[i, 'Total Sale']}{ledger_df.at[i, 'Payment Method']}"
    block_hash = hash_block(block_data, prev_hash)
    ledger_df.at[i, "Prev Hash"] = prev_hash
    ledger_df.at[i, "Hash"] = block_hash
    prev_hash = block_hash

# Display
st.subheader("📋 Hashed Sales Ledger")
st.dataframe(ledger_df, use_container_width=True)

# Optional: download CSV
csv = ledger_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Ledger as CSV",
    data=csv,
    file_name="hashed_sales_ledger.csv",
    mime='text/csv',
)
