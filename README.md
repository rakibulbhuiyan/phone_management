# Samsung Phone Query and Review System

A Django REST API based Samsung phone information system that scrapes phone specifications from GSMArena, stores the data in a database, provides search and comparison APIs, and prepares the foundation for an LLM-powered RAG chatbot and multi-agent review system.

---

## Project Overview

The system collects Samsung phone specifications from GSMArena and stores structured information in a Django database.

The application provides REST APIs for:

- Listing Samsung phones
- Retrieving individual phone details
- Searching phones
- Comparing two phones
- Conversational phone queries

The project is being extended with:

- Retrieval-Augmented Generation (RAG)
- LLM-based chatbot
- Multi-agent system
- Automated phone reviews

---

## Architecture

```text
GSMArena
    |
    v
Web Scraper
(requests + BeautifulSoup)
    |
    v
Structured Phone Data
    |
    v
Django Phone Model
    |
    v
Database
    |
    +----------------------+
    |                      |
    v                      v
REST API              Retrieval Layer
                           |
                           v
                    Context Builder
                           |
                           v
                          LLM
                           |
                           v
                    Chatbot Response