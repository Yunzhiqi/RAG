import time
import config
from rag import RagService
from knowledge_service import KnowledgeBaseService
import streamlit as st

# 页面配置
st.set_page_config(
    page_title="智能客服系统",
    page_icon="🤖",
    layout="wide"
)

# 初始化会话状态
if 'message' not in st.session_state:
    st.session_state['message'] = [{'role': 'assistant', 'content': '你好,有什么可以帮助你?'}]
if 'rag' not in st.session_state:
    st.session_state['rag'] = RagService()
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'knowledge_service' not in st.session_state:
    st.session_state['knowledge_service'] = KnowledgeBaseService()

# 侧边栏导航
st.sidebar.title("🤖 智能客服系统")
page = st.sidebar.radio(
    "选择功能",
    ["智能客服", "更新知识库"],
    index=0
)

st.sidebar.divider()
st.sidebar.markdown("### 系统信息")
st.sidebar.info("这是一个基于RAG的智能客服系统，支持文档问答和知识库更新。")

if page == "智能客服":
    # 智能客服页面
    st.title('🤖 智能客服')
    st.divider()
    
    # 显示聊天历史
    for message in st.session_state['message']:
        with st.chat_message(message['role']):
            st.write(message['content'])
    
    # 聊天输入
    prompt = st.chat_input("请输入您的问题...")
    if prompt:
        # 显示用户消息
        with st.chat_message('user'):
            st.write(prompt)
        st.session_state['message'].append({'role': 'user', 'content': prompt})
        
        # 生成AI回复
        with st.chat_message('assistant'):
            with st.spinner('AI思考中...'):
                try:
                    chain = st.session_state['rag'].get_chain()
                    stream_res = chain.stream({'input': prompt}, config.session_config)
                    st.write(stream_res)
                    st.session_state['message'].append({'role': 'assistant', 'content': stream_res})
                except Exception as e:
                    error_msg = f"抱歉，处理问题时出现错误: {str(e)}"
                    st.error(error_msg)
                    st.session_state['message'].append({'role': 'assistant', 'content': error_msg})
        
        # 自动滚动到最新消息
        st.rerun()

elif page == "更新知识库":
    # 更新知识库页面
    st.title('📚 更新知识库')
    st.divider()
    
    # 文件上传器
    file = st.file_uploader(
        label="上传TXT文件",
        type=['txt'],
        accept_multiple_files=False,
        help="请上传txt格式的文件"
    )
    
    if file:
        # 显示文件信息
        name = file.name
        type = file.type
        size = float(int(file.size / 10.24)) / 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("文件名", name)
        with col2:
            st.metric("文件类型", type)
        with col3:
            st.metric("文件大小", f"{size} KB")
        
        st.divider()
        
        # 预览文件内容
        with st.expander("📄 预览文件内容", expanded=False):
            try:
                text = file.getvalue().decode('utf-8')
                # 只显示前1000字符作为预览
                preview_text = text[:1000] + ("..." if len(text) > 1000 else "")
                st.text_area("文件内容", preview_text, height=200, disabled=True)
            except:
                st.warning("无法解码文件内容，请确保是UTF-8编码的文本文件")
        
        # 处理上传
        if st.button("🚀 上传到知识库", type="primary"):
            with st.spinner('正在上传并处理文件...'):
                try:
                    text = file.getvalue().decode('utf-8')
                    ans = st.session_state['knowledge_service'].upload_str(text, name)
                    
                    # 显示结果
                    st.success("✅ 文件上传成功！")
                    st.info(f"处理结果: {ans}")
                    
                    # 更新计数器
                    st.session_state['counter'] += 1
                    st.metric("已上传文件数量", st.session_state['counter'])
                    
                except Exception as e:
                    st.error(f"上传失败: {str(e)}")
    
    # 显示统计信息
    st.divider()
    st.subheader("📊 知识库统计")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("已上传文件数", st.session_state['counter'])
    with col2:
        st.metric("状态", "正常" if st.session_state['counter'] > 0 else "待上传")
    
    # 使用指南
    with st.expander("📖 使用指南", expanded=False):
        st.markdown("""
        1. 点击"选择文件"或拖拽文件到上传区域
        2. 系统会自动显示文件基本信息
        3. 点击"上传到知识库"按钮开始处理
        4. 上传成功后，文件内容将被添加到知识库中
        5. 返回"智能客服"页面即可使用新知识进行问答
        """)

# 页脚
st.sidebar.divider()
st.sidebar.caption(f"© {time.strftime('%Y')} 智能客服系统 v1.0")
