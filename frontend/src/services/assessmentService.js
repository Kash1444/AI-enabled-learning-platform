/**
 * assessmentService.js
 *
 * Integration layer for trainer material uploads, MCQ generation, and
 * quiz taking/evaluation. Used by trainer pages (UploadMaterials.jsx,
 * GenerateAssessment.jsx, Assessments.jsx, LearnerResults.jsx) and
 * employee pages (Quiz.jsx, QuizResult.jsx).
 */

import { apiGet, apiPost, apiUpload } from "./apiClient";

/**
 * Upload a learning material (PDF, DOCX, PPTX or TXT).
 *
 * @param {File} file
 * @param {{title:string, competencyDomain?:string, competencySkill?:string, uploadedBy?:string}} meta
 * Returns: { id, title, original_filename, file_type, status, chunk_count, ... }
 */
export async function uploadMaterial(file, meta = {}) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("title", meta.title || file.name);
  formData.append("competency_domain", meta.competencyDomain || "");
  formData.append("competency_skill", meta.competencySkill || "");
  formData.append("uploaded_by", meta.uploadedBy || "trainer");
  return apiUpload("/api/materials/upload", formData);
}

/** List all uploaded materials. Returns: { materials: [...] } */
export async function listMaterials() {
  return apiGet("/api/materials");
}

/** Get a single material with a preview of its extracted chunks. */
export async function getMaterial(materialId) {
  return apiGet(`/api/materials/${encodeURIComponent(materialId)}`);
}

/**
 * Generate an MCQ assessment.
 *
 * If `materialId` is provided, questions are grounded in that uploaded
 * material via RAG. If omitted, a generic competency self-check is
 * generated instead (no material needed).
 *
 * @param {{materialId?:string, competency:string, domain?:string,
 *          numQuestions?:number, difficulty?:'Easy'|'Intermediate'|'Advanced',
 *          employeeId?:string}} params
 */
export async function generateAssessment({
  materialId,
  competency,
  domain = "Statistical",
  numQuestions = 5,
  difficulty = "Intermediate",
  employeeId,
} = {}) {
  return apiPost("/api/assessment/generate", {
    material_id: materialId,
    competency,
    domain,
    num_questions: numQuestions,
    difficulty,
    employee_id: employeeId,
  });
}

/**
 * Get an assessment for a learner to attempt (answer key withheld).
 * Returns: { id, title, competency_domain, competency_skill, difficulty,
 *            questions: [{ id, question, options, competency, difficulty }] }
 */
export async function getAssessment(assessmentId) {
  return apiGet(`/api/assessment/${encodeURIComponent(assessmentId)}`);
}

/**
 * Submit a learner's answers for grading.
 *
 * @param {string} assessmentId
 * @param {string} employeeId
 * @param {Record<string, number>} answers - { [questionId]: chosenOptionIndex }
 */
export async function submitAssessment(assessmentId, employeeId, answers) {
  return apiPost("/api/assessment/evaluate", {
    assessment_id: assessmentId,
    employee_id: employeeId,
    answers,
  });
}

export default {
  uploadMaterial,
  listMaterials,
  getMaterial,
  generateAssessment,
  getAssessment,
  submitAssessment,
};
