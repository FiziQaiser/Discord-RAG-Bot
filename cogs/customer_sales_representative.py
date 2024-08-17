from discord.ext import commands
from discord.ext.commands import Context
import discord
from discord import app_commands

from io import BytesIO
import fitz  # PyMuPDF
import os
from logger_config import logger  # Import the logger

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

from chromadb import PersistentClient

# Define constants and initialize components
CHROMA_BASE_PATH = "./db"
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

model = ChatGroq(
    temperature=0,
    model="llama3-70b-8192",
    api_key=GROQ_API_KEY
)

template = """
You are a customer sales representative. Strictly use the tone of a customer sale representative.
Answer the question based on the context below. If you can't answer the question 
or the context is not relevant to the question, reply "I don't know".

Context: {context}

Question: {question}
"""

prompt = PromptTemplate.from_template(template)

class CSR(commands.Cog, name="CSR"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="query",
        description="Ask a question based on the uploaded PDF content.",
    )
    @app_commands.describe(question="Ask a question based on the uploaded PDF content.")
    async def query(self, context: Context, *, question: str) -> None:
        await context.defer()
        try:
            server_id = str(context.guild.id)  # Get the server ID as a string
            chroma_path = os.path.join(CHROMA_BASE_PATH, server_id)

            # Check if the Chroma database for this server exists
            if not os.path.exists(chroma_path):
                await context.send("No database found for this server. Please upload a PDF to create a database first.")
                return

            db = Chroma(persist_directory=chroma_path, embedding_function=embedding)
            results = db.similarity_search_with_relevance_scores(question, k=3)

            if len(results) == 0 or results[0][1] < 0.3:
                await context.send("Unable to find matching results.")
                return

            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

            # Generate the response using the model
            chain = prompt | model | StrOutputParser()
            response = chain.invoke({
                "context": context_text,
                "question": question
            })

            await context.send(content=response)
        except Exception as e:
            await context.send(content=f"Error processing query: {e}")
            logger.error(f"Error processing query: {e}")

    @commands.hybrid_command(
        name="upload_file",
        description="Upload a PDF file to enable the bot to answer queries based on its content.",
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(file="The PDF file to be processed for answering future queries.")
    async def upload_file(self, context: Context, file: discord.Attachment) -> None:
        await context.defer()

        if file and file.filename.endswith('.pdf'):
            # Load the file content into memory
            file_data = await file.read()
            pdf_stream = BytesIO(file_data)

            # Process the file to create Chroma DB
            try:
                server_id = str(context.guild.id)  # Get the server ID as a string
                create_chroma_db(pdf_stream, server_id)
                await context.send(content=f"{file.filename} successfully uploaded ✅")
                logger.success(f"{file.filename} successfully uploaded ✅")
            except Exception as e:
                await context.send(content=f"Error uploading file: {e}")
                logger.error(f"Error uploading file: {e}")

        else:
            await context.send("Please upload a valid PDF file.")


    @upload_file.error
    async def upload_file_error(self, context: Context, error):
        logger.error(f"Error uploading file: {error}")
        await context.send(error, ephemeral= True)


    # Delete the server's data when the bot is kicked
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            server_id = str(guild.id)
            chroma_path = os.path.join(CHROMA_BASE_PATH, server_id)
            
            # Delete the server's ChromaDB data if it exists
            if os.path.exists(chroma_path):
                delete_collection(chroma_path)
                logger.success(f"Deleted ChromaDB directory for server: {guild.name} ({guild.id})")

        except Exception as e:
            logger.error(f"Failed to handle on_guild_remove event for server: {guild.name} ({guild.id}): {e}")


def delete_collection(path: str):
	try:
		# Default collection name
		collection_name = "langchain"
		
		# Initialize the ChromaDB client
		chroma_client = PersistentClient(path=path)
		
		# Retrieve all collections
		collections = chroma_client.list_collections()
		
		# Check if the collection exists
		if any(collection.name == collection_name for collection in collections):
			# Delete the collection if it exists
			chroma_client.delete_collection(collection_name)
			logger.info(f"Collection '{collection_name}' deleted successfully")
		else:
			logger.info(f"Collection '{collection_name}' does not exist")
	except Exception as e:
		logger.error(f"Unable to delete collection: {e}")


def create_chroma_db(pdf_stream: BytesIO, server_id: str):
    def generate_data_store():
        documents = load_documents()
        chunks = split_text(documents)
        save_to_chroma(chunks)

    def load_documents():
        documents = []
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text = page.get_text("text")
            metadata = {
                "page_number": page_number + 1,
                "server_id": server_id  # Add server ID to metadata
            }
            documents.append(Document(page_content=text, metadata=metadata))
        logger.info("Documents loaded")
        return documents

    def split_text(documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks


    def save_to_chroma(chunks: list[Document]):
        chroma_path = os.path.join(CHROMA_BASE_PATH, server_id)
        
        # Clear out the existing database for this server
        if os.path.exists(chroma_path):
            delete_collection(chroma_path)

        logger.info(f"Creating new Chroma database in directory {chroma_path}")
        try:
            # Create a new DB from the documents
            db = Chroma.from_documents(
                chunks, embedding, persist_directory=chroma_path
            )

            logger.success(f"ChromaDB successfully created and persisted for server: {server_id}")
        except Exception as e:
            logger.error(f"Error creating or persisting Chroma database for server: {server_id} | {e}")
            raise  # Re-raise the exception to be caught in the `upload_file` method

    generate_data_store()

async def setup(bot) -> None:
    await bot.add_cog(CSR(bot))