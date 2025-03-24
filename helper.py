from urlextract import URLExtract
import emoji
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

def fetch_stats(selected_user, df):
    if(selected_user != "Overall"):
        df = df[df['sender'] == selected_user]

    # 1. Fetch number of messages
    num_messages = df.shape[0]

    # 2. Number of words
    words = []
    for message in df['user_message']:
        words.extend(message.split())

    # 3. Number of media messages
    num_media_messages = df[df['user_message'] == "Image omitted"].shape[0] + df[df['user_message'] == "Video omitted"].shape[0] + df[df['user_message'] == "GIF omitted"].shape[0] + df[df['user_message'] == "Sticker omitted"].shape[0] + df[df['user_message'] == "Contact card omitted"].shape[0] + df[df['user_message'] == "Live location omitted"].shape[0] + df[df['user_message'] == "Location omitted"].shape[0] + df[df['user_message'] == "Document omitted"].shape[0] + df[df['user_message'] == "Audio omitted"].shape[0] + df[df['user_message'] == "Voice omitted"].shape[0] + df[df['user_message'] == "Missed voice call"].shape[0] + df[df['user_message'] == "Missed video call"].shape[0]
    
    # 4. Average words per message
    words_per_message = round(len(words)/num_messages, 2)
    
    # 5. Number of URls shared
    extractor = URLExtract()
    urls = []
    for message in df['user_message']:
        urls.extend(extractor.find_urls(message))
    num_urls = len(urls)

    # 6. Number of emojis shared
    emojis = []
    for message in df['user_message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    num_emojis = len(emojis)

    return num_messages, len(words), num_media_messages, words_per_message, num_urls, num_emojis

def busy_users(df):
    user_stats = df['sender'].value_counts().reset_index()
    user_stats.columns = ['sender', 'messages']
    user_stats = user_stats.sort_values(by='messages', ascending=False)
    return user_stats.head(5)

def busiest_users(df):
    df = round((df["sender"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={"index": "sender", "sender": "percent"})
    return df

def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['sender'] == selected_user]
    
    df = df[~df['user_message'].str.contains('omitted', na=False)]
    df = df[df['user_message'].str.len() > 0]
    
    if df.empty or df['user_message'].str.cat(sep=" ").strip() == "":
        return None
        
    wordcloud = WordCloud(
        width=800,
        height=800,
        min_font_size=10,
        background_color='white'
    )
    df_wc = wordcloud.generate(df['user_message'].str.cat(sep=" "))
    return df_wc