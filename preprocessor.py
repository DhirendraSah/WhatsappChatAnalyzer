import re
import pandas as pd


def preprocess(data):

    # Supports:
    # 12/10/23, 10:15 -
    # 12/10/2023, 10:15 AM -
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'date': dates})

    # Robust datetime parsing
    df['date'] = (
        df['date']
        .str.replace(' - ', '', regex=False)
        .pipe(pd.to_datetime, dayfirst=True, errors='coerce')
    )

    users, msgs = [], []

    for message in df['user_message']:
        entry = re.split(r'^([^:]+):\s', message)
        if len(entry) > 2:
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs
    df.drop(columns=['user_message'], inplace=True)

    # Time features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour

    df['period'] = df['hour'].apply(
        lambda h: "23-00" if h == 23 else "00-01" if h == 0 else f"{h}-{h+1}"
    )

    return df
