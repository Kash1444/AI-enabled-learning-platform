import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";

const demoUsers = [
  {
    email: "employee@demo.com",
    password: "Employee@123",
    role: "employee",
    name: "Arun Kumar",
  },
  {
    email: "trainer@demo.com",
    password: "Trainer@123",
    role: "trainer",
    name: "Priya Sharma",
  },
  {
    email: "admin@demo.com",
    password: "Admin@123",
    role: "admin",
    name: "Dr. Rajesh Kumar",
  },
];

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    setTimeout(() => {
      const user = demoUsers.find(
        (user) =>
          user.email === email.trim() &&
          user.password === password
      );

      if (!user) {
        setError("Invalid email or password.");
        setLoading(false);
        return;
      }

      localStorage.setItem(
        "authUser",
        JSON.stringify({
          name: user.name,
          email: user.email,
          role: user.role,
        })
      );

      if (user.role === "employee") {
        navigate("/employee/dashboard");
      } else if (user.role === "trainer") {
        navigate("/trainer/dashboard");
      } else if (user.role === "admin") {
        navigate("/admin/dashboard");
      }

      setLoading(false);
    }, 500);
  };

  const useDemoAccount = (user) => {
    setEmail(user.email);
    setPassword(user.password);
    setError("");
  };

  return (
    <div className="login-page">

      {/* LEFT SIDE */}
      <div className="login-left">

        <div className="brand">
          <div className="brand-icon">AI</div>

          <div>
            <h2>Skill Intelligence</h2>
            <p>Official Statistics</p>
          </div>
        </div>

        <div className="hero-content">

          <span className="eyebrow">
            AI-ENABLED LEARNING PLATFORM
          </span>

          <h1>
            Build skills.
            <br />
            <span>Shape the future.</span>
          </h1>

          <p>
            Personalized learning and competency intelligence
            for India's Official Statistical System.
          </p>

          <div className="feature-list">

            <div className="feature">
              <div className="feature-icon">✓</div>

              <div>
                <strong>
                  AI-Powered Skill Intelligence
                </strong>

                <p>
                  Identify competency gaps intelligently.
                </p>
              </div>
            </div>

            <div className="feature">
              <div className="feature-icon">✓</div>

              <div>
                <strong>
                  Personalized Learning
                </strong>

                <p>
                  Get learning recommendations based on your role.
                </p>
              </div>
            </div>

            <div className="feature">
              <div className="feature-icon">✓</div>

              <div>
                <strong>
                  AI Assessments
                </strong>

                <p>
                  Generate quizzes and MCQs from learning materials.
                </p>
              </div>
            </div>

          </div>
        </div>

        <div className="login-footer">
          <span>Demo Prototype</span>
          <span>•</span>
          <span>
            Capacity Building for Official Statistics
          </span>
        </div>

      </div>

      {/* RIGHT SIDE */}
      <div className="login-right">

        <div className="login-card">

          <div className="login-heading">

            <div className="mobile-logo">
              AI
            </div>

            <h1>Welcome back</h1>

            <p>
              Sign in to access your personalized
              learning dashboard.
            </p>

          </div>

          <form onSubmit={handleLogin}>

            {/* EMAIL */}

            <div className="form-group">

              <label htmlFor="email">
                Email address
              </label>

              <div className="input-wrapper">

                <span className="input-icon">
                  ✉
                </span>

                <input
                  id="email"
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />

              </div>

            </div>

            {/* PASSWORD */}

            <div className="form-group">

              <label htmlFor="password">
                Password
              </label>

              <div className="input-wrapper">

                <span className="input-icon">
                  🔒
                </span>

                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                >
                  {showPassword ? "Hide" : "Show"}
                </button>

              </div>

            </div>

            {/* ERROR */}

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {/* LOGIN */}

            <button
              type="submit"
              className="login-button"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>

          </form>

          {/* DEMO ACCOUNTS */}

          <div className="demo-section">

            <div className="demo-title">
              DEMO ACCESS
            </div>

            {demoUsers.map((user) => (
              <div
                className="demo-account"
                key={user.role}
              >

                <div>
                  <strong>
                    {user.role.charAt(0).toUpperCase() +
                      user.role.slice(1)}
                  </strong>

                  <small>
                    {user.email}
                  </small>
                </div>

                <button
                  type="button"
                  onClick={() => useDemoAccount(user)}
                >
                  Use
                </button>

              </div>
            ))}

          </div>

          <div className="security-note">
            🔒 Secure demo environment
          </div>

        </div>

      </div>

    </div>
  );
}

export default Login;