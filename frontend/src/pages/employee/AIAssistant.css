import { useState } from "react";
import "./AIAssistant.css";

function AIAssistant() {
  const [message, setMessage] = useState("");

  const suggestions = [
    "What skills should I improve next?",
    "Recommend a course for sampling methodology",
    "Explain my current skill gaps",
    "How can I improve my R programming skills?",
  ];

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hello Arun! 👋 I'm your AI Learning Assistant. I can help you understand your competency profile, skill gaps, learning recommendations and assessments.",
    },
  ]);

  const sendMessage = (text = message) => {
    if (!text.trim()) return;

    setMessages((prev) => [
      ...prev,
      { sender: "user", text },
      {
        sender: "ai",
        text: "Based on your current competency profile, I recommend focusing on Sampling Methodology and Statistical Programming with R. These are currently your highest-priority skill gaps.",
      },
    ]);

    setMessage("");
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
          AI Online
        </div>
      </div>

      <div className="assistant-layout">
        <aside className="assistant-sidebar">
          <h3>Quick Questions</h3>

          {suggestions.map((item) => (
            <button key={item} onClick={() => sendMessage(item)}>
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
          </div>

          <div className="chat-input-area">
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") sendMessage();
              }}
              placeholder="Ask your AI learning assistant..."
            />

            <button onClick={() => sendMessage()}>
              Send
            </button>
          </div>
        </section>
      </div>

      <div className="assistant-demo-note">
        <strong>Demo Mode:</strong> AI responses are currently simulated.
        Gemini/LLM integration will be connected through the backend later.
      </div>
    </div>
  );
}

export default AIAssistant;