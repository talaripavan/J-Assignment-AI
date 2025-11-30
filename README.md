# Resume Classification & Candidate Query System

An automated recruiting pipeline that ingests unstructured resume text, classifies candidate roles (TECH vs. NON_TECH), and extracts structured candidate profiles with built-in hallucination detection.

---

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API Key (set as `OPENAI_API_KEY` environment variable)

### Setup

```bash
# Clone the repository
git clone https://github.com/talaripavan/J-Assignment-AI.git
cd J-Assignment-AI

# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows:
.\env\Scripts\activate
# On macOS/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
OPENAI_API_KEY = "<key>"
```

### Dependencies

```
llama-index==0.14.7
llama-index-vector-stores-milvus==0.9.4
pymilvus==2.6.3
pylint==4.0.3
```

---

## Project Structure

```
J-Assignment-AI/
├── schema.py              # Pydantic models for data validation
├── prompts.py             # LLM prompt templates
├── resume_router.py       # Resume validation (Router)
├── classifier.py          # Role classification (Classifier)
├── resume_skill.py        # Skill extraction & querying (Extractor)
├── evaluator.py           # Hallucination detection (Auditor)
├── agent.py               # LlamaIndex agent orchestration
├── test/
│   ├── test_agent.py
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not committed)
└── README.md              
```

---

## Prompt Engineering Strategy

**Decision**: Separate, focused prompts for each stage (Router → Classifier → Agent).

**Rationale**:
- **Clarity**: Each prompt has a single, well-defined purpose
- **Reusability**: Prompts can be tested and versioned independently
- **Maintainability**: Easy to adjust rules without touching code

**Prompts**:
- `SYSTEM_PROMPT`: Defines TECH/NON_TECH classification rules
- `CLASSIFIER_PROMPT`: Pairs system instructions with user template
- `AGENT_SYSTEM_PROMPT`: Describes tool usage for agent

---
## How to Run the Pipeline

### Run All Tests

To execute the test suite:

```bash
cd J-Assignment-AI
python -m test.test_agent
```

This runs all tests to verify that the pipeline (Router → Classifier → Extractor → Auditor).

---

### Process a Single Resume

You can process a single resume string using `process_resume`:

```python
import asyncio
from agent import process_resume

resume_text = """
[Name] | [Recent Position]. 4+ years of experience in full-stack dev.
Specialized in Python, LlamaIndex, and building RAG agents.
Implemented DeepEval for hallucination tracking.
Deployed systems on AWS EC2.
Contact: hello@example.com
"""

resume_result = asyncio.run(process_resume(resume_text=resume_text))
print(resume_result)
```

**Expected Extraction:**

```
### Summary of Findings:
- **Classification**: The resume belongs to a **Technical Role** with a confidence score of 1.0.
- **Contact Information**: Email: hello@example.com
- **Technical Skills**: Python, LlamaIndex, RAG agents, DeepEval, AWS EC2
- **Summary**: The individual is an experienced full-stack developer specialized in Python, LlamaIndex, and building RAG agents. They have implemented DeepEval for hallucination tracking and deployed systems on AWS EC2.

### Detailed Evaluation:
- **Faithfulness**: The resume is faithful with a score of 1.0.

The resume has been analyzed successfully. If you have any specific questions or need further details, feel free to ask!
```

---

### Process Resume with a Query

You can also run a query on a candidate's resume:

```python
import asyncio
from agent import process_resume_with_query

resume_text = """
[Name] | [Recent Position]. 4+ years of experience in full-stack dev.
Specialized in Python, LlamaIndex, and building RAG agents.
Implemented DeepEval for hallucination tracking.
Deployed systems on AWS EC2.
Contact: hello@example.com
"""

query = "Show me Python developers with experience in RAG systems."

query_result = asyncio.run(
    process_resume_with_query(resume_text=resume_text, query=query)
)
print(query_result)
```

---

**Expected Extraction:**

```
### Summary of Findings:
- The resume is valid and faithful with a high faithfulness score of 1.0.
- The candidate is an experienced full-stack developer with expertise in Python, LlamaIndex, and building RAG agents. They have also implemented DeepEval for hallucination tracking and deployed systems on AWS EC2.      
- Contact information: hello@example.com

### Resume Analysis:
- **Role Type:** Technical
- **Years of Experience:** Not provided
- **Technical Skills:** Python, LlamaIndex, RAG agents, DeepEval, AWS EC2
- **Summary:** Experienced full-stack developer specialized in Python, LlamaIndex, and building RAG agents. Implemented DeepEval for hallucination tracking.

### Query Response:
- The resume matches the query for Python developers with experience in RAG systems.

The candidate in the resume has the required experience in Python and RAG systems as per the query.
```
