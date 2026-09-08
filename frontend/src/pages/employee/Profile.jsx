import { employeeProfile } from "../../data/employeeData";
import "./Profile.css";

function Profile() {
  return (
    <div className="profile-page">

      <div className="profile-page-header">
        <div>
          <div className="profile-breadcrumb">
            Employee Portal / My Profile
          </div>

          <h1>My Profile</h1>

          <p>
            View your professional profile and employment information.
          </p>
        </div>

        <button className="profile-edit-button">
          ✎ Edit Profile
        </button>
      </div>


      {/* Profile Summary */}

      <section className="profile-summary-card">

        <div className="profile-avatar-large">
          AK
        </div>

        <div className="profile-summary-info">

          <h2>{employeeProfile.name}</h2>

          <p className="profile-designation">
            {employeeProfile.designation}
          </p>

          <p>
            {employeeProfile.department}
          </p>

          <span className="profile-status">
            ● Active
          </span>

        </div>

      </section>


      {/* Basic Information */}

      <section className="profile-section">

        <div className="profile-section-header">
          <div>
            <h2>Basic Information</h2>
            <p>Personal and employment details</p>
          </div>
        </div>

        <div className="profile-grid">

          <div className="profile-field">
            <span>Employee ID</span>
            <strong>{employeeProfile.employeeId}</strong>
          </div>

          <div className="profile-field">
            <span>Full Name</span>
            <strong>{employeeProfile.name}</strong>
          </div>

          <div className="profile-field">
            <span>Email</span>
            <strong>{employeeProfile.email}</strong>
          </div>

          <div className="profile-field">
            <span>Designation</span>
            <strong>{employeeProfile.designation}</strong>
          </div>

          <div className="profile-field">
            <span>Department</span>
            <strong>{employeeProfile.department}</strong>
          </div>

          <div className="profile-field">
            <span>Ministry</span>
            <strong>{employeeProfile.ministry}</strong>
          </div>

          <div className="profile-field">
            <span>Location</span>
            <strong>{employeeProfile.location}</strong>
          </div>

          <div className="profile-field">
            <span>Years of Experience</span>
            <strong>{employeeProfile.experience} Years</strong>
          </div>

        </div>

      </section>


      {/* Education */}

      <section className="profile-section">

        <div className="profile-section-header">
          <div>
            <h2>Education & Background</h2>
            <p>Academic and professional background</p>
          </div>
        </div>

        <div className="education-card">

          <div className="education-icon">
            🎓
          </div>

          <div>
            <h3>{employeeProfile.education}</h3>
            <p>Highest Qualification</p>
          </div>

        </div>

      </section>


      {/* AI Profile Intelligence */}

      <section className="profile-ai-card">

        <div className="profile-ai-icon">
          ✨
        </div>

        <div>
          <h2>AI Profile Intelligence</h2>

          <p>
            Your profile information is used to build your competency
            profile, identify skill gaps, and personalize your learning
            recommendations.
          </p>

          <div className="profile-ai-points">
            <span>✓ Competency Mapping</span>
            <span>✓ Skill Gap Analysis</span>
            <span>✓ Personalized Learning</span>
          </div>
        </div>

      </section>

    </div>
  );
}

export default Profile;