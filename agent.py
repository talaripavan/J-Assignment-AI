""" Resume Analysis Agent """
import logging
from typing import Optional
from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from prompts import AGENT_SYSTEM_PROMPT
from resume_skill import analyze_resume,query_resume
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

llm = OpenAI(model="gpt-3.5-turbo")

analyze_resume_tool = FunctionTool.from_defaults(
    name="analyze_resume",
    description=(
        "Use this tool when the user provides resume text and wants it analyzed. "
        "The tool extracts skills, experience, projects, seniority, strengths, weaknesses, "
        "and produces a structured evaluation of the resume."
    ),
    fn=analyze_resume
)

query_resume_tool = FunctionTool.from_defaults(
    name="query_resume_data",
    description=(
        "Use this tool when the user asks a question about a resume or wants to retrieve "
        "information from it. This tool answers queries such as skills, tech stack, "
        "experience match, and specific capability checks using the provided resume text."
    ),
    fn=query_resume
)

async def run_resume_agent(resume_text: Optional[str] = None,
                           query: Optional[str] = None) -> str:
    """Run the resume analysis agent.

    Args:
        resume_text (Optional[str]): The resume text provided by the user.
        query (Optional[str]): A follow-up query related to the resume.

    Returns:
        str: The agent's final response.

    Raises:
        ValueError: If neither resume_text nor query is provided.
    """
    agent_worker = FunctionAgent(
        name="Resume Agent",
        tools=[analyze_resume_tool, query_resume_tool],
        system_prompt=AGENT_SYSTEM_PROMPT,
        llm=llm
    )

    if resume_text and query:
        prompt = (
            "Analyze the resume and then answer the query.\n\n"
            f"Resume:\n{resume_text}\n\nQuery: {query}"
        )

    elif resume_text and not query:
        prompt = f"Analyze the resume:\n\n{resume_text}"

    else:
        raise ValueError("You must provide at least resume_text or query")

    response = await agent_worker.run(user_msg=prompt)
    #print(response)
    return response
