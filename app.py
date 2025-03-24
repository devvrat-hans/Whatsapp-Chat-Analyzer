import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    st.title("File uploaded successfully")
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # Selecting the user

    user_list = df['sender'].unique().tolist()
    user_list.remove("Group Notifications")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select a user", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, words_per_message, num_urls, num_emojis = helper.fetch_stats(selected_user, df)

        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        with col1:
            st.header("Total Messages")
            st.title(num_messages) 
        with col2:
            st.header("Total Words")
            st.title(words) 
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages) 
        with col4:
            st.header("Average Words per Message")
            st.title(words_per_message)
        with col5:
            st.header("Total URLs Shared")
            st.title(num_urls)
        with col6:
            st.header("Total Emojis Shared")
            st.title(num_emojis)

        # Finding the Busiest users in the group
        if selected_user == "Overall":
            st.subheader("Busiest Users")
            busy_df = helper.busy_users(df)
            st.write(busy_df)

        if selected_user == "Overall":
            st.title("Most Busy Users")

            busy_df = helper.busy_users(df)  
            new_df = helper.busiest_users(df)

            st.subheader("Messages Distribution")
            
            plt.figure(figsize=(10, 6))
            
            sns.histplot(data=df, 
                        x='sender', 
                        hue='sender',
                        multiple='stack', 
                        palette='viridis')
            
            plt.xticks(rotation=45, ha='right')
            plt.title('Messages Distribution')
            plt.xlabel('User')
            plt.ylabel('Number of Messages')
            
            plt.tight_layout() 
            
            st.pyplot(plt)


            st.subheader("Busiest Users")
            st.dataframe(new_df)

        # Word Cloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)

        plt.figure(figsize=(8,8))
        plt.imshow(df_wc, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        


                
            