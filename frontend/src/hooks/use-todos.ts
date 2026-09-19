"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { ApiError } from "@/lib/api-client";
import { tokenStorage } from "@/lib/token-storage";
import { todoService } from "@/services/todo-service";
import type { Todo } from "@/types/todo";

function getErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    const firstError = Object.values(error.data)[0];

    if (Array.isArray(firstError)) {
      return firstError[0] ?? error.message;
    }

    return firstError ?? error.message;
  }

  return "Could not connect to the server. Please try again.";
}

export function useTodos() {
  const router = useRouter();

  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const completed = useMemo(
    () => todos.filter((todo) => todo.completed).length,
    [todos],
  );

  const flash = (message: string) => {
    setNotice(message);
    window.setTimeout(() => setNotice(""), 2400);
  };

  const handleRequestError = useCallback(
    (caughtError: unknown) => {
      if (caughtError instanceof ApiError && caughtError.status === 401) {
        tokenStorage.clear();
        router.replace("/login");
        return;
      }

      setError(getErrorMessage(caughtError));
    },
    [router],
  );

  useEffect(() => {
    let cancelled = false;

    todoService
      .list()
      .then((data) => {
        if (!cancelled) {
          setTodos(data);
        }
      })
      .catch((caughtError: unknown) => {
        if (!cancelled) {
          handleRequestError(caughtError);
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [handleRequestError]);

  const add = async (title: string) => {
    setError("");

    try {
      const createdTodo = await todoService.create({
        title,
      });

      setTodos((items) => [createdTodo, ...items]);
      flash("Task added");
    } catch (caughtError) {
      handleRequestError(caughtError);
    }
  };

  const update = async (id: number, title: string) => {
    setError("");

    try {
      const updatedTodo = await todoService.update(id, {
        title,
      });

      setTodos((items) =>
        items.map((item) => (item.id === id ? updatedTodo : item)),
      );

      flash("Task updated");
    } catch (caughtError) {
      handleRequestError(caughtError);
    }
  };

  const toggle = async (id: number) => {
    const currentTodo = todos.find((todo) => todo.id === id);

    if (!currentTodo) {
      return;
    }

    setError("");

    try {
      const updatedTodo = await todoService.update(id, {
        completed: !currentTodo.completed,
      });

      setTodos((items) =>
        items.map((item) => (item.id === id ? updatedTodo : item)),
      );

      flash(
        updatedTodo.completed
          ? "Task completed"
          : "Task marked incomplete",
      );
    } catch (caughtError) {
      handleRequestError(caughtError);
    }
  };

  const remove = async (id: number) => {
    setError("");

    try {
      await todoService.remove(id);

      setTodos((items) => items.filter((item) => item.id !== id));
      flash("Task deleted");
    } catch (caughtError) {
      handleRequestError(caughtError);
    }
  };

  return {
    todos,
    completed,
    loading,
    error,
    notice,
    add,
    update,
    toggle,
    remove,
  };
}