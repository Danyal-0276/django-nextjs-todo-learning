import { tokenStorage } from "@/lib/token-storage";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api";

export type ApiErrorData = Record<string, string | string[]>;

export class ApiError extends Error {
  constructor(
    public status: number,
    public data: ApiErrorData,
  ) {
    const detail = data.detail;

    const message = Array.isArray(detail)
      ? detail[0]
      : (detail ?? "The API request failed.");

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

  if (!response.ok) {
    let errorData: ApiErrorData = {};

    try {
      errorData = (await response.json()) as ApiErrorData;
    } catch {
      // The server did not return JSON.
    }

    throw new ApiError(response.status, errorData);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}
