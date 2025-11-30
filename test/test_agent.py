from agent import run_resume_agent
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tech_resume_1 = """
Michael Rodriguez | Senior Backend Engineer
Experience:
- 7 years building distributed backend systems
- Designed microservices using Python, FastAPI, and Redis
- Developed RAG-based internal documentation assistant using LlamaIndex
- Built event-driven workflows with Kafka
- Deployed scalable apps using Docker + Kubernetes + AWS EKS
Skills:
Python, FastAPI, Redis, Kafka, PostgreSQL, Docker, Kubernetes, AWS, CI/CD
Contact:
Email: michael.rodriguez@example.com
Phone: +1-312-555-9090
"""

tech_resume_2 = """
Priya Sharma | Machine Learning Engineer
Experience:
- 4 years in applied ML research and production ML systems
- Created text-classification pipelines with HuggingFace Transformers
- Implemented RAG search enhanced with Milvus vector DB
- Built monitoring dashboards for hallucination rates using DeepEval
- Automated ML deployment via GitHub Actions and Sagemaker
Skills:
Python, PyTorch, Transformers, ML Ops, AWS Sagemaker, Milvus, LlamaIndex
Contact:
Email: priya.sharma@example.com
Phone: +91-88555-22119
"""

tech_resume_3 = """
David Kim | Full-Stack Developer
Experience:
- 6 years of experience in full-stack engineering
- Built scalable SaaS platforms using React + Django
- Created LLM-driven support bots with RAG + LangChain
- Integrated payment systems and role-based access modules
- Deployed production apps on GCP Cloud Run
Skills:
Django, React, PostgreSQL, GCP, REST APIs, LlamaIndex, Docker
Contact:
Email: david.k@example.com
Phone: +1-702-441-2288
"""  

assignment_resume = """
    [Name] | [Recent Position]. 4+ years of experience in full-stack dev. 
    Specialized in Python, LlamaIndex, and building RAG agents. 
    Implemented DeepEval for hallucination tracking. 
    Deployed systems on AWS EC2. 
    Contact: hello@example.com
"""

pavan_resume = """
Motivated Software Engineer with over 1.8 year of experience at an AI startup, specializing in building end-to-end 
RAG (Retrieval-Augmented Generation) systems and LLM-powered agents. Skilled in Python, Django, and 
LlamaIndex, with experience in developing Prompt Studios, Agent Evaluation frameworks, and Multi-Agent 
Workflows. Proficient in implementing vector databases (Milvus), prompt engineering techniques, and 
integrating MCP servers for database interaction. Passionate about experimenting with emerging AI 
technologies, turning ideas into working prototypes, and delivering scalable, intelligent solutions that enhance 
automation and decision-making. 
"""

non_tech_resume_1 = """
Emily Carter | HR Coordinator
Experience:
- 5 years in HR operations and employee onboarding
- Managed recruitment pipelines for technical and non-technical roles
- Conducted policy training sessions and employee engagement events
- Oversaw payroll coordination and compliance documentation
Skills:
HRIS, Employee Engagement, Recruitment Coordination, Policy Compliance
Contact:
Email: emily.carter@example.com
Phone: +1-555-201-9876
"""

non_tech_resume_2 = """
Daniel Green | Financial Analyst
Experience:
- 6 years analyzing financial models and investment strategies
- Created quarterly forecasting reports and budget planning tools
- Managed portfolios worth $8M+ for corporate clients
- Conducted market risk assessments and competitive analyses
Skills:
Excel, Financial Modeling, Power BI, Risk Analysis, Budgeting
Contact:
Email: daniel.green@example.com
Phone: +1-444-998-2201
"""

non_tech_resume_3 = """
Lisa Brown | Marketing Coordinator
Experience:
- 4 years in digital marketing and brand campaigns
- Managed social media accounts totaling 150K+ audience
- Coordinated cross-channel ad campaigns and product launches
- Analyzed SEO performance and website traffic metrics
Skills:
SEO, Social Media Management, Google Analytics, Copywriting, Branding
Contact:
Email: lisa.brown@example.com
Phone: +1-333-101-4650
"""

invalid_doc_1="""
Title: A Comprehensive Guide to Caring for Your Pet Iguana
Chapters:
1. Understanding Iguana Moods
2. Proper Sunlamp Etiquette
3. Why Your Iguana Judges You (Science)
This guide contains zero information about employment history.
"""

invalid_doc_2="""
Recipe: Grandmas Secret Pancake Formula
Ingredients:
- Flour
- Two Eggs (preferably happy ones)
- A questionable amount of butter
Instructions:
Mix, flip, eat.  
"""

invalid_doc_3="""
Galactic Federation Report
Subject: Alien Mineral Activity on Sector X-92  
Findings:
- The rocks are shiny  
- The researchers are confused  
"""

async def process_resume(resume_text: str) -> str:
    try:
        logger.info("Running Test process_resume agent...")
        response = await run_resume_agent(resume_text=resume_text, query=None)
        return response
    except Exception as e:
        logger.error(f"Failed to process resume: {e}")
        return ""

# Function to process resume with a query
async def process_resume_with_query(resume_text: str, query: str) -> str:
    try:
        logger.info("Running Test process_resume_with_query agent...")
        response = await run_resume_agent(resume_text=resume_text, query=query)
        return response
    except Exception as e:
        logger.error(f"Failed to process resume with query: {e}")
        return ""


resume_text = assignment_resume
query = "Show me Python developers with experience in RAG systems."
#query = "I believe he have 10 years of experience in Python ?"
if __name__ == "__main__":
    '''
    resume_result = asyncio.run(
        process_resume(
            resume_text=resume_text
        )
    )
    print(resume_result)
    '''
    query_result = asyncio.run(
        process_resume_with_query(
            resume_text=resume_text,
            query=query
        )
    )
    print(query_result)
    