"use client";

import { FormEvent, useState } from "react";
import type { Todo } from "@/types/todo";
import { Button } from "@/components/ui/button";

type TodoItemProps = {
  todo: Todo;
  onToggle: () => void | Promise<void>;
  onUpdate: (title: string) => void | Promise<void>;
  onDelete: () => void | Promise<void>;
};

function formatCreatedAt(createdAt: string) {
  const date = new Date(createdAt);

  if (Number.isNaN(date.getTime())) {
    return "Date unavailable";
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function TodoItem({
  todo,
  onToggle,
  onUpdate,
  onDelete,
}: TodoItemProps) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(todo.title);

  function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const cleanedTitle = title.trim();

    if (!cleanedTitle) {
      return;
    }

    onUpdate(cleanedTitle);
    setEditing(false);
  }

  function cancelEditing() {
    setTitle(todo.title);
    setEditing(false);
  }

  return (
    <li className="group rounded-2xl border border-line bg-card p-4 transition hover:-translate-y-0.5 hover:shadow-[0_12px_32px_rgba(24,49,44,.08)]">
      {editing ? (
        <form onSubmit={save} className="flex flex-col gap-3 sm:flex-row">
          <label className="sr-only" htmlFor={`edit-${todo.id}`}>
            Edit task
          </label>

          <input
            id={`edit-${todo.id}`}
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            maxLength={120}
            autoFocus
            className="h-11 flex-1 rounded-xl border border-ink bg-white px-3 outline-none ring-4 ring-[#b9dfd166]"
          />

          <Button type="submit">Save</Button>

          <Button
            type="button"
            variant="secondary"
            onClick={cancelEditing}
          >
            Cancel
          </Button>
        </form>
      ) : (
        <div className="flex items-start gap-3">
          <button
            type="button"
            onClick={onToggle}
            aria-label={`${
              todo.completed ? "Mark incomplete" : "Mark complete"
            }: ${todo.title}`}
            className={`mt-0.5 grid size-7 shrink-0 place-items-center rounded-lg border-2 transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent ${
              todo.completed
                ? "border-ink bg-ink text-white"
                : "border-[#9ba7a3] hover:border-ink"
            }`}
          >
            {todo.completed && <span aria-hidden>✓</span>}
          </button>

          <div className="min-w-0 flex-1">
            <p
              className={`font-bold leading-7 ${
                todo.completed
                  ? "text-muted line-through decoration-2"
                  : "text-ink"
              }`}
            >
              {todo.title}
            </p>

            <p className="mt-1 text-xs font-semibold uppercase tracking-wider text-muted">
              {formatCreatedAt(todo.created_at)}
            </p>
          </div>

          <div className="flex shrink-0 gap-1">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setEditing(true)}
              aria-label={`Edit ${todo.title}`}
              className="px-3"
            >
              Edit
            </Button>

            <Button
              type="button"
              variant="danger"
              onClick={onDelete}
              aria-label={`Delete ${todo.title}`}
              className="px-3"
            >
              Delete
            </Button>
          </div>
        </div>
      )}
    </li>
  );
}
