md5_path="E:/RAG+Agent/RAG智能体开发/md5.text"



#Chroma
collection_name="RAG"
persist_directory="E:/RAG+Agent/RAG智能体开发/chroma_db"



#spiliter
chunk_size=1000
chunk_overlap=100
separators=[',','.','?','，','。','？','\n\n','\n',' ','']

max_split_char_number=1000      #文本分割的阈值



#
similarity_threshold=2          #检索返回的匹配文本数量



#AI-model
embedding_model="text-embedding-v4"
chat_model="qwen3-max"