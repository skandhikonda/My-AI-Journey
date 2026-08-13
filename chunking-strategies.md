When you're building a **RAG (Retrieval-Augmented Generation)** system, chunking means taking a large document and breaking it into smaller pieces before creating embeddings.

For example, imagine this document:

> **Page 1:** Apple reported revenue of $100M in 2025. Revenue increased 20% from 2024.
> **Page 2:** Microsoft reported revenue of $200M in 2025. Revenue increased 10% from 2024.
> **Page 3:** Tesla delivered 2 million vehicles in 2025.

Instead of embedding the entire document as one giant piece, you create several **chunks**.

### 1. Fixed-size chunking

Split text after a fixed number of characters or tokens.

Suppose `chunk_size = 10 words`:

```text
Chunk 1:
Apple reported revenue of $100M in 2025.
Revenue increased...

Chunk 2:
20% from 2024. Microsoft reported revenue of
$200M in...

Chunk 3:
2025. Revenue increased 10% from 2024...
```

It's very simple and fast.

The downside is that it doesn't understand meaning. You might accidentally split:

```text
Microsoft reported revenue of
------------------------------
$200M in 2025.
```

So related information ends up in different chunks.

---

### 2. Fixed-size chunking with overlap

This is one of the most common approaches.

Instead of:

```text
Chunk 1: words 1–100
Chunk 2: words 101–200
Chunk 3: words 201–300
```

you introduce overlap:

```text
Chunk 1: words   1–100
Chunk 2: words  81–180
Chunk 3: words 161–260
```

So 20 words appear in both neighboring chunks.

Why?

Imagine the sentence:

```text
The bond has a coupon of 5.25%
and matures on April 27, 2029.
```

Without overlap, you could get:

```text
Chunk 1:
The bond has a coupon of 5.25%

Chunk 2:
and matures on April 27, 2029.
```

With overlap, you might preserve the full sentence in one of the chunks.

Typical code looks something like:

```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```

Meaning roughly:

```text
Maximum chunk size → 1000
Repeated content   → 200
```

---

### 3. Recursive chunking

This is extremely common with frameworks such as LangChain.

The idea is:

> **Try to split naturally first. If the pieces are still too large, use progressively smaller boundaries.**

For example, the splitter might try:

```python
separators = [
    "\n\n",   # paragraph
    "\n",     # line
    ". ",     # sentence
    " "       # word
]
```

Suppose the document is:

```text
Bond Overview

CAMBEO issued a 5.25% bond maturing in 2029.
The bond is available as Reg S and 144A.

Portfolio Information

Portfolio A owns $5 million of the bond.
Portfolio B owns $10 million.
```

It first tries paragraphs:

```text
Chunk 1:
Bond Overview

CAMBEO issued a 5.25% bond maturing in 2029.
The bond is available as Reg S and 144A.
```

If Chunk 1 is too large, it can split further into sentences.

This is generally better than blindly cutting every N characters because it attempts to preserve natural text boundaries.

---

### 4. Sentence-based chunking

Split based on sentences.

```text
Sentence 1:
CAMBEO issued a 5.25% bond.

Sentence 2:
The bond matures in 2029.

Sentence 3:
The bond has Reg S and 144A versions.
```

You might then group several sentences:

```text
Chunk 1:
CAMBEO issued a 5.25% bond.
The bond matures in 2029.

Chunk 2:
The bond has Reg S and 144A versions.
```

This avoids cutting sentences in half.

But sentence lengths vary significantly, so chunk sizes aren't necessarily consistent.

---

### 5. Paragraph-based chunking

Each paragraph becomes a chunk.

Original:

```text
CAMBEO issued a 5.25% bond maturing in 2029.
It has both Reg S and 144A securities.

Apple issued $5 billion of bonds in 2025.
The bonds have several maturities.

Microsoft also entered the debt market.
It issued $10 billion.
```

Becomes:

```text
Chunk 1 → CAMBEO paragraph

Chunk 2 → Apple paragraph

Chunk 3 → Microsoft paragraph
```

This works nicely when the documents themselves have well-structured paragraphs.

The problem is that one paragraph might contain 30 tokens while another contains 3,000.

---

### 6. Structure-aware chunking

Instead of treating everything as plain text, use the document's **structure**.

For example:

```text
# CAMBEO Bond

## Overview
CAMBEO issued a 5.25% bond...

## Trading
The bond trades as Reg S and 144A...

## Portfolio Exposure
Portfolio A owns $5M...
```

You could create:

```text
Chunk 1
Heading: Overview
Text: CAMBEO issued...

Chunk 2
Heading: Trading
Text: The bond trades...

Chunk 3
Heading: Portfolio Exposure
Text: Portfolio A owns...
```

This is especially useful for documents with clear sections, such as research reports, policies, manuals, and documentation.

You can also store the heading as metadata:

```python
{
    "chunk_id": "...",
    "page_number": 5,
    "section": "Trading",
    "text": "The bond trades as..."
}
```

That can make retrieval much more useful.

---

### 7. Page-based chunking

For PDFs, the simplest strategy is:

```text
Page 1 → Chunk 1
Page 2 → Chunk 2
Page 3 → Chunk 3
```

This has a major advantage: citations are easy.

Your metadata can simply contain:

```python
{
    "page_number": 7
}
```

But page boundaries aren't semantic boundaries.

A paragraph might start:

```text
Page 7:
The investment committee determined that the
```

and continue:

```text
Page 8:
position should be reduced by 50%.
```

So blindly chunking by page can hurt retrieval.

A common compromise is to use **smaller semantic/text chunks while retaining page number as metadata**, similar to what your earlier code is doing.

---

### 8. Semantic chunking

This is more sophisticated.

Instead of saying:

> "Every 500 tokens, create a new chunk."

you say:

> "Create a new chunk when the topic meaning changes."

Consider:

```text
Apple reported strong iPhone sales.
iPhone revenue increased 15%.
Services revenue also increased.

The Federal Reserve raised interest rates.
Treasury yields subsequently increased.

Tesla launched a new vehicle.
Deliveries are expected next year.
```

Semantic chunking tries to recognize three topics:

```text
Chunk 1 → Apple
Chunk 2 → Federal Reserve
Chunk 3 → Tesla
```

Usually embeddings or another model are used to determine when the meaning has changed significantly.

The advantage is **better conceptual coherence**.

The disadvantages are additional complexity, processing time, and cost.

---

### 9. Parent-child chunking

This is particularly useful in more sophisticated RAG systems.

You create **small chunks for searching** but retain **larger chunks for giving context to the LLM**.

For example:

```text
Parent chunk
────────────────────────────
CAMBEO Bond Analysis
~2000 tokens

    Child 1
    CAMBEO issued a 5.25% bond...

    Child 2
    The bond has Reg S and 144A...

    Child 3
    Portfolio A owns $5M...

    Child 4
    Spread duration is...
```

Embeddings are generated for the small child chunks.

User asks:

```text
Does CAMBEO have a 144A bond?
```

Vector search finds:

```text
Child 2
```

But instead of sending only Child 2 to the LLM, the system can retrieve its **parent**, providing more surrounding context.

This addresses an important RAG tradeoff:

```text
Small chunks
    ↓
Better precise retrieval
    ↓
But less context

Large chunks
    ↓
More context
    ↓
But less precise retrieval
```

Parent-child chunking attempts to get the benefits of both.

---

### How these compare

| Strategy        | Basic idea                   | Main advantage              | Main weakness               |
| --------------- | ---------------------------- | --------------------------- | --------------------------- |
| Fixed size      | Every N tokens               | Simple                      | Cuts ideas apart            |
| Fixed + overlap | N tokens + repeated text     | Preserves boundaries better | Duplicate content           |
| Recursive       | Paragraph → sentence → word  | Good general-purpose option | Still size-driven           |
| Sentence        | Split on sentences           | Natural boundaries          | Uneven sizes                |
| Paragraph       | One/few paragraphs           | Keeps ideas together        | Huge paragraphs possible    |
| Structure-aware | Use headings/sections        | Preserves document meaning  | Requires document structure |
| Page            | Split PDF pages              | Easy citations              | Page ≠ topic                |
| Semantic        | Split when meaning changes   | Strong semantic coherence   | More expensive/complex      |
| Parent-child    | Search small, retrieve large | Precision + context         | More architecture           |

For the type of code you showed earlier—`chunks`, embeddings, `page_number`, `chunk_number`, metadata—a very common starting architecture is **recursive chunking + overlap + page metadata**:

```text
PDF
 ↓
Extract text
 ↓
Recursive splitting
 ↓
Chunk 1 ── page=1, chunk=1
Chunk 2 ── page=1, chunk=2
Chunk 3 ── page=2, chunk=3
 ↓
Create embedding for each chunk
 ↓
Store:
    chunk text
    embedding
    chunk_id
    chunk_number
    page_number
 ↓
Vector database
```

Then when someone asks a question, you embed the **question**, find the most similar chunks, and give those chunks to the LLM as context.
