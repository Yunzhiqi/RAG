# <bash> streamlit run upload_file.py
import time
import streamlit as st
from knowledge_service import KnowledgeBaseService
st.title('更新知识库')

file=st.file_uploader(
    label="上传TXT文件",
    type=['txt'],
    accept_multiple_files=False
)

# streamlit每当有元素更新时都会重新运行，靠sessionstate保存信息
if 'counter' not in st.session_state:
    st.session_state['counter']=0
    st.session_state['service']=KnowledgeBaseService()

if file:
    name=file.name
    type=file.type
    size=float(int(file.size/10.24))/100
    
    st.subheader('文件名'+name)
    st.write('格式'+type+'\t|\t大小'+str(size)+'KB')
    
    text=file.getvalue().decode('utf-8')
    
    ans=st.session_state['service'].upload_str(text,name)
    
    with st.spinner('载入知识库中...'):
        # time.sleep(1)
        st.write(ans)
        # st.write(text)
        st.session_state['counter']+=1
    
print('上传了'+str(st.session_state['counter'])+'个文件')
    