import streamlit as st
from RAG import RAGService
import config_data as config

st.title("智能机器人")
st.divider()        #分隔符

if "message" not in st.session_state:
    st.session_state["message"]=[{"role":"assistant","content":"你好，请问有什么能帮助你？"}]

if "rag" not in st.session_state:
    st.session_state["rag"]=RAGService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt=st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)       #输出用户的提问 
    st.session_state["message"].append({"role":"user","content":prompt})

    prompt_list=[]

    with st.spinner("AI思考中......"):
        res=st.session_state["rag"].chain.stream({"input":prompt},config.session_config)
        
        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res,prompt_list))
        #   这里使用chain.stream作为流式输出，但stream作为一个迭代器，本质上与invoke不同
        #   因此，这里的st.session_state无法追加历史到session_state中
        #   需要使用类似抓包的形式，将获取的stream转成list，每个字符串单独保存在list中
        st.session_state["message"].append({"role":"assistant","content":"".join(prompt_list)})
        #   使用空字符串链接list中全部字符串    -->['a','b','c'] "".join(list) ==>abc