import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from mongoengine import connect
from mongoengine.errors import DoesNotExist
from django_app.models import Product, ProductCategory

load_dotenv()
connect(
    db="inventory_db",
    username=os.getenv("MONGO_USER", "root"),
    password=os.getenv("MONGO_PASS", "example"),
    host=os.getenv("MONGO_HOST", "localhost"),
    port=int(os.getenv("MONGO_PORT", "27019")),
    authentication_source="admin"
)

st.set_page_config(page_title="Inventory Dashboard", layout="wide")
st.title("Inventory Management Dashboard")

@st.cache_data(ttl=5) 
def fetch_inventory():
    products = Product.objects.all()
    data = []
    for p in products:
        try:
            cat_title = p.category.title if p.category else "Uncategorized"
        except DoesNotExist:
            cat_title = "Broken Reference"

        data.append({
            "ID": str(p.id),
            "Name": p.name,
            "Brand": p.brand,
            "Category": cat_title,
            "Price ($)": p.price,
            "Quantity": p.quantity
        })
    return pd.DataFrame(data)

def fetch_categories():
    return [cat.title for cat in ProductCategory.objects.all()]

df = fetch_inventory()
categories = fetch_categories()

st.sidebar.header("Filter Inventory")
selected_category = st.sidebar.selectbox("Filter by Category", ["All"] + categories)

if selected_category != "All":
    df = df[df["Category"] == selected_category]

st.subheader("Current Stock Levels")
LOW_STOCK_THRESHOLD = 10

if not df.empty:
    low_stock_items = df[df["Quantity"] < LOW_STOCK_THRESHOLD]
    if not low_stock_items.empty:
        st.error(f"Alert: {len(low_stock_items)} item(s) are running critically low on stock!")
        st.dataframe(low_stock_items.style.highlight_max(subset=['Quantity'], color='red'))
    
    st.dataframe(df, width='stretch')
else:
    st.info("No products found in the database.")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Add New Product")
    with st.form("add_product_form"):
        new_name = st.text_input("Name")
        new_brand = st.text_input("Brand")
        new_cat_title = st.selectbox("Category", categories) if categories else None
        new_price = st.number_input("Price", min_value=0.01, format="%.2f")
        new_qty = st.number_input("Quantity", min_value=0, step=1)
        
        if st.form_submit_button("Add Product"):
            if new_name and new_brand and new_cat_title:
                cat_obj = ProductCategory.objects(title=new_cat_title).first()
                new_p = Product(name=new_name, brand=new_brand, category=cat_obj, price=new_price, quantity=new_qty)
                new_p.save()
                st.success(f"Added {new_name} successfully!")
                st.rerun()
            else:
                st.warning("Please fill out all required fields.")

with col2:
    st.subheader("Remove Product")
    with st.form("remove_product_form"):
        if not df.empty:
            prod_to_remove = st.selectbox("Select Product to Delete", df["Name"].tolist())
            if st.form_submit_button("Delete Product"):
                prod_obj = Product.objects(name=prod_to_remove).first()
                if prod_obj:
                    prod_obj.delete()
                    st.success(f"Deleted {prod_to_remove}.")
                    st.rerun()
        else:
            st.write("No products to remove.")