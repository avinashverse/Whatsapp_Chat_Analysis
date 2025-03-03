import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
import helper
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file") 
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue() 
    
    data = bytes_data.decode("utf-8" ) 
    
    df = preprocessor.preprocess(data) 

    st.dataframe(df)

    # find unique users
    user_list = df['user'].unique().tolist() 
    user_list.remove('group_notification') 
    user_list.sort() 
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt" , user_list)

    if(st.sidebar.button("Show Analysis")):
        st.title("Statistics")
        col1 , col2 , col3 , col4 , col5= st.columns(5)
        num_message , num_words , num_media , num_links , num_deleted = helper.fetch_stats(selected_user , df )

        with col1:
            st.markdown("<h3>Total Messages</h3>", unsafe_allow_html=True)
            st.title(num_message)

        with col2:
            st.markdown("<h3>Total Words</h3>", unsafe_allow_html=True)
            st.title(num_words)
        
        with col3: 
            st.markdown("<h3>Total Media</h3>", unsafe_allow_html=True)
            st.title(num_media)
        
        with col4:
            st.markdown("<h3>Total Links</h3>", unsafe_allow_html=True)
            st.title(num_links) 

        with col5: 
            st.markdown("<h3>Total Deleted</h3>", unsafe_allow_html=True)
            st.title(num_deleted)
    


        if selected_user == "Overall":
            st.title("Most Busy Users")
            x , temp = helper.most_busy_users(df) 
            fig,ax = plt.subplots()
            
            col1 , col2 = st.columns(2) 

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation = 90)
                st.pyplot(fig)

            with col2:
                st.dataframe(temp)


        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user , df ) 

        fig,ax = plt.subplots()
        ax.imshow(df_wc) 
        st.pyplot(fig)


        st.title("Most common words")
        
        st.markdown(f"<h4>Average number of words per message -  {helper.average_num_of_words(selected_user ,df ) } </h4>", unsafe_allow_html=True)
        most_common_word = helper.most_used_words(selected_user , df )
        
        bar_width = 0.8
        bar_distance = 0.25

        fig, ax = plt.subplots()

        ax.barh(most_common_word[0], most_common_word[1], height=bar_width, align='center', color='skyblue')

        ax.set_yticklabels(most_common_word[0])

        st.pyplot(fig)

        st.title("Most common emojis" )

        most_emojis_used = helper.most_emojis_used(selected_user , df ) 
        st.dataframe(most_emojis_used)
        

        st.title("Analysis over time")
        col1 , col2 = st.columns(2 )

        with col1:
            #monthly timeline 
            st.markdown("<h3>Monthly Analysis</h3>", unsafe_allow_html=True)
            monthly_timeline = helper.monthly_timeline(selected_user , df ) 
            
            fig,ax = plt.subplots() 
            ax.bar(monthly_timeline['time'] , monthly_timeline['message'])
            plt.xticks(rotation = 90)
            st.pyplot(fig)
        with col2:
            # daily timeline
            st.markdown("<h3>Daily Analysis</h3>", unsafe_allow_html=True)
            daily_timeline = helper.daily_timeline(selected_user , df ) 
            fig , ax = plt.subplots() 
            ax.plot(daily_timeline['date'], daily_timeline['message'])

            x_ticks_indices = range(0, len(daily_timeline['date']), 30)
            x_ticks_labels = daily_timeline['date'][::30]  

            x_ticks_indices = list(x_ticks_indices) + [len(daily_timeline['date']) - 1]
            x_ticks_labels = list(x_ticks_labels) + [daily_timeline['date'].iloc[-1]]

            plt.xticks(x_ticks_indices, x_ticks_labels, rotation=45)  

            plt.xlabel('Date')
            plt.ylabel('Message')
            plt.title('Messages Over Time') 
            st.pyplot(fig)
        

        # weekly and monthly 
        st.title("Activity Map " ) 
        col1 , col2 = st.columns(2) 
        with col1 : 
            st.markdown("<h3>Most busy day</h3>", unsafe_allow_html=True)
            busy_day = helper.weekly_activity(selected_user , df ) 
            fig , ax = plt.subplots() 
            ax.bar(busy_day.index , busy_day.values) 
            plt.xticks(rotation = 90 )
            st.pyplot(fig)
        
        with col2 : 
            st.markdown("<h3>Most busy month</h3>", unsafe_allow_html=True)
            busy_month = helper.monthly_activity(selected_user , df ) 
            fig , ax = plt.subplots() 
            ax.bar(busy_month.index , busy_month.values) 
            plt.xticks(rotation = 90 )
            st.pyplot(fig)
        
        # activity heat map 
        st.title("Weekly Activity Heatmap")
        
        user_heatmap = helper.activity_heatmap(selected_user , df ) 

        user_heatmap = user_heatmap.sort_values(by = 'start')
        fig , ax = plt.subplots( figsize = (20, 10 ))  
        ax = sns.heatmap(user_heatmap.pivot_table(index='day_name' , columns='period' , values = 'message' , aggfunc = 'count').fillna(0))
        plt.yticks(rotation = 0)
        st.pyplot(fig)
