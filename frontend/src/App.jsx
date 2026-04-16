import { useState, useRef } from "react"

const API = import.meta.env.VITE_API_URL || "http://localhost:8000"

export default function App() {
  const [documentId, setDocumentId] = useState(null)
  const [documentName, setDocumentName] = useState(null)
  const [chunks, setChunks] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [messages, setMessages] = useState([])
  const [question, setQuestion] = useState("")
  const [loading, setLoading] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const fileInputRef = useRef(null)
  const messagesEndRef = useRef(null)

  // ── upload handler ──────────────────────────────────────────
  async function handleFile(file) {
    if (!file || !file.name.endsWith(".pdf")) {
      alert("Please upload a PDF file.")
      return
    }
    setUploading(true)
    setMessages([])
    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch(`${API}/upload`, { method: "POST", body: formData })
      const data = await res.json()
      setDocumentId(data.document_id)
      setDocumentName(file.name)
      setChunks(data.chunks_created)
    } catch {
      alert("Upload failed. Make sure your FastAPI server is running.")
    } finally {
      setUploading(false)
    }
  }

  // ── ask handler ─────────────────────────────────────────────
  async function handleAsk() {
    if (!question.trim() || !documentId) return
    const userMsg = { role: "user", text: question }
    setMessages(prev => [...prev, userMsg])
    setQuestion("")
    setLoading(true)

    try {
      const res = await fetch(`${API}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMsg.text, document_id: documentId })
      })
      const data = await res.json()
      setMessages(prev => [...prev, {
        role: "ai",
        text: data.answer,
        sources: data.sources_used,
        tokens: data.tokens_used
      }])
    } catch {
      setMessages(prev => [...prev, { role: "ai", text: "Error contacting server." }])
    } finally {
      setLoading(false)
      setTimeout(() => messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }), 100)
    }
  }

  // ── drag and drop ───────────────────────────────────────────
  function onDrop(e) {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    handleFile(file)
  }

  // ── render ──────────────────────────────────────────────────
  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "system-ui, sans-serif", background: "#f5f5f0" }}>

      {/* ── LEFT PANEL ── */}
      <div style={{ width: 280, background: "#fff", borderRight: "1px solid #e5e5e0", display: "flex", flexDirection: "column", padding: 20, gap: 16 }}>
        <h1 style={{ fontSize: 18, fontWeight: 600, margin: 0, color: "#1a1a1a" }}>DocuMind</h1>
        <p style={{ fontSize: 13, color: "#888", margin: 0 }}>Upload a PDF and ask questions about it.</p>

        {/* drop zone */}
        <div
          onClick={() => fileInputRef.current.click()}
          onDragOver={e => { e.preventDefault(); setDragOver(true) }}
          onDragLeave={() => setDragOver(false)}
          onDrop={onDrop}
          style={{
            border: `2px dashed ${dragOver ? "#378ADD" : "#ccc"}`,
            borderRadius: 10,
            padding: "24px 16px",
            textAlign: "center",
            cursor: "pointer",
            background: dragOver ? "#E6F1FB" : "#fafafa",
            transition: "all 0.15s"
          }}
        >
          <div style={{ fontSize: 28, marginBottom: 8 }}>📄</div>
          <p style={{ fontSize: 13, color: "#666", margin: 0 }}>
            {uploading ? "Processing..." : "Drop PDF here or click to upload"}
          </p>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          style={{ display: "none" }}
          onChange={e => handleFile(e.target.files[0])}
        />

        {/* document status */}
        {documentId && (
          <div style={{ background: "#f0faf5", border: "1px solid #5DCAA5", borderRadius: 8, padding: "10px 12px" }}>
            <p style={{ fontSize: 13, fontWeight: 500, color: "#0F6E56", margin: "0 0 2px" }}>{documentName}</p>
            <p style={{ fontSize: 12, color: "#1D9E75", margin: 0 }}>{chunks} chunks ready</p>
          </div>
        )}

        {/* stats */}
        {messages.length > 0 && (
          <div style={{ marginTop: "auto", paddingTop: 12, borderTop: "1px solid #eee" }}>
            <p style={{ fontSize: 11, color: "#aaa", margin: "0 0 2px" }}>Questions asked</p>
            <p style={{ fontSize: 20, fontWeight: 600, color: "#1a1a1a", margin: 0 }}>
              {messages.filter(m => m.role === "user").length}
            </p>
          </div>
        )}
      </div>

      {/* ── RIGHT PANEL ── */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>

        {/* messages */}
        <div style={{ flex: 1, overflowY: "auto", padding: "24px 32px", display: "flex", flexDirection: "column", gap: 16 }}>
          {messages.length === 0 && (
            <div style={{ margin: "auto", textAlign: "center", color: "#aaa" }}>
              <p style={{ fontSize: 32, marginBottom: 8 }}>💬</p>
              <p style={{ fontSize: 15 }}>{documentId ? "Ask anything about your document" : "Upload a PDF to get started"}</p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} style={{ display: "flex", justifyContent: msg.role === "user" ? "flex-end" : "flex-start", gap: 10, alignItems: "flex-start" }}>
              {msg.role === "ai" && (
                <div style={{ width: 28, height: 28, borderRadius: "50%", background: "#eee", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 600, color: "#666", flexShrink: 0 }}>AI</div>
              )}
              <div style={{ maxWidth: "70%" }}>
                <div style={{
                  background: msg.role === "user" ? "#378ADD" : "#fff",
                  color: msg.role === "user" ? "#fff" : "#1a1a1a",
                  borderRadius: msg.role === "user" ? "16px 16px 4px 16px" : "4px 16px 16px 16px",
                  padding: "10px 14px",
                  fontSize: 14,
                  lineHeight: 1.5,
                  border: msg.role === "ai" ? "1px solid #e5e5e0" : "none"
                }}>
                  {msg.text}
                </div>
                {msg.sources && msg.sources.length > 0 && (
                  <div style={{ marginTop: 6, paddingLeft: 4, borderLeft: "2px solid #378ADD" }}>
                    <p style={{ fontSize: 11, color: "#aaa", margin: "0 0 2px" }}>Sources used</p>
                    {msg.sources.slice(0, 1).map((s, si) => (
                      <p key={si} style={{ fontSize: 11, color: "#888", margin: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: 400 }}>
                        "{s.slice(0, 120)}..."
                      </p>
                    ))}
                    <p style={{ fontSize: 11, color: "#aaa", margin: "2px 0 0" }}>{msg.tokens} tokens used</p>
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
              <div style={{ width: 28, height: 28, borderRadius: "50%", background: "#eee", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 600, color: "#666" }}>AI</div>
              <div style={{ background: "#fff", border: "1px solid #e5e5e0", borderRadius: "4px 16px 16px 16px", padding: "10px 14px", fontSize: 14, color: "#aaa" }}>Thinking...</div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* input bar */}
        <div style={{ borderTop: "1px solid #e5e5e0", padding: "16px 32px", background: "#fff", display: "flex", gap: 10 }}>
          <input
            value={question}
            onChange={e => setQuestion(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleAsk()}
            placeholder={documentId ? "Ask a question about your document..." : "Upload a PDF first..."}
            disabled={!documentId || loading}
            style={{ flex: 1, padding: "10px 14px", borderRadius: 10, border: "1px solid #e5e5e0", fontSize: 14, outline: "none", background: !documentId ? "#fafafa" : "#fff" }}
          />
          <button
            onClick={handleAsk}
            disabled={!documentId || loading || !question.trim()}
            style={{ padding: "10px 20px", borderRadius: 10, border: "none", background: "#378ADD", color: "#fff", fontSize: 14, fontWeight: 500, cursor: "pointer", opacity: (!documentId || loading || !question.trim()) ? 0.5 : 1 }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  )
}