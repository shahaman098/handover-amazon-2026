import { useCallback, useEffect, useState } from "react";

const API = "/api";

async function api(path, options = {}) {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail?.message || data.message || res.statusText);
  }
  return data;
}

export default function App() {
  const [role, setRole] = useState("adviser");
  const [caseData, setCaseData] = useState(null);
  const [messages, setMessages] = useState([
    {
      from: "assistant",
      text:
        "Handover simulation ready. Try inspecting A1 or correcting payslip evidence.",
    },
  ]);
  const [input, setInput] = useState(
    "That is my old payslip. Use the September document instead."
  );
  const [proposal, setProposal] = useState(null);
  const [clarify, setClarify] = useState(null);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    const data = await api("/case");
    setCaseData(data);
  }, []);

  useEffect(() => {
    refresh().catch((e) => setError(String(e)));
  }, [refresh]);

  const pushMsg = (from, text) =>
    setMessages((m) => [...m, { from, text }]);

  const sendIntent = async (text, choice) => {
    setError("");
    pushMsg("user", text);
    const path = choice ? `/intent/clarify?choice=${encodeURIComponent(choice)}` : "/intent";
    const body = { role, text };
    const res = await api(path, { method: "POST", body: JSON.stringify(body) });
    pushMsg("assistant", res.message);
    if (res.kind === "clarify") {
      setClarify(res.options);
      setProposal(null);
    } else if (res.kind === "proposal") {
      setProposal(res.proposal);
      setClarify(null);
    } else {
      setProposal(null);
      setClarify(null);
    }
    await refresh();
  };

  const confirm = async () => {
    if (!proposal?.proposal_id) return;
    setRole("applicant");
    try {
      await api(`/proposals/${proposal.proposal_id}/confirm`, {
        method: "POST",
        body: JSON.stringify({ role: "applicant" }),
      });
      pushMsg("assistant", "Correction confirmed and ledger updated.");
      setProposal(null);
      await refresh();
    } catch (e) {
      setError(String(e));
    }
  };

  const cancel = async () => {
    if (!proposal?.proposal_id) return;
    await api(`/proposals/${proposal.proposal_id}/cancel`, { method: "POST" });
    setProposal(null);
    pushMsg("assistant", "Proposal cancelled — ledger unchanged.");
  };

  const reset = async () => {
    await api("/reset", { method: "POST" });
    setProposal(null);
    setClarify(null);
    setMessages([{ from: "assistant", text: "Case reset to Riverside fixture." }]);
    await refresh();
  };

  const downloadReceipt = async () => {
    const receipt = await api("/receipt");
    const blob = new Blob([JSON.stringify(receipt, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `handover-receipt-rev${receipt.case_revision}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app">
      <div className="banner">
        Entrant-built Alexa+ simulation — not a production Alexa device. Simulated
        applicant and adviser roles only.
      </div>
      <header>
        <h1>Handover</h1>
        <p>Evidence-linked application corrections with a provenance ledger</p>
      </header>

      <div className="role-toggle panel">
        <strong>Simulated role:</strong>
        <label>
          <input
            type="radio"
            checked={role === "adviser"}
            onChange={() => setRole("adviser")}
          />
          Adviser
        </label>
        <label>
          <input
            type="radio"
            checked={role === "applicant"}
            onChange={() => setRole("applicant")}
          />
          Applicant
        </label>
        <span className="muted" style={{ marginLeft: "1rem" }}>
          Revision {caseData?.case_revision ?? "—"}
        </span>
      </div>

      <div className="layout">
        <section className="panel">
          <h2>Conversation</h2>
          <div className="chat-log">
            {messages.map((m, i) => (
              <div key={i} className={`bubble ${m.from === "user" ? "user" : "assistant"}`}>
                {m.text}
              </div>
            ))}
          </div>
          {clarify && (
            <div className="card">
              <p>Choose document:</p>
              {clarify.map((o) => (
                <button
                  key={o.id}
                  className="secondary"
                  style={{ marginRight: "0.5rem" }}
                  onClick={() => sendIntent(input, o.id)}
                >
                  {o.label}
                </button>
              ))}
            </div>
          )}
          {proposal && (
            <div className="card">
              <h3>Confirm correction</h3>
              <p>Income → £{proposal.new_income_value}</p>
              <p className="muted">
                Affected: {proposal.affected_assessment_ids?.join(", ")}
              </p>
              <p className="muted">Hash {proposal.proposal_hash}</p>
              <button onClick={confirm}>Applicant confirms</button>
              <button className="secondary" onClick={cancel}>Cancel</button>
            </div>
          )}
          <div className="controls">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendIntent(input)}
            />
            <button onClick={() => sendIntent(input)}>Send</button>
            <button className="secondary" onClick={() => sendIntent("inspect source for A1")}>
              Inspect A1
            </button>
          </div>
          {error && <p style={{ color: "#ff8a8a" }}>{error}</p>}
        </section>

        <aside className="panel">
          <h2>Case state</h2>
          <button className="secondary" onClick={reset}>Reset demo</button>
          <button className="secondary" onClick={downloadReceipt} style={{ marginLeft: "0.5rem" }}>
            Export receipt
          </button>
          <p className="muted" style={{ marginTop: "0.75rem" }}>
            Ready to export: {caseData?.ready_to_export ? "yes" : "no"}
          </p>
          {caseData?.conflicts?.length > 0 && (
            <p className="muted">Conflicts: {caseData.conflicts.join(", ")}</p>
          )}
          {caseData?.assessments?.map((a) => (
            <div key={a.id} className="assessment">
              <div className="status">{a.id} · {a.status}</div>
              <strong>{a.title}</strong>
              <div>{a.value ?? "—"}</div>
              <div className="muted">{a.explanation}</div>
            </div>
          ))}
        </aside>
      </div>
    </div>
  );
}
