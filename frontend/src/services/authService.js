import { apiFetch, setSession, clearSession } from "./api.js";

export async function login(email, password) {
  const data = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  setSession(data.token, data.user);
  return data;
}

export async function getMe() {
  const data = await apiFetch("/auth/me");
  if (data.user) setSession(null, data.user);
  return data.user;
}

export function logout() {
  clearSession();
}
