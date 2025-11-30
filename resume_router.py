""" Resume Router """
from typing import Optional
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import LLM
from dotenv import load_dotenv
from schema import ResumeValidationResult
from prompts import RESUME_ROUTER_PROMPT

load_dotenv()


class ResumeRouter:
    """
    Single source of truth for resume detection.
    Two approaches:
      1. LLM-based (accurate, slower, costs money)
      2. Heuristic-based (fast, cheap, good enough for 90% cases)
    """
    def __init__(self, llm: Optional[LLM] = None):
        self.llm = llm or OpenAI(model="gpt-3.5-turbo", temperature=0.0)
        self._llm_program = self._build_llm_program()

    def classify_with_llm(self, text: str):
        """
        Uses LLM + structured output to determine if text is a resume.
        Best accuracy, especially for edge cases.
        """
        result = self._llm_program(query_str=text)
        return result

    def classify_with_heuristics(self, text: str):
        """
        Fast keyword + anti-keyword matching.
        Great for filtering obvious non-resumes early.
        """
        text_low = text.lower()
        resume_signals = [
            "experience", "skills", "education", "contact", "email:", "phone:",
            "years of experience", "software engineer", "developer", "cv", "resume"
        ]
        non_resume_signals = [
            "invoice", "receipt", "recipe", "ingredients", "bake at", "serves",
            "job description", "we are hiring", "salary", "benefits"
        ]

        if any(sig in text_low for sig in non_resume_signals):
            return False

        if sum(sig in text_low for sig in resume_signals) >= 2:
            return True

        return None

    @staticmethod
    def _build_llm_program() -> LLMTextCompletionProgram:
        prompt = RESUME_ROUTER_PROMPT
        return LLMTextCompletionProgram.from_defaults(
            output_cls=ResumeValidationResult,
            prompt=prompt,
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0.0),
        )
