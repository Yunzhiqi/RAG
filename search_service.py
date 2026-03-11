from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
import config

class SearchService(object):
    def __init__(self,embedding_fun):
        self.chroma=Chroma(
            collection_name=config.collection_name,
            embedding_function=embedding_fun,
            persist_directory=config.persist_path
        )
    def get_retriever(self):
        return self.chroma.as_retriever(search_kwargs={'k':config.topk})
    
if __name__=='__main__':
    service=SearchService(embedding_fun=DashScopeEmbeddings(model=config.embbeding_fun_name))
    r=service.get_retriever()
    ans=r.invoke(input='体重180斤尺码推荐')
    print(ans)