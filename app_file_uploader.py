# 基于Streamlit完成WEB网页上传服务

import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

# 添加网页标题
st.title("知识库更新服务")

if "service" not in st.session_state:
    st.session_state["service"]=KnowledgeBaseService()

#file_uploader
uploader_file=st.file_uploader(    #文件上传框
    label="请上传TXT文件",          #提示语
    type=["txt"],
    accept_multiple_files=False     #是否接受多文件上传，False->禁止
)

if uploader_file is not None:           #若上传文件不为空
    file_name=uploader_file.name        #获取文件名
    file_type=uploader_file.type        #获取文件类型
    file_size=uploader_file.size/1024   #获取文件大小(KB)
    st.subheader(f"文件名:{file_name}") #st.subheader-->二级标题
    st.write(f"文件格式：{file_type} | 文件大小：{file_size:.2f}KB")   #st.write-->正文  |  file_size:.2f-->精确的小数点后2位
    st.write("-"*100)
    
    text=uploader_file.getvalue().decode("utf-8")   #getvalue(获取文件内容)-->字节(bytes)-->decode("utf-8")

    with st.spinner("载入中。。。"):        #在运行st.spinner时，会有一个等待时间
        time.sleep(3)
        res=st.session_state['service'].upload_by_str(text,file_name)
        st.write(res)

    
