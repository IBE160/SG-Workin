# ibe160 - Product Requirements Document

**Author:** BIP
**Date:** 2025-11-17
**Version:** 1.0

---

## Executive Summary

This project will create an AI-powered chatbot to solve the frustration students face when searching for study program information on the university's disorganized website. By providing a single, intelligent source of truth, the chatbot will empower users to find clear, synthesized answers quickly, improving their experience and freeing up university staff from repetitive inquiries.

### What Makes This Special

The "wow" moment for users occurs when they ask a vague or complex question and the chatbot instantly delivers a single, synthesized answer that pulls information from multiple, hard-to-find pages on the university website. It acts as a personal research assistant, saving users from the frustrating task of piecing together information themselves.

---

## Project Classification

**Technical Type:** Web App
**Domain:** EdTech
**Complexity:** Medium

The project operates in the EdTech domain, specifically focusing on university-level educational information. This requires a high degree of accuracy and reliability, as students will be making important academic decisions based on the information provided. The chatbot must be able to understand the nuances of study programs, course prerequisites, and academic pathways.


---

## Success Criteria

Success is defined by students feeling empowered and confident after using the chatbot. We will measure this through:
- **High User Satisfaction:** Achieving an average user satisfaction score of 8/10 or higher on a 1-10 scale presented after each conversation.
- **Task Completion:** A high percentage of users (>80%) indicating that their query was fully resolved.
- **Positive Qualitative Feedback:** Users voluntarily leaving positive comments about the chatbot's speed, accuracy, and ease of use.

### Business Metrics

- **Reduced Staff Inquiries:** A measurable decrease in the number of repetitive, study-program-related questions directed to university staff.
- **Low Escalation Rate:** A low percentage of conversations (<10%) that need to be escalated to a human agent.

---

## Product Scope

### MVP - Minimum Viable Product

- **Basic Q&A for Study Programs:** The chatbot must be able to provide quick, direct, and accurate answers to common questions about university study programs.
- **Suggesting Study Paths:** Ability to guide students in exploring long-term study options and potential academic routes.
- **Suggesting Program Combinations:** Functionality to assist students in understanding how different fields of study or programs can be combined.
- **Information Sourcing & Referencing:** All answers must include links to "more information" and explicitly cite the source URL(s) from the university website.
- **Interactive Guidance:** The chatbot will proactively ask clarifying questions to guide users towards the correct information, especially when initial queries are ambiguous.
- **Information Synthesis:** Capability to combine and summarize relevant information from multiple pages on the university website to provide comprehensive answers.
- **One-Click Access:** The chatbot must be easily accessible via a single click from the university's main website.
- **Escalation to Contact:** If the chatbot cannot answer a question, it must provide a direct link to the university's contact page.
- **User Satisfaction Feedback:** Implement a 1-10 satisfaction scale at the end of each conversation, with an optional text field for user comments.

### Growth Features (Post-MVP)

- **Automated Daily Website Scraping:** Implement automated processes for daily updates to the chatbot's knowledge base from the university website.
- **Multilingual Support:** Expand chatbot capabilities to support multiple languages to cater to a diverse student body.
- **Email Conversation Log:** Allow users to receive a transcript of their chat via email for future reference.
- **Forward Log on Escalation:** Implement functionality to automatically forward chat history to relevant staff members when a query is escalated.

### Vision (Future)

- **Comprehensive Student Assistant:** Evolve into a comprehensive assistant that supports students throughout their entire academic journey, from initial inquiry to graduation, covering topics like admissions, campus life, and academic support.
- **Personalized Information:** Integrate with university systems to provide personalized information (e.g., course schedules, grades) while maintaining strict privacy and security.
- **Proactive Support:** Develop features for proactive outreach, such as sending reminders for deadlines or suggesting relevant resources based on student profiles.
- **Voice Interface:** Explore the development of a voice-activated interface for hands-free interaction.

### Expansion Opportunities

*   **Organic Growth:** A measurable increase in chatbot usage over time, driven by word-of-mouth recommendations from satisfied users.
*   **Personalized Information:** Integration with student information systems to provide personalized data (e.g., course schedules, grades) while maintaining strict privacy and security.
*   **Broader Knowledge Domains:** Expanding the chatbot's knowledge base to include FAQs on admissions, financial aid, student housing, career services, and campus events.
*   **Proactive Support:** Developing features for proactive outreach, such as sending reminders for deadlines or suggesting relevant resources based on student profiles.
*   **Integration with Other Platforms:** Embedding the chatbot into other university platforms like the student portal, learning management systems, or mobile applications.
*   **Voice Interface:** Exploring the development of a voice-activated interface for hands-free interaction.

---

## Innovation & Novel Patterns

The chatbot introduces novel patterns in university information retrieval through:
*   **Interactive Guidance:** Proactively guiding users with clarifying questions to refine ambiguous queries, ensuring accurate information discovery even when the user is unsure what to ask.
*   **Information Synthesis:** The ability to instantly gather and synthesize relevant data from multiple, disparate university website pages into a single, consolidated, and easy-to-understand answer.

### Validation Approach

The innovation will be validated through:
*   **User Satisfaction Feedback:** Direct feedback from users via the in-chat satisfaction scale and optional comments.
*   **Conversation Completion Rate:** Tracking the percentage of queries successfully resolved by the chatbot without escalation.
*   **Qualitative User Interviews:** Conducting interviews to understand user perception of the interactive guidance and information synthesis capabilities.

---

## Project-Specific Requirements

As a Web App, the chatbot must adhere to the following:
*   **Deployment:** Publicly available without user authentication.
*   **Accessibility:** Must adhere to accessibility standards (WCAG guidelines).
*   **Responsiveness:** The user interface must be mobile-responsive to ensure usability across various devices.
*   **Integration:** Initially, the chatbot will be accessible via a direct link from the university's website. Deeper integration (e.g., iframe, widget, direct embed) will be considered in future iterations.
*   **Browser Support:** Compatibility with modern web browsers (Chrome, Firefox, Safari, Edge).
*   **Performance:** Fast loading times and smooth interactions are critical for user experience.

---

## User Experience Principles

- **Effortless and Intuitive:** The interface should be simple, clean, and easy to navigate, requiring minimal effort from the user to initiate and complete interactions.
- **Conversational and Guiding:** The chatbot should engage users in a natural, conversational manner, proactively asking clarifying questions to guide them to the correct information.
- **Positive and Confident:** Users should leave each interaction feeling positive, well-informed, and confident in the information received, reinforcing trust in the system.
- **Delightful Experience:** The chatbot's personality, speed, and accuracy should be so exceptional that it creates a "delightful" experience, encouraging users to recommend it to their peers.

### Key Interactions

- **Simple Greeting and Prompt:** Users are greeted with a clear, concise prompt encouraging them to ask questions.
- **Quick, Direct Answers:** The chatbot provides immediate and accurate responses to queries.
- **Clarifying Follow-up Questions:** When a query is ambiguous, the chatbot asks relevant questions to refine the user's intent.
- **Source Referencing:** All answers include clear links to the original source material on the university website.
- **Escalation Path:** A clear and easy way to escalate to a human contact if the chatbot cannot resolve the query.
- **Satisfaction Feedback:** A simple 1-10 satisfaction scale with an optional text field at the end of each conversation.

---

## Functional Requirements

*   **User Management:**
    *   **Requirement:** The system must be publicly accessible without user authentication.
    *   **User Value:** Provides a frictionless experience for all users.
    *   **Acceptance Criteria:** The chatbot is immediately usable upon visiting the page, with no login or registration required.

*   **Information Retrieval:**
    *   **Requirement:** The chatbot must answer questions about university study programs, study paths, and program combinations.
    *   **User Value:** Provides a single source of truth for all study-related inquiries.
    *   **Acceptance Criteria:** The chatbot accurately answers a predefined set of test questions covering a range of study program topics.

*   **Conversational Interface:**
    *   **Requirement:** The chatbot must engage users in a natural, conversational manner.
    *   **User Value:** Creates a more engaging and less intimidating user experience.
    *   **Acceptance Criteria:** The chatbot's responses are grammatically correct, use a friendly tone, and are easy to understand.

*   **Interactive Guidance (Magic):**
    *   **Requirement:** The chatbot must proactively ask clarifying questions when a user's query is ambiguous.
    *   **User Value:** Helps users find the correct information even when they are unsure what to ask.
    *   **Acceptance Criteria:** When presented with a vague query (e.g., "tell me about business"), the chatbot responds with a question to narrow down the user's intent.

*   **Information Synthesis (Magic):**
    *   **Requirement:** The chatbot must be able to combine and summarize relevant information from multiple pages on the university website.
    *   **User Value:** Saves users from the frustrating task of manually piecing together information from different sources.
    *   **Acceptance Criteria:** For a query that requires information from multiple sources, the chatbot provides a single, consolidated answer.

*   **Source Referencing:**
    *   **Requirement:** All answers must include links to "more information" and explicitly cite the source URL(s).
    *   **User Value:** Builds trust and allows users to verify information.
    *   **Acceptance Criteria:** Every answer is accompanied by a list of source URLs.

*   **Escalation:**
    *   **Requirement:** If the chatbot cannot answer a question, it must provide a direct link to the university's contact page.
    *   **User Value:** Provides a clear path for users to get help when needed.
    *   **Acceptance Criteria:** After a reasonable number of failed attempts, the chatbot provides a clickable link to the contact page.

*   **User Feedback:**
    *   **Requirement:** Implement a 1-10 satisfaction scale at the end of each conversation, with an optional text field.
    *   **User Value:** Allows users to contribute to the improvement of the system.
    *   **Acceptance Criteria:** The feedback mechanism is presented at the end of each conversation.

---

## Non-Functional Requirements

### Performance

*   **Requirement:** The chatbot must provide a near-instantaneous response to user queries.
*   **Why it matters:** A slow or laggy chatbot will lead to user frustration and abandonment.
*   **Measurable criteria:** 95% of responses should be delivered in under 2 seconds.

### Accessibility

*   **Requirement:** The chatbot interface must be accessible to users with disabilities.
*   **Why it matters:** To ensure equal access to information for all students.
*   **Measurable criteria:** The UI must comply with WCAG 2.1 AA standards.

### Scalability

*   **Requirement:** The system must handle a reasonable number of concurrent users without significant performance degradation.
*   **Why it matters:** To ensure a consistent experience as user adoption grows.
*   **Measurable criteria:** The system must maintain its performance targets with up to 50 concurrent users.

### Integration

*   **Requirement:** The chatbot must be easily accessible from the university website.
*   **Why it matters:** To ensure users can easily find and use the chatbot.
*   **Measurable criteria:** A direct link to the chatbot is prominently displayed on the university's main student-facing pages.

---

## Risks and Open Questions

### Key Risks
- **Insufficient Intent Understanding:** If the chatbot's intent detection is not robust or the conversational design is poor, it will likely misunderstand user queries, leading to frustrating interactions and low user satisfaction.

---

## Implementation Planning

### Epic Breakdown Required

Requirements must be decomposed into epics and bite-sized stories (200k context limit).

**Next Step:** Run `workflow epics-stories` to create the implementation breakdown.

---

## References

- Product Brief: /Users/linelyngsnesjohansen/ib160/SG-Workin/docs/product-brief-ibe160-Monday, November 10, 2025.md
- Research: /Users/linelyngsnesjohansen/ib160/SG-Workin/docs/research-technical-fredag 7. november 2025.md

---

## Next Steps

1. **Epic & Story Breakdown** - Run: `workflow epics-stories`
2. **UX Design** (if UI) - Run: `workflow ux-design`
3. **Architecture** - Run: `workflow create-architecture`

---

_This PRD captures the essence of ibe160 - The "wow" moment for users occurs when they ask a vague or complex question and the chatbot instantly delivers a single, synthesized answer that pulls information from multiple, hard-to-find pages on the university website. It acts as a personal research assistant, saving users from the frustrating task of piecing together information themselves._

_Created through collaborative discovery between BIP and AI facilitator._
