# Claude Agent SDK

The Agent SDK lets you run Claude Code programmatically from your own applications and scripts. It's available for TypeScript and Python, and gives you the same agent loop the CLI uses — file reading, editing, tool use — under your control.

## Installation

Create a directory for the project and install the SDK package:

```bash
mkdir sdk-demo
cd sdk-demo
npm init -y
npm install @anthropic-ai/claude-agent-sdk
```

The package is `@anthropic-ai/claude-agent-sdk`. (The similarly-named `@anthropic-ai/claude-code` is the CLI itself and can't be imported.)

## A Minimal Example

Create a file called `index.mjs` using your editor (or `nano index.mjs` in the terminal) and paste:

```javascript
import { query } from "@anthropic-ai/claude-agent-sdk";

const prompt = "List the files in the current directory";

for await (const message of query({ prompt })) {
  console.log(JSON.stringify(message, null, 2));
}
```

Run it:

```bash
node index.mjs
```

You'll see a stream of JSON messages — the same conversation events you'd see in the CLI, including tool calls, tool results, and Claude's text.

## Restricting Tools

By default the SDK has access to the full tool set. To narrow it, pass `allowedTools`:

```javascript
for await (const message of query({
  prompt,
  options: { allowedTools: ["Read", "Glob"] },
})) {
  // ...
}
```

This is the SDK equivalent of the CLI's `--allowedTools` flag.

## Where to Go Next

The SDK supports everything the CLI does: custom system prompts, MCP servers, hooks, subagents, and session resumption. See the [Agent SDK documentation](https://anthropic.com) for the full reference.