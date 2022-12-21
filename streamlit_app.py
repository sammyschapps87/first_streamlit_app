import streamlit as sl
import pandas as pd
import requests
import snowflake.connector

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

sl.title('My Parents New Healthy Diner')
sl.header('Breakfast Favorites')
sl.text('🥣Omega 3 & Blueberry Oatmeal')
sl.text('🥗Kale, Spinach & Rocket Smoothie')
sl.text('🐔Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
sl.dataframe(fruits_to_show)




sl.header('Fruityvice Fruit Advice!')
fruit_choice = sl.text_input('What fruit would you like information about?','Kiwi')
sl.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

# normalize json file
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# show data 
sl.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
sl.header("The fruit load list contains:")
sl.dataframe(my_data_rows)

add_my_fruit = sl.text_input('What fruit would you like to add?','Jackfruit') 
sl.write('The user entered ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")