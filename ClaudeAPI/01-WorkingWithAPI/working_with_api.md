# Intro

## Making API Requests

When your server contacts the Anthropic API, you can use either an official SDK or make plain HTTP requests. Anthropic provides SDKs for Python, TypeScript, JavaScript, Go, and Ruby.

![alt text](images/api-request-fields.png)

## Every request must include these essential fields:

* API Key - Identifies your request to Anthropic
* Model - Name of the model to use (like "claude-3-sonnet")
* Messages - List containing the user's input text
* Max Tokens - Limit for how many tokens Claude can generate

## Inside Claude's Processing

Once Anthropic receives your request, Claude processes it through four main stages: tokenization, embedding, contextualization, and generation.

![alt text](images/tokenization-example.png)

### Tokenization

Claude first breaks your input text into smaller chunks called tokens. These can be whole words, parts of words, spaces, or symbols. For simplicity, think of each word as one token.


### Embedding

Each token gets converted into an embedding - a long list of numbers that represents all possible meanings of that word. Think of embeddings as numerical definitions that capture semantic relationships.

![alt text](images/quantum-word-meanings.png)

Words often have multiple meanings. For example, "quantum" could refer to:

* A discrete unit of physical quantity (physics)
* Quantum mechanics or quantum physics concepts
* Something extremely small or subatomic
* Quantum computing applications

### Contextualization

Claude refines each embedding based on surrounding words to determine the most likely meaning in context. This process adjusts the numerical representations to highlight the appropriate definition.

![alt text](images/embeddings-example.png)

### Generation

The contextualized embeddings pass through an output layer that calculates probabilities for each possible next word. Claude doesn't always pick the highest probability word - it uses a mix of probability and controlled randomness to create natural, varied responses.

![alt text](images/output-layer-probabilities.png)

After selecting each word, Claude adds it to the sequence and repeats the entire process for the next word.

## When Claude Stops Generating

After each token, Claude checks several conditions to decide whether to continue:

![alt text](images/generation-stop-conditions.png)

* Max tokens reached - Has it hit the limit you specified?
* Natural ending - Did it generate an end-of-sequence token?
* Stop sequence - Did it encounter a predefined stop phrase?

## The API Response

When generation completes, the API sends back a structured response containing:

* Message - The generated text
* Usage - Count of input and output tokens
* Stop Reason - Why generation ended

![alt text](images/api-response-fields.png)

Your server receives this response and forwards the generated text back to your client application, where it appears in the user interface.


## Temperature

It controls how predictable or creative Claude's responses will be. Understanding how to use it effectively can dramatically improve your AI applications.
![alt text](images/neural-network-next-token.png)

![alt text](images/temperature-ranges.png)

# Streaming

Events
![alt text](images/streaming-event-types-table.png)

Flow
![alt text](images/streaming-event-sequence.png)

# Structured Data

The Problem with Default Responses

By default, when you ask Claude to generate JSON, you might get something like this:
```
_```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
_```
```
This rule captures EC2 instance state changes when instances start running.

The JSON is correct, but it's wrapped in markdown formatting and includes explanatory text. For a web app where users need to copy the raw JSON, this creates friction in the user experience.
The Solution: Assistant Message Prefilling + Stop Sequences

You can combine assistant message prefilling with stop sequences to get exactly the content you want. Here's how it works:

```
messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])
```

This technique works by:

1) The user message tells Claude what to generate
2) The prefilled assistant message makes Claude think it already started a markdown code block
3) Claude continues by writing just the JSON content
4) When Claude tries to close the code block with ```, the stop sequence immediately ends generation

![alt text](images/stop-sequence-example.png)

The result is clean JSON with no extra formatting:

```
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```