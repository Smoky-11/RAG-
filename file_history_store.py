import os,json
from typing import Sequence
from langchain_core.messages import message_to_dict,messages_from_dict,BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
# message_to_dict：单个消息对象（BaseMessage类实例） =》字典
# messages_from_dict：[字典、字典……] =》[BaseMessage、BaseMessage……]
# AIMessage、Human Message、SystemMessage都是BaseMessage的子类


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id=session_id          #会话id
        self.storage_path=storage_path      #不同会话id存储文件所在的存储路径
        
        self.file_path=os.path.join(self.storage_path,self.session_id)      #完整的文件路径

        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)          #确保文件夹存在

    
    #add_messages函数，返回None
    def add_messages(self,messages:Sequence[BaseMessage]) -> None:           #Sequence序列类似于list、tuple
        all_messages=list(self.messages)        #已有的消息列表
        all_messages.extend(messages)           #将新的消息和已有消息合成一个新的消息列表

        # 将数据同步写入到本地文件中
        #类对象写入文件 ->二进制
        #可以使用message_to_dict将BaseMessage转化为dict，借助json将dict写入文件

        # new_messages=[]
        # for message in all_messages:
        #     d=message_to_dict(message)
        #     new_messages.append(d)
            
        new_messages=[message_to_dict(message) for message in all_messages]

        with open(self.file_path,"w",encoding="utf-8")as f:
            json.dump(new_messages,f)

    @property    # @property装饰器将messages方法变成成员属性应用
    def messages(self) -> list[BaseMessage]:
        # 当前文件：[字典]
        try:
            with open(self.file_path,"r",encoding="utf-8")as f:
                message_data=json.load(f)                   #返回值是：[字典]
                return messages_from_dict(message_data)     #返回BaseMessage
        except FileNotFoundError:
            return []
        
    def clear(self) -> None:
        with open(self.file_path,"w",encoding="utf-8")as f:
            json.dump([],f)


#实现通过session_id获取InMemoryChatMessageHistory类对象
def get_history(session_id):
    return FileChatMessageHistory(session_id,storage_path="./data/examp_data")
