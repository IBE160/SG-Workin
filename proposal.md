## Case Title
FAQ Chatbot for a University Website

## Background
University websites often contain a large amount of information that can be difficult for visitors to navigate. Students, applicants, and staff frequently have recurring questions about admissions, programs, deadlines, and services. A chatbot can automate responses, providing instant and consistent answers, while reducing the workload on administrative staff.

## Purpose
The purpose of this application is to create an AI-powered FAQ chatbot that helps users quickly find accurate information from the university’s website. It will answer questions related to studies, admission, facilities, and contact information, improving accessibility and user experience.

## Target Users
- Prospective students seeking program and admission information  
- Current students looking for academic or administrative details  
- Visitors and staff needing general university information  

## Core Functionality

### Must Have (MVP)
- **Feature 1:** Retrieval-based answering system that provides accurate responses from a public knowledge base (university website content).  
- **Feature 2:** Source references and relevant links included in chatbot answers.  
- **Feature 3:** Open access for all users, without authentication or login.  

### Nice to Have (Optional Extensions)
- **Feature 4:** Contextual conversation memory for smoother follow-up questions.  
- **Feature 5:** Multilingual support for international visitors.  
- **Feature 6:** Interactive follow-up suggestions after each response to guide users toward related topics.
- **Feature 7:** Accessibility features such as screen reader compatibility, text-to-speech support, and high-contrast mode to ensure universal access for all users.  

## Data Requirements
- **Data entity 1:** Knowledge Base – course descriptions, admission info, contact details, deadlines, FAQs.  
- **Data entity 2:** Metadata – page titles, categories, and keywords for improved retrieval accuracy.  
- **Data entity 3:** User Queries – anonymized logs of user questions and chatbot responses for analysis and improvement.  

## User Stories (Optional)
1. As a **prospective student**, I want to ask questions about study programs so that I can find the right degree for me.  
2. As a **current student**, I want to get information about deadlines and exams so that I can plan my studies efficiently.  
3. As a **visitor**, I want to ask for directions or contact details so that I can reach the correct department easily.  

## Technical Constraints
- Must be publicly available without user authentication.  
- Must be mobile-responsive and easy to integrate into the university’s website.  
- Should handle uncertain or ambiguous queries with fallback strategies.  
- Should allow for easy updates when website information changes.  

## Success Criteria
- **Criterion 1:** Users receive accurate and relevant answers within seconds.  
- **Criterion 2:** Responses include links or references to official university pages.  
- **Criterion 3:** Chatbot maintains consistent performance across devices.  
- **Criterion 4:** User satisfaction (measured through feedback or survey) exceeds 80%.  
- **Criterion 5:** The chatbot reduces repetitive inquiries to the university’s support staff.


## User Flows

### Flow 1: Enter site ask questions about study program
**Entry point:**  


| Step | User Action | Bot Response / System Action | Branch / Condition |
|------|-------------|------------------------------|--------------------|
| **0** | User lands on website  → clicks **“Ask EduBot”** chat bubble | Bot opens with greeting:<br>**“Hello! I'm EduBot, your guide to our study programs. What would you like to know about Computer Science (or another program)?”**<br>Quick replies: [Admissions] [Curriculum] [Fees] [Start chat] | — |
| **1** | User types initial question (e.g., “What are the entry requirements for Computer Science?”) | **RAG Process:**<br>- Embed query → Retrieve top-3 chunks from KB (e.g., admissions PDF).<br>- Augment LLM prompt with retrieved context.<br>- Generate response: **“For our BSc Computer Science, you'll need a high school diploma with 70% in Math & Science, plus English proficiency (IELTS 6.5). International students get fee waivers—want details?”**<br>Source citation: [Admissions Guide, p. 5] | → **2** (always, for conversation) |
| **1A** | User selects quick reply (e.g., [Curriculum]) | **RAG Process:**<br>- Retrieve from syllabus KB.<br>- Response: **“The curriculum covers Algorithms, AI, and Web Dev over 3 years. Core modules: Year 1 - Programming Basics (30 credits). See full outline?”**<br>Attaches structured card (e.g., module list). | → **2** |
| **1B** | Unrecognized intent / off-topic (e.g., “Weather today?”) | Fallback: **“I'm specialized in study programs—try asking about admissions or courses. Or rephrase?”**<br>Loops to quick replies. | Loop to **1** until relevant |
| **2** | User asks follow-up (e.g., “What about international fee waivers?”) | **RAG Process (Context-Aware):**<br>- Embed query + conversation history (prior context on CS admissions).<br>- Retrieve updated chunks (e.g., fees section, filtered by “international”).<br>- Generate: **“International students pay $15,000/year (vs. $20,000 domestic), with 20% waivers for top applicants. Apply by March 1—need application tips?”**<br>Cites source: [Fees Policy 2025, Sec. 3] | → **3** or loop to **2** |
| **2A** | Follow-up builds on prior (e.g., “More on AI module?” after curriculum) | **RAG Process:**<br>- History-aware retrieval (prioritizes AI-related chunks).<br>- Response: **“The AI module (Year 2) includes Machine Learning and Ethics, taught by Dr. Lee. Prerequisites: Programming Basics. Syllabus PDF available—download?”**<br>Attaches link/PDF snippet. | Loop to **2** for multi-turn |
| **2B** | Shift topic slightly (e.g., “Compare to Data Science program?”) | **RAG Process:**<br>- Retrieve comparative chunks (e.g., program overviews).<br>- Response: **“CS focuses on software engineering; Data Science emphasizes stats & big data (80% overlap). Both share Year 1 core—switch possible after Semester 1.”**<br>Offers: [Side-by-side table] | → **2** (continue) |
| **3** | User satisfied (e.g., “That's all, thanks!”) or idles >2min | Bot: **“Great chatting! If you have more questions, I'm here 24/7. Apply now? [Apply Link]”**<br>Session summary emailed (opt-in). | End session |
| **4** | User not satisfied (e.g., “need more info”) | Bot:  **“sorry couldnt answer all your questions,  I will forward your message to a academic advisor”**<br>Forward chat log to academic advisor.<br>Session summary emailed (opt-in) | End session |
| **End** | User closes chat (X) or says “bye” | Bot: **“Thanks for inquiring! Best of luck with your studies.”**<br>Logs session for analytics (query success, retrieval relevance). | Session closed; KB update if needed |



### Flow 2: Administrator user flow, Administrator enter site, list, add or modify URL for crawl/scrape/search, or to add Administrator users.

| Step | User Action | System Action | Branch / Condition |
|------|-------------|------------------------------|--------------------|
| **0** | Administrator open admin url of website  →  **“Login”** | Admin page opens opens with a list of already scraped url with time stamp of last scrape, status /error messages and the possibility to update, delete or exclude(Pause) selected url's, or to add a new url through a field. The option for new url should be on top of the page. There should also be a link to a page to add new administrator users | → **1** **2** **3** **4** **5** |
| **1** | Administrator **add new url:** (Admin type or paste a url into the add url field, cliks button for "add url")	 |System add the url to the database and crawl/scrape/search, when finished updates time stamp.| → **0** |
| **2** | Administrator **update url:** (Admin click button for "update url")	 |System crawl/scrape/search the given url, when finished updates time stamp.| → **0** |
| **3** | Administrator **delete url:** (Admin click button for "delete url")	 |System delete the given url from database.| → **0** |
| **4** | Administrator **exclude url:** (Admin click button for "exclude url")	 |System marks the given url in the database for exclusion.| → **0** |
| **5** | Administrator **Manage administrator users:** (Admin click button to "Manage administrators")	 |System open new page to manage Administrator, list all administrators with the possibility to add new administrator (Admin Click button for "add admin"), or "Delete" or "reset password" for existing administrators.| → **5A** **5B** **5C** |
| **5A** | Administrator **Add administrator users:** (Admin click button to "Add administrator users")	 |System open new page to add a new Administrator, 2 fields for new administrator: username and e-mail(must be filled) New Administrator added to database| → **5** |
| **5B** | Administrator **Delete:** (Admin click button for "Delete administrator")|System delete the given Administrator user.| → **5** |
| **5C** | Administrator **Delete:** (Admin click button for "reset password")|System send email to given Administrator user to reset password.| → **5** |
| **End** | Administrator **"logs out:** | | Session closed |


## Technical Specifications

### Frontend Specification
- **Framework**: Next.js 14+ with App Router for server-side rendering and optimal performance
- **Language**: TypeScript for type safety and better AI-assisted development
- **Styling**: Tailwind CSS for rapid, responsive UI development
- **Shadcn UI**: Shadcn UI for rapid, responsive UI development
- **Forms**: React Hook Form with Zod validation for robust form handling
- **API Communication**: Axios with interceptors for authenticated requests
- **Deployment**: Vercel for frontend hosting with automatic CI/CD

**Architecture Pattern**: Component-based architecture with clear separation between presentation components, container components, and business logic hooks.

### Backend Specification
- **Framework**: FastAPI (Python) for high-performance RESTful API development
- **Language**: Python for AI integration compatibility and rapid development
- **Database**: Supabase (PostgreSQL) for managed database, real-time capabilities and vectordatabase(pgvector)
- **Authentication**: Supabase Auth for Administrator users management, JWT tokens, and email verification
- **Authorization**: Row Level Security (RLS) policies in Supabase + role-based middleware (user/admin roles)
- **ORM**: SQLAlchemy for database operations and type safety
- **Database Migrations**: Alembic for version-controlled schema changes
- **AI Integration**:
  - GOOGLE Gemini 2.5 Pro for chat
  - Custom prompt engineering for consistent AI behavior
  - Fallback logic for API failures
- **API Documentation**: FastAPI automatic OpenAPI/Swagger documentation
- **Testing**: Pytest for unit and integration tests
- **Build Tool**: UV for fast Python package management
- **Deployment**: Vercel (FastAPI supports Vercel deployment)

**API Architecture**: RESTful API design with versioning (/api/v1/) and clear resource-oriented endpoints.


### Database Specification
- **Database Type**: Supabase (PostgreSQL-based relational database and Vector database)
- **ORM**: SQLAlchemy for Python-based type-safe database access
- **Migrations**: Alembic for database schema version control
- **Hosting**: Supabase managed cloud (includes automatic backups, scaling, and monitoring)

**Schema Design**:
- **Normalized relational schema** with proper foreign key constraints
- **Indexes** on frequently queried fields
- **Supabase Auth integration**: Users table managed by Supabase Auth with extended profile data
- **Vector embeddings**: to enable similarity search and contextual retrieval
- **Timestamps**: for versioning and updates.


### AI Integration Specification
**AI Use Cases**:
1. **AI chatBot**: Answer, and ask concise relevant follow up questions to deepen understanding, clarify ambiguities, or explore related aspects of the question from the user. should be relevant to the indexed url's (data in the vectordatabase.)

**Implementation**:
- **Model**: Gemini 2.5 pro/flash
- **Prompt Design**:
  - User ask question about study program.
  - The backend get relevant data from the vector database and includes this information in the answers and possible follow-up questions.
  - If the user ask question not relevant to the indexed data, remind the user of the intention of this chatbot and suggest alternative questions. 
 
- **Rate Limiting**: Implement request queuing and caching for cost optimization
- **Fallback**: Explanatory error message if API fails
- **Cost Management**: Budget monitoring and usage alerts

**API Integration Architecture**:
- Separate service layer for AI calls
- Retry logic with exponential backoff
- Response validation and sanitization
- Caching for repeated similar scenarios

### Platform Type
**Primary Platform**: Web application (browser-based)

**Target Devices**:
- Desktop computers (primary): Windows, macOS, Linux
- Laptops (primary): All operating systems
- Tablets (secondary): iPad, Android tablets (landscape orientation recommended)
- Mobile phones (future): iOS and Android via responsive design or dedicated apps

**Browser Compatibility**:
- Chrome 90+ (primary testing target)
- Firefox 88+
- Safari 14+
- Edge 90+

**Responsive Breakpoints**:
- Desktop: 1280px+ (optimal experience)
- Laptop: 1024px-1279px (full features)
- Tablet: 768px-1023px (adapted layout)
- Mobile: 375px-767px (future phase - simplified UI)

### Admin User Authentication Specification
**Authentication Method**: Supabase Auth with JWT-based authentication

**Features**:
- Email/password registration with built-in validation
- Automatic email verification via Supabase Auth email templates
- Secure password reset flow with magic links
- Session management with automatic refresh token rotation
- "Remember me" functionality via Supabase persistent sessions
- Account lockout and rate limiting built into Supabase Auth
- User metadata storage for roles (user/admin)

**Implementation Details**:
- Passwords automatically hashed by Supabase (bcrypt)
- JWT access tokens managed by Supabase (automatic expiry and refresh)
- Refresh tokens securely stored by Supabase (httpOnly cookies)
- Role-based access control via Supabase user metadata + RLS policies
- OAuth 2.0 support built-in (Google, Microsoft, GitHub) - can enable with configuration

**Supabase Auth Benefits**:
- Built-in security best practices (password hashing, token management)
- Automatic rate limiting on authentication endpoints
- CAPTCHA support for bot prevention
- Multi-factor authentication (MFA) support available
- Email templates customizable for branding
- User management dashboard in Supabase console

**Security Measures**:
- HTTPS enforced by Supabase and Vercel
- CSRF protection on authentication forms
- Email verification required before full account access
- Password strength requirements configurable in Supabase
- Row Level Security (RLS) policies enforce data access control
- Supabase API keys separated (public anon key vs. service role key)

