from search_service import SearchService
from knowledge_service import KnowledgeBaseService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import config

def print_prompt(prompt):
    print('='*20)
    print(prompt.to_string())
    print('='*20)
    return prompt

class RagService(object):
    def __init__(self):
        self.search_service=SearchService(DashScopeEmbeddings(model=config.embbeding_fun_name))
        self.prompt_tamplate=ChatPromptTemplate.from_messages(
            [
                ('system','如有参考资料,以提供的参考资料为主,简洁专业地回答用户的问题。参考资料:{context}'),
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
        
        chain=(
            {
                'input':RunnablePassthrough(),
                'context': retriever | change_doc_format
            } | self.prompt_tamplate | print_prompt | self.chat_model | StrOutputParser()
        )
        
        return chain

if __name__=='__main__':
    service=RagService()
    chain=service.get_chain()
    ans=chain.invoke('体重180斤尺码推荐')
    print(ans)