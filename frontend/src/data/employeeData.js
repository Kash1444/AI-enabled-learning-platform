// ============================================================
// EMPLOYEE DEMO DATA
// ============================================================
// CURRENT VERSION:
// This file contains mock data for the frontend demo.
//
// FUTURE VERSION:
// These values will come from the backend/database/API.
// Example:
// GET /api/employee/dashboard
// ============================================================


// ============================================================
// 1. EMPLOYEE PROFILE
// ============================================================

export const employeeProfile = {
  id: "EMP001",

  name: "Arun Kumar",

  designation: "Statistical Officer",

  department: "National Statistical Office",

  organization: "Ministry of Statistics & Programme Implementation",

  email: "arun.kumar@demo.gov.in",

  location: "New Delhi",

  experience: 6,

  education: "M.Sc. Statistics",

  joiningYear: 2020,
};


// ============================================================
// 2. DASHBOARD SUMMARY
// ============================================================
// These values are displayed in the four KPI cards.

export const dashboardSummary = {
  overallCompetency: 72,
  competencyChange: 6,

  totalSkillGaps: 4,
  highPriorityGaps: 2,
  mediumPriorityGaps: 2,

  learningProgress: 68,
  learningProgressChange: 12,

  coursesCompleted: 8,
  coursesCompletedChange: 2,
};


// ============================================================
// 3. COMPETENCY OVERVIEW
// ============================================================
// current = employee's current competency level
// required = competency level required for the job role

export const competencyOverview = [
  {
    domain: "Statistical",
    current: 4.1,
    required: 4.5,
  },

  {
    domain: "Technical",
    current: 3.2,
    required: 4.2,
  },

  {
    domain: "Digital Governance",
    current: 3.6,
    required: 4.0,
  },

  {
    domain: "Behavioral / Managerial",
    current: 4.0,
    required: 4.2,
  },
];


// ============================================================
// 4. SKILL GAPS
// ============================================================

export const skillGaps = [
  {
    id: 1,

    skill: "Statistical Programming",

    current: 2.5,

    required: 4.0,

    gap: 1.5,

    priority: "High",

    description:
      "Improve ability to use programming tools for statistical analysis and data processing.",

    recommendedAction:
      "Complete Statistical Programming with R and take the competency assessment.",
  },

  {
    id: 2,

    skill: "Sampling Methodology",

    current: 2.8,

    required: 4.2,

    gap: 1.4,

    priority: "High",

    description:
      "Strengthen sampling design, estimation techniques and official survey methodology.",

    recommendedAction:
      "Complete the NSSTA Sampling Techniques programme.",
  },

  {
    id: 3,

    skill: "Data Visualization",

    current: 3.0,

    required: 4.0,

    gap: 1.0,

    priority: "Medium",

    description:
      "Develop stronger skills for communicating statistical insights through visual reporting.",

    recommendedAction:
      "Complete Data Visualization for Statistical Reporting.",
  },

  {
    id: 4,

    skill: "Digital Governance",

    current: 3.2,

    required: 4.0,

    gap: 0.8,

    priority: "Medium",

    description:
      "Improve understanding of digital governance practices and data-driven public services.",

    recommendedAction:
      "Complete the recommended Digital Governance learning module.",
  },
];


// ============================================================
// 5. AI LEARNING RECOMMENDATIONS
// ============================================================

export const aiRecommendations = [
  {
    id: 1,

    title: "Sampling Techniques for Official Statistics",

    provider: "NSSTA TPAC",

    category: "Statistical",

    level: "Intermediate",

    duration: "6 hours",

    reason:
      "Recommended because Sampling Methodology is currently a high-priority competency gap.",

    progress: 0,

    action: "Start Learning",
  },

  {
    id: 2,

    title: "Statistical Programming with R",

    provider: "iGOT Karmayogi",

    category: "Technical",

    level: "Intermediate",

    duration: "8 hours",

    reason:
      "Recommended to improve the Statistical Programming competency required for your role.",

    progress: 25,

    action: "Continue Learning",
  },

  {
    id: 3,

    title: "Data Visualization for Statistical Reporting",

    provider: "iGOT Karmayogi",

    category: "Technical",

    level: "Intermediate",

    duration: "4 hours",

    reason:
      "Recommended because Data Visualization has a medium-priority skill gap.",

    progress: 40,

    action: "Continue Learning",
  },
];


// ============================================================
// 6. CURRENT LEARNING PROGRESS
// ============================================================

export const learningProgress = [
  {
    id: 1,

    course: "Statistical Programming with R",

    provider: "iGOT Karmayogi",

    progress: 65,

    status: "In Progress",

    remaining: "2 hours remaining",
  },

  {
    id: 2,

    course: "Data Visualization for Statistical Reporting",

    provider: "iGOT Karmayogi",

    progress: 40,

    status: "In Progress",

    remaining: "2.5 hours remaining",
  },

  {
    id: 3,

    course: "Fundamentals of Official Statistics",

    provider: "NSSTA",

    progress: 100,

    status: "Completed",

    remaining: "Completed",
  },
];


// ============================================================
// 7. UPCOMING ASSESSMENTS
// ============================================================

export const upcomingAssessments = [
  {
    id: 1,

    title: "Sampling Methodology Assessment",

    questions: 10,

    duration: "10 min",

    type: "Recommended",

    reason: "High-priority skill gap",
  },

  {
    id: 2,

    title: "Statistical Programming Assessment",

    questions: 15,

    duration: "15 min",

    type: "Available",

    reason: "Measure current competency",
  },
];


// ============================================================
// 8. RECENT ACTIVITY
// ============================================================

export const recentActivity = [
  {
    id: 1,

    title: "Completed Fundamentals of Official Statistics",

    type: "Course",

    time: "2 days ago",

    status: "Completed",
  },

  {
    id: 2,

    title: "Scored 80% in Statistical Methods Quiz",

    type: "Assessment",

    time: "3 days ago",

    status: "80%",
  },

  {
    id: 3,

    title: "Competency profile updated",

    type: "AI Update",

    time: "4 days ago",

    status: "Updated",
  },

  {
    id: 4,

    title: "Started Statistical Programming with R",

    type: "Learning",

    time: "5 days ago",

    status: "25%",
  },
];


// ============================================================
// 9. NOTIFICATIONS
// ============================================================

export const notifications = [
  {
    id: 1,

    title: "New AI recommendation",

    message:
      "A new learning programme has been recommended based on your skill gaps.",

    time: "Today",
  },

  {
    id: 2,

    title: "Assessment available",

    message:
      "Your Sampling Methodology assessment is ready.",

    time: "Today",
  },

  {
    id: 3,

    title: "Continue learning",

    message:
      "You are 65% complete with Statistical Programming with R.",

    time: "Yesterday",
  },
];


// ============================================================
// 10. AI ASSISTANT SUGGESTIONS
// ============================================================

export const aiAssistantSuggestions = [
  "What are my biggest skill gaps?",

  "What should I learn next?",

  "Why was this course recommended?",

  "Show my competency progress",

  "Which assessment should I take?",
];