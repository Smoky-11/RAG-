import os
import config_data as config    #导入自定义配置文件config_data.py文件
import hashlib                  #Python 内置库，用于生成 MD5 哈希值
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter     #递归文本分割器
from datetime import datetime   #获取当前时间


def check_md5(md5_str):        #检查传入的md5字符串是否已经被处理过
    if not os.path.exists(config.md5_path):
        #若文件不存在，表示未有处理过的md5
        open(config.md5_path,'w',encoding='utf-8').close()  
        #若文件不存在，则自动创建一个文件并关闭
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():
            #若文件存在，则打开文件，并读取全部行
            line=line.strip()   #strip：处理（去掉）字符串前后的空格和回车
            if line==md5_str:
                return True     #文件已处理
        return False            #文件未找到


def save_md5(md5_str):         #将传入的md5字符串记录到文件内保存
    with open(config.md5_path,'a',encoding='utf-8') as f:
        #'a'表示追加模式
        f.write(md5_str+'\n')


def get_string_md5(input_str,encoding='utf-8'):   #将传入的字符串转化为md5字符串
    str_bytes=input_str.encode(encoding=encoding)
    #将字符串转换为bytes字节数组

    md5_obj=hashlib.md5()           #创建md5对象
    md5_obj.update(str_bytes)       #将str_bytes转换为md5
    md5_hex=md5_obj.hexdigest()     #将md5转化为16进制数
    
    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True) #若文件夹不存在，则创建文件夹

        self.chroma=Chroma(                                 #向量存储的实例
            collection_name=config.collection_name,         #创建向量库表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),  #嵌入模板
            persist_directory=config.persist_directory      #文件夹存储路径
        )        

        self.spliter=RecursiveCharacterTextSplitter(       #文本分割器的对象
            chunk_size=config.chunk_size,                   #文本长度
            chunk_overlap=config.chunk_overlap,             #连续文本段之间的重叠数量
            separators=config.separators,                   #自然段了划分符号
            length_function=len                             #使用Python的len函数做长度统计依据
        )      

    def upload_by_str(self,data,filename):      #将传入的字符串进行向量化，存入向量库中
        
        md5_hex=get_string_md5(data)            #先获取md5值

        if check_md5(md5_hex):                  #存在则返回True
            return "[跳过]，内容已存在知识库中"

        if len(data)>config.max_split_char_number:
            knowledge_chunks=self.spliter.split_text(data)      #返回值是list[str]
        else:
            knowledge_chunks=[data]                             #保持一致

        
        # 构造元数据（metadata），记录这段内容的来源信息
        metadata={
            "source":filename,      #文件名称
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),     #时间
            "operator":"System"     #操作员
        }

        self.chroma.add_texts(      #将内容加载到向量库中   Chroma的批量写入方法                                
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]  # 遍历 knowledge_chunks 中的每一段文本,把同一个 metadata 字典塞进去
        )
        """如果两段文本只给一段metadata，Chroma会报错（长度不匹配）。所以必须保证len(metadatas)==len(texts)"""

        save_md5(md5_hex)
        
        return "[成功]内容已经成功载入向量库"


if __name__=='__main__':
    # num1=get_string_md5('周杰伦')       #输出7a8941058aaf4df5147042ce104568da   
    # num2=get_string_md5('周杰伦')       #输出7a8941058aaf4df5147042ce104568da
    # num3=get_string_md5('周杰伦3')      #输出94df1b1ac1d38d55aa46713888519459
    """完全相同的字符串，md5值是一样的，哪怕有一点变化，md5值就会改变"""

    # save_md5(num1)
    # print(check_md5(num1),check_md5(num2),check_md5(num3))  #输出：True、True、False

    service=KnowledgeBaseService()
    pr=service.upload_by_str("张雪峰老师","testfile")
    print(pr)