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
- **Database**: Supabase (PostgreSQL) for managed database and real-time capabilities
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
- **Database Type**: Supabase (PostgreSQL-based relational database)
- **ORM**: SQLAlchemy for Python-based type-safe database access
- **Migrations**: Alembic for database schema version control
- **Hosting**: Supabase managed cloud (includes automatic backups, scaling, and monitoring)

**Schema Design**:
- **Normalized relational schema** with proper foreign key constraints
- **Row Level Security (RLS)**: Supabase RLS policies to ensure users only access their own data
- **Indexes** on frequently queried fields (user_id, game_id, session_id, class_id)
- **JSON/JSONB columns** for flexible configuration storage (game_config, questions, metrics)
- **Partitioning** for game_rounds table if data volume grows (future optimization)
- **Soft deletes** for user data (GDPR compliance)
- **Supabase Auth integration**: Users table managed by Supabase Auth with extended profile data

**Supabase-Specific Features**:
- **Real-time subscriptions**: Frontend can subscribe to game_rounds and player_states changes for live updates
- **RLS Policies**: Students can only view their own games; teachers can view their class games

### AI Integration Specification
**AI Use Cases**:
1. **AI Players**: Generate ordering decisions for AI-controlled supply chain positions
2. **Question Generation**: Create contextual multiple-choice questions based on game events
3. **Feedback Generation**: Provide personalized feedback on student performance
4. **Performance Analysis**: Generate insights about decision patterns and strategy effectiveness

**Implementation**:
- **Model**: Gemini 2.5 pro/flash
- **Prompt Design**:
  - AI players receive game rules, current state, and role context
  - Question generator receives game transcript and specific events
  - Few-shot examples for consistent output format
- **Rate Limiting**: Implement request queuing and caching for cost optimization
- **Fallback**: Rule-based AI for critical game functions if API fails
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

### User Authentication Specification
**Authentication Method**: Supabase Auth with JWT-based authentication

**Features**:
- Email/password registration with built-in validation
- Automatic email verification via Supabase Auth email templates
- Secure password reset flow with magic links
- Session management with automatic refresh token rotation
- "Remember me" functionality via Supabase persistent sessions
- Account lockout and rate limiting built into Supabase Auth
- User metadata storage for roles (student/teacher/admin)

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
