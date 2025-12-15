from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ibe160-chatbot"
    ALLOWED_ORIGINS: str = "*"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str  # Anon key for client-side
    SUPABASE_SERVICE_ROLE_KEY: str # For backend admin operations
    DATABASE_URL: str # Postgres connection string for SQLAlchemy
    GOOGLE_API_KEY: str # For Google Gemini AI
    
    # RAG Configuration
    GEMINI_MODEL: str = "models/gemini-flash-latest" # Stable flash alias
    
    RAG_SYSTEM_PROMPT: str = """You are a helpful assistant for the University of Molde (HiMolde).
Use the following context to answer the user's question. The context may contain multiple snippets from different pages.
Synthesize the information from these snippets into a single, coherent, and comprehensive answer.
Do not simply list the snippets; combine the facts to provide a smooth reading experience.
If the answer is not in the context, say you don't know and provide the university contact link: https://www.himolde.no/om/kontakt/

Context:
{context_text}

User Query: {query}
"""

    AMBIGUITY_SYSTEM_PROMPT: str = """You are a helpful assistant for University of Molde. Your job is to determine if a student's query is specific enough to search for a definitive answer or if it is too broad/ambiguous.

Query: "{query}"

If the query is specific (e.g., "What are the admission requirements for Nursing?", "Who is the dean of Logistics?"), output JSON: {{"is_ambiguous": false}}

If the query is ambiguous (e.g., "Tell me about studies", "business", "nursing", "courses"), output JSON: {{"is_ambiguous": true, "clarifying_question": "..."}}

Ensure the clarifying question is polite and helps narrow down their intent (e.g. asking for specific degree level or program).
Output ONLY valid JSON.
"""

    ESCALATION_LINK: str = "https://www.himolde.no/om/kontakt/"

    CONTEXTUALIZE_SYSTEM_PROMPT: str = """You are a helpful assistant for University of Molde.
Your task is to rewrite the user's latest query to be self-contained, based on the conversation history.
The user might ask a follow-up question that depends on previous context.
Rewrite the query so that it can be understood without the history.

History:
{history}

Latest Query: "{query}"

Rewritten Query:"""

    class Config:
        env_file = ".env"

settings = Settings()
