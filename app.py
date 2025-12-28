import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config("WhatsApp Chat Analyzer", layout="wide")
st.title("📊 WhatsApp Chat Analyzer")

st.sidebar.header("Upload Chat File")
uploaded_file = st.sidebar.file_uploader("Choose WhatsApp .txt file")

if uploaded_file:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = sorted(df['user'].unique().tolist())
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select User", user_list)

    if st.sidebar.button("Analyze 🚀"):

        # ===== Stats =====
        st.subheader("📌 Key Statistics")
        c1, c2, c3, c4 = st.columns(4)
        stats = helper.fetch_stats(selected_user, df)

        c1.metric("Messages", stats[0])
        c2.metric("Words", stats[1])
        c3.metric("Media", stats[2])
        c4.metric("Links", stats[3])

        # ===== Monthly Timeline =====
        st.subheader("📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], marker='o')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # ===== Daily Timeline =====
        st.subheader("🗓️ Daily Timeline")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily['only_date'], daily['message'])
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # ===== Activity Map =====
        st.subheader("🔥 Activity Map")
        c1, c2 = st.columns(2)

        with c1:
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with c2:
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # ===== Heatmap =====
        st.subheader("🧊 Weekly Heatmap")
        heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(heatmap, cmap="YlGnBu", ax=ax)
        st.pyplot(fig)

        # ===== Busy Users =====
        if selected_user == "Overall":
            st.subheader("👥 Most Active Users")
            x, user_df = helper.most_busy_users(df)
            st.bar_chart(x)
            st.dataframe(user_df)

        # ===== WordCloud =====
        st.subheader("☁️ Word Cloud")
        wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        # ===== Common Words =====
        st.subheader("📝 Common Words")
        common = helper.most_common_words(selected_user, df)
        st.bar_chart(common.set_index('word'))

        # ===== Emoji Analysis =====
        st.subheader("😄 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        st.dataframe(emoji_df.head(10))
