import type { AuthTokens } from "@/types/auth";
const ACCESS_KEY="daymark_access_token"; const REFRESH_KEY="daymark_refresh_token";
// For learning only: localStorage is convenient but exposed to JavaScript. Before
// production, compare this with secure HttpOnly cookies and understand XSS/CSRF.
export const tokenStorage={
  getAccess:()=>typeof window==="undefined"?null:localStorage.getItem(ACCESS_KEY),
  getRefresh:()=>typeof window==="undefined"?null:localStorage.getItem(REFRESH_KEY),
  save(tokens:AuthTokens){ localStorage.setItem(ACCESS_KEY,tokens.access); localStorage.setItem(REFRESH_KEY,tokens.refresh); },
  clear(){ localStorage.removeItem(ACCESS_KEY); localStorage.removeItem(REFRESH_KEY); },
};
