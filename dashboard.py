import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns

st.title("Customer Behavior Segmentation Dashboard")
# Load the dataset
@st.cache_data
def load_data():
    # Load your dataset here
    data = pd.read_csv("data/merged_segment_data.csv")
    return data

data = load_data()


# Sidebar Filters
st.sidebar.header("Filter Options")
websitebehavior_segments = st.sidebar.multiselect("Select Segments to Filter", options=data["WebsiteBehaviorSegment"].unique(), default=data["WebsiteBehaviorSegment"].unique())
purchase_segments = st.sidebar.multiselect("Select Purchase Segments", options=data["PurchasingSegment"].unique(), default=data["PurchasingSegment"].unique())

filtered_data = data[(data["WebsiteBehaviorSegment"].isin(websitebehavior_segments)) & (data["PurchasingSegment"].isin(purchase_segments))]



# Tailored Visualizations

# 1. Bubble Chart: Purchase Amount vs Website Visits vs Time on Site
st.subheader("Purchase Behavior vs Website Engagement")
bubble_chart = px.scatter(
    filtered_data, 
    x="WebsiteVisits", 
    y="PurchaseAmount", 
    size="TimeOnSite", 
    color="WebsiteBehaviorSegment",
    hover_name="CustomerID",
    title="Bubble Chart: Purchase Amount vs Website Visits",
    labels={"WebsiteVisits": "Website Visits", "PurchaseAmount": "Purchase Amount"}
)
st.plotly_chart(bubble_chart)

# 2. Scatter Plot: Time on Site vs Purchases
st.subheader("Engagement Duration and Conversion")
scatter_plot = px.scatter(
    filtered_data,
    x="TimeOnSite",
    y="PurchaseAmount",
    color="PurchasingSegment",
    size="WebsiteVisits",
    hover_name="CustomerID",
    title="Scatter Plot: Time on Site vs Purchases",
    labels={"TimeOnSite": "Time on Site", "PurchaseAmount": "Purchase Amount"}
)
st.plotly_chart(scatter_plot)

# 3. Pie Chart: Segment Composition
st.subheader("Website Segment Distribution")
pie_chart = px.pie(
    filtered_data, 
    names="WebsiteBehaviorSegment", 
    values="CustomerID",
    title="Website Segment Distribution",
    labels={"WebsiteBehaviorSegment": "Segment"}
)
st.plotly_chart(pie_chart)

#time on site distribution
st.subheader("Distribution of Time on Site")
hist_chart = px.histogram(
    filtered_data,
    x="TimeOnSite",
    color="WebsiteBehaviorSegment",
    nbins=20,
    title="Histogram: Time on Site Distribution",
    labels={"TimeOnSite": "Time on Site (minutes)"}
)
st.plotly_chart(hist_chart)

#correlation heatmap
st.subheader("Feature Correlation Heatmap")
correlation_data = filtered_data[["WebsiteVisits", "TimeOnSite", "PurchaseAmount"]]
corr_matrix = correlation_data.corr()

fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

#bar chart; purchase amount by segments
st.subheader("Purchase Amount by Segment")
bar_chart = px.bar(
    filtered_data,
    x="PurchasingSegment",
    y="PurchaseAmount",
    color="WebsiteBehaviorSegment",
    title="Purchase Amount by Segment",
    labels={"PurchasingSegment": "Purchase Segment", "PurchaseAmount": "Purchase Amount"}
)
st.plotly_chart(bar_chart)

#sunburst chart ; combined segmentation
st.subheader("Combined Segmentation: Website + Purchase")
sunburst_chart = px.sunburst(
    filtered_data,
    path=["WebsiteBehaviorSegment", "PurchasingSegment"],
    values="CustomerID",
    title="Combined Segmentation",
    labels={"CustomerID": "Number of Customers"}
)
st.plotly_chart(sunburst_chart)

#stacked_bar; segment contribution to revenue
st.subheader("Segment Contribution to Revenue")
stacked_bar = px.bar(
    filtered_data,
    x="WebsiteBehaviorSegment",
    y="PurchaseAmount",
    color="PurchasingSegment",
    title="Segment Contribution to Revenue",
    labels={"WebsiteBehaviorSegment": "Website Segment", "PurchaseAmount": "Total Revenue"}
)
st.plotly_chart(stacked_bar)

#box_plot; purchase amount by segment
st.subheader("Purchase Amount Distribution by Segment")
box_chart = px.box(
    filtered_data,
    x="PurchasingSegment",
    y="PurchaseAmount",
    color="WebsiteBehaviorSegment",
    title="Box Plot: Purchase Amount by Segment",
    labels={"PurchasingSegment": "Segment", "PurchaseAmount": "Purchase Amount"}
)
st.plotly_chart(box_chart)








# Insights Table
st.subheader("Domain-Specific Insights")
insights = [
    {"Pattern": "High Website Visits & High Purchase Amount", "Insight": "These are loyal customers; offer loyalty rewards."},
    {"Pattern": "High Website Visits & Low Purchase Amount", "Insight": "Optimize product descriptions; consider retargeting ads."},
    {"Pattern": "Low Website Visits & High Purchase Amount", "Insight": "Efficient shoppers; introduce a streamlined 'Quick Buy' feature."},
    {"Pattern": "Low Website Visits & Low Purchase Amount", "Insight": "Increase awareness through social media campaigns."},
]
insights_df = pd.DataFrame(insights)
st.table(insights_df)



# Save Filtered Data
if st.sidebar.button("Download Filtered Data"):
    filtered_data.to_csv("filtered_customer_data.csv", index=False)
    st.success("Filtered data saved successfully!")

