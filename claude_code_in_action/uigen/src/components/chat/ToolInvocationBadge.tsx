"use client";

import { Loader2 } from "lucide-react";
import type { ToolInvocation } from "ai";

interface ToolInvocationBadgeProps {
  toolInvocation: ToolInvocation;
}

function basename(path?: string): string | undefined {
  if (!path) return undefined;
  const parts = path.split(/[/\\]/).filter(Boolean);
  return parts[parts.length - 1] || path;
}

export function getToolInvocationMessage(toolInvocation: ToolInvocation): string {
  const { toolName, args, state } = toolInvocation;
  const isDone =
    state === "result" && "result" in toolInvocation && !!toolInvocation.result;

  const command = (args as { command?: string } | undefined)?.command;
  const file = basename((args as { path?: string } | undefined)?.path) ?? "file";

  if (toolName === "str_replace_editor") {
    switch (command) {
      case "create":
        return isDone ? `Created ${file}` : `Creating ${file}`;
      case "str_replace":
      case "insert":
        return isDone ? `Edited ${file}` : `Editing ${file}`;
      case "view":
        return isDone ? `Viewed ${file}` : `Viewing ${file}`;
      default:
        return isDone ? `Updated ${file}` : `Updating ${file}`;
    }
  }

  if (toolName === "file_manager") {
    switch (command) {
      case "rename": {
        const newFile =
          basename((args as { new_path?: string } | undefined)?.new_path) ?? "file";
        return isDone
          ? `Renamed ${file} to ${newFile}`
          : `Renaming ${file} to ${newFile}`;
      }
      case "delete":
        return isDone ? `Deleted ${file}` : `Deleting ${file}`;
      default:
        return isDone ? `Updated ${file}` : `Updating ${file}`;
    }
  }

  return toolName;
}

export function ToolInvocationBadge({ toolInvocation }: ToolInvocationBadgeProps) {
  const isDone =
    toolInvocation.state === "result" &&
    "result" in toolInvocation &&
    !!toolInvocation.result;
  const message = getToolInvocationMessage(toolInvocation);

  return (
    <div className="inline-flex items-center gap-2 mt-2 px-3 py-1.5 bg-neutral-50 rounded-lg text-xs font-mono border border-neutral-200">
      {isDone ? (
        <>
          <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
          <span className="text-neutral-700">{message}</span>
        </>
      ) : (
        <>
          <Loader2 className="w-3 h-3 animate-spin text-blue-600" />
          <span className="text-neutral-700">{message}</span>
        </>
      )}
    </div>
  );
}
