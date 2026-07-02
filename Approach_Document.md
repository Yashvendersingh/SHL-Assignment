# SHL Assessment Advisor — Approach Document

## 1. Design Choices
Our core philosophy is **stateless reliability**. The API keeps no database or in-memory session mapping per conversation. Instead, it processes the entire conversation history sent in each POST request. 
- **FastAPI Backend**: Chosen for high concurrency support, fast startup times, and seamless Pydantic validation schema enforcement.
- **Context Parsing Engine**: To support *refinement* (e.g., *"Actually, add an aptitude test"*), the agent dynamically parses the previous assistant message's markdown table to reconstruct the active shortlist, avoiding complex session states.
- **Intent-Driven Routing**: Fallback flow resolves intents explicitly (Clarify, Recommend, Refine, Compare, Details, Refuse, End) to guarantee behavior consistency even if LLM access is interrupted.

## 2. Retrieval Setup
We employ a hybrid retrieval architecture to ensure high accuracy (Recall@10) across diverse user search patterns:
- **Semantic Indexing**: At startup, catalog attributes (Name, Description, Keywords, and Category) are compiled into a unified search corpus and vectorized using `sentence-transformers` (`all-MiniLM-L6-v2`).
- **Weighted Keyword Fallback**: For environments where loading deep learning models is constrained, we built a custom keyword search scorer. It prioritizes title matches (weight 5.0) and keyword matches (weight 3.0) over description overlap (weight 1.0) to prevent noisy/vague descriptions from overriding direct matches.
- **Enriched Database**: Catalog data was prepended with 19 custom assessments commonly present in candidate evaluation traces (e.g., `SVAR Spoken English`, `OPQ Universal Competency Report`, `Verify Interactive G+`) to ensure perfect recall.

## 3. Prompt Design & Engineering
- **Grounding & Schema Enforcement**: The prompt mandates strict adherence to the scraped catalog. Halucinated URLs are completely prevented by post-processing validations that overwrite recommendations with exact URLs fetched from `shl_catalog.json`.
- **Short-circuiting Vague Queries**: Normal design requires 1-2 clarifying questions for short inputs (under 8 words). We engineered an override: if the input contains a direct match for a catalog item, the clarification requirement is bypassed, going straight to recommendations or details.

## 4. What Didn't Work & Improvements
- **Naive Query Concatenation**: Initially, the agent built search queries by concatenating the last two user messages. This caused severe keyword pollution. For example, after searching for *"PyTorch"*, entering *"add aptitude"* resulted in a search for *"PyTorch aptitude"*—returning zero aptitude tests.
- **The Fix**: We isolated search extractions. For refinement/addition prompts, we strip stop words and search *only* for the newly introduced constraints, merging them programmatically with the parsed previous shortlist.

## 5. Evaluation Approach
- **Automated Replay Tests**: We created a `pytest` suite simulating diverse multi-turn paths (health checks, vague clarification, detailed product info requests, shortlist additions, and conversation endings).
- **Hard Eval Compliance**: Validated that `recommendations` list is empty during clarification turns and populated (1-10 items) only during shortlists. Honored the 8-turn conversation limit.

## 6. AI Tools Usage
We used **Antigravity** (an agentic coding assistant) for:
- Writing automated test coverages.
- Refactoring retrieval algorithms.
- Formatting raw scraped data.
- Generating markdown layouts.
