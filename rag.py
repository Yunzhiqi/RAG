from operator import itemgetter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough,RunnableWithMessageHistory,RunnableLambda
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from search_service import SearchService
from knowledge_service import KnowledgeBaseService
import history
import config

def print_prompt(prompt):
    print('='*20)
    print(prompt.to_string())
    print('='*20)
    return prompt

class RagService(object):
    def __init__(self):
        self.search_service=SearchService(DashScopeEmbeddings(model=config.embbeding_fun_name))
        self.prompt_template=ChatPromptTemplate.from_messages(
            [
                ('system','如有参考资料,以提供的参考资料为主,简洁专业地回答用户的问题。参考资料:{context}/n'),
                ('system','并且提供用户的历史对话记录如下:'),
                MessagesPlaceholder('history'),
                ('user','请回答用户提问:{input}')
            ]
        )
        self.chat_model=ChatOpenAI(model=config.chat_model_name,base_url='https://api.deepseek.com/v1')
    def get_chain(self):
        retriever=self.search_service.get_retriever()
        
        def change_doc_format(docs:list[Document]):
            if not docs:
                return '无相关参考资料'
            ans=''
            for doc in docs:
                ans+='文档片段:'+doc.page_content+'\n'+'文档元数据:'+str(doc.metadata)+'\n\n'
            return ans
        
        # def temp1(value:dict):
        #     return value['input']
        
        # def temp2(value):
        #     new_value={
        #         'input':value['input']['input'],
        #         'context':value['context'],
        #         'history':value['input']['history']
        #     }
        #     return new_value
        
        # chain=(
        #     {
        #         'input':RunnablePassthrough(),
        #         'context': temp1 |retriever | change_doc_format
        #     } | RunnableLambda(temp2) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        # )
        
        chain = (
        {
            'input': itemgetter('input'),  # 提取用户输入
            'context': itemgetter('input') | retriever | change_doc_format,
            'history': itemgetter('history')  # 提取历史记录
        } 
        | self.prompt_template
        | print_prompt
        | self.chat_model
        | StrOutputParser()
    )
        
        his_chain=RunnableWithMessageHistory(
            chain,history.get_history,input_messages_key='input',history_messages_key='history'
        )
        
        return his_chain
    def new_get_chain(self):
        retriever=self.search_service.get_retriever()
        
        def change_doc_format(docs:list[Document]):
            if not docs:
                return '无相关参考资料'
            ans=''
            for doc in docs:
                ans+='文档片段:'+doc.page_content+'\n'+'文档元数据:'+str(doc.metadata)+'\n\n'
            return ans
        
        def temp1(value:dict):
            return value['input']
        
        def temp2(value):
            new_value={
                'input':value['input']['input'],
                'context':value['context'],
                'history':value['input']['history']
            }
            return new_value
        
        chain=(
            {
                'input':RunnablePassthrough(),
                'context': temp1 |retriever | change_doc_format
            } | RunnableLambda(temp2) | self.prompt_tamplate | print_prompt | self.chat_model | StrOutputParser()
        )
        
        his_chain=RunnableWithMessageHistory(
            chain,history.get_history,input_messages_key='input',history_messages_key='history'
        )
        
        return his_chain
    

if __name__=='__main__':
    session_config={
        'configurable':{
            'session_id':'user_001'
        }
    }

    service=RagService()
    chain=service.get_chain()
    ans=chain.invoke({'input':'冬天呢'},session_config)
    print(ans)