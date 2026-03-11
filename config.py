md5_data_path='./md5.txt'

# chroma
collection_name='test'
persist_path='./chroma_db'
embbeding_fun_name='text-embedding-v4'
topk=2

#spliter
chunk_size=1000
chunk_overlap=100
seperators=['\n\n','\n','.',',','?','!','。','，','！','？',' ','']
max_split_char_num=1000

chat_model_name='deepseek-chat'