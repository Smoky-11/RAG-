md5_path="./md5.text"



#Chroma
collection_name="RAG"
persist_directory="./chroma_db"



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


#session_config
session_config={
    "configurable":{
        "session_id":"user_01"
    }
}