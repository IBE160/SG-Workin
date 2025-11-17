# ibe160 - Epic Breakdown

**Author:** BIP
**Date:** 2025-11-17
**Project Level:** method
**Target Scale:** Not specified

---

## Overview

This document provides the complete epic and story breakdown for ibe160, decomposing the requirements from the [PRD](./PRD.md) into implementable stories.

The project is broken down into the following epics:

*   **Epic 1: Foundation & Core Chat:** Establishes the project infrastructure and basic chat functionality.
*   **Epic 2: Knowledge Base & Retrieval:** Focuses on building the RAG pipeline and knowledge base.
*   **Epic 3: Conversational Intelligence & User Experience:** Enhances the chatbot's conversational abilities and user experience.
*   **Epic 4: Deployment & Integration:** Handles deployment, integration with the university website, and NFR testing.

We have successfully broken down the PRD into 4 epics and 16 stories. Each story follows the BDD format with clear acceptance criteria and technical notes. The epics are sequenced to deliver incremental value, with Epic 1 laying the essential foundation.

---

<!-- Repeat for each epic (N = 1, 2, 3...) -->

## Epic 1: Foundation & Core Chat

Establish the foundational infrastructure and deliver the most basic, end-to-end chat functionality.

### Story 1.1: Project Setup & Infrastructure Initialization

As a developer,
I want to set up the project structure and core dependencies,
So that I have a foundation for building the application.

**Acceptance Criteria:**

**Given** a new project,
**When** the setup script is run,
**Then** a new Next.js project is created with TypeScript, Tailwind CSS, and Shadcn UI.
**And** a new FastAPI project is created with SQLAlchemy.
**And** a new Supabase project is created with the `pgvector` extension enabled.
**And** the project is initialized as a Git repository with a main branch.

**Prerequisites:** None

**Technical Notes:** Use `create-next-app`, `poetry new`, `supabase init`.

### Story 1.2: Basic Chat Interface

As a user,
I want to see a basic chat interface,
So that I can interact with the chatbot.

**Acceptance Criteria:**

**Given** the application is running,
**When** I open the application in a browser,
**Then** I see a chat window with a text input field and a "Send" button.
**And** I can type a message into the input field.

**Prerequisites:** Story 1.1

**Technical Notes:** Implement basic Next.js page with input and button.

### Story 1.3: "Hello World" Chat Response

As a user,
I want to receive a simple, hardcoded response from the chatbot,
So that I can confirm the chat functionality is working.

**Acceptance Criteria:**

**Given** I have sent a message to the chatbot,
**When** the chatbot receives the message,
**Then** the chatbot responds with a hardcoded message (e.g., "Hello! I am the university chatbot. How can I help you today?").

**Prerequisites:** Story 1.2

**Technical Notes:** Implement a basic API endpoint in FastAPI that returns a static string.

### Story 1.4: Basic Deployment Pipeline

As a developer,
I want to set up a basic deployment pipeline,
So that I can automatically deploy the application.

**Acceptance Criteria:**

**Given** a new commit is pushed to the main branch,
**When** the deployment pipeline is triggered,
**Then** the application is automatically deployed to a hosting provider (e.g., Vercel).
**And** the deployed application is accessible via a public URL.

**Prerequisites:** Story 1.1, 1.2, 1.3

**Technical Notes:** Configure Vercel for Next.js and FastAPI deployment.

## Epic 2: Knowledge Base & Retrieval

Enable the chatbot to answer questions by retrieving information from the university website.

### Story 2.1: Supabase Vector Database Setup

As a developer,
I want to configure Supabase with `pgvector` for storing document embeddings,
So that the chatbot can perform efficient similarity searches.

**Acceptance Criteria:**

**Given** a Supabase project,
**When** the setup script is run,
**Then** the `pgvector` extension is enabled.
**And** a table is created to store document chunks and their embeddings.

**Prerequisites:** Story 1.1

**Technical Notes:** Supabase dashboard configuration, SQL migration for table creation.

### Story 2.2: University Website Scraper

As a developer,
I want to build a web scraper that extracts content from specified university website URLs,
So that the content can be used to build the chatbot's knowledge base.

**Acceptance Criteria:**

**Given** a list of university website URLs,
**When** the scraper is executed,
**Then** it successfully extracts text content from those URLs.
**And** the extracted content is cleaned and formatted for processing.

**Prerequisites:** Story 1.1

**Technical Notes:** Use Playwright or BeautifulSoup for scraping.

### Story 2.3: Document Chunking and Embedding

As a developer,
I want to process extracted website content by chunking it and generating embeddings using Google Gemini 2.5 Pro,
So that the content can be stored in the vector database for RAG.

**Acceptance Criteria:**

**Given** cleaned text content,
**When** the chunking and embedding process is run,
**Then** the text is divided into appropriate chunks.
**And** each chunk has a corresponding vector embedding generated by Google Gemini 2.5 Pro.
**And** these chunks and embeddings are stored in the Supabase vector database.

**Prerequisites:** Story 2.1, 2.2

**Technical Notes:** Implement Python script for chunking and calling Gemini API for embeddings.

### Story 2.4: Basic RAG Pipeline Integration

As a developer,
I want to integrate the vector database with the FastAPI backend to perform basic RAG,
So that the chatbot can retrieve relevant information based on user queries.

**Acceptance Criteria:**

**Given** a user query,
**When** the FastAPI backend receives the query,
**Then** it performs a similarity search in the vector database.
**And** retrieves the top N most relevant document chunks.
**And** passes these chunks to Google Gemini 2.5 Pro along with the user query to generate a response.

**Prerequisites:** Story 1.3, 2.3

**Technical Notes:** FastAPI endpoint for RAG, Supabase client for vector search, Gemini API for response generation.

## Epic 3: Conversational Intelligence & User Experience

Enhance the chatbot's conversational abilities and user experience.

### Story 3.1: Interactive Guidance Implementation

As a user,
I want the chatbot to ask clarifying questions when my query is ambiguous,
So that I can get more precise answers.

**Acceptance Criteria:**

**Given** I ask an ambiguous question (e.g., "Tell me about business"),
**When** the chatbot detects ambiguity,
**Then** it responds with a clarifying question (e.g., "Are you interested in a specific business degree, or would you like to know about business courses in general?").
**And** my subsequent response is used to refine the search.

**Prerequisites:** Story 2.4

**Technical Notes:** Implement intent detection and response generation logic in FastAPI, leveraging Gemini's conversational capabilities.

### Story 3.2: Information Synthesis & Summarization

As a user,
I want the chatbot to combine and summarize information from multiple sources,
So that I get a comprehensive answer without having to visit many pages.

**Acceptance Criteria:**

**Given** a query requiring information from multiple sources,
**When** the chatbot retrieves relevant chunks,
**Then** it synthesizes these into a single, coherent answer.
**And** the synthesized answer is presented to me.

**Prerequisites:** Story 2.4

**Technical Notes:** Enhance RAG pipeline to include summarization capabilities using Gemini.

### Story 3.3: Source Referencing Display

As a user,
I want to see the original source URLs for the chatbot's answers,
So that I can verify the information and explore further.

**Acceptance Criteria:**

**Given** the chatbot provides an answer,
**When** the answer is displayed,
**Then** a list of source URLs is presented alongside the answer.
**And** clicking on a URL opens the original page.

**Prerequisites:** Story 3.2

**Technical Notes:** Frontend development to display URLs, backend to extract and provide them.

### Story 3.4: User Satisfaction Feedback Mechanism

As a user,
I want to provide feedback on my chatbot experience,
So that the system can be improved.

**Acceptance Criteria:**

**Given** a conversation has ended,
**When** the chatbot prompts for feedback,
**Then** I can rate my satisfaction on a 1-10 scale.
**And** I can optionally provide text comments.

**Prerequisites:** Story 1.2

**Technical Notes:** Frontend UI for feedback, FastAPI endpoint to store feedback in Supabase.

## Epic 4: Deployment & Integration

Make the chatbot publicly available and accessible to users.

### Story 4.1: Production Deployment

As a developer,
I want to deploy the application to a production environment,
So that it is publicly accessible.

**Acceptance Criteria:**

**Given** the application is ready for production,
**When** the deployment script is run,
**Then** the application is deployed to the production environment on Vercel.
**And** the production deployment is stable and accessible via a public URL.

**Prerequisites:** Story 1.4, 2.4, 3.4

**Technical Notes:** Finalize Vercel configuration, environment variables for production.

### Story 4.2: University Website Integration

As a user,
I want to easily find and access the chatbot from the university website,
So that I can get help quickly.

**Acceptance Criteria:**

**Given** the chatbot is deployed,
**When** I visit the university's main student-facing pages,
**Then** I see a prominent link to the chatbot.
**And** clicking the link opens the chatbot in a new tab.

**Prerequisites:** Story 4.1

**Technical Notes:** Coordinate with university web team for link placement.

### Story 4.3: Performance & Scalability Testing

As a developer,
I want to test the performance and scalability of the deployed application,
So that I can ensure it meets the non-functional requirements.

**Acceptance Criteria:**

**Given** the application is deployed to production,
**When** load tests are performed,
**Then** the application meets the P95 response time of under 2 seconds with up to 50 concurrent users.

**Prerequisites:** Story 4.1

**Technical Notes:** Use tools like Locust or k6 for load testing.

### Story 4.4: Accessibility Audit

As a developer,
I want to audit the chatbot's accessibility,
So that I can ensure it complies with WCAG 2.1 AA standards.

**Acceptance Criteria:**

**Given** the application is deployed,
**When** an accessibility audit is performed,
**Then** a report is generated detailing any accessibility issues.
**And** any critical issues are addressed.

**Prerequisites:** Story 4.1

**Technical Notes:** Use tools like Lighthouse or Axe for accessibility auditing.

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._