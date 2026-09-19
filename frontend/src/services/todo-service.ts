import { apiRequest } from "@/lib/api-client";
import type { CreateTodoInput, Todo, UpdateTodoInput } from "@/types/todo";
// Real CRUD requests sent to the authenticated Django Todo API.
export const todoService = {
  list: () => apiRequest<Todo[]>("/todos/"),
  create: (data: CreateTodoInput) =>
    apiRequest<Todo>("/todos/", { method: "POST", body: JSON.stringify(data) }),
  update: (id: number, data: UpdateTodoInput) =>
    apiRequest<Todo>(`/todos/${id}/`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  remove: (id: number) =>
    apiRequest<void>(`/todos/${id}/`, {
      method: "DELETE",
    }),
};
