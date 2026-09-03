import { tokenStorage } from "@/lib/token-storage";
// Set the future Django URL in frontend/.env.local (copied from .env.example).
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api";
export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}
export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const accessToken = tokenStorage.getAccess();
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...options.headers,
    },
  });
  // Future: on 401, use the refresh token once, save the new access token, then retry.
  if (!response.ok)
    throw new ApiError(response.status, "The API request failed.");
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}
