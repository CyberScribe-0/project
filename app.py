import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)

#     fetch unique users
    user_list = df['user'].unique().tolist()

    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("show analysis wrt ", user_list)

    if st.sidebar.button("Show Analysis"):



        # stats area
        num_messages, words, num_media_messages, num_links= helper.fetch_stats(selected_user,df)
        st.title("Complete Statistics")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links shared")
            st.title(num_links)

        #timeline
        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

#         daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='cyan')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity map")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color = 'yellow')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)




#         finding busiest user group level
        if selected_user == "Overall":
            st.title("Most busy users")
            x , new_df= helper.most_busy_user(df)
            fig,ax = plt.subplots()

            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color ='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
#         wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

#         most common words
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.title("Most common words")
        st.pyplot(fig)

#         emoji analysis

        # emoji_df = helper.emoji_helper(selected_user,df)
        # st.title("Emoji Analysis")
        #
        # col1, col2 = st.columns(2)
        #
        # with col1:
        #     st.dataframe(emoji_df)
        # with col2:
        #     fig, ax = plt.subplots()
        #     ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        #     st.pyplot(fig)

        st.title("Weekly activity map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Sentiment Analysis


        # if selected_user != "Overall":
        #     messages = df[df['user'] == selected_user]['message'].tolist()
        # else:
        #     messages = df['message'].tolist()
        # sentiment_scores = [TextBlob(message).sentiment.polarity for message in messages]
        # average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        # st.header("Sentiment Analysis")
        # st.write("Average Sentiment Score:", round(average_sentiment, 2))

        if selected_user == "Overall":
            messages = df['message']  # Analyze sentiment for all messages
        else:
            messages = df[df['user'] == selected_user]['message']  # Analyze sentiment for selected user's messages

            # Perform sentiment analysis
        sentiment_scores = helper.analyze_sentiment(messages)
        # 0.2
        # Plot time-series sentiment analysis
        st.title('Time-Series Sentiment Analysis')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(sentiment_scores, color='blue', marker='o', linestyle='-')
        ax.set_xlabel('Message Index')
        ax.set_ylabel('Sentiment Polarity Score')
        ax.set_title('Sentiment Analysis Over Time')
        st.pyplot(fig)

