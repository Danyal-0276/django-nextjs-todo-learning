import { apiRequest } from "@/lib/api-client";
import type {
  AuthTokens,
  AuthUser,
  LoginCredentials,
  RegisterPayload,
} from "@/types/auth";
// Planned only: the mock forms do not call these until Django REST endpoints exist.
export const authService = {
  login: (data: LoginCredentials) =>
    apiRequest<AuthTokens>("/auth/token/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  register: (data: RegisterPayload) =>
    apiRequest<AuthUser>("/auth/register/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  refresh: (refresh: string) =>
    apiRequest<Pick<AuthTokens, "access">>("/auth/token/refresh/", {
      method: "POST",
      body: JSON.stringify({ refresh }),
    }),
};
