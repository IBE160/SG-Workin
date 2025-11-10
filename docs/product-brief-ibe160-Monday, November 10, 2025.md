# Product Brief: ibe160

**Date:** Monday, November 10, 2025
**Author:** BIP
**Status:** Draft for PM Review

---

## Executive Summary

This project proposes the development of an AI-powered chatbot designed to revolutionize how prospective and current university students access information about study programs. The primary problem addressed is the significant frustration experienced by students due to the university website's poor organization and search functionality, leading to potential loss of enrollment and overwhelming staff with repetitive inquiries.

The chatbot's core value proposition lies in its ability to provide quick, accurate, and interactively guided information, synthesizing data from multiple sources on the university website. This will empower students to find the information they need efficiently, reducing their frustration and enhancing their decision-making process, while simultaneously freeing up valuable staff time. The project, a school initiative focused on AI programming, is constrained by a 3-week timeline and a free-tier-only budget, targeting a latent need for a more effective information retrieval system within the university community.

---

## Problem Statement

Prospective and current university students struggle to find clear and accessible information about study programs due to the university website's poor organization. This difficulty leads to significant frustration and can result in prospective students abandoning their applications in favor of other universities, while current students may experience a decline in motivation.

Consequently, university staff spend 3-4 hours per week answering repetitive questions that should be easily self-serviced, diverting their time from more complex student support tasks. The existing website, as the primary information source, fails to meet user needs, creating a negative experience and potential loss of student enrollment.

This project aims to address these issues within a 3-week timeframe to deliver a functional solution as part of a school project.

---

## Proposed Solution

We propose the development of an AI-powered chatbot, accessible with a single click from the university website, to serve as the primary, user-friendly interface for all study program-related inquiries.

**Core Approach:**
The chatbot's essential function is to provide immediate, accurate answers to student questions, supplemented with links to the original source material on the university website and optional "more information" links for deeper exploration.

**Ideal User Experience:**
The experience is designed to be effortless and intuitive. Students will be greeted with a simple interface that encourages them to ask questions. The chatbot will provide quick, direct answers and engage in a conversational manner, asking clarifying follow-up questions to ensure it fully understands the user's intent. If a query is beyond its scope, it will seamlessly direct the user to the university's contact page. The goal is for every user to leave the interaction feeling positive, well-informed, and confident in the information they received.

**Key Differentiators:**
This solution surpasses a simple website search or FAQ page through two key differentiators:
1.  **Interactive Guidance:** The chatbot actively guides users by asking questions to refine their queries, ensuring they find the correct information even if they don't know what to search for.
2.  **Information Synthesis:** It can instantly gather and synthesize information from multiple, disparate pages on the university website, presenting a single, consolidated answer that would otherwise require significant manual effort from the user.

**Why It Will Succeed:**
The chatbot's success will be driven by its sheer effectiveness. It addresses a significant, albeit latent, need among students for a more efficient and reliable way to access information. By providing a superior user experience and tangible time savings for both students and staff, it will quickly become an indispensable tool for the university community.

---

## Target Users

### Primary User Segment

#### Primary User Segment 1: Prospective Students

*   **Profile:** Typical high school graduates who are generally tech-savvy and in the process of exploring higher education options.
*   **Goals:** To discover and evaluate potential study programs, including understanding options for extra courses, specializations, and program expansions. Their primary goal is to gather enough information to make an informed decision about which university and program to apply for.
*   **Current Problem-Solving Methods:** They primarily rely on the university website and its search functionality to find this information.
*   **Specific Pain Points:** They experience significant frustration due to the website's poor organization and complex navigation. This difficulty in finding clear, consolidated information can lead them to abandon their research and consider other universities.

### Secondary User Segment

#### Primary User Segment 2: Current Students

*   **Profile:** Enrolled students from all years of study (first-year to final-year) who are actively managing their academic journey.
*   **Goals:** To find accurate information about available courses and their prerequisites to plan their semesters, ensure they meet degree requirements, and explore potential areas of interest.
*   **Current Problem-Solving Methods:** They use a combination of the university website and academic advisors.
*   **Specific Pain Points:**
    *   **Website:** They are hindered by poor search functionality and complex navigation, making it difficult to find specific course details and prerequisite information.
    *   **Academic Advisors:** They find that advisors are often overwhelmed with basic, repetitive questions, which can lead to delays in getting help and reduces the advisors' availability for more complex, personalized guidance.

---

## Goals and Success Metrics

### Business Objectives

*   **Learning AI Programming:** The primary objective for this school project is to provide a practical application for learning and implementing AI programming concepts.
*   **Demonstrate Chatbot Effectiveness:** To successfully build and deploy a functional chatbot that addresses a real-world problem within the university context.

### User Success Metrics

*   **User Satisfaction:** Measured by a 1-10 satisfaction scale presented at the end of each chatbot conversation, with an optional text field for qualitative feedback. A target average score of 7/10 or higher indicates success.

### Key Performance Indicators (KPIs)

*   **User Satisfaction Score:** Average score from the 1-10 satisfaction scale.
*   **Conversation Completion Rate:** Percentage of conversations where users indicate their query was resolved.
*   **Escalation Rate:** Frequency at which users are directed to the university contact page.

---

## Strategic Alignment and Financial Impact

### Financial Impact

The project will be developed exclusively using free-tier services for all technologies, including the language model (e.g., Google Gemini 2.5 Pro), hosting (e.g., Vercel), and database (e.g., Supabase). This ensures that the development and initial deployment of the chatbot will incur no direct financial cost. The primary investment will be the development time and effort within the 3-week project timeline.

### Company Objectives Alignment

While this is a school project, the chatbot aligns with broader university objectives by:
*   **Improving Student Experience:** Enhancing access to critical information for both prospective and current students.
*   **Operational Efficiency:** Potentially reducing the administrative burden on staff by automating responses to common inquiries.
*   **Innovation:** Demonstrating the university's commitment to leveraging modern AI technologies to support its community.

### Strategic Initiatives

This project supports strategic initiatives focused on:
*   **Digital Transformation:** Modernizing student support services through AI.
*   **Student Success:** Providing tools that help students navigate their academic journey more effectively.
*   **Resource Optimization:** Reallocating staff time from repetitive tasks to more impactful student engagement.

---

## MVP Scope

### Core Features (Must Have)

*   **Basic Q&A for Study Programs:** The chatbot must be able to provide quick, direct, and accurate answers to common questions about university study programs.
*   **Suggesting Study Paths:** Ability to guide students in exploring long-term study options and potential academic routes.
*   **Suggesting Program Combinations:** Functionality to assist students in understanding how different fields of study or programs can be combined.
*   **Information Sourcing & Referencing:** All answers must include links to "more information" and explicitly cite the source URL(s) from the university website.
*   **Interactive Guidance:** The chatbot will proactively ask clarifying questions to guide users towards the correct information, especially when initial queries are ambiguous.
*   **Information Synthesis:** Capability to combine and summarize relevant information from multiple pages on the university website to provide comprehensive answers.
*   **One-Click Access:** The chatbot must be easily accessible via a single click from the university's main website.
*   **Escalation to Contact:** If the chatbot cannot answer a question, it must provide a direct link to the university's contact page.
*   **User Satisfaction Feedback:** Implement a 1-10 satisfaction scale at the end of each conversation, with an optional text field for user comments.

### Out of Scope for MVP

*   **Email Conversation Log:** The ability for users to receive a transcript of their chat via email.
*   **Forward Log on Escalation:** Automatically sending chat history to staff upon escalation.
*   **Multilingual Support:** Initial launch will focus on a single language (e.g., English).
*   **Daily Automated Website Scraping:** Initial knowledge base updates may be manual or less frequent; automated daily scraping will be a future enhancement.

### MVP Success Criteria

*   **High User Satisfaction:** Achieve an average user satisfaction score of 7/10 or higher on the in-chat feedback mechanism.
*   **Effective Information Retrieval:** The chatbot successfully answers a high percentage of user queries related to study programs, study paths, and program combinations.
*   **Positive User Experience:** Students report feeling informed, confident, and positive after using the chatbot, indicating that their information needs were met efficiently.
*   **Accessibility:** The chatbot is seamlessly integrated and easily launched from the university website.

---

## Post-MVP Vision

### Phase 2 Features

*   **Automated Daily Website Scraping:** Implement automated processes for daily updates to the chatbot's knowledge base from the university website.
*   **Multilingual Support:** Expand chatbot capabilities to support multiple languages to cater to a diverse student body.
*   **Email Conversation Log:** Allow users to receive a transcript of their chat via email for future reference.
*   **Forward Log on Escalation:** Implement functionality to automatically forward chat history to relevant staff members when a query is escalated.

### Long-term Vision

The long-term vision for the chatbot is to evolve into a comprehensive, intelligent assistant that supports students throughout their entire academic journey, from initial inquiry to graduation. This includes expanding its knowledge domain beyond study programs to encompass student services, campus life, and academic support. The chatbot could also integrate with university systems to provide personalized information (e.g., course schedules, financial aid status) while maintaining strict privacy and security protocols. Ultimately, it aims to be a central hub for student information, significantly enhancing the overall student experience and operational efficiency of the university.

### Expansion Opportunities

*   **Personalized Information:** Integration with student information systems to provide personalized data (e.g., course schedules, grades, financial aid status) securely.
*   **Broader Knowledge Domains:** Expanding the chatbot's knowledge base to include FAQs on admissions, financial aid, student housing, career services, and campus events.
*   **Proactive Support:** Developing features for proactive outreach, such as sending reminders for deadlines or suggesting relevant resources based on student profiles.
*   **Integration with Other Platforms:** Embedding the chatbot into other university platforms like the student portal, learning management systems, or mobile applications.
*   **Voice Interface:** Exploring the development of a voice-activated interface for hands-free interaction.

---

## Technical Considerations

### Platform Requirements

*   **Deployment:** The chatbot will be publicly available without user authentication.
*   **Accessibility:** Must adhere to accessibility standards.
*   **Responsiveness:** The user interface must be mobile-responsive to ensure usability across various devices.
*   **Integration:** Designed for easy integration into the university's existing website infrastructure.

### Technology Preferences

*   **Frontend:**
    *   **Framework:** Next.js 14+ (for performance, developer experience, and SEO capabilities).
    *   **Language:** TypeScript (for type safety, readability, and maintainability).
    *   **Styling:** Tailwind CSS (for rapid UI development, customizability, and consistency).
    *   **UI Components:** Shadcn UI (for customizable, accessible, and dependency-minimal components).
*   **Backend:**
    *   **Framework:** FastAPI (Python) (for high performance, automatic documentation, and AI/ML suitability).
    *   **Database:** Supabase (PostgreSQL with `pgvector`) (for unified relational and vector data storage, efficient RAG, and scalability).
    *   **ORM:** SQLAlchemy (for type-safe and flexible database interactions).
    *   **Large Language Model (LLM):** Google Gemini 2.5 Pro (for advanced RAG capabilities, accurate responses, and potential multimodality).

### Architecture Considerations

*   **Retrieval-Augmented Generation (RAG):** The core architecture will leverage RAG, combining the LLM with a vector database for efficient and accurate information retrieval from the university's knowledge base.
*   **Type Safety:** End-to-end type safety will be maintained across the stack (TypeScript, Pydantic in FastAPI, SQLAlchemy).
*   **Scalability:** All chosen components are designed for scalability to handle increasing user loads and data volumes.
*   **Knowledge Base Updates:** The system should support easy and efficient updates to the knowledge base.

---

## Constraints and Assumptions

### Constraints

*   **Timeline:** The project must be completed within a strict 3-week timeframe due to it being a school project.
*   **Budget:** The project is limited to using only the free tiers of all selected technologies and services, with no budget for paid resources.

### Key Assumptions

*   **User Adoption:** We assume that both prospective and current students will be willing to use the chatbot and will find it a preferable alternative to navigating the website or contacting staff.
*   **Technical Feasibility:** We assume that the chosen technology stack (Next.js, FastAPI, Supabase, Gemini 2.5 Pro) can be successfully integrated and will perform adequately within the limitations of their respective free tiers.
*   **Data Availability and Quality:** We assume that the university website contains all the necessary information for the chatbot's knowledge base and that this information is accessible and structured in a way that allows for effective scraping and processing.

---

## Risks and Open Questions

### Key Risks

*   **Scope Creep:** Given the 3-week timeline, there is a risk of expanding the project scope beyond the MVP, which could jeopardize timely completion.
*   **Data Quality/Accessibility:** The effectiveness of the RAG system heavily relies on the quality and accessibility of information on the university website. Poorly structured or inconsistent data could impact chatbot accuracy.
*   **Free-Tier Limitations:** Reliance on free-tier services might introduce performance bottlenecks, usage limits, or feature restrictions that could impact the chatbot's functionality or scalability.
*   **LLM Performance:** The Google Gemini 2.5 Pro model's performance in understanding and generating relevant responses for specific university-related queries needs continuous evaluation.
*   **User Adoption/Acceptance:** Despite the perceived need, there's a risk that students may not fully adopt the chatbot, or may have negative perceptions if initial interactions are not seamless.

### Open Questions

*   **Specific Data Sources:** Which exact sections or pages of the university website will serve as the primary knowledge base for the chatbot?
*   **Knowledge Base Update Frequency:** How often will the knowledge base need to be updated to reflect changes on the university website, especially during the MVP phase?
*   **Integration Mechanism:** What is the precise technical mechanism for integrating the chatbot into the university's existing website (e.g., iframe, widget, direct embed)?
*   **Performance Benchmarks:** What are the specific performance benchmarks (e.g., response time, accuracy rate) that the MVP should aim to achieve?

### Areas Needing Further Research

*   **Optimal Prompt Engineering:** Further research into prompt engineering techniques for Google Gemini 2.5 Pro to maximize accuracy and relevance for university-specific queries.
*   **Vector Database Optimization:** Investigate optimal chunking strategies and embedding models for the `pgvector` database to enhance retrieval performance.
*   **User Interface Best Practices:** Research best practices for chatbot UI/UX design to ensure an intuitive and engaging user experience.
*   **Scalability Testing (Free Tier):** Conduct thorough testing to understand the true limits and potential bottlenecks of the chosen free-tier services under anticipated load.

---

## Appendices

### A. Research Summary

*   **Brainstorming Session (November 6, 2025):** Focused on generating ideas for a university AI chatbot for study program information. Key principles established were simplicity, focus on study programs, general advice, and using the official website as a single source of truth. Top priorities identified were basic Q&A for study programs, suggesting study paths, and suggesting program combinations.
*   **Technical Research Report (November 7, 2025):** Validated a robust technology stack for a RAG-based chatbot, including Next.js 14+, TypeScript, Tailwind CSS, Shadcn UI for the frontend, and FastAPI, Supabase (PostgreSQL with `pgvector`), SQLAlchemy, and Google Gemini 2.5 Pro for the backend. The report confirmed the stack's suitability for performance, scalability, maintainability, and AI integration, emphasizing end-to-end type safety and cost-effectiveness through free-tier usage.

### B. Stakeholder Input

*   **User (BIP):** Provided critical insights into student and staff frustrations, defined the ideal user experience (one-click access, quick direct answers, follow-up questions, positive feeling), clarified the core approach (accurate info with source links), identified key differentiators (interactive guidance, information synthesis), and confirmed the project's focus on AI programming learning within a 3-week, free-tier constraint.

### C. References

*   `brainstorming-session-results-Thursday, November 6, 2025.md`
*   `research-technical-fredag 7. november 2025.md`

---

_This Product Brief serves as the foundational input for Product Requirements Document (PRD) creation._

_Next Steps: Handoff to Product Manager for PRD development using the `workflow prd` command._
