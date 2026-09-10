/**
 * assistantService.js
 *
 * New service (not one of the originally-empty stubs) for the AI learning
 * assistant, used by AIAssistant.jsx. Not requested explicitly in the
 * original file list, but required to support "POST /api/assistant/chat"
 * from the frontend - included here for completeness. Safe to delete if
 * unused.
 */

import { apiPost } from "./apiClient";

/**
 * Send a message to the AI learning assistant.
 *
 * @param {string} employeeId
 * @param {string} message
 * @param {string} [materialId] - if provided, the assistant uses RAG over that material
 * Returns: { answer, sources: [{material_id, material_title, chunk_id, text_preview}],
 *            used_rag, mode: "rag"|"profile"|"general" }
 */
export async function sendMessage(employeeId, message, materialId) {
  return apiPost("/api/assistant/chat", {
    employee_id: employeeId,
    message,
    material_id: materialId,
  });
}

export default { sendMessage };
