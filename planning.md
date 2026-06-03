# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

**Campus survival tips for college students** — the practical, experience-based knowledge that students share with each other informally but that no official university website publishes. This includes advice on roommates, dorm packing, academics, time management, money, mental health, and social life. This knowledge is hard to find through official channels because it lives in Reddit threads, personal blog posts, and word-of-mouth — scattered across dozens of sources with no unified, searchable interface.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Type |Description|
|---|--------|-------------|-----------------|
| 1 | `Get_comfortable_with_using_an_onlin.txt` | Reddit thread | Time management, calendars, study habits, professors |
| 2 | `dormroom.txt` | Reddit thread | Roommate experiences, expectations, conflict |
| 3 | `Free_Stuff_for_College_Students.txt` | Blog article | Student discounts, free tools, banking |
| 4 | `So_I_just_graduated_last_month_and.txt` | Blog post | Useful apps for college (PDFs, notes, task management) |
| 5 | `Find_somewhere_where_you_can_get_go.txt` | Personal blog | Food, downtime, mental health, staying in touch with family |
| 6 | `25_Tips_to_Help_You_Survive_and_Thr.txt` | Listicle article | Broad freshman survival: academics, social, health, money |
| 7 | `If_you_are_a_first_year_or_going_in.txt` | Personal blog | First-year tips: packing, professors, roommates, self-care |
| 8 | `The_prospect_of_moving_to_an_entire.txt` | Personal blog | Making friends, social anxiety, college social life |
| 9 | `reddit_freshman_advice.md` | Reddit thread | Academics, textbooks, work ethic, social life |
| 10 | `reddit_dorm_tips.txt` | Reddit thread | What to pack for dorms, supplies, medicine, comfort items |


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** ~400 characters with ~80 character overlap
Looking at the documents, most useful pieces of advice are 2–4 sentences long. A single tip like "Wait to buy textbooks until after the first week — your professor may not require them" is complete and answerable on its own. At 400 characters, we capture one full tip or idea without merging it with unrelated advice.

- Too small (e.g. 100 chars): chunks become sentence fragments with no standalone meaning — "Get to know your roommate" tells us nothing useful on its own.
- Too large (e.g. 1000+ chars): multiple unrelated tips get merged into one chunk. A chunk mixing advice about medicine AND dorm packing AND roommates can't match any specific query well.

**Overlap:** Some tips span two sentences where the second sentence explains the first. Overlap ensures that if a key idea crosses a chunk boundary, at least one of the two chunks contains enough context to be retrieved. Without overlap, we'd lose the "because" or "for example" that makes the advice actually useful.

**Reasoning:**
We'll split by paragraph first (since these documents use line breaks between ideas), then fall back to character-count splitting if any paragraph is longer than 400 characters.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`

This runs locally — no API key, no rate limits, no cost. It's fast and works well for short, conversational text, which matches our document style.

**Top-k:**  4 chunks per query

- Too few (k=1 or 2): If the most relevant chunk is split slightly wrong, we might miss it entirely.
- Too many (k=8+): We start pulling in loosely related content. If someone asks about roommates, we don't want chunks about textbooks diluting the context.
- k=4 gives the LLM enough variety to synthesize a good answer without noise.

**Production tradeoff reflection:** if this were real
 `text-embedding-3-small` (OpenAI) would give better accuracy but costs money per embed
- `multilingual-e5` would be needed if serving international students
- Context length matters if documents were much longer — MiniLM maxes out at 256 tokens, which is fine for our short advice chunks
- For a real deployment, we'd re-embed periodically as new student posts are added
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What should I pack for medicine and health supplies in my dorm? | Cough/cold medicine, pain relievers, fever reducers, anti-diarrheal, vitamins (C, D, magnesium), first aid kit with bandaids and neosporin, allergy medication |
| 2 | How should I handle a bad roommate situation? | Set expectations early (cleanliness, sleep schedules), watch for red flags before move-in, communicate directly, consider switching if necessary |
| 3 | What free stuff or discounts can college students get? | Amazon Prime free for 6 months, Microsoft Office free with school email, Spotify trial, public transit passes, museum discounts, YNAB free for a year |
| 4 | What's the best way to manage time and avoid procrastination in college? | Use a calendar app, treat study blocks like a job, start assignments the day they're given, don't cram, use tools like TickTick or Shovel |
| 5 | How do I make friends in college if I'm introverted or nervous? | Realize everyone feels the same way, be the first to say hi, don't cling to first people you meet, take it moment by moment, join clubs |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Advice overlap across documents** — Multiple documents cover the same topics (e.g. "go to office hours" appears in at least 4 documents). Retrieval may return 4 chunks that all say the same thing, giving the LLM redundant rather than complementary context. This could produce repetitive answers.

2. **Short chunks losing context** — Some Reddit tips are already only 1–2 sentences. After chunking, these become very small embeddings with weak semantic signal, which may cause poor retrieval matches (high distance scores even for relevant content).


---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
┌─────────────────────────────────────────────────────────────┐
│                     OFFLINE (build once)                     │
│                                                             │
│  [.txt files]                                               │
│      │                                                      │
│      ▼                                                      │
│  1. DOCUMENT INGESTION                                      │
│     Load & clean raw text (Python / open())                 │
│      │                                                      │
│      ▼                                                      │
│  2. CHUNKING                                                │
│     ~400 char chunks, 80 char overlap                       │
│     Split by paragraph → fallback to char count            │
│      │                                                      │
│      ▼                                                      │
│  3. EMBEDDING + VECTOR STORE                                │
│     all-MiniLM-L6-v2 (sentence-transformers)               │
│     Stored in ChromaDB with source filename metadata        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    ONLINE (each query)                       │
│                                                             │
│  [User question]                                            │
│      │                                                      │
│      ▼                                                      │
│  4. RETRIEVAL                                               │
│     Semantic search → top-4 chunks (ChromaDB)              │
│      │                                                      │
│      ▼                                                      │
│  5. GENERATION                                              │
│     Groq llama-3.3-70b-versatile                           │
│     Prompt: answer from context only + cite sources        │
│      │                                                      │
│      ▼                                                      │
│  [Answer + source list → Gradio UI]                        │
└─────────────────────────────────────────────────────────────┘
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

| Pipeline Stage | What I'll give the AI | What I expect it to produce |
|---|---|---|
| Document ingestion & chunking | This planning.md (Documents + Chunking Strategy sections) | A Python script that loads all 10 `.txt` files, cleans them (strips extra whitespace/blank lines), and splits them into ~400 char chunks with 80 char overlap, outputting a list of `{text, source}` dicts |
| Embedding + ChromaDB | Retrieval Approach section + pipeline diagram | Code to embed chunks with `all-MiniLM-L6-v2` and store them in ChromaDB with source metadata |
| Grounded generation | My grounding requirement: "answer from retrieved context only, cite sources" | A `query.py` function that takes a question, retrieves top-4 chunks, builds a prompt, calls Groq, and returns `{answer, sources}` |
| Gradio UI | The interface description from Milestone 5 | A working `app.py` with a text input, answer box, and sources box |

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
