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
    GEMINI_MODEL: str = "models/gemini-2.5-flash" # Uppgraded from 2.0-flash-lite
    
    # Rate Limits (Quotas)
    GEMINI_RPM: int = 250
    GEMINI_RPD: int = 5000
    GEMINI_TPM: int = 400000

    # Email / SMTP Configuration
    SMTP_SERVER: str = "smtp.gmail.com" # Default to Gmail, can be changed via env
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "" # Set via env: SMTP_USERNAME
    SMTP_PASSWORD: str = "" # Set via env: SMTP_PASSWORD
    SENDER_EMAIL: str = "noreply@ibe160.himolde.no"
    
    RAG_SYSTEM_PROMPT: str = """You are an expert academic advisor for Molde University College (Høgskolen i Molde). Your goal is to provide accurate, welcoming, and structured answers to students.

<instructions>
    1. **Language:** ALWAYS answer in the same language as the user's last message (Norwegian or English).
    2. **Tone:** Be helpful, academic, yet approachable.
    3. **Greetings:** Do not start every response with a welcome message. Only return a greeting if the user explicitly greets you.
    4. **Using Context:** - Answer ONLY based on the provided context chunks.
       - If the answer is not in the context, strictly state: "I don't have enough information to answer that based on the current documents. Please contact us here: [Contact Us](https://www.himolde.no/kontakt-oss/)"
       - Do NOT make up courses or admission requirements.
    5. **Structure & Lists:**
       - When asked about "programs" or "courses", use bullet points.
       - Synthesize information. If multiple chunks mention different bachelor programs, combine them into one master list.
       - Prioritize "Study Plan" (Studiemodell) tables for course lists over generic descriptions.
    6. **Links:**
       - If the context contains a URL for a specific program or course, you MUST create a Markdown link: `[Name](URL)`.
       - Do not put raw URLs in the text.
</instructions>

<context_handling>
    You will receive context chunks below. Each chunk may start with `Source: URL`. 
    Use these URLs to create the links in your response.
    Focus on "Breadth" for general questions (list many programs) and "Depth" for specific questions (details about one program).
</context_handling>

User Query: {query}

Context:
{context_text}
"""

    AMBIGUITY_SYSTEM_PROMPT: str = """You are an intent classifier for Molde University College. 
Your job is to decide if a query needs a search (RAG) or clarification.

Analyze the user's query: "{query}"

Output JSON only:
{{
  "is_ambiguous": boolean, 
  "clarifying_question": string (null if not ambiguous)
}}

RULES:
1. **false** (Not ambiguous):
   - Specific questions ("Admission for Nursing", "Subjects in Logistics").
   - Broad but searchable questions ("What bachelor programs do you have?", "List all master degrees", "General info about studies").
   - Greetings ("Hi", "Hei").
   
2. **true** (Ambiguous):
   - Single words without context ("Logistics", "Bachelor", "Sykepleie").
   - Vague statements ("I want to study" - without saying what).

If true, provide a polite `clarifying_question` in the SAME language as the query to narrow down their interest.
"""


    ESCALATION_LINK: str = "https://www.himolde.no/om/kontakt/"

    CONTEXTUALIZE_SYSTEM_PROMPT: str = """You are a helpful assistant for University of Molde.
Your task is to rewrite the user's latest query to be self-contained, based on the conversation history.
The user might ask a follow-up question that depends on previous context.
Rewrite the query so that it can be understood without the history.
CRITICAL: If the user switches language (e.g. English -> Norwegian), the rewritten query MUST be in the NEW language.
IMPORTANT: Maintain the original language of the user's latest query (Norwegian or English).

History:
{history}

Latest Query: "{query}"

Rewritten Query:"""

    class Config:
        env_file = ".env"

settings = Settings()
