import os
import fnmatch
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.vectorstores import Chroma
from langchain import VectorDBQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.agents import Tool
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(document_model_name=os.getenv("EMBEDDING_DEPLOYMENT_NAME"), chunk_size=1)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

def importedMarkdownTools(name, llm):
    tools = []
    for root, dirnames, filenames in os.walk('./markdowns'):
        if (os.path.basename(root) != "markdowns"):
            data = []
            for filename in fnmatch.filter(filenames, '*.md'):
                loader = UnstructuredMarkdownLoader(os.path.join(root, filename))
                data += loader.load()
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="mddocs")
            doc = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            tools.append(Tool(
                name = name + ": " + os.path.basename(root),
                func=doc.run,
                description=f"useful for when you need to answer questions about {os.path.basename(root)} in {name}. Input should be a fully formed question."
            ))
    return tools