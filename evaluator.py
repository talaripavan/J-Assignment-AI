""" Resume Evaluator """
from typing import List, Dict, Any , Optional
import logging
from llama_index.core.evaluation import FaithfulnessEvaluator
from llama_index.core.llms import LLM
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

class RAGEvaluators:
    """ Resume Evaluator """
    def __init__(self, llm: LLM):
        self.faithfulness = FaithfulnessEvaluator(llm=llm)

    def evaluate_response(
        self,
        query: Optional[str],
        response: str,
        contexts: List[str],
    ) -> Dict[str, Any]:
        """
        Evaluate response for faithfulness.

        Args:
            query: Original user question.
            response: Generated answer from the model
            contexts: Retrieved context chunks

        Returns:
            Dict with faithfulness results.
        """
        if not contexts:
            raise ValueError("Contexts cannot be empty")
        logger.info("Running faithfulness evaluation...")
        # Always evaluate faithfulness
        faithfulness_result = self.faithfulness.evaluate(
            query=query or None,
            response=response,
            contexts=contexts,
        )

        results: Dict[str, Any] = {
            "faithfulness_passing": faithfulness_result.passing,
            "faithfulness_score": faithfulness_result.score,
            "faithfulness_feedback": faithfulness_result.feedback or "",
        }

        return results
