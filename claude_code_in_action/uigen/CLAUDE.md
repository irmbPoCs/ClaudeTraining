# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

UIGen: a Next.js app that generates React components with Claude (via Vercel AI SDK) and renders them live in a sandboxed iframe preview — without ever writing generated files to disk. Generated code lives entirely in an in-memory virtual file system that gets serialized into SQLite for persistence.

## Commands

```bash
npm run setup       # install deps + prisma generate + migrate dev (run this first)
npm run dev         # start dev server (Turbopack) at http://localhost:3000
npm run build       # production build
npm run lint        # next lint
npm test            # run vitest once (not watch mode by default)
npm run db:reset    # reset the SQLite dev database (destructive)
```

Run a single test file: `npx vitest run src/lib/__tests__/file-system.test.ts`
Run tests matching a name: `npx vitest run -t "normalizes paths"`

**Never run `npm audit fix`** — dependency versions are pinned deliberately for compatibility; `audit fix` can bump packages past what works. Fix known CVEs by bumping the specific pinned version instead.

No API key is required to run the app. Without `ANTHROPIC_API_KEY` set in `.env` (or left as the placeholder), [src/lib/provider.ts](src/lib/provider.ts) falls back to `MockLanguageModel`, a canned/scripted responder used for local dev and tests.

## Architecture

### Virtual file system, not disk

[src/lib/file-system.ts](src/lib/file-system.ts) (`VirtualFileSystem`) is an in-memory tree of files/directories. All AI-generated code lives here — nothing is written to the real filesystem. It supports editor-style operations (`view`, `create`, `str_replace`, `insert`) plus rename/delete, and can `serialize()`/`deserializeFromNodes()` to/from a plain object for storage or transport between server and client.

### Client-side state: two nested contexts

`MainContent` ([src/app/main-content.tsx](src/app/main-content.tsx)) wraps the workspace in:
- **`FileSystemProvider`** ([src/lib/contexts/file-system-context.tsx](src/lib/contexts/file-system-context.tsx)) — owns the single `VirtualFileSystem` instance for the session, exposes CRUD helpers, and has `handleToolCall()` which applies AI tool calls (`str_replace_editor`, `file_manager`) to the file system and bumps a `refreshTrigger` to re-render dependents.
- **`ChatProvider`** ([src/lib/contexts/chat-context.tsx](src/lib/contexts/chat-context.tsx)) — wraps `@ai-sdk/react`'s `useChat`, posts to `/api/chat` with the serialized file system + `projectId`, and forwards every `onToolCall` to `FileSystemContext.handleToolCall`. This is the wiring that makes AI responses actually mutate the visible file tree/preview.

For anonymous (non-authenticated) users, [src/lib/anon-work-tracker.ts](src/lib/anon-work-tracker.ts) mirrors messages + file system state into `sessionStorage` so in-progress work isn't lost across a sign-up/sign-in flow.

### Generation flow (server)

[src/app/api/chat/route.ts](src/app/api/chat/route.ts) is the only AI entry point:
1. Prepends the system prompt ([src/lib/prompts/generation.tsx](src/lib/prompts/generation.tsx)) with Anthropic prompt caching enabled.
2. Rehydrates a server-side `VirtualFileSystem` from the client's serialized files.
3. Calls `streamText` with two tools bound to that file system instance:
   - `str_replace_editor` ([src/lib/tools/str-replace.ts](src/lib/tools/str-replace.ts)) — view/create/str_replace/insert (`undo_edit` is intentionally unimplemented).
   - `file_manager` ([src/lib/tools/file-manager.ts](src/lib/tools/file-manager.ts)) — rename/delete.
4. `maxSteps` is capped at 4 for the mock provider (to avoid repetition loops) vs 40 for real Claude.
5. On finish, if `projectId` is present, persists the updated message history and serialized file system back to the `Project` row — gated on `getSession()` succeeding and owning that project.

### Live preview (client)

[src/components/preview/PreviewFrame.tsx](src/components/preview/PreviewFrame.tsx) re-renders whenever the file system's `refreshTrigger` changes. [src/lib/transform/jsx-transformer.ts](src/lib/transform/jsx-transformer.ts) does the heavy lifting entirely in-browser:
- Transpiles each JS/JSX/TS/TSX file with `@babel/standalone` and turns it into a `Blob` URL.
- Builds a browser **import map** so bare specifiers resolve to those blob URLs; unresolved third-party packages are pointed at `esm.sh`; unresolved local imports get a placeholder module so a broken/missing import doesn't crash the whole preview.
- Assembles a full HTML document (Tailwind via CDN script, an inline `ErrorBoundary`, syntax-error panel) and injects it via `iframe.srcdoc` — the iframe is sandboxed with `allow-scripts allow-same-origin allow-forms`.
- Entry point resolution tries `/App.jsx`, `/App.tsx`, `/index.jsx`, `/index.tsx`, `/src/App.jsx`, `/src/App.tsx`, then falls back to the first `.jsx`/`.tsx` file found.

### Auth & persistence

- JWT sessions via `jose`, stored in an httpOnly `auth-token` cookie ([src/lib/auth.ts](src/lib/auth.ts)). `JWT_SECRET` env var, falls back to a dev default if unset.
- [src/middleware.ts](src/middleware.ts) only gates `/api/projects` and `/api/filesystem` — it does **not** protect `/api/chat`; that route checks session itself before persisting.
- Prisma + SQLite ([prisma/schema.prisma](prisma/schema.prisma)): `User` and `Project`. `Project.messages` and `Project.data` are JSON stored as strings (not native JSON columns) — serialize/deserialize on every read/write. `Project.userId` is optional, allowing (in principle) projects unlinked to a user.
- Server actions live in [src/actions/](src/actions/) (`"use server"`), not API routes, for auth/signup/signin/project CRUD.
- Prisma client is generated to `src/generated/prisma` (not `node_modules/.prisma`) per the `generator client { output = ... }` in the schema — regenerate with `npx prisma generate` after schema changes, and don't hand-edit files under that path.

### Windows/Node-version compatibility shims

- [node-compat.cjs](node-compat.cjs) deletes global `localStorage`/`sessionStorage` on the server when running on Node 25+, which otherwise exposes a broken Web Storage API that breaks SSR guard checks (`typeof localStorage === "undefined"`). It's imported at the top of [next.config.ts](next.config.ts) so it runs before any app code.
- `next.config.ts` pins Turbopack's workspace root to `process.cwd()` to prevent a stray lockfile/package.json elsewhere on the machine from hijacking module resolution.

## Testing

Vitest + jsdom + React Testing Library ([vitest.config.mts](vitest.config.mts)). Tests are colocated in `__tests__` directories next to the code they cover (e.g. [src/lib/__tests__/file-system.test.ts](src/lib/__tests__/file-system.test.ts), [src/components/chat/__tests__/](src/components/chat/__tests__/)). Path alias `@/*` → `src/*` is honored in tests via `vite-tsconfig-paths`.

## UI components

shadcn/ui ("new-york" style, neutral base color) — see [components.json](components.json) for aliases (`@/components`, `@/components/ui`, `@/lib`, `@/hooks`). Icons via `lucide-react`.

## Code style

Use comments sparingly. Only comment complex code.
