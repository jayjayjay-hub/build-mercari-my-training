import streamlit as st
import pandas as pd
import random
import requests
import json

page = st.sidebar.selectbox('Choose a page', ['Home', 'Post Item', 'Get Items', 'Get Item by ID', 'Search Items', 'Delete Item'])

if page == 'Home':
	st.title("Welcome to the Item Management System")
	st.write("Please select a page from the sidebar")

if page == 'Post Item':
	st.title("Item Management System")
	with st.form(key="Item Form"):
		name = st.text_input("Name",
						  help="Please input the name of the item",
						  max_chars=20)
		category = st.text_input("Category", help="Please input the category of the item", max_chars=20)
		image = st.file_uploader("Image", help="Please upload the image of the item", type=["jpg", "png"])
		data = {
			'name': name,
			'category': category,
			'image': image
		}
		submit_button = st.form_submit_button(label="Add Item")

	if submit_button:
		st.write("Item received: ", data)
		st.write('response:')
		# APIにリクエストを送信
		response = requests.post("http://localhost:8000/items", data=data)
		# レスポンスのステータスコードを表示
		st.write(response.status_code)
		# レスポンスのJSONを表示
		st.json(response.json())
