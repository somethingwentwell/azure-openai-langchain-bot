import os
import fnmatch
from langchain.document_loaders import UnstructuredHTMLLoader, UnstructuredMarkdownLoader, UnstructuredURLLoader, UnstructuredPDFLoader, TextLoader, CSVLoader
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.agents import Tool
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

embeddings = OpenAIEmbeddings(client=None, model=str(os.getenv("EMBEDDING_DEPLOYMENT_NAME")), chunk_size=1)
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=20)

class DocsInput(BaseModel):
    question: str = Field()

def importedMarkdownTools(llm):
    tools = []
    for root, dirnames, filenames in os.walk('./docs-data/markdowns'):
        if (os.path.basename(root) != "markdowns"):
            data = []
            for filename in fnmatch.filter(filenames, '*.md'):
                loader = UnstructuredMarkdownLoader(os.path.join(root, filename))
                data += loader.load()
            print("Embedding " + str(filenames))
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="mddocs")
            # doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_db.as_retriever(search_kwargs={"k": 1}))
            tools.append(Tool(
                name = os.path.basename(root),
                func=doc.run,
                coroutine=doc.arun,
                description=f"useful for when you need to answer questions about {os.path.basename(root)}. Input should be a fully formed question.",
                args_schema=DocsInput
            ))
    return tools

def importedHtmlTools(llm):
    tools = []
    for root, dirnames, filenames in os.walk('./docs-data/htmls'):
        if (os.path.basename(root) != "htmls"):
            data = []
            for filename in fnmatch.filter(filenames, '*.html'):
                loader = UnstructuredHTMLLoader(os.path.join(root, filename))
                data += loader.load()
            print("Embedding " + str(filenames))
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="htmldocs")
            # doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_db.as_retriever(search_kwargs={"k": 1}))
            tools.append(Tool(
                name = os.path.basename(root),
                func=doc.run,
                coroutine=doc.arun,
                description=f"useful for when you need to answer questions about {os.path.basename(root)}. Input should be a fully formed question.",
                args_schema=DocsInput
            ))
    return tools

def importedPdfTools(llm):
    tools = []
    for root, dirnames, filenames in os.walk('./docs-data/pdfs'):
        if (os.path.basename(root) != "pdfs"):
            data = []
            for filename in fnmatch.filter(filenames, '*.pdf'):
                loader = UnstructuredPDFLoader(os.path.join(root, filename), mode="elements")
                data += loader.load()
            print("Embedding " + str(filenames))
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="pdfdocs")
            # doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_db.as_retriever(search_kwargs={"k": 1}))
            tools.append(Tool(
                name = os.path.basename(root),
                func=doc.run,
                coroutine=doc.arun,
                description=f"useful for when you need to answer questions about {os.path.basename(root)}. Input should be a fully formed question.",
                args_schema=DocsInput
            ))
    return tools

def importedTxtTools(llm):
    tools = []
    for root, dirnames, filenames in os.walk('./docs-data/txts'):
        if (os.path.basename(root) != "txts"):
            data = []
            for filename in fnmatch.filter(filenames, '*.txt'):
                loader = TextLoader(os.path.join(root, filename))
                data += loader.load()
            print("Embedding " + str(filenames))
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="txtdocs")
            # doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_db.as_retriever(search_kwargs={"k": 1}))
            tools.append(Tool(
                name = os.path.basename(root),
                func=doc.run,
                coroutine=doc.arun,
                description=f"useful for when you need to answer questions about {os.path.basename(root)}. Input should be a fully formed question.",
                args_schema=DocsInput
            ))
    return tools

def importedCsvTools(llm):
    tools = []
    for root, dirnames, filenames in os.walk('./docs-data/csvs'):
        if (os.path.basename(root) != "csvs"):
            data = []
            for filename in fnmatch.filter(filenames, '*.csv'):
                loader = CSVLoader(os.path.join(root, filename))
                data += loader.load()
            print("Embedding " + str(filenames))
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="csvdocs")
            # doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_db.as_retriever(search_kwargs={"k": 1}))
            tools.append(Tool(
                name = os.path.basename(root),
                func=doc.run,
                coroutine=doc.arun,
                description=f"useful for when you need to answer questions about {os.path.basename(root)}. Input should be a fully formed question.",
                args_schema=DocsInput
            ))
    return tools

def docsimport(llm):
    tools = []
    tools.extend(importedTxtTools(llm))
    tools.extend(importedCsvTools(llm))
    tools.extend(importedPdfTools(llm))
    tools.extend(importedHtmlTools(llm))
    tools.extend(importedMarkdownTools(llm))
    return tools