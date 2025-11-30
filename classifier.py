"""Profile classification schema used for structured metadata extraction."""

import logging
from llama_index.llms.openai import OpenAI
from llama_index.core.program import LLMTextCompletionProgram
from dotenv import load_dotenv
from schema import Profile
from prompts import CLASSIFIER_PROMPT
# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = OpenAI(model="gpt-3.5-turbo")

def classify_resume(resume_text: str):
    """
    Classify a resume as TECH or NON_TECH using LLM.
    
    Args:
        resume_text (str): Raw resume text
        
    Returns:
        ClassificationOutput: Structured classification result
    """
    logger.info("Starting resume classification...")
    try:
        prompt = CLASSIFIER_PROMPT.format(resume_text=resume_text)
        classifier_program = LLMTextCompletionProgram.from_defaults(
            output_cls=Profile,
            llm=llm,
            prompt_template_str=prompt,
            verbose=False,
        )
        # Call the LLM program
        output = classifier_program(resume_text=resume_text)
        return output
    except Exception as e:
        logger.error("Error during classification: %s", e)
        raise
