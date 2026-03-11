import md5,config
from datetime import datetime
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class KnowledgeBaseService(object):
    
    def __init__(self):
        self.chroma=Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model='text-embedding-v4'),
            persist_directory=config.persist_path
        )
        
        self.spliter=RecursiveCharacterTextSplitter(
            separators=config.seperators
        )
        return
    
    def upload_str(self,data:str,filename:str):
        md5_hex=md5.get_md5(data)
        if md5.check_md5(md5_hex):
            return '[失败]已有,跳过'
        knowledge_data=self.spliter.split_text(data)
        meta_data={
            'source':filename,
            'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }    
        self.chroma.add_texts(
            knowledge_data,
            metadatas=[meta_data for _ in knowledge_data]
        )
        md5.save_md5(md5_hex)
        return '[成功]已写入文件'+filename
    
if __name__=='__main__':
    service=KnowledgeBaseService()
    ans=service.upload_str('ABC','test')
    print(ans)