# MCP Servers

You can extend Claude Code's capabilities by adding MCP (Model Context Protocol) servers. These servers run either remotely or locally on your machine and provide Claude with new tools and abilities it wouldn't normally have.

One of the most popular MCP servers is Playwright, which gives Claude the ability to control a web browser. This opens up powerful possibilities for web development workflows.

## Installing MPC Server

```
claude mcp add <mcp_servevr>
```

Example

```
claude mcp add playwright npx @playwright/mcp@latest
```

## Permissions

> .claude/settings.local.json

```
{
  "permissions": {
    "allow": ["mcp__playwright"],
    "deny": []
  }
}
```

## Exploring Other MCP Servers

Playwright is just one example of what's possible with MCP servers. The ecosystem includes servers for:

    Database interactions
    API testing and monitoring
    File system operations
    Cloud service integrations
    Development tool automation

Consider exploring MCP servers that align with your specific development needs. They can transform Claude from a code assistant into a comprehensive development partner that can interact with your entire toolchain.