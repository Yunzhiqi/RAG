import time

import config
from rag import RagService
import streamlit as st

st.title('智能客服')
st.divider()

if 'message' not in st.session_state:
    st.session_state['message']=[{'role':'assistant','content':'你好,有什么可以帮助你?'}]
if 'rag' not in st.session_state:
    st.session_state['rag']=RagService()

for message in st.session_state['message']:
    st.chat_message(message['role']).write(message['content'])

prompt=st.chat_input()
if prompt:
    st.chat_message('user').write(prompt)
    st.session_state['message'].append({'role':'user','content':prompt})
    with st.spinner('AI思考中'):
        # time.sleep(1)
        # ans='test1'
        
        chain=st.session_state['rag'].get_chain()
        stream_res=chain.stream({'input':prompt},config.session_config)
        st.chat_message('assistant').write(stream_res)
        
        st.session_state['message'].append({'role':'assistant','content':stream_res})