# =================================== IMPORT MODULE YANG DIGUNAKAN =============================== #

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from   streamlit_option_menu import option_menu 
import plotly.express as px
import plotly.figure_factory as ff
import base64
import pickle

# ====================================== IMPORT DATASET VISUALISASI ====================================== #

df = pd.read_csv('Jurusan_Klasifikasi_SMA_SMK.csv')
def data():
	col1, col2,col3 = st.columns(3)
	with col2:
		st.write("* Data Ini Bersumber dari referensi Artikel")
		st.dataframe(df)
# ====================================== MEMBUAT TAMEPILAM ====================================== #

st.set_page_config(
    page_title="knn_peralaman_jurusan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Encoding untuk gambar background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('bg_knn_fix.jpg') 

# Encoding untuk gambar side bar
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("side.jpg")
page_bg_img = f"""
<style>

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.write("""
            # APLIKASI PENERAPAN ALGORITMA KNN DALAM PENENTUAN JURUSAN DI SEKOLAH TINGGI ILMU KOMPUTER 🎓
""")
# ====================================== FUNGSI PERAMALAN ====================================== #
def math ():
    loaded_model = pickle.load(open("Peramalan_Jurusan.sav", "rb"))
    # Mencetak Akurasi
    akurasi = 75


    col1, col2,col3= st.columns(3)
    with col1:
        MTK = st.number_input("Nilai Matematika", min_value=0, max_value=100)
        FIS = st.number_input("Masukan Nilai Fisika", min_value=0, max_value=100)
    with col3:
        BIO = st.number_input("Masukan Nilai Biologi", min_value=0, max_value=100)
        KIM = st.number_input("Masukan Nilai Kimia", min_value=0, max_value=100)

        

    user = ([[MTK,FIS,KIM,BIO]])

    knn_pred = loaded_model.predict(user)

    def tengah() :
        if st.button("Submit"):
                if knn_pred == ([0]):
                    st.success("Jurusan Yang Tepat Untuk Anda adalah Teknik Informatika")
                    st.write("Akurasi yang didapat : ", akurasi, "%")
                elif knn_pred == ([1]):
                    st.success("Jurusan Yang Tepat Untuk Anda adalah Sistem Informasi")
                    st.write("Akurasi yang didapat : ", akurasi, "%")
                else :
                    st.success("Jurusan Yang Tepat Untuk Anda adalah Ilmu Komputer ")
                    st.write("Akurasi yang didapat : ", akurasi, "%")
    tengah()

# ====================================== FUNGSI VISUALISASI DATASET ====================================== #
def jumlah_prodi ():
	st.write("# JUMLAH PRODI")
	fig = px.histogram(df, x="PRODI", color = 'PRODI', width=800, height=400)
	st.plotly_chart(fig,use_container_width = True)

def perseberan ():
	st.write("# PERSEBARAN PRODI BERDASARKAN NILAI ")
	col1, col2 = st.columns(2)
	fig = px.scatter(df, x='KIM',y='BIO',color='PRODI')
	col1.plotly_chart(fig,use_container_width = True)
	
	fig = px.scatter(df, x='MTK',y='FIS',color='PRODI')
	col2.plotly_chart(fig,use_container_width = True)

	fig = px.scatter(df, x='KIM',y='MTK',color='PRODI')
	col1.plotly_chart(fig,use_container_width = True)

	fig = px.scatter(df, x='MTK',y='BIO',color='PRODI')
	col2.plotly_chart(fig,use_container_width = True)

	# st.plotly_chart(fig,use_container_width = True)
# ====================================== MENU APLIKASI ====================================== #

pilihan = option_menu(
         menu_title=None,  # required
         options=["Home", "Klasifikasi", "Referensi"],  # required
         icons=["house", "book", "envelope"],  # optional
         menu_icon="cast",  # optional
         default_index=0,  # optional
         orientation="horizontal",
         styles={
             "container": {"padding": "0!important", "background-color": "#fafafa"},
             "icon": {"color": "orange", "font-size": "25px"},
             "nav-link": {
                 "font-size": "25px",
                 "text-align": "left",
                 "margin": "0px",
                 "--hover-color": "#eee",
             },
             "nav-link-selected": {"background-color": "orange"},
         },
     )
#==========================> MEMBUAT FUNGSI LOG IN DAN SIGN UP USER <=============================== #

# Membuat Enkripsi
# digunakan untuk keamanan data admin

import hashlib                                      # Module untuk melakukan penyandian atau enkripsi

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# ============================================ MEMBUAT DATABASE ======================================= #

import sqlite3 
conn = sqlite3.connect('data_admin.db')
c = conn.cursor()

# Membuat Fungsi sebagai tabel data admin
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

# Membuat Fungsi sebagai inputan data user
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

# Membuat Fungsi sebagai login user
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

# Fungsi menampilkan semua data admin/user
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

# ============================================ SETTING TAMPILAN TIAP MENU ======================================= #

if pilihan == "Home":
    st.image('bg_home.jpg')
elif pilihan == "Klasifikasi":
   
	menu = ["Login","SignUp"]
	gambar = st.sidebar.image("atas.png", use_column_width=True)
	choice = st.sidebar.selectbox(" ",menu)


	if choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))

			if result:

				# main.refresh()
				st.success("Logged In as {}".format(username))
				st.sidebar.image("maba.png", use_column_width=True)

				task = st.selectbox("Pilih Informasi",["Visualisasi Data","Analytics","Profiles"])
				if task == "Visualisasi Data":
					jumlah_prodi()
					perseberan()
				elif task == "Analytics":
					st.write("Klasifikasikan Nilai Anda")
					math()
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")

	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")

elif pilihan == "Referensi":
	data()
