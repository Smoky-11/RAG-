from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda, RunnablePassthrough,RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history


def print_prompt(prompt):           #打印prompt
    print("-"*100)
    print(prompt.to_string())
    return prompt

class RAGService(object):
    def __init__(self):
        self.vector_service=VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model)
        )

        self.prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system","以我的参考资料为主，简洁和专业的回答用户提问的问题，参考资料{context}"),
                ("system","并且我将会给你一个历史记录，如下："),
                MessagesPlaceholder("history"),
                ("human","请回答：{input}")
            ]
        )

        self.chat_model=ChatTongyi(model=config.chat_model,streaming=True)

        self.chain=self.__get_chain()

    def __get_chain(self):      #获取最终的执行链
        retriever=self.vector_service.get_retriever()

        def format_doucment(docs):
            if not docs:
                return "无相关参考资料"
            
            formatted_str=""
            for doc in docs:
                formatted_str+=f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"

            return formatted_str
        
        def format_for_restriever(value):
            return value["input"]
        
        def format_for_prompt_template(value):
            new_value={}
            new_value["input"]=value["input"]["input"]
            new_value["context"]=value["context"]
            new_value["history"]=value["input"]["history"]
            return new_value

        chain=(
            {
                "input":RunnablePassthrough(),
                "context": RunnableLambda(format_for_restriever) | retriever | format_doucment 
            }   | RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )
        
    
        conversation_chain=RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        
        return conversation_chain

if __name__ == "__main__":
    session_config=config.session_config
    service=RAGService().chain.invoke({"input":"我去草原应该搭配什么颜色的衣服"},session_config)
    print(service)