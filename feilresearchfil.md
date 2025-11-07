# Technical Research: FAQ Chatbot

**Date:** Friday, November 7, 2025

**Project:** ibe160 - FAQ Chatbot

## 1. Recommended Open-Source Retrieval-Based Chatbot Frameworks for Beginners

For a beginner, the best open-source retrieval-based chatbot frameworks are those that are easy to set up, have good documentation, and a supportive community.

*   **Rasa:**
    *   **Description:** Rasa is a popular open-source framework for building conversational AI. It provides all the necessary tools to build a chatbot from scratch, including NLU (Natural Language Understanding) and dialogue management.
    *   **Why it's good for beginners:** Rasa has extensive documentation, a large and active community, and offers a gentle learning curve for new users. It also has a user-friendly interface called Rasa X for conversation-driven development.
    *   **Link:** [https://rasa.com/](https://rasa.com/)

*   **Botpress:**
    *   **Description:** Botpress is another excellent open-source chatbot platform. It offers a visual conversation builder and a modular architecture, making it easy to extend its functionality.
    *   **Why it's good for beginners:** The visual builder in Botpress is a significant advantage for beginners, as it allows you to design conversations without writing a lot of code. It also has a good set of pre-built modules for common chatbot features.
    *   **Link:** [https://botpress.com/](https://botpress.com/)

*   **Microsoft Bot Framework:**
    *   **Description:** This framework, while backed by a major corporation, has a strong open-source presence. It provides a comprehensive set of tools and services to build and deploy chatbots on various channels.
    *   **Why it's good for beginners:** It offers a free tier for its Azure Bot Service, excellent documentation, and a large number of samples and templates to get you started.
    *   **Link:** [https://dev.botframework.com/](https://dev.botframework.com/)

## 2. Techniques for Indexing and Searching Public Web Pages

To build a knowledge base from public URLs, you need a way to crawl, index, and search the content of those pages.

*   **Web Crawling:**
    *   **Scrapy:** A powerful and popular Python library for web crawling. It's fast, extensible, and has a large community.
    *   **Beautiful Soup:** A Python library for pulling data out of HTML and XML files. It's often used in conjunction with a web crawling framework like Scrapy.

*   **Indexing and Searching:**
    *   **Elasticsearch:** A highly scalable open-source search and analytics engine. It's a popular choice for indexing large amounts of text data and provides fast and accurate search results.
    *   **Apache Solr:** Another popular open-source search platform built on Apache Lucene. It's also highly scalable and offers a rich set of features for search and indexing.
    *   **Whoosh:** A pure-Python search engine library. It's a good choice for smaller projects or for developers who want to stay within the Python ecosystem.

## 3. Best Practices for FAQ Chatbot UI Design

The user interface of a FAQ chatbot should be clean, simple, and intuitive.

*   **Clear Welcome Message:** The chatbot should introduce itself and explain what it can do.
*   **Simple Input:** A simple text input field is all that's needed. Avoid cluttering the interface with unnecessary buttons or options.
*   **Displaying Answers:** Answers should be displayed in a clear and readable format. Use formatting like bolding, bullet points, and links to improve readability.
*   **Source Attribution:** As requested in the brainstorming session, always display the source of the information. This builds trust with the user.
*   **Feedback Mechanism:** Allow users to provide feedback on the answers (e.g., a simple thumbs up/down). This can help you improve the chatbot's performance over time.

## 4. Ensuring Accuracy and Up-to-Date Answers

Keeping the chatbot's knowledge base current is crucial for its success.

*   **Regular Crawling:** Schedule regular crawls of the indexed websites to check for new or updated content. The frequency of the crawls will depend on how often the source websites are updated.
*   **Content Validation:** Before updating the knowledge base, validate the new content to ensure it's accurate and relevant.
*   **Versioning:** Keep track of different versions of the knowledge base. This will allow you to roll back to a previous version if you discover any issues with the new content.
*   **Monitoring:** Monitor the chatbot's conversations to identify any recurring issues or questions that it's unable to answer. This can help you identify gaps in the knowledge base.