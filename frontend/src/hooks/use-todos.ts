"use client";
import { useMemo, useState } from "react";
import type { Todo } from "@/types/todo";
const starterTodos: Todo[] = [
  {
    id: "1",
    title: "Map the Django data model",
    completed: true,
    createdAt: "Today",
  },
  {
    id: "2",
    title: "Design the first API endpoint",
    completed: false,
    createdAt: "Today",
  },
  {
    id: "3",
    title: "Test the response in Postman",
    completed: false,
    createdAt: "Tomorrow",
  },
];
// Local mock state is intentional. Later, call todoService here without rewriting UI.
export function useTodos() {
  const [todos, setTodos] = useState<Todo[]>(starterTodos);
  const [notice, setNotice] = useState("");
  const completed = useMemo(
    () => todos.filter((todo) => todo.completed).length,
    [todos],
  );
  const flash = (message: string) => {
    setNotice(message);
    window.setTimeout(() => setNotice(""), 2400);
  };
  const add = (title: string) => {
    setTodos((items) => [
      {
        id: crypto.randomUUID(),
        title,
        completed: false,
        createdAt: "Just now",
      },
      ...items,
    ]);
    flash("Task added");
  };
  const update = (id: string, title: string) => {
    setTodos((items) =>
      items.map((item) => (item.id === id ? { ...item, title } : item)),
    );
    flash("Task updated");
  };
  const toggle = (id: string) =>
    setTodos((items) =>
      items.map((item) =>
        item.id === id ? { ...item, completed: !item.completed } : item,
      ),
    );
  const remove = (id: string) => {
    setTodos((items) => items.filter((item) => item.id !== id));
    flash("Task deleted");
  };
  return { todos, completed, notice, add, update, toggle, remove };
}
