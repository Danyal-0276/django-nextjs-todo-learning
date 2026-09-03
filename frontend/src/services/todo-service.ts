import { apiRequest } from "@/lib/api-client";
import type { CreateTodoInput,Todo,UpdateTodoInput } from "@/types/todo";
// Replace the dashboard hook's local handlers with these calls when the API exists.
export const todoService={
  list:()=>apiRequest<Todo[]>("/todos/"),
  create:(data:CreateTodoInput)=>apiRequest<Todo>("/todos/",{method:"POST",body:JSON.stringify(data)}),
  update:(id:string,data:UpdateTodoInput)=>apiRequest<Todo>(`/todos/${id}/`,{method:"PATCH",body:JSON.stringify(data)}),
  remove:(id:string)=>apiRequest<void>(`/todos/${id}/`,{method:"DELETE"}),
};
