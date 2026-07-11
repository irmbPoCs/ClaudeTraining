# Claude Code Cheat Sheet

## Model & Configuration
- `/model` — Open model picker (Sonnet, Opus, Haiku, Fable)
- `/config` — Quick access to settings (model, theme, etc.)
- `/fast` — Toggle fast mode for quicker responses

## Planning & Review
- `/plan` — Enter plan mode to design before implementing
- `/code-review` — Review current diff for bugs and improvements
- `/code-review ultra` — Deep multi-agent cloud review
- `/code-review <PR#>` — Review a GitHub pull request
- `/simplify` — Simplify and clean up changed code
- `/security-review` — Security review of pending changes

## Execution & Verification
- `/run` — Launch and drive the project app
- `/verify` — Verify changes work end-to-end in the real app

## Project & Documentation
- `/review <PR#>` — Review a GitHub pull request
- `/init` — Initialize a new CLAUDE.md file with codebase documentation

### CLAUDE.md File Hierarchy
Claude Code reads `CLAUDE.md` files at multiple levels to understand project context and your preferences:

**Project-level CLAUDE.md** (Root Directory)
- Lives in the root directory of your project
- Shared with the team and checked into version control
- Contains: project architecture, build/test commands, coding conventions, team guidelines
- Example location: `/your-project/CLAUDE.md`

**Directory-specific CLAUDE.md** (Subdirectories)
- Specialized guidance for specific modules, packages, or subdirectories
- Provides context for that area of the codebase
- Overrides project-level guidance when more specific

**User-level CLAUDE.md** (Configuration Folder)
- Lives in your personal Claude Code configuration folder
- Just for you — never shared with the team
- Contains: your personal preferences, common commands you use across projects, private workflows
- Location: `~/.claude/CLAUDE.md` (or your system's Claude config folder)

**Search Precedence**
Claude Code searches from most specific to most general:
1. Current directory's CLAUDE.md (if any)
2. Parent directories' CLAUDE.md (if any)
3. Project root CLAUDE.md
4. User-level CLAUDE.md (applies across all projects)

## Scheduling & Automation
- `/loop <interval> <command>` — Run a command on recurring interval (e.g., `5m`, `30s`)
- `/schedule` — Create scheduled cloud agents with cron schedule

## Workspace & Status
- `/context` — Show context usage and available tokens
- `/clear` — Clear conversation (context-dependent)
- `/mcp` — Manage MCP tools and servers
- `/skills` — Show available skills
- `/compact` — Resizes the context size

## Memory & Persistence
- `/remember` — Save information to your personal memory for future sessions
- `/memory` — View, manage, or organize your saved memories
- `/save-feedback` — Record feedback or preferences about how Claude should approach work
- `/forget` — Remove specific memories from your personal memory store

**Memory Types:**
- **User** — Your role, preferences, responsibilities, expertise
- **Feedback** — Rules for how Claude should approach work (what to do/avoid)
- **Project** — Current project goals, deadlines, initiatives, context
- **Reference** — Pointers to external resources (Linear boards, Slack channels, docs)

## Agents

Claude Code includes built-in agent types for specialized tasks. Spawn an agent with the `Agent` tool or by asking Claude directly.

| Agent Type | Purpose |
|---|---|
| **claude** | Catch-all for any task that doesn't fit a more specific agent. Default general-purpose agent. |
| **claude-code-guide** | For questions about Claude Code features, Claude Agent SDK, or Claude API (pricing, models, limits, caching, token counting). |
| **Explore** | Fast read-only search agent for locating code by file patterns, grepping symbols/keywords, or finding where code is defined/referenced. |
| **general-purpose** | For researching complex questions, searching code, and executing multi-step tasks. |
| **Plan** | Software architect agent for designing implementation plans, identifying critical files, and considering architectural trade-offs. |
| **statusline-setup** | Specialized agent to configure Claude Code's status line settings. |

**Custom Subagents:** Define your own subagents in `.claude/agents/` (project-level) or `~/.claude/agents/` (user-level).

## General
- `/help` — Get help using Claude Code
- `! <command>` — Run a shell command in this session

## Keyboard Shortcuts
- **Shift+Tab** — Cycle through permission modes
- **Enter** — Submit prompt
- **Ctrl+L** — Clear conversation (context-dependent)

## Quick Tips
- Set default model: `/config` → model
- Allow permissions globally: Use `/config` or update `settings.json`
- Skip plan mode confirmation: Press **Shift+Tab** to cycle modes
- Check current context: Model, permissions, and mode shown in status line
