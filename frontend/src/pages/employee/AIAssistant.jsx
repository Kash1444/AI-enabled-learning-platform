import { useState } from "react";
import "./AIAssistant.css";
import { sendMessage as sendAIMessage } from "../../services/assistantService";

function AIAssistant() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const suggestions = [
    "What skills should I improve next?",
    "Recommend a course for sampling methodology",
    "Explain my current skill gaps",
    "How can I improve my R programming skills?",
  ];

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hello! 👋 I'm your AI Learning Assistant. I can help you understand your competency profile, skill gaps, learning recommendations and assessments.",
    },
  ]);

  const sendMessage = async (text = message) => {
    const trimmed = text.trim();

    if (!trimmed || loading) return;

    setMessages((prev) => [
      ...prev,
      { sender: "user", text: trimmed },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await sendAIMessage("EMP001", trimmed);

      const aiText =
        response?.response ||
        response?.message ||
        response?.answer ||
        "I received your question, but the AI response was empty.";

      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: aiText },
      ]);
    } catch (error) {
      console.error("AI assistant error:", error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "I'm unable to connect to the AI backend right now. Please make sure the backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="assistant-page">
      <div className="assistant-header">
        <div>
          <span>AI LEARNING ASSISTANT</span>
          <h1>Your AI Learning Coach</h1>
          <p>
            Get personalized guidance based on your competency profile.
          </p>
        </div>

        <div className="assistant-status">
          <span></span>
          {loading ? "Thinking..." : "AI Online"}
        </div>
      </div>

      <div className="assistant-layout">
        <aside className="assistant-sidebar">
          <h3>Quick Questions</h3>

          {suggestions.map((item) => (
            <button
              key={item}
              onClick={() => sendMessage(item)}
              disabled={loading}
            >
              {item}
            </button>
          ))}

          <div className="assistant-context">
            <strong>AI Context</strong>
            <p>Profile</p>
            <p>Competencies</p>
            <p>Skill Gaps</p>
            <p>Learning History</p>
          </div>
        </aside>

        <section className="chat-container">
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`chat-message ${msg.sender}`}
              >
                <div className="message-avatar">
                  {msg.sender === "ai" ? "AI" : "AK"}
                </div>

                <div className="message-bubble">
                  {msg.text}
                </div>
              </div>
            ))}

            {loading && (
              <div className="chat-message ai">
                <div className="message-avatar">AI</div>
                <div className="message-bubble">
                  Thinking...
                </div>
              </div>
            )}
          </div>

          <div className="chat-input-area">
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") sendMessage();
              }}
              placeholder="Ask your AI learning assistant..."
              disabled={loading}
            />

            <button
              onClick={() => sendMessage()}
              disabled={loading}
            >
              {loading ? "..." : "Send"}
            </button>
          </div>
        </section>
      </div>

      <div className="assistant-demo-note">
        <strong>AI Mode:</strong> Responses are generated through the
        AI backend.
      </div>
    </div>
  );
}

export default AIAssistant;