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

embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_DEPLOYMENT_NAME"), chunk_size=1)
text_splitter = CharacterTextSplitter(chunk_size=600, chunk_overlap=0)

class DocsInput(BaseModel):
    question: str = Field()

def importedMarkdownTools(name, llm):
    tools = []
    for root, dirnames, filenames in os.walk('./markdowns'):
        if (os.path.basename(root) != "markdowns"):
            data = []
            for filename in fnmatch.filter(filenames, '*.md'):
                loader = UnstructuredMarkdownLoader(os.path.join(root, filename))
                data += loader.load()
            print(filenames)
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="mddocs")
            # doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_db.as_retriever(search_kwargs={"k": 1}))
            tools.append(Tool(
                name = name + ": " + os.path.basename(root),
                func=doc.run,
                description=f"useful for when you need to answer questions about {os.path.basename(root)} in {name}. Input should be a fully formed question.",
                args_schema=DocsInput
            ))
    return tools

def importedHtmlTools(name, llm):
    tools = []
    for root, dirnames, filenames in os.walk('./htmls'):
        if (os.path.basename(root) != "htmls"):
            data = []
            for filename in fnmatch.filter(filenames, '*.html'):
                loader = UnstructuredHTMLLoader(os.path.join(root, filename))
                data += loader.load()
            print(filenames)
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="htmldocs")
            # doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_db.as_retriever(search_kwargs={"k": 1}))
            tools.append(Tool(
                name = name + ": " + os.path.basename(root),
                func=doc.run,
                description=f"useful for when you need to answer questions about {os.path.basename(root)} in {name}. Input should be a fully formed question.",
                args_schema=DocsInput
            ))
    return tools

def importedPdfTools(name, llm):
    tools = []
    for root, dirnames, filenames in os.walk('./pdfs'):
        if (os.path.basename(root) != "pdfs"):
            data = []
            for filename in fnmatch.filter(filenames, '*.pdf'):
                loader = UnstructuredPDFLoader(os.path.join(root, filename), mode="elements")
                data += loader.load()
            print(filenames)
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="pdfdocs")
            # doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_db.as_retriever(search_kwargs={"k": 1}))
            tools.append(Tool(
                name = name + ": " + os.path.basename(root),
                func=doc.run,
                description=f"useful for when you need to answer questions about {os.path.basename(root)} in {name}. Input should be a fully formed question.",
                args_schema=DocsInput
            ))
    return tools

def importedTxtTools(name, llm):
    tools = []
    for root, dirnames, filenames in os.walk('./txts'):
        if (os.path.basename(root) != "txts"):
            data = []
            for filename in fnmatch.filter(filenames, '*.txt'):
                loader = TextLoader(os.path.join(root, filename))
                data += loader.load()
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="txtdocs")
            # doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_db.as_retriever(search_kwargs={"k": 1}))
            tools.append(Tool(
                name = name + " " + os.path.basename(root),
                func=doc.run,
                description=f"useful for when you need to answer questions about {os.path.basename(root)} in {name}. Input should be a fully formed question.",
                args_schema=DocsInput
            ))
    return tools

def importedCsvTools(name, llm):
    tools = []
    for root, dirnames, filenames in os.walk('./csvs'):
        if (os.path.basename(root) != "csvs"):
            data = []
            for filename in fnmatch.filter(filenames, '*.csv'):
                loader = CSVLoader(os.path.join(root, filename))
                data += loader.load()
            doc_texts = text_splitter.split_documents(data)
            doc_db = Chroma.from_documents(doc_texts, embeddings, collection_name="csvdocs")
            # doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_db)
            doc = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=doc_db.as_retriever(search_kwargs={"k": 1}))
            tools.append(Tool(
                name = name + " " + os.path.basename(root),
                func=doc.run,
                description=f"useful for when you need to answer questions about {os.path.basename(root)} in {name}. Input should be a fully formed question.",
                args_schema=DocsInput
            ))
    return tools

def allImportedTools(name, llm):
    tools = []
    # tools.extend(importedCsvTools(name, llm))
    tools.extend(importedTxtTools(name, llm))
    # tools.extend(importedPdfTools(name, llm))
    # tools.extend(importedHtmlTools(name, llm))
    # tools.extend(importedMarkdownTools(name, llm))
    return tools