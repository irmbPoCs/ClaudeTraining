# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a training and reference guide for Claude Code. It contains:

- **ClaudeCode101/**: Foundational educational content explaining what Claude Code is, how it works, and core workflows
- **CLAUDE_CODE_CHEATSHEET.md**: Quick reference of commonly used Claude Code commands and shortcuts

The purpose is to help users learn Claude Code features and best practices.

## Content Organization

**ClaudeCode101/** is structured as a learning path:
- `01-WhatIsClaudeCode.md` — Introduction to Claude Code and its core concepts
- `02-HowClaudeCodeWorks.md` — Technical explanation of Claude Code internals (in progress)
- `03-PRs.md` — Git and pull request workflows using Claude Code features

**CLAUDE_CODE_CHEATSHEET.md** is organized by category:
- Model & Configuration
- Planning & Review
- Execution & Verification
- Project & Documentation
- Scheduling & Automation
- Workspace & Status
- General
- Keyboard Shortcuts
- Quick Tips

## Maintenance Guidelines

### Markdown Formatting
- Use consistent header levels (# for main titles, ## for sections, ### for subsections)
- Highlight command references with backticks (e.g., `/model`, `--from-pr`)
- Enclose code examples in fenced code blocks with language specification
- Keep line lengths reasonable for readability (under 100 characters where possible)

### Keeping Content Accurate
- Update command references if Claude Code slash commands change
- Verify keyboard shortcuts against the latest Claude Code version
- Test command examples before committing changes
- Document new features promptly as they're released

### Content Consistency
- Match the writing style across all files (clear, concise, practical)
- Use consistent terminology (e.g., "skill" vs "command", "subagent")
- Link to related concepts when appropriate
- Include concrete examples alongside explanations

## How to Contribute

When adding new content:
1. Follow the existing markdown formatting conventions
2. Add entries to the appropriate section (don't create new top-level sections without discussion)
3. Test any commands or instructions you document
4. Keep explanations concise — avoid duplication between files
5. If content belongs in multiple places, link between files rather than duplicating

When updating CLAUDE_CODE_CHEATSHEET.md:
- Maintain alphabetical or logical grouping within sections
- Keep descriptions to one line where possible
- Include practical context (e.g., "e.g., `5m`, `30s`" for `/loop`)

## Common Tasks

**Adding a new slash command to the cheatsheet:**
- Identify the appropriate section based on command category
- Add the entry in consistent format: `- `/command-name` — Description`
- Include examples or context in parentheses if helpful

**Expanding educational content:**
- Write in the second person ("you can", "ask Claude")
- Include real-world examples showing why a feature matters
- Link back to the cheatsheet for quick reference
- Build on concepts introduced in earlier files

**Keeping up with Claude Code updates:**
- Monitor new features and commands released
- Update relevant sections to reflect current capabilities
- Deprecate outdated instructions if features change

## Reference

For current Claude Code documentation and latest features, visit claude.ai/code or run `/help` in Claude Code.
