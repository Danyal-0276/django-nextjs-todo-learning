export interface LoginCredentials {
  username: string;
  password: string;
}
export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}
export interface AuthTokens {
  access: string;
  refresh: string;
}
export interface AuthUser {
  id: number;
  username: string;
  email: string;
}
