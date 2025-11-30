""" Skill / Tool for our Agent """
from typing import Dict, Any , Optional
import logging
from llama_index.llms.openai import OpenAI
from llama_index.core import Document
from llama_index.core import VectorStoreIndex
from dotenv import load_dotenv
from resume_router import ResumeRouter
from classifier import classify_resume
from evaluator import RAGEvaluators
# Load environment variables
load_dotenv()
llm = OpenAI(model="gpt-3.5-turbo")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize once at import time (safe in most agent frameworks)
_resume_router = ResumeRouter()
_resume_evaluators = RAGEvaluators(llm=llm)

def analyze_resume(resume_text: str) -> Dict[str, Any]:
    """
    Analyze Resume Tool: Full resume analysis pipeline.
    
    1. Fast heuristic check → is this even a resume?
    2. If yes → run full structured classification (skills, experience, etc.)
    3. If yes → evaluate the structured output for hallucinations (faithfulness)
    
    Returns consistent dict — perfect for tool calling in agents.
    """
    if not resume_text or not resume_text.strip():
        return {
            "passed_check": False,
            "reason": "Empty or invalid input",
            "classification": None,
            "evaluation": None,
        }

    logger.info("Starting resume analysis pipeline...")

    # Step 1: Fast guardrail — is this even a resume?
    router_result = _resume_router.classify_with_heuristics(resume_text)

    if not router_result:
        return {
            "passed_check": False,
            "reason": "Rejected by router: Non a resume",
            "classification": None,
            "evaluation": None,
        }

    # Step 2: Full structured classification
    try:
        classification_result = classify_resume(resume_text=resume_text)
    except RuntimeError as e:
        logger.error("Classification failed: %s",e)
        return {
            "passed_check": False,
            "reason": "Classification step failed",
            "classification": None,
            "evaluation": None,
        }

    # Step 3: Faithfulness evaluation (no query → relevancy skipped)
    evaluation_result=_resume_evaluators.evaluate_response(
        query=None,
        response=str(classification_result),
        contexts=[resume_text],
    )

    return {
        "passed_check": True,
        "classification": classification_result,
        "evaluation": evaluation_result,
        "summary": {
            "is_valid_resume": True,
            "faithfulness_score": evaluation_result.get("faithfulness_score"),
            "hallucination_detected": not evaluation_result.get("faithfulness_passing", True),
        }
    }


def build_resume_index(resume_text: str) -> VectorStoreIndex:
    """Build a vector index for the resume text.

    Args:
        resume_text (str): Raw resume text provided by the user.

    Returns:
        VectorStoreIndex: A vector index created from the resume document.

    Raises:
        ValueError: If resume_text is empty.
    """
    if not resume_text.strip():
        raise ValueError("resume_text cannot be empty.")

    logger.info("Building VectorStoreIndex for resume...")
    documents = [Document(text=resume_text)]
    index = VectorStoreIndex.from_documents(documents)
    return index


def query_resume(resume_text: Optional[str] = None, 
                 query: Optional[str] = None) -> str:
    """Query information from a resume using semantic search and LLM reasoning.

    Args:
        resume_text (Optional[str]): The raw resume text to analyze.
        query (Optional[str]): User query about the resume (skills, experience, etc.).

    Returns:
        str: The result from the semantic resume query.

    Raises:
        ValueError: If resume_text or query is missing.
        Exception: For any unexpected errors during query execution.
    
    Steps:
        Step 1: Build vector index
        Step 2: Create query engine
        Step 3: Execute query
    """
    logger.info("Executing resume query...")

    if not resume_text:
        raise ValueError("resume_text is required.")

    if not query:
        raise ValueError("query is required.")

    try:
        index = build_resume_index(resume_text)
        logger.debug("Creating query engine...")
        query_engine = index.as_query_engine(llm=llm)
        logger.debug("Running semantic query...")
        response = query_engine.query(query)
        return str(response)

    except Exception as e:
        logger.error("Error occurred during resume query: %s",e)
        raise

