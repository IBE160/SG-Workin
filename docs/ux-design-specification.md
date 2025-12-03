# ibe160 UX Design Specification

_Created on 2025-11-21 by BIP_
_Generated using BMad Method - Create UX Design Workflow v1.0_

---

## Executive Summary

This document outlines the User Experience (UX) and User Interface (UI) design for the **ibe160 project**: An AI-powered chatbot to help students find information about study programs, solving the frustration of using the disorganized university website. The "wow" factor is its ability to synthesize information from multiple pages into a single, clear answer.

The design prioritizes an effortless, precise, and motivating experience, guided by a "Sharp & Modern" aesthetic and a color palette inspired by the "Mountain Majesty" theme.

---

## 1. Design System Foundation

### 1.1 Design System Choice

The project will use **shadcn/ui**. This choice, aligned with the PRD's tech stack (React, Tailwind CSS), provides high customizability, direct code ownership, and strong accessibility through Radix Primitives, which is perfect for creating a unique and branded user experience.

---

## 2. Core User Experience

### 2.1 Defining Experience

The core interaction pattern is a **Synthesizing Conversational UI**. The defining experience is the feeling of "ease and precision" that leads to "finding the right info" and "feeling motivated to take a course."

The core principles guiding the design are:
*   **Speed:** Instantaneous response to user queries.
*   **Guidance:** Proactive clarification for ambiguous questions.
*   **Clarity:** Precise, easy-to-understand answers with clear source links.
*   **Motivation:** Empowering users to take the next step in their academic journey.

### 2.2 Novel UX Patterns

No novel UX patterns were required. The design relies on a best-in-class implementation of an established "Synthesizing Conversational UI" pattern. The innovation lies in the quality of the synthesized response, not in a new UI mechanic.

---

## 3. Visual Foundation

### 3.1 Color System

The chosen color palette is **"Mountain Majesty,"** inspired by the calm and natural beauty of the Molde panorama.

*   **Primary:** `#2A4B7C` (Deep Fjord Blue)
*   **Secondary:** `#4A6D4D` (Forest Green)
*   **Accent:** `#A9B2B9` (Stone Gray)
*   **Neutral:** `#F5F5F5` (Snowy White)
*   **Text:** Dark gray (`#212529`) for high readability.

### 3.2 Typography

*   **Font Families:** 'Inter' for headings, 'Roboto' for body text (or similar sans-serif system fonts).
*   **Type Scale:** Base size of 16px (1rem) with a modular scale for headings.
*   **Line Heights:** 1.5 for body text, 1.2-1.3 for headings.

### 3.3 Spacing and Layout

*   **Base Spacing Unit:** An 8px grid system for all padding and margins.
*   **Layout Grid:** A fluid, single-column layout within a max-width container.
*   **Max Content Width:** ~768px on larger screens for optimal readability.

**Interactive Visualizations:**

- Color Theme Explorer: [ux-color-themes.html](./ux-color-themes.html)

---

## 4. Design Direction

### 4.1 Chosen Design Approach

The chosen design direction is **#2: Sharp & Modern**. This direction offers a clean, contemporary feel with a structured look, using outlined bot messages for clear differentiation. It aligns well with the goal of an "effortless and precise" experience.

**Interactive Mockups:**

- Design Direction Showcase: [ux-design-directions.html](./ux-design-directions.html)

---

## 5. User Journey Flows

### 5.1 Critical User Paths

The primary user journey is the **"Basic Q&A for Study Programs,"** which operates on a **Hybrid Assistant** model:

1.  **Entry:** User is greeted with an inviting question.
2.  **Intent Recognition:** The chatbot assesses if the query is specific or ambiguous.
3.  **Path A (Direct Answer):** For specific queries, the bot provides a concise, synthesized answer with clear source links.
4.  **Path B (Guided Clarification):** For ambiguous queries, the bot asks clarifying questions to guide the user.
5.  **Escalation:** If the bot cannot answer, it provides a clear link to a human contact page.
6.  **Feedback:** A satisfaction survey is presented after the query is resolved.

---

## 6. Component Library

### 6.1 Component Strategy

The strategy is to use the **shadcn/ui** library for all standard components (buttons, inputs, etc.) and define custom styles and components for the unique conversational interface.

**Custom Components:**
*   **Chat Bubble:** The container for all messages. User bubbles are right-aligned with a primary background color. Bot bubbles are left-aligned with a light neutral background and a subtle outline to match the "Sharp & Modern" theme. Interactive bubbles will have clearly styled clickable elements (buttons or links).
*   **Synthesized Answer Card:** A container within a bot bubble for comprehensive answers. It features the answer text first, followed by an icon-based link (e.g., an arrow) to the source material, which opens in a new tab.
*   **Chat Input Area:** An always-visible area fixed to the bottom of the screen on mobile. It features a text input field with helpful placeholder text (e.g., "Ask about studies...") and a prominent "Send" button.

---

## 7. UX Pattern Decisions

### 7.1 Consistency Rules

*   **Button Hierarchy:** Primary actions use solid, filled buttons. Secondary actions use outlined or subtle styles. Destructive actions use a distinct red color.
*   **Feedback Patterns:** Loading states are indicated by a subtle "typing..." indicator. Errors are communicated via inline messages.
*   **Empty State:** The initial chat window will display a welcoming message and 2-3 clickable "suggested questions" to guide the user.
*   **Confirmation Patterns:** Potentially destructive actions (e.g., "Clear History") will use a simple confirmation modal.

---

## 8. Responsive Design & Accessibility

### 8.1 Responsive Strategy

*   **Desktop/Tablet:** The chat interface will be centered with a fixed maximum width (~768px) for optimal readability.
*   **Mobile:** The interface will be full-width. The chat input area will be fixed to the bottom of the screen for constant access. All interactive elements will have touch-friendly target sizes.

### 8.2 Accessibility

*   **Compliance Target:** The interface will be designed and built to meet **WCAG 2.1 Level AA** standards.
*   **Key Requirements:** This includes sufficient color contrast, full keyboard navigation, visible focus indicators, proper ARIA labels for all interactive elements and landmarks, and descriptive alt text where necessary.

---

## 9. Implementation Guidance

### 9.1 Completion Summary

This UX Design Specification provides a comprehensive blueprint for the design and development of the ibe160 chatbot. We have collaboratively defined:
*   A clear **Design System** and **Visual Foundation**.
*   A specific **Design Direction** for the user interface.
*   A detailed **User Journey** for the core Q&A experience.
*   A **Component Strategy** for both standard and custom elements.
*   A set of **UX Patterns** for a consistent user experience.
*   A robust **Responsive & Accessibility Strategy**.

This document ensures that the implementation phase can proceed with a clear and shared understanding of the desired user experience.

---

## Appendix

### Related Documents

- Product Requirements: `docs/PRD.md`
- Product Brief: `docs/product-brief-ibe160-Monday, November 10, 2025.md`
- Brainstorming: `docs/brainstorming-session-results-Thursday, November 6, 2025.md`

### Core Interactive Deliverables

This UX Design Specification was created through visual collaboration:

- **Color Theme Visualizer**: docs/ux-color-themes.html
- **Design Direction Mockups**: docs/ux-design-directions.html

### Version History

| Date     | Version | Changes                         | Author        |
| -------- | ------- | ------------------------------- | ------------- |
| 2025-11-21 | 1.0     | Initial UX Design Specification | BIP |
| 2025-11-21 | 1.1     | Updated to reflect all design decisions | Sally (UX Agent) |

---

_This UX Design Specification was created through collaborative design facilitation, not template generation. All decisions were made with user input and are documented with rationale._