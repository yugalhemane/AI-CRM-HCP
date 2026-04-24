import { useState } from "react";
import { useDispatch } from "react-redux";
import { updateForm } from "../redux/interactionSlice";
import API from "../services/api";

const SAMPLE_FIRST_PROMPT =
  "Today I met with Dr. Smith and discussed Product X efficiency. The sentiment was positive and I shared brochures. I distributed 5 starter samples. Outcome: doctor agreed to evaluate in next cycle. Follow-up: schedule a revisit next week.";

const ChatPanel = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "ai",
      text:
        "Welcome! I will fill the interaction form for you from chat. Try the sample prompt or type your own interaction details.",
    },
  ]);
  const [isSending, setIsSending] = useState(false);
  const dispatch = useDispatch();

  const sendMessage = async () => {
    if (!input.trim() || isSending) return;

    const updatedMessages = [...messages, { role: "user", text: input.trim() }];
    setMessages(updatedMessages);
    setIsSending(true);

    try {
      const res = await API.post("/chat", { message: input.trim() });
      const data = res.data ?? {};

      if (data.form_data) {
        dispatch(updateForm(data.form_data));
      }

      const assistantText =
        data.assistant_message ||
        data.suggestion ||
        data.summary ||
        data.history ||
        "Processed.";

      setMessages([
        ...updatedMessages,
        { role: "ai", text: assistantText }
      ]);

      setInput("");
    } catch (err) {
      console.error(err);
      const errorText =
        err?.response?.data?.detail ||
        "Request failed. Please check backend logs and try again.";
      setMessages([...updatedMessages, { role: "ai", text: errorText }]);
    } finally {
      setIsSending(false);
    }
  };

  const resetConversation = async () => {
    try {
      await API.post("/reset");
      dispatch(
        updateForm({
          hcp_name: "",
          interaction_type: "Meeting",
          date: "",
          time: "",
          attendees: "",
          topics: "",
          sentiment: "",
          materials: "",
          samples_distributed: "",
          outcomes: "",
          follow_up_actions: "",
        })
      );
      setMessages([{ role: "ai", text: "Session reset. You can log a new interaction." }]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="chat-panel d-flex flex-column">
      <div className="chat-header d-flex justify-content-between align-items-start gap-2">
        <div>
        <h3>AI Assistant</h3>
        <p>Log interaction details here via chat</p>
        </div>
        <button type="button" className="btn btn-sm btn-outline-secondary" onClick={resetConversation}>
          Reset
        </button>
      </div>

      <div className="chat-hint">
        Log interaction details (e.g., "Met Dr. Smith, discussed Product X, positive sentiment, shared brochure") or ask for next actions.
      </div>

      <div className="sample-prompt-wrap">
        <button
          type="button"
          className="btn btn-sm btn-outline-primary"
          onClick={() => setInput(SAMPLE_FIRST_PROMPT)}
        >
          Use First-Time Sample Prompt
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-row ${msg.role === "user" ? "user" : "ai"}`}>
            <span className={`chat-bubble ${msg.role === "user" ? "user" : "ai"}`}>
              {msg.text}
            </span>
          </div>
        ))}
      </div>

      <div className="chat-input-row">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe interaction..."
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
        />
        <button type="button" onClick={sendMessage} disabled={isSending}>
          {isSending ? "..." : "Log"}
        </button>
      </div>
    </div>
  );
};

export default ChatPanel;