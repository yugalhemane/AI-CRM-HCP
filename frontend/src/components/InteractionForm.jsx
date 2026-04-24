import { useSelector } from "react-redux";

const InteractionForm = () => {
  const form = useSelector((state) => state.interaction);

  return (
    <div className="p-3 p-md-4 p-xl-5">
      <div className="interaction-card">
        <h2 className="mb-1">Log HCP Interaction</h2>
        <p className="interaction-subtitle">Interaction Details</p>

        <div className="row g-3">
          <div className="col-12 col-md-6">
            <label className="form-label">HCP Name</label>
            <input className="form-control" value={form.hcp_name} readOnly />
          </div>

          <div className="col-12 col-md-6">
            <label className="form-label">Interaction Type</label>
            <input className="form-control" value={form.interaction_type} readOnly />
          </div>

          <div className="col-12 col-md-6">
            <label className="form-label">Date</label>
            <input className="form-control" value={form.date} readOnly />
          </div>

          <div className="col-12 col-md-6">
            <label className="form-label">Time</label>
            <input className="form-control" value={form.time} readOnly />
          </div>

          <div className="col-12">
            <label className="form-label">Attendees</label>
            <input className="form-control" value={form.attendees} readOnly />
          </div>

          <div className="col-12">
            <label className="form-label">Topics Discussed</label>
            <textarea className="form-control topic-box" value={form.topics} readOnly />
          </div>

          <div className="col-12 col-md-6">
            <label className="form-label">Sentiment</label>
            <div className="sentiment-row">
              <span className={`sentiment-pill ${form.sentiment === "positive" ? "active" : ""}`}>Positive</span>
              <span className={`sentiment-pill ${form.sentiment === "neutral" ? "active" : ""}`}>Neutral</span>
              <span className={`sentiment-pill ${form.sentiment === "negative" ? "active" : ""}`}>Negative</span>
            </div>
          </div>

          <div className="col-12 col-md-6">
            <label className="form-label">Materials Shared</label>
            <input className="form-control" value={form.materials} readOnly />
          </div>

          <div className="col-12">
            <label className="form-label">Samples Distributed</label>
            <input className="form-control" value={form.samples_distributed} readOnly />
          </div>

          <div className="col-12">
            <label className="form-label">Outcomes</label>
            <textarea className="form-control topic-box" value={form.outcomes} readOnly />
          </div>

          <div className="col-12">
            <label className="form-label">Follow-up Actions</label>
            <textarea className="form-control topic-box" value={form.follow_up_actions} readOnly />
          </div>
        </div>
      </div>
    </div>
  );
};

export default InteractionForm;