# The Unofficial Guide — Project 1

---

## Domain

**Campus survival tips for college students** — the practical, experience-based knowledge that students share with each other informally but that no official university website publishes. This includes advice on roommates, dorm packing, academics, time management, money, mental health, and social life.

This knowledge is valuable because it reflects real student experience, not institutional messaging. Official university websites tell you how to register for classes; they don't tell you to wait until after the first week to buy textbooks, or that you should lock your valuables away from a new roommate. That kind of advice lives in Reddit threads, personal blogs, and word-of-mouth — scattered across dozens of sources with no unified, searchable interface. This system makes it findable through plain-language questions.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | reddit_time_management.txt | Reddit thread | documents/reddit_time_management.txt |
| 2 | reddit_roommate_experiences.txt | Reddit thread | documents/reddit_roommate_experiences.txt |
| 3 | blog_free_stuff_discounts.txt | Blog article | documents/blog_free_stuff_discounts.txt |
| 4 | blog_useful_apps.txt | Blog post | documents/blog_useful_apps.txt |
| 5 | blog_general_survival_tips.txt | Personal blog | documents/blog_general_survival_tips.txt |
| 6 | blog_25_freshman_tips.txt | Listicle article | documents/blog_25_freshman_tips.txt |
| 7 | blog_firstyear_advice.txt | Personal blog | documents/blog_firstyear_advice.txt |
| 8 | blog_making_friends.txt | Personal blog | documents/blog_making_friends.txt |
| 9 | reddit_freshman_advice.txt | Reddit thread | documents/reddit_freshman_advice.txt |
| 10 | reddit_dorm_packing.txt | Reddit thread | documents/reddit_dorm_packing.txt |

---

## Chunking Strategy

**Chunk size:** ~400 characters

**Overlap:** ~80 characters

**Why these choices fit your documents:**
The documents are a mix of short Reddit-style tips (1–4 sentences) and longer blog posts. Most useful pieces of advice are 2–4 sentences long and complete on their own — for example, "Wait to buy textbooks until after the first week; your professor may not require them." At 400 characters, each chunk captures one full tip without merging unrelated advice. Chunks smaller than ~150 characters became sentence fragments with no standalone meaning. Chunks larger than ~800 characters merged multiple unrelated tips, making it impossible to match any specific query precisely.

The 80-character overlap (~one sentence) prevents losing advice that spans a chunk boundary. Some tips are structured as a claim followed by an explanation — without overlap, the explanation could end up in the next chunk with no connection to the claim that motivated it.

The chunking strategy splits by paragraph first (since these documents use line breaks between ideas), then falls back to character-count splitting if any paragraph exceeds 400 characters. Before chunking, documents were cleaned by normalizing line endings, stripping HTML tags, and removing blank lines.

**Final chunk count:** 376 chunks across 10 documents

---

## Sample Chunks

**Chunk 1** (source: reddit_dorm_packing.txt)
> "College is a Petri dish, get medicine. Cough/cold, fever, pain reliever, nasal spray if needed, vapor rub, anti diarrheal/stomach relief medicine, cough drops."

**Chunk 2** (source: reddit_roommate_experiences.txt)
> "Expectations for sleeping is actually really important - what time you/they go to bed and get up, alarm noises and if that will make a difference, how dark or quiet you or they need the room to be. It's really important to get good sleep in college."

**Chunk 3** (source: blog_making_friends.txt)
> "The prospect of moving to an entirely new place and rebuilding your social circle from scratch is a pretty scary one, especially if social situations tend to stress you out. With that said, making new friends and putting yourself out there is one of the most rewarding experiences that college has to offer."

**Chunk 4** (source: blog_25_freshman_tips.txt)
> "Don't procrastinate; prioritize your life. It may have been easy in high school to wait until the last minute to complete an assignment and still get a good grade, but that kind of stuff will not work for you in college. Give yourself deadlines and stick to them."

**Chunk 5** (source: blog_free_stuff_discounts.txt)
> "Students get Amazon Prime free for six months. This includes free two-day shipping on over 100 million items including textbooks, unlimited streaming of Prime movies and TV shows, and 20% off pre-order and new release video games."

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`, running locally.

This model was chosen because it runs entirely on the local machine with no API key, no rate limits, and no cost. It is fast and well-suited for short, conversational text, which matches the style of the documents in this corpus.

**Production tradeoff reflection:**
For a real deployment serving thousands of students, several tradeoffs would need to be weighed. OpenAI's `text-embedding-3-small` would likely produce more accurate embeddings, especially for nuanced queries, but introduces per-request API costs and a dependency on an external service. If the system served international students, a multilingual model like `multilingual-e5-base` would be necessary since `all-MiniLM-L6-v2` is English-only. Context length is not a concern here — MiniLM supports up to 256 tokens, which is sufficient for our 400-character chunks — but would matter if documents were longer. For a production system, I would also consider re-embedding the collection periodically as new student posts are added, which is easier with a local model that has no per-call cost.

---

## Retrieval Test Results

**Query 1: "What medicine should I pack for my dorm?"**

Top returned chunks:
- `reddit_dorm_packing.txt`: "College is a Petri dish, get medicine. Cough/cold, fever, pain reliever, nasal spray if needed, vapor rub, anti diarrheal/stomach relief medicine, cough drops." (distance: 0.801)
- `reddit_dorm_packing.txt`: "magnesium, iron, d4, multivitamins. I carried all of this and although it seems like an excess I have not yet had to ask a friend for medicine." (distance: 0.935)
- `reddit_dorm_packing.txt`: "First aid kit - just a basic one, no need for a tourniquet. But having neosporin, bandaids, gauze, gloves can help if someone gets hurt in the dorms." (distance: 1.02)

These chunks are directly relevant — all three come from the dorm packing document and contain specific medicine recommendations. The retrieval correctly identified the right source document for this query.

**Query 2: "How do I make friends in college if I'm shy?"**

Top returned chunks:
- `blog_making_friends.txt`: "...sometimes you have to be the first one to seem approachable. Asking about someone's day or even just a quick 'hi' will let people know that you're friendly." (distance: 0.801)
- `blog_making_friends.txt`: "...socializing becomes a little bit less intimidating. Friendliness = Friendship. Know that people want to make friends, so don't be afraid to be overly social." (distance: 0.901)

Both chunks are highly relevant and come from the correct document about social anxiety in college. The retrieval correctly matched a query about shyness to content about overcoming social nervousness.

**Query 3: "What free stuff can college students get?"** *(partial failure)*

Top returned chunks:
- `blog_free_stuff_discounts.txt`: introductory paragraph about student discounts (distance: 0.823)
- `blog_free_stuff_discounts.txt`: Amazon Prime section (distance: 0.891)

The correct document was retrieved, but only the intro and Amazon section were returned. Chunks containing Microsoft Office, Spotify, YNAB, and public transit discounts were not ranked in the top 4. This is explained in the Failure Case Analysis below.

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are a helpful college survival guide assistant.
Answer the user's question using ONLY the information provided in the context below.
Do not use any outside knowledge — if the context doesn't contain enough information
to answer, say "I don't have enough information on that in my documents."
At the end of your answer, always list the sources you drew from under a "Sources:" heading.
```

**How source attribution is surfaced in the response:**
Each retrieved chunk is passed to the LLM with its source filename labeled inline: `[1] (Source: reddit_dorm_packing.txt)`. The system prompt instructs the model to list sources at the end of every response. Additionally, the `query.py` function programmatically extracts the source filenames from retrieved chunk metadata and returns them in the `sources` field, which the Gradio UI displays in a separate "Retrieved from" box — independent of what the LLM writes. This means source attribution is guaranteed structurally, not just hoped for from the model.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What should I pack for medicine and health supplies in my dorm? | Cough/cold, pain relievers, vitamins, first aid kit, allergy meds | First aid kit, neosporin, bandaids, vitamins — missed cough meds and allergy meds; garbled "magnesium" as "nesium" | Relevant | Partially accurate |
| 2 | How should I handle a bad roommate situation? | Set expectations early, watch for red flags, communicate, consider switching | Establish mutual respect, lock belongings, build support network in residence hall | Relevant | Accurate |
| 3 | What free stuff or discounts can college students get? | Amazon Prime, MS Office, Spotify, YNAB, transit passes, museum discounts | Only mentioned Amazon Prime and general discounts — missed most of the specific items | Partially relevant | Partially accurate |
| 4 | What's the best way to manage time and avoid procrastination? | Calendar app, treat study blocks like a job, start early, don't cram | Build calendar blocks, treat it like a job, give yourself deadlines, study in 20-30 min chunks | Relevant | Accurate |
| 5 | How do I make friends in college if I'm introverted or nervous? | Everyone feels the same, say hi first, don't cling to first people, join clubs | Everyone feels nervous, say hi, be patient, it takes time to find your people | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** What free stuff or discounts can college students get?

**What the system returned:** A vague answer mentioning only Amazon Prime and general categories like "student discounts on computers and clothes." The specific items in the source document — Microsoft Office (free with school email), Spotify ($6.99/month after trial), YNAB (free for a year), public transit passes, and museum admission — were not included.

**Root cause (tied to a specific pipeline stage):** This is a retrieval failure. The source document `blog_free_stuff_discounts.txt` is structured as a long list where each item is a short separate paragraph. After paragraph-based chunking, each item became its own small chunk (~100–200 characters). When the query "what free stuff can college students get" was embedded, it matched most strongly against the document's introductory paragraph — which uses nearly that exact phrasing — and the Amazon Prime section. The other items use different vocabulary (e.g., "eligible institutions," "valid college email address," "six months of free access") that didn't match the query embedding closely enough to rank in the top 4 results. With k=4, there wasn't room to surface the full list.

**What you would change to fix it:** Two approaches would help. First, increasing k to 6 or 8 for this type of query would bring in more chunks from the same document. Second, storing the entire free stuff list as a single larger chunk (rather than splitting each item separately) would mean a single retrieval hit captures all the items at once. This is a case where the general chunking strategy (optimized for tip-style advice) didn't fit a list-structured document well.

---

## Spec Reflection

**One way the spec helped during implementation:**
Writing the chunking strategy in `planning.md` before touching any code forced a concrete decision about chunk size before seeing the consequences. When the 400-character chunks were actually printed and inspected during Milestone 3, they matched what the spec predicted — short, self-contained tips. Without the spec, it would have been tempting to just use a default chunk size from a tutorial without thinking about whether it fit the document structure.

**One way implementation diverged from the spec, and why:**
The spec anticipated chunk counts between 50 and 2,000 and predicted 398 chunks. The actual count was 376. The difference came from the `len(chunk) > 30` filter in `chunk.py`, which discarded very short fragments — mostly overlap artifacts and single-word lines that survived the paragraph split. This was a small deviation that improved output quality by removing noise, but it wasn't explicitly planned in the spec.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Documents and Chunking Strategy sections of `planning.md`, plus the pipeline architecture diagram showing the five stages.
- *What it produced:* `ingest.py` and `chunk.py` — a document loader that reads all `.txt` and `.md` files from a `documents/` folder, cleans them, and a chunker that splits by paragraph first then falls back to character count with overlap.
- *What I changed or overrode:* The initial generated version of `chunk.py` used a simple fixed character split with no paragraph awareness. I directed the AI to revise it to try paragraph boundaries first, because the documents use line breaks between ideas and splitting mid-paragraph would break the semantic coherence of individual tips.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section of `planning.md`, the grounding requirement ("answer from retrieved context only, cite sources"), and the desired output format (`{answer, sources}`).
- *What it produced:* `query.py` — a function that retrieves top-4 chunks from ChromaDB, formats them as numbered context blocks with source labels, passes them to Groq's llama-3.3-70b-versatile with a system prompt enforcing grounding, and returns the answer with sources.
- *What I changed or overrode:* The generated system prompt originally said "try to use the provided documents." I strengthened it to "answer using ONLY the information provided" and added the explicit fallback instruction: "if the context doesn't contain enough information, say 'I don't have enough information on that in my documents.'" This change was necessary to make grounding enforceable rather than just suggested.