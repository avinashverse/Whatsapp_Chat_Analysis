from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import re
import pandas as pd
import emoji

def fetch_stats(selected_user , df ) : 

    if(selected_user != 'Overall'):
        new_df = df[df['user'] == selected_user].copy()
    else:
        new_df = df.copy()
    # number of message 
    num_message = len(new_df)

    # number of words
    num_words = 0 
    for message in new_df['message']:
        num_words += len(message.split(" ")) 
    
    # number of media
    num_media = len(new_df[new_df['message'] == 'Media_file'] )

    # number of links 
    
    extractor = URLExtract() 

    num_links = 0
    for message in new_df['message']: 
        num_links += len(extractor.find_urls(message))


    num_deleted = len(new_df[new_df['message'] == 'This message was deleted'] )
    num_deleted += len(new_df[new_df['message'] == 'You deleted this message'] ) 
    
    return num_message , num_words , num_media , num_links , num_deleted 

def most_busy_users(df):
    x = df['user'].value_counts().head()
    temp = round((df['user'].value_counts()/df.shape[0]) * 100 , 2 ).reset_index().rename(columns = {'index':'name','user':'percent'})

    return x , temp


def create_wordcloud(selected_user ,df ) : 
    # temp = df.copy()
    if(selected_user!= "Overall"):
        df = df[df['user'] == selected_user] 
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != 'Media_file']
    temp = temp[temp['message'] != 'This message was deleted']
    temp = temp[temp['message'] != 'You deleted this message']    
    
    stop_words = open("stop_words.txt" ,'r').read()
    pattern = r'^[A-Za-z]+$'
    def remove_stop_words(message):
        y = [] 
        for word in message.lower().split():
            if word not in stop_words and re.match(pattern, word):
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500 , height= 500 , min_font_size=10 , background_color='white') 
    temp["message"] = temp['message'].apply(remove_stop_words)
    df_wc  = wc.generate(temp['message'].str.cat(sep = " ")) 
    return df_wc

def most_used_words(selected_user , df ) : 
    if(selected_user!= "Overall"):
        df = df[df['user'] == selected_user] 
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != 'Media_file']
    temp = temp[temp['message'] != 'This message was deleted']
    temp = temp[temp['message'] != 'You deleted this message']


    stop_words = open("stop_words.txt" ,'r').read()
    words = [] 

    pattern = r'^[A-Za-z]+$'
    for message in temp['message']:
        valid_words = [word for word in message.lower().split(" ") if re.match(pattern, word) and word not in stop_words]
        words.extend(valid_words)

    word_counts = Counter(words)
    most_common_words = pd.DataFrame(word_counts.most_common(min( 20 , len(word_counts))) ) 
    return most_common_words


def most_emojis_used(selected_user , df ) : 
    if(selected_user!= "Overall"):
        df = df[df['user'] == selected_user] 
    
    emojis = [] 
    for message in df['message']:
        emojis.extend( [c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_counts = Counter(emojis) 
    most_common_emojis = pd.DataFrame(emoji_counts.most_common(min( 20   , len(emoji_counts))) ) 
    return most_common_emojis


def monthly_timeline(selected_user ,df ) : 
    if(selected_user!= "Overall"):
        df = df[df['user'] == selected_user] 
    
    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year' , 'month_num' , 'month']).count()['message'].reset_index()
    time = []
    for i in range(len(timeline)):
        time.append(timeline['month'][i] + " " + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user , df ) : 
    if(selected_user!= "Overall"):
        df = df[df['user'] == selected_user] 
    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year' , 'month_num' , 'month' , 'day']).count()['message'].reset_index()
    time = []
    for i in range(len(timeline)):
        time.append(timeline['month'][i] + " " + str(timeline['year'][i]))
    timeline['time'] = time
    date = [] 
    for i in range(len(timeline)):
        date.append(str(timeline['day'][i])+" "+str(timeline['month'][i]) +" " + str(timeline['year'][i]))
    timeline['date'] = date

    return timeline

def weekly_activity(selected_user , df ) : 
    if(selected_user!= "Overall"):
        df = df[df['user'] == selected_user] 
    df['day_name'] = df['date'].dt.day_name() 
    return df['day_name'].value_counts() 

def monthly_activity(selected_user , df ) : 
    if(selected_user!= "Overall"):
        df = df[df['user'] == selected_user] 
    return df['month'].value_counts()


def activity_heatmap(selected_user , df ) : 
    if(selected_user!= "Overall"):
        df = df[df['user'] == selected_user] 

    period = [] 
    df['day_name'] = df['date'].dt.day_name() 
    start = []
    for hour in df[['day_name' , 'hour'] ]['hour']:
        if(hour == 23 ) : 
            period.append(str(hour) +"-" + str("0"))
            start.append(hour)
        elif hour == 0 : 
            period.append(str("0") + "-" + str(hour + 1 )) 
            start.append(0)
        else: 
            period.append(str(hour) + "-" + str(hour + 1 ))
            start.append(hour)
    df['period'] = period
    df['start'] = start
    return df 

def average_num_of_words(selected_user , df ) : 
    if(selected_user!= "Overall"):
        df = df[df['user'] == selected_user] 
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != 'Media_file']
    temp = temp[temp['message'] != 'This message was deleted']
    temp = temp[temp['message'] != 'You deleted this message']

    num_words = 0 
    for i in temp['message']:
        num_words += len(i.split(" ")) 
    
    return num_words//len(temp)