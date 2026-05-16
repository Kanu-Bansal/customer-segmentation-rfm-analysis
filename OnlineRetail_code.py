import pandas as pd
import datetime as dt

# Data Load
df = pd.read_csv(r"F:\Data Analysis Projects\OnlineRetail.csv", encoding='ISO-8859-1')
# print(df.isnull().sum())


# InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country

# Date Format Convert
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Handle Missing and Duplicates
df = df.dropna(subset=["CustomerID"])
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

# Total Amount Column Create
df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

# Recency Calculate
# Latest Date
current_date = df["InvoiceDate"].max()

# Group by Customer
rfm = df.groupby("CustomerID").agg({
    "InvoiceDate" : lambda x: (current_date - x.max()).days,
    "InvoiceNo" : "nunique",
    "TotalAmount":"sum"})

rfm.columns = ["Recency","Frequency","Monetary"]

# RFM Score (Ranking)
rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method="first"),4,labels=[4,3,2,1])
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"),4,labels=[1,2,3,4])
rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"),4,labels=[1,2,3,4])

rfm["RFM_Score"] = rfm["R_Score"].astype(str)+\
rfm["F_Score"].astype(str) + \
rfm["M_Score"].astype(str)

# Customer Segmentation
def segment(row):
    if row["RFM_Score"] == '444':
        return "High Score"
    elif row["R_Score"] == 4:
        return "Loyal Customer"
    else:
        return "At Risk"
    
rfm["Segment"] = rfm.apply(segment,axis=1)
rfm = rfm.reset_index()
rfm.to_csv("rfm_output.csv",index=False)