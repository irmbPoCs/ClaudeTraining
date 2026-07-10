import { test, expect, afterEach } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";
import {
  ToolInvocationBadge,
  getToolInvocationMessage,
} from "../ToolInvocationBadge";
import type { ToolInvocation } from "ai";

afterEach(() => {
  cleanup();
});

test("shows 'Creating' message and spinner while a file is being created", () => {
  const toolInvocation = {
    toolCallId: "1",
    toolName: "str_replace_editor",
    args: { command: "create", path: "App.jsx" },
    state: "call",
  } as ToolInvocation;

  const { container } = render(
    <ToolInvocationBadge toolInvocation={toolInvocation} />
  );

  expect(screen.getByText("Creating App.jsx")).toBeDefined();
  expect(container.querySelector(".animate-spin")).not.toBeNull();
  expect(container.querySelector(".bg-emerald-500")).toBeNull();
});

test("shows 'Created' message and success dot once a file has been created", () => {
  const toolInvocation = {
    toolCallId: "1",
    toolName: "str_replace_editor",
    args: { command: "create", path: "App.jsx" },
    state: "result",
    result: "Success",
  } as ToolInvocation;

  const { container } = render(
    <ToolInvocationBadge toolInvocation={toolInvocation} />
  );

  expect(screen.getByText("Created App.jsx")).toBeDefined();
  expect(container.querySelector(".bg-emerald-500")).not.toBeNull();
  expect(container.querySelector(".animate-spin")).toBeNull();
});

test("uses only the file's basename, not the full path", () => {
  const toolInvocation = {
    toolCallId: "1",
    toolName: "str_replace_editor",
    args: { command: "str_replace", path: "src/components/Button.tsx" },
    state: "result",
    result: "Success",
  } as ToolInvocation;

  render(<ToolInvocationBadge toolInvocation={toolInvocation} />);

  expect(screen.getByText("Edited Button.tsx")).toBeDefined();
});

test("shows 'Editing' message for an in-progress insert command", () => {
  const toolInvocation = {
    toolCallId: "1",
    toolName: "str_replace_editor",
    args: { command: "insert", path: "Button.tsx" },
    state: "call",
  } as ToolInvocation;

  render(<ToolInvocationBadge toolInvocation={toolInvocation} />);

  expect(screen.getByText("Editing Button.tsx")).toBeDefined();
});

test("shows 'Viewed' message for a completed view command", () => {
  const toolInvocation = {
    toolCallId: "1",
    toolName: "str_replace_editor",
    args: { command: "view", path: "Button.tsx" },
    state: "result",
    result: "file contents",
  } as ToolInvocation;

  render(<ToolInvocationBadge toolInvocation={toolInvocation} />);

  expect(screen.getByText("Viewed Button.tsx")).toBeDefined();
});

test("shows rename message with both old and new file names", () => {
  const toolInvocation = {
    toolCallId: "1",
    toolName: "file_manager",
    args: { command: "rename", path: "old-name.js", new_path: "new-name.js" },
    state: "result",
    result: { success: true, message: "Successfully renamed" },
  } as ToolInvocation;

  render(<ToolInvocationBadge toolInvocation={toolInvocation} />);

  expect(screen.getByText("Renamed old-name.js to new-name.js")).toBeDefined();
});

test("shows 'Deleting' message for an in-progress delete command", () => {
  const toolInvocation = {
    toolCallId: "1",
    toolName: "file_manager",
    args: { command: "delete", path: "old-file.js" },
    state: "call",
  } as ToolInvocation;

  render(<ToolInvocationBadge toolInvocation={toolInvocation} />);

  expect(screen.getByText("Deleting old-file.js")).toBeDefined();
});

test("does not crash and shows a fallback when args are missing (partial-call)", () => {
  const toolInvocation = {
    toolCallId: "1",
    toolName: "str_replace_editor",
    args: {},
    state: "partial-call",
  } as ToolInvocation;

  render(<ToolInvocationBadge toolInvocation={toolInvocation} />);

  expect(screen.getByText("Updating file")).toBeDefined();
});

test("falls back to the raw tool name for an unrecognized tool", () => {
  const toolInvocation = {
    toolCallId: "1",
    toolName: "some_other_tool",
    args: {},
    state: "result",
    result: "done",
  } as ToolInvocation;

  render(<ToolInvocationBadge toolInvocation={toolInvocation} />);

  expect(screen.getByText("some_other_tool")).toBeDefined();
});

test("getToolInvocationMessage maps str_replace_editor commands and tenses", () => {
  const make = (command: string, state: string, result?: unknown) =>
    ({
      toolCallId: "1",
      toolName: "str_replace_editor",
      args: { command, path: "App.jsx" },
      state,
      ...(result !== undefined ? { result } : {}),
    }) as ToolInvocation;

  expect(getToolInvocationMessage(make("create", "call"))).toBe(
    "Creating App.jsx"
  );
  expect(getToolInvocationMessage(make("create", "result", "ok"))).toBe(
    "Created App.jsx"
  );
  expect(getToolInvocationMessage(make("str_replace", "call"))).toBe(
    "Editing App.jsx"
  );
  expect(getToolInvocationMessage(make("insert", "result", "ok"))).toBe(
    "Edited App.jsx"
  );
  expect(getToolInvocationMessage(make("view", "call"))).toBe(
    "Viewing App.jsx"
  );
  expect(getToolInvocationMessage(make("undo_edit", "call"))).toBe(
    "Updating App.jsx"
  );
});

test("getToolInvocationMessage maps file_manager commands and tenses", () => {
  const rename = {
    toolCallId: "1",
    toolName: "file_manager",
    args: { command: "rename", path: "a.js", new_path: "b.js" },
    state: "call",
  } as ToolInvocation;

  const deleteDone = {
    toolCallId: "1",
    toolName: "file_manager",
    args: { command: "delete", path: "a.js" },
    state: "result",
    result: { success: true },
  } as ToolInvocation;

  expect(getToolInvocationMessage(rename)).toBe("Renaming a.js to b.js");
  expect(getToolInvocationMessage(deleteDone)).toBe("Deleted a.js");
});
