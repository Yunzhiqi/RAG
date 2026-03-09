# <bash> streamlit run upload_file.py

import streamlit as st

st.title('更新知识库')

file=st.file_uploader(
    label="上传TXT文件",
    type=['txt'],
    accept_multiple_files=False
)

if file:
    name=file.name
    type=file.type
    size=float(int(file.size/10.24))/100
    
    st.subheader('文件名'+name)
    st.write('格式'+type+'|大小'+str(size)+'KB')
    
    text=file.getvalue().decode('utf-8')
    st.write(text)
    
    