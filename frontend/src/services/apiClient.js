/**
 * Shared HTTP client for talking to the AI backend.
 *
 * The backend URL is read from VITE_API_URL (see .env.example) so it is
 * never hardcoded anywhere else in the app. Falls back to
 * http://localhost:8000 for local development if the env var isn't set.
 *
 * Usage:
 *   import { apiGet, apiPost, apiUpload } from "./apiClient";
 *   const data = await apiGet("/api/competency/EMP001");
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  constructor(message, status, details) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

async function handleResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const body = isJson ? await response.json().catch(() => null) : await response.text();

  if (!response.ok) {
    const message =
      (body && typeof body === "object" && (body.detail || body.message)) ||
      `Request failed with status ${response.status}`;
    throw new ApiError(
      typeof message === "string" ? message : JSON.stringify(message),
      response.status,
      body
    );
  }
  return body;
}

export async function apiGet(path, params) {
  const url = new URL(API_BASE_URL + path);
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) url.searchParams.set(key, value);
    });
  }
  const response = await fetch(url.toString(), {
    method: "GET",
    headers: { Accept: "application/json" },
  });
  return handleResponse(response);
}

export async function apiPost(path, body) {
  const response = await fetch(API_BASE_URL + path, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(body ?? {}),
  });
  return handleResponse(response);
}

export async function apiUpload(path, formData) {
  const response = await fetch(API_BASE_URL + path, {
    method: "POST",
    body: formData, // browser sets the multipart Content-Type boundary automatically
  });
  return handleResponse(response);
}

export { API_BASE_URL };
