import type { Todo } from "@/types/todo";
import { TodoItem } from "@/components/todos/todo-item";

type TodoListProps = {
  todos: Todo[];
  onToggle: (id: number) => void | Promise<void>;
  onUpdate: (id: number, title: string) => void | Promise<void>;
  onDelete: (id: number) => void | Promise<void>;
};

export function TodoList({
  todos,
  onToggle,
  onUpdate,
  onDelete,
}: TodoListProps) {
  if (!todos.length) {
    return (
      <div className="rounded-2xl border border-dashed border-[#aab4b1] px-6 py-14 text-center">
        <div
          className="mx-auto grid size-12 place-items-center rounded-2xl bg-[#e1eee9] text-xl"
          aria-hidden
        >
          ✓
        </div>

        <h3 className="mt-4 font-display text-2xl font-semibold">
          Your list is clear
        </h3>

        <p className="mt-1 text-sm text-muted">
          Add a task above when something comes to mind.
        </p>
      </div>
    );
  }

  return (
    <ul className="grid gap-3">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={() => onToggle(todo.id)}
          onUpdate={(title) => onUpdate(todo.id, title)}
          onDelete={() => onDelete(todo.id)}
        />
      ))}
    </ul>
  );
}
