from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = sum(len(msg.split()) for msg in df['message'])
    num_media = df[df['message'].str.contains('media omitted', case=False, na=False)].shape[0]
    links = sum(len(extract.find_urls(msg)) for msg in df['message'])

    return num_messages, words, num_media, links


def most_busy_users(df):
    count = df['user'].value_counts()
    percent = round((count / count.sum()) * 100, 2).reset_index()
    percent.columns = ['name', 'percent']
    return count.head(), percent


def create_wordcloud(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[~df['message'].str.contains('media omitted', case=False, na=False)]

    text = " ".join(
        w for msg in temp['message']
        for w in msg.lower().split()
        if w not in stop_words
    )

    return WordCloud(width=600, height=600, background_color='white').generate(text)


def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    words = [
        w for msg in df['message']
        for w in msg.lower().split()
        if w not in stop_words
    ]

    return pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = [
        ch for msg in df['message']
        for ch in msg
        if ch in emoji.EMOJI_DATA
    ]

    return pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])


# ===== FIXED TIMELINES =====

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = (
        df.groupby(['year', 'month_num', 'month'])
        .size()
        .reset_index(name='message')
        .sort_values(['year', 'month_num'])
    )

    timeline['time'] = timeline['month'] + " " + timeline['year'].astype(str)
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return (
        df.groupby('only_date')
        .size()
        .reset_index(name='message')
        .sort_values('only_date')
    )


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    return df['day_name'].value_counts().reindex(order).fillna(0)


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    if df.empty:
        return pd.DataFrame()

    return (
        df.pivot_table(
            index='day_name',
            columns='period',
            values='message',
            aggfunc='count'
        )
        .fillna(0)
    )
