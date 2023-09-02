import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#lesson 2
streamlit.title('My Mon\'s New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



#lesson 3
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado", "Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)



#lesson 9/12
streamlit.header("Fruityvice Fruit Advice!")

#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)

#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json())

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    # normalized json
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice: 
    streamlit.error("Please select a fruit to get informaton.")
  else:
    #"""
    ##fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    ## normalized json
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    ## table output
    #streamlit.dataframe(fruityvice_normalized)
    #"""
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)    
except URLError as e:
  streamlit.error()





#lesson 12
#streamlit.stop()

#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
#my_cnx.close()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains 1:")
streamlit.text(my_data_row)

my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains 2:")
streamlit.dataframe(my_data_row)


# 12 last part
streamlit.header("The fruit load list contains 3:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    #my_cnx.close()
    streamlit.dataframe(my_data_row)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        #my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
        my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('"+new_fruit+"')")
        return 'Thanks for adding ' + new_fruit


add_my_fruit = streamlit.text_input('What fruit would you like to add?')      

if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
    
    


streamlit.stop()
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
#insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('test');
