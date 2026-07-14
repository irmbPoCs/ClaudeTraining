# Intro

## Making API Requests

When your server contacts the Anthropic API, you can use either an official SDK or make plain HTTP requests. Anthropic provides SDKs for Python, TypeScript, JavaScript, Go, and Ruby.

![alt text](image.png)

## Every request must include these essential fields:

* API Key - Identifies your request to Anthropic
* Model - Name of the model to use (like "claude-3-sonnet")
* Messages - List containing the user's input text
* Max Tokens - Limit for how many tokens Claude can generate

## Inside Claude's Processing

Once Anthropic receives your request, Claude processes it through four main stages: tokenization, embedding, contextualization, and generation.

![alt text](image-1.png)

### Tokenization

Claude first breaks your input text into smaller chunks called tokens. These can be whole words, parts of words, spaces, or symbols. For simplicity, think of each word as one token.


### Embedding

Each token gets converted into an embedding - a long list of numbers that represents all possible meanings of that word. Think of embeddings as numerical definitions that capture semantic relationships.

![alt text](image-2.png)

Words often have multiple meanings. For example, "quantum" could refer to:

* A discrete unit of physical quantity (physics)
* Quantum mechanics or quantum physics concepts
* Something extremely small or subatomic
* Quantum computing applications

### Contextualization

Claude refines each embedding based on surrounding words to determine the most likely meaning in context. This process adjusts the numerical representations to highlight the appropriate definition.

![alt text](image-3.png)

### Generation

The contextualized embeddings pass through an output layer that calculates probabilities for each possible next word. Claude doesn't always pick the highest probability word - it uses a mix of probability and controlled randomness to create natural, varied responses.

![alt text](image-4.png)

After selecting each word, Claude adds it to the sequence and repeats the entire process for the next word.

## When Claude Stops Generating

After each token, Claude checks several conditions to decide whether to continue:

![alt text](image-5.png)

* Max tokens reached - Has it hit the limit you specified?
* Natural ending - Did it generate an end-of-sequence token?
* Stop sequence - Did it encounter a predefined stop phrase?

## The API Response

When generation completes, the API sends back a structured response containing:

* Message - The generated text
* Usage - Count of input and output tokens
* Stop Reason - Why generation ended

![alt text](image-6.png)

Your server receives this response and forwards the generated text back to your client application, where it appears in the user interface.


## Temperature

It controls how predictable or creative Claude's responses will be. Understanding how to use it effectively can dramatically improve your AI applications.
![alt text](image-8.png)

![alt text](image-7.png)