/**
 * competencyService.js
 *
 * Integration layer between the React frontend and the AI backend's
 * competency & skill-gap endpoints. Response shapes intentionally match
 * the existing mock data in src/data/employeeData.js
 * (competencyOverview, skillGaps) so pages like Competencies.jsx and
 * SkillGaps.jsx can switch from the static import to this service with a
 * minimal code change, e.g.:
 *
 *   // before:
 *   import { competencyOverview } from "../../data/employeeData";
 *
 *   // after:
 *   import { getCompetency } from "../../services/competencyService";
 *   const competencyOverview = await getCompetency(employeeId);
 */

import { apiGet, apiPost } from "./apiClient";

/**
 * Get an employee's competency overview.
 * Returns: { employee_id, overall_competency_pct, current_score,
 *            required_score, total_gap, domains: [{domain,current,required}] }
 */
export async function getCompetency(employeeId) {
  return apiGet(`/api/competency/${encodeURIComponent(employeeId)}`);
}

/**
 * Get an employee's skill gap analysis.
 * Returns: { employee_id, total_gaps, high_priority_gaps,
 *            medium_priority_gaps, low_priority_gaps, total_competency_gap,
 *            gaps: [{ id, skill, domain, current, required, gap, priority,
 *                     description, recommendedAction }] }
 */
export async function getSkillGaps(employeeId) {
  return apiGet(`/api/competency/${encodeURIComponent(employeeId)}/gaps`);
}

/**
 * Submit a completed competency assessment for scoring.
 *
 * @param {string} employeeId
 * @param {Array<{question_id:string, skill:string, domain:string,
 *                 difficulty?:string, is_correct:boolean, weight?:number}>} answers
 * @param {string} [role] - optional role override
 */
export async function submitAssessment(employeeId, answers, role) {
  return apiPost("/api/competency/assess", {
    employee_id: employeeId,
    role,
    answers,
  });
}

export default { getCompetency, getSkillGaps, submitAssessment };
