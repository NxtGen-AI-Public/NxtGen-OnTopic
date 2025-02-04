import os

from enum import Enum
from typing import List
from typing_extensions import TypedDict

# langchain imports
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate

# langgraph imports
from langgraph.graph import StateGraph, END

class LLMType(str, Enum):
    """
    Defines an enumeration for LLM types
    """
    OLLAMA = "ollama"

# Define constants for model parameters
MODEL_OLLAMA = "llama3.1:8b"
MODEL_OPENAI = "gpt-4o-mini"
TEMPERATURE_DEFAULT = 0

SYSTEM_MESSAGE_REWRITER = (
    "You are a question re-writer that converts an input question to a better version "
    "that is optimized for retrieval. Look at the input and try to reason about the "
    "underlying semantic intent / meaning."
)

HUMAN_MESSAGE_TEMPLATE_REWRITER = (
    "Here is the initial question:\\n\\n{question}\\nFormulate an improved question."
)

# Example documents
docs = [
    Document(
        page_content="EOD REPORT THURSDAY 14 NOVEMBER\\nARYAA\\n\\n"
                     "- Tested out lab workflow using sample data provided by them "
                     "and created a small model.\\n\\n"
                     "- Created a small knowledge file using our GOA_GST data and used "
                     "this to train the Granite model to test if it is working as expected "
                     "-- IT IS -- also resulted in a small model fine-tuned on GOA GST "
                     "data.\\n\\n"
                     "- Now generating a large knowledge file which will contain data from "
                     "an entire directory of PDFs about CA ACTS, which will be used to train "
                     "our model.",
        metadata={"source": "AI-Engineering Channel", "created_at": "2024-11-14"},
    ),
    Document(
        page_content="Shilpa\\n"
                     "- Moved workflow to PEFT-oriented strategies\\n"
                     "- Post InstructLab pipeline is in place. Aryaa will cover other "
                     "workflows within the NeMo framework as her pipeline on InstructLab "
                     "runs.\\n\\nSush\\n"
                     "- Produced code analysis report for CSC on their code base\\n"
                     "- Explored Meta Self-evaluator to evaluate AMD 1B language model.",
        metadata={"source": "AI-Engineering Channel", "created_at": "2024-11-15"},
    ),
    Document(
        page_content="EOD Report Friday 15 November\\nShilpa\\n"
                     "I have been doing model downloading and model conversion in .nemo "
                     "format but it is still having an error while conversion. So, I will "
                     "be solving that error.\\n\\nSushmender\\n"
                     "I am exploring Meta's Self-taught-evaluator (Llama-70B) model and "
                     "requested Nvidia GPU for deploying the model.",
        metadata={"source": "AI-Engineering Channel", "created_at": "2024-11-18"},
    ),
    Document(
        page_content="Report 27th Nov\\nAryaa\\n"
                     "The model trained on section 1 is ready.\\n\\nShilpa\\n"
                     "I completed my pipeline for making the dataset. Now I will move to "
                     "split my dataset into train, test, and valid to train my model.\\n\\n"
                     "Sushmender\\nI pulled the 'AI-Engineering' channel posts using a GET "
                     "request, converted them into JSON format, and am using it as a "
                     "knowledge base for my RAG setup.",
        metadata={"source": "AI-Engineering Channel", "created_at": "2024-11-28"},
    ),
]

def log_with_horizontal_line(message):
    """Function to print logs in a structured and readable format"""
    # Get the terminal width
    terminal_width = os.get_terminal_size().columns

    # Create the horizontal line
    horizontal_line = '-' * terminal_width

    # Print the formatted message
    print(horizontal_line)
    print()
    print(message)
    print()
    print(horizontal_line)

def get_llm():
    """
    Retrieves an instance of a Large Language Model (LLM) based on the environment 
    variable 'LLM_TYPE'.

    The function checks the value of the 'LLM_TYPE' environment variable and returns 
    an instance of the corresponding LLM. If the environment variable is not set or 
    has an unexpected value, it defaults to Ollama.

    Returns:
        An instance of either ChatOllama or ChatOpenAI.
    """

    llm_type = os.getenv("LLM_TYPE", LLMType.OLLAMA.value)

    if llm_type == LLMType.OLLAMA.value:
        return ChatOllama(model = MODEL_OLLAMA, temperature = TEMPERATURE_DEFAULT)

    return ChatOpenAI(model = MODEL_OPENAI, temperature = TEMPERATURE_DEFAULT)

def get_embeddings():
    """Function to get embedding instance based on environment variable."""

    embedding_type = os.getenv("LLM_TYPE", LLMType.OLLAMA.value)

    if embedding_type == LLMType.OLLAMA.value:
        return OllamaEmbeddings(model = MODEL_OLLAMA)

    return OpenAIEmbeddings()

# Embedding function and documents
embedding_function = get_embeddings()

# Initialize Chroma vector store
db = Chroma.from_documents(docs, embedding_function)
retriever = db.as_retriever()

class AgentState(TypedDict):
    """
    Represents the state of an agent.

    Attributes:
        question (str): The question posed to the agent.
        top_documents (List[str]): A list of top relevant documents.
        llm_output (str): The output from the language model.
        classification_result (str): The result of the classification.
    """
    question: str
    top_documents: List[str]
    llm_output: str
    classification_result: str

def create_prompt(question: str) -> ChatPromptTemplate:
    """
    Create a chat prompt template for the LLM.

    Args:
        question (str): The initial question to be rewritten.

    Returns:
        ChatPromptTemplate: The chat prompt template.
    """
    human_message = HUMAN_MESSAGE_TEMPLATE_REWRITER.format(question=question)
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_MESSAGE_REWRITER),
            ("human", human_message),
        ]
    )

def rewrite_question(prompt: ChatPromptTemplate, question: str) -> str:
    """
    Use the LLM to rewrite the question.

    Args:
        prompt (ChatPromptTemplate): The chat prompt template.
        question (str): The initial question to be rewritten.

    Returns:
        str: The rewritten question.
    """
    llm = get_llm()
    question_rewriter = prompt | llm | StrOutputParser()
    rewritten_question = question_rewriter.invoke({"question": question})
    return rewritten_question

def rewriter(agent_state: AgentState) -> AgentState:
    """
    Rewrites a given question to an optimized version for retrieval.

    Args:
        agent_state (AgentState): The current state of the agent, including the initial question.

    Returns:
        AgentState: The updated agent state with the rewritten question.
    """
    log_with_horizontal_line("Starting query rewriting...")
    question = agent_state["question"]

    prompt = create_prompt(question)
    rewritten_question = rewrite_question(prompt, question)

    agent_state["question"] = rewritten_question

    log_with_horizontal_line(f"Rewritten question:\\n{rewritten_question}")
    return agent_state

# Function to retrieve documents
def retrieve_documents(agent_state: AgentState):
    """
    Retrieves relevant documents based on the question in the agent's state.

    :param agent_state: A dictionary containing the current state of the agent, 
    including the question.
    :return: The updated agent state with the top 3 retrieved documents.
    """
    log_with_horizontal_line("Starting document retrieval...")
    question = agent_state["question"]
    documents = retriever.invoke(question)

    # Retrieve top 3 docs
    agent_state["top_documents"] = [doc.page_content for doc in documents[:3]]

    log_with_horizontal_line(f"Retrieved documents: {agent_state['top_documents']}")
    return agent_state

# Define the classifier function
def question_classifier(agent_state: AgentState) -> AgentState:
    """
    Classifies a question and its retrieved documents as on-topic or off-topic using 
    an LLM-based approach.

    Args:
        agent_state (AgentState): The current agent state containing the question and 
        top documents.

    Returns:
        AgentState: The updated agent state with the classification result.
    """

    log_with_horizontal_line("Starting topic classification...")

    # Extract relevant information from the agent state
    question = agent_state["question"]
    documents = agent_state["top_documents"]

    # Define the LLM-based classifier prompt
    classifier_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a classifier that determines if a question and retrieved documents are on-topic."),
            (
                "human",
                "Question: {question}\\n\\nDocuments: {documents}\\n\\nIs this on-topic? Respond with 'on-topic' or 'off-topic'.",
            ),
        ]
    )

    # Initialize the LLM instance
    llm = get_llm()

    # Create a pipeline for classification
    classifier_chain = classifier_prompt | llm | StrOutputParser()

    # Invoke the classification pipeline
    input_data = {"question": question, "documents": "\\n".join(documents)}
    raw_classification_result = classifier_chain.invoke(input_data)

    # Determine the classification result based on the LLM's response
    classification_result = "on-topic" if "on-topic" in raw_classification_result.lower() else "off-topic"

    # Update the agent state with the classification result
    agent_state["classification_result"] = classification_result

    log_with_horizontal_line(f"Classification result: {agent_state['classification_result']}")
    return agent_state

# Define the off-topic response function
def off_topic_response(state: AgentState):
    log_with_horizontal_line("Question is off-topic. Ending process.")
    state["llm_output"] = "The question is off-topic, ending the process."
    return state

# Function to rerank documents based on preference order
def rerank_documents(state: AgentState):
    log_with_horizontal_line("Starting document reranking with preferences...")
    question = state["question"]
    top_documents = state["top_documents"]

    reranker_prompt = PromptTemplate(
        input_variables=["question", "documents"],
        template="""Given the question and doccuments , rank the following documents in order of preference (1st, 2nd, 3rd) based on the relevence to the question. 
        Provide your ranking as "1st preference: <complete chunk>", "2nd preference: <complete chunk>", and "3rd preference: <complete chunk>".
        If there are fewer than 3 relevant documents, skip ranking those that are not useful.
        please give the complete chunks .
        
        Question: {question}
        Documents:{documents}"""
    )

    llm = get_llm()
    chain = reranker_prompt | llm | StrOutputParser()
    
    # Generate rankings
    ranking_result = chain.invoke({
        "question": question,
        "documents": top_documents
    })
    
    log_with_horizontal_line(f"Ranking result: {ranking_result}")
    
    # Pass the raw ranking result directly to the next stage (answer generation)
    state["top_documents"] = [ranking_result.strip()]  # Pass raw result directly to next node
    
    return state


# Function to generate answers
def generate_answer(state: AgentState):
    log_with_horizontal_line("Generating answer...")
    llm = get_llm()
    question = state["question"]
    context = "\n".join(state["top_documents"])  # This includes the raw ranking result

    template = """Answer the question based only on the following context:\n{context}\n\nQuestion: {question}. Dont mention like prefernce and context while generating the answer"""

    prompt = ChatPromptTemplate.from_template(template=template)
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"question": question, "context": context})
    state["llm_output"] = result
    log_with_horizontal_line(f"Generated answer: {result}")
    return state

# Updated workflow
workflow = StateGraph(AgentState)

# Add nodes for query rewriting, classification, off-topic response, and document retrieval
workflow.add_node("rewriter", rewriter)
workflow.add_node("retrieve_documents", retrieve_documents)
workflow.add_node("topic_decision", question_classifier)
workflow.add_node("off_topic_response", off_topic_response)
workflow.add_node("rerank_documents", rerank_documents)
workflow.add_node("generate_answer", generate_answer)

# Add conditional edges for topic decision after retrieval
workflow.add_conditional_edges(
    "topic_decision",
    lambda state: "on-topic" if state["classification_result"] == "on-topic" else "off-topic",
    {
        "on-topic": "rerank_documents",
        "off-topic": "off_topic_response",
    },
)

# Add edges for reranking and answer generation
workflow.add_edge("rewriter", "retrieve_documents")
workflow.add_edge("retrieve_documents", "topic_decision")
workflow.add_edge("rerank_documents", "generate_answer")
workflow.add_edge("generate_answer", END)

# Set entry point to query rewriting
workflow.set_entry_point("rewriter")

# Compile app
app = workflow.compile()


# Example invocation
if __name__ == "__main__":
    state = {"question": "What sushmender is working on?"}
    result = app.invoke(state)
    log_with_horizontal_line(f"Final answer: {result.get('llm_output', 'Process ended.')}")