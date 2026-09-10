/**
 * courseService.js
 *
 * Integration layer for personalized recommendations, iGOT Karmayogi
 * courses, and NSSTA TPAC programs. Response shapes match the existing
 * frontend pages (LearningPath.jsx's `aiRecommendations`, IGOTCourses.jsx,
 * NSSTAPrograms.jsx).
 */

import { apiGet } from "./apiClient";

/**
 * Get ranked, personalized learning recommendations for an employee.
 * Returns: { employee_id, recommendations: [{ id, title, provider,
 *   category, skill, level, duration, reason, progress, action, priority,
 *   relevanceScore, type, sourceUrl, isDemoData }] }
 */
export async function getRecommendations(employeeId, limit) {
  return apiGet(`/api/recommendations/${encodeURIComponent(employeeId)}`, limit ? { limit } : undefined);
}

/**
 * Get recommended iGOT Karmayogi courses for an employee.
 * Returns: { employee_id, source: "mock"|"live", courses: [...] }
 *
 * NOTE: `source` will be "mock" until real iGOT API credentials are
 * configured on the backend (see ai-backend/.env: IGOT_API_BASE_URL /
 * IGOT_API_KEY). The frontend can use this flag to show a "Demo Data"
 * badge if desired.
 */
export async function getIGOTCourses(employeeId) {
  return apiGet(`/api/recommendations/${encodeURIComponent(employeeId)}/igot`);
}

/**
 * Get recommended NSSTA TPAC training programs for an employee.
 * Returns: { employee_id, source: "mock"|"live", programs: [...] }
 */
export async function getNSSTAPrograms(employeeId) {
  return apiGet(`/api/recommendations/${encodeURIComponent(employeeId)}/nssta`);
}

export default { getRecommendations, getIGOTCourses, getNSSTAPrograms };
