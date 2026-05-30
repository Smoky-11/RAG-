from langchain_chroma import Chroma
import config_data as config

class VectorStoreService(object):
    def __init__(self,embedding):
        self.embedding=embedding

        self.vector_store=Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )

    def get_retriever(self):        #返回向量检索器，方便入链
        return self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})
    

if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings

    service=VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()
    res=service.invoke("我身高180cm，我应该选择什么样尺码的衣服？")
    
    print(res)
