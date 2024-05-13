import streamlit as st
import pandas as pd

def load_data():
    df = pd.read_csv('scraped_data.csv')
    return df

def main():
    st.title("News Article Clustering")

    st.sidebar.title("Options")

    data = load_data()

    unique_clusters = data['Cluster'].unique()
    unique_clusters = ['All'] + sorted(unique_clusters, reverse=True)

    selected_cluster = st.sidebar.selectbox("Select a Cluster", unique_clusters)

    st.sidebar.markdown("---")

    # Filtering by category
    selected_category = st.sidebar.selectbox("Filter by Category", ["All"] + list(data['Category'].unique()))

    if selected_cluster == 'All':
        filtered_data = data
    else:
        filtered_data = data[data['Cluster'] == selected_cluster]

    if selected_category != "All":
        filtered_data = filtered_data[filtered_data['Category'] == selected_category]

    st.subheader(f"Articles in Cluster {selected_cluster}")

    # Summary of the cluster
    st.write(f"Total Articles: {len(filtered_data)}")

    # Display articles
    for idx, row in filtered_data.iterrows():
        st.markdown(f"### {row['Title']}")
        st.markdown(f"**Category:** {row['Category']}")
        st.markdown(f"**Source:** {row['Source']}")
        st.markdown(f"[Read More]({row['Link']})")
        st.markdown("---")

# Running the app
if __name__ == "__main__":
    main()
