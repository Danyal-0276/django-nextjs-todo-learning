"use client";
import { Header } from "@/components/layout/header";
import { TodoForm } from "@/components/todos/todo-form";
import { TodoList } from "@/components/todos/todo-list";
import { useTodos } from "@/hooks/use-todos";
export function TodoDashboard() {
  const { todos, completed, notice, add, update, toggle, remove } = useTodos();
  const remaining = todos.length - completed;
  return (
    <main className="min-h-screen">
      <Header />
      <section className="mx-auto w-full max-w-4xl px-5 pb-20 pt-8 sm:px-8 sm:pt-14">
        <div className="animate-rise flex flex-col justify-between gap-6 sm:flex-row sm:items-end">
          <div>
            <p className="text-sm font-extrabold uppercase tracking-[.18em] text-accent">
              Thursday · Your workspace
            </p>
            <h1 className="mt-3 font-display text-5xl font-semibold tracking-[-.04em] sm:text-6xl">
              Good evening, Doni.
            </h1>
            <p className="mt-3 text-muted">One thoughtful step at a time.</p>
          </div>
          <div className="rounded-2xl border border-line bg-card px-5 py-4 text-right">
            <strong className="font-display text-3xl">{remaining}</strong>
            <p className="text-xs font-bold uppercase tracking-wider text-muted">
              left to do
            </p>
          </div>
        </div>
        <div className="mt-10 rounded-[2rem] border border-line bg-white/55 p-5 shadow-[0_24px_70px_rgba(24,49,44,.09)] backdrop-blur sm:p-8">
          <TodoForm onAdd={add} />
          <div className="my-7 flex items-center justify-between border-b border-line pb-4">
            <h2 className="font-display text-2xl font-semibold">
              Today&apos;s list
            </h2>
            <p className="text-sm font-bold text-muted">
              {completed} of {todos.length} complete
            </p>
          </div>
          <TodoList
            todos={todos}
            onToggle={toggle}
            onUpdate={update}
            onDelete={remove}
          />
        </div>
        <p className="mt-5 text-center text-xs font-semibold text-muted">
          Mock data resets when you refresh. API integration is intentionally
          planned, not active.
        </p>
        <div
          aria-live="polite"
          aria-atomic="true"
          className={`fixed right-5 bottom-5 rounded-xl bg-ink px-5 py-3 text-sm font-bold text-white shadow-xl transition ${notice ? "translate-y-0 opacity-100" : "pointer-events-none translate-y-3 opacity-0"}`}
        >
          {notice}
        </div>
      </section>
    </main>
  );
}
