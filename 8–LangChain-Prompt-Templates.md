# Day 8 – LangChain Prompt Templates & Dynamic Prompts

Day 8 focused on **prompt management in LangChain**, especially how to create **dynamic and reusable prompts using `PromptTemplate`**. The session built on the previous day's concepts of messages, conversation history, and LLM invocation. 

## 1. What is a Prompt?

A **prompt** is the input or instruction given to an LLM to obtain a desired response.

A prompt can be:

* A question — *What is Python?*
* An instruction — *Explain Python in simple English.*
* A task — *Write a birthday message.*
* A role or set of instructions for the LLM.

The quality of the prompt matters: a **clear and specific prompt generally produces a more useful response**. 

---

## 2. Static vs Dynamic Prompts

### Static Prompt

A static prompt has fixed content that does not change.

```text
Explain Python in simple English.
```

Every time the application runs, the same prompt is sent to the LLM.

### Dynamic Prompt

A dynamic prompt contains **variables/placeholders** whose values can change at runtime.

```text
Explain {topic} in simple English.
```

If the user enters `Python`:

```text
Explain Python in simple English.
```

If the user enters `Java`:

```text
Explain Java in simple English.
```

The prompt structure remains the same, but the value changes based on user input. 

---

## 3. Why Dynamic Prompts?

Hardcoding a separate prompt/application for every topic is difficult to maintain.

For example, instead of creating separate applications for:

* Python
* Java
* Docker
* AWS
* LangChain

we can create **one reusable prompt template** and supply the topic dynamically.

This makes the application more **reusable, flexible, and maintainable**.

The instructor compared this to a certificate template: instead of creating a completely new certificate for every student, create one template and fill in the student's details at runtime. 

---

# 4. LangChain `PromptTemplate`

LangChain provides the **`PromptTemplate`** class to create reusable prompts containing variables.

Import:

```python
from langchain_core.prompts import PromptTemplate
```

Create a template:

```python
prompt_template = PromptTemplate.from_template(
    "Explain {topic} in simple English."
)
```

Here:

```text
{topic}
```

is a **placeholder/input variable**.

`PromptTemplate` allows us to separate the **prompt structure** from the **actual values** supplied at runtime. 

---

## 5. Supplying Values to the Template

The template can be formatted using the `invoke()` method.

```python
result = prompt_template.invoke({
    "topic": "Python"
})
```

The resulting prompt becomes:

```text
Explain Python in simple English.
```

The argument supplied to `invoke()` is a **dictionary containing variable names and their values**.

For example:

```python
{
    "topic": "Python",
    "level": "beginner"
}
```

This follows the key-value structure:

```text
variable name → variable value
```

The instructor compared Python dictionaries to Java's `Map` concept. 

---

# 6. `PromptTemplate.invoke()` vs `LLM.invoke()`

This was one of the **most important points of Day 8**.

Although both methods are called `invoke()`, they perform different jobs.

### `PromptTemplate.invoke()`

Purpose:

> **Format the prompt by replacing variables with their values.**

```python
prompt_value = prompt_template.invoke({
    "topic": "Python"
})
```

It produces a `PromptValue` containing the formatted prompt.

### `LLM.invoke()`

Purpose:

> **Send the formatted prompt to the LLM and obtain the AI response.**

```python
response = llm.invoke(prompt_value)
```

So the flow is:

```text
User Input
    ↓
PromptTemplate
    ↓
PromptTemplate.invoke()
    ↓
Formatted Prompt / PromptValue
    ↓
LLM.invoke()
    ↓
AI Message
    ↓
response.content
```

The distinction between these two `invoke()` methods was specifically emphasized in the class. 

---

# 7. Example: Topic Explainer

A reusable topic-explainer application can use:

```python
prompt_template = PromptTemplate.from_template("""
Explain {topic} to a beginner.
Use very simple English.
Give five important points.
Give one real-life example.
""")
```

The user can enter:

```text
Vector Database
```

The template dynamically becomes:

```text
Explain Vector Database to a beginner.
Use very simple English.
Give five important points.
Give one real-life example.
```

If the user enters:

```text
LangChain
```

the same template becomes:

```text
Explain LangChain to a beginner.
Use very simple English.
Give five important points.
Give one real-life example.
```

No change to the program itself is required. 

---

# 8. Example: Recipe Generator

Another example demonstrated was a **recipe generator**.

Template:

```text
Give me a simple recipe for {dish}.
Explain it step by step.
```

If the user enters:

```text
Chicken Biryani
```

the final prompt becomes:

```text
Give me a simple recipe for Chicken Biryani.
Explain it step by step.
```

The LLM can then generate the recipe.

The same application can handle:

* Chicken Biryani
* Paneer Butter Masala
* Idli
* Dosa
* Sambar
* Any other dish

This demonstrates the usefulness of **one reusable application with dynamic prompts**. 

---

# 9. Multiple Variables

A prompt can contain multiple variables.

For example:

```python
prompt_template = PromptTemplate.from_template(
    "Explain {topic} for a {level} learner with {experience} years of experience."
)
```

Values can be supplied using a dictionary:

```python
result = prompt_template.invoke({
    "topic": "Python",
    "level": "intermediate",
    "experience": 10
})
```

This produces a dynamically generated prompt using all three values. 

---

# 10. Multi-line Prompt Templates

Triple quotes can be used to create multi-line prompts:

```python
prompt_template = PromptTemplate.from_template("""
Explain {topic} to a beginner.
Use very simple English.
Give five important points.
Give one real-life example.
""")
```

This makes longer prompts much easier to read and maintain.

---

# 11. End User Doesn't Need to Be a Prompt Engineer

An important application-design concept discussed was:

> **The end user should provide the requirement; the application should construct the appropriate prompt.**

For example, the user only enters:

```text
LangChain
```

The application internally constructs:

```text
Explain LangChain to a beginner.
Use very simple English.
Give five important points.
Give one real-life example.
```

The user doesn't need to know how to construct the full prompt.

This is one of the reasons prompt templates are useful in real-world LLM applications. 

---

# 12. `PromptTemplate` vs Python f-strings

Python f-strings can also dynamically insert values:

```python
prompt = f"Explain {topic} in simple English."
```

For simple prompts, this works.

However, the instructor emphasized that **LangChain's `PromptTemplate` becomes more useful for larger applications**, where prompts need to connect with other LangChain components such as memory, output parsers, and pipelines. 

---

# 13. Key Takeaways

* A **prompt** is an input/instruction given to an LLM.
* Prompts should be **clear and specific**.
* **Static prompts** have fixed content.
* **Dynamic prompts** change based on runtime values.
* `{variable}` represents a **placeholder/input variable**.
* LangChain provides the `**PromptTemplate**` class for reusable dynamic prompts.
* `PromptTemplate.from_template()` creates a prompt template.
* `PromptTemplate.invoke()` replaces variables with supplied values.
* The values are provided as a **dictionary**.
* `LLM.invoke()` sends the resulting prompt to the LLM.
* `PromptTemplate.invoke()` and `LLM.invoke()` have **different purposes**.
* Prompt templates allow one application to support many different user inputs.
* Multi-line prompts can be created using triple quotes.
* Prompt templates are particularly useful when building larger LangChain pipelines.

### Day 8 Core Flow

```text
User Input
     ↓
Prompt Template
     ↓
Replace {variables}
     ↓
Final Prompt
     ↓
LLM.invoke()
     ↓
AI Message
     ↓
response.content
```

**In one sentence:**

> **Day 8 introduced LangChain's `PromptTemplate` and showed how static prompts can be converted into reusable dynamic prompts by replacing runtime variables before sending the final prompt to an LLM.**
