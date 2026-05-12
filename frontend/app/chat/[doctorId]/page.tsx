"use client";
import { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import { getDoctor, sendChatbotMessage, saveChatbotLead } from "@/lib/api";
import { Doctor, ChatMessage, ChatbotState, ChatbotCollectedData, ChatbotLeadResponse } from "@/lib/types";
import LoadingState from "@/components/LoadingState";
import SafetyNote from "@/components/SafetyNote";
import { MessageSquare, Send, Bot, User, CheckCircle } from "lucide-react";

export default function ChatPage() {
  const params = useParams();
  const doctorId = Number(params.doctorId);

  const [doctor, setDoctor] = useState<Doctor | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [state, setState] = useState<ChatbotState>("START");
  const [collectedData, setCollectedData] = useState<ChatbotCollectedData>({
    patient_name: null,
    patient_contact: null,
    problem: null,
  });
  const [leadSaved, setLeadSaved] = useState<ChatbotLeadResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getDoctor(doctorId)
      .then((doc) => {
        setDoctor(doc);
        // Initial AI greeting
        setMessages([
          {
            id: "init",
            sender: "ai",
            text: `Dr. ${doc.name} is currently ${doc.is_available ? "available" : "unavailable"}. I'm the patient-side AI assistant. I'll collect your details so the doctor can follow up by email. What is your full name?`,
          },
        ]);
        setState("ASK_NAME");
      })
      .catch(() => {
        setMessages([{ id: "err", sender: "system", text: "Could not connect to doctor. Please try again." }]);
      })
      .finally(() => setLoading(false));
  }, [doctorId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    if (!input.trim() || sending) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: "patient",
      text: input.trim(),
    };

    setMessages((prev) => [...prev, userMsg]);
    const currentInput = input.trim();
    setInput("");
    setSending(true);

    try {
      const response = await sendChatbotMessage({
        doctor_id: doctorId,
        message: currentInput,
        conversation_state: state,
        collected_data: collectedData,
      });

      const aiMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "ai",
        text: response.reply,
      };

      setMessages((prev) => [...prev, aiMsg]);
      setState(response.next_state);
      setCollectedData(response.collected_data);

      // Auto-save lead when complete
      if (response.is_complete && response.collected_data.patient_name && response.collected_data.patient_contact && response.collected_data.problem) {
        const lead = await saveChatbotLead({
          doctor_id: doctorId,
          patient_name: response.collected_data.patient_name,
          patient_contact: response.collected_data.patient_contact,
          problem: response.collected_data.problem,
        });
        setLeadSaved(lead);
        setMessages((prev) => [
          ...prev,
          {
            id: "lead-saved",
            sender: "system",
            text: `Your details have been saved (Lead #${lead.lead_id}). The doctor will contact you by email soon. ${lead.email_sent ? "Doctor has been notified via email." : ""}`,
          },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { id: "err" + Date.now(), sender: "system", text: "Failed to get AI response. Please try again." },
      ]);
    } finally {
      setSending(false);
    }
  }

  if (loading) return <LoadingState />;

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-violet-600 to-purple-600 text-white rounded-3xl p-5 mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
            <MessageSquare className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold">AI Assistant</h1>
            {doctor && (
              <p className="text-violet-200 text-sm">For {doctor.name} — {doctor.specialization}</p>
            )}
          </div>
        </div>
      </div>

      {/* Lead saved confirmation */}
      {leadSaved && (
        <div className="bg-green-50 border border-green-200 rounded-2xl p-4 mb-4 flex items-start gap-3">
          <CheckCircle className="w-5 h-5 text-green-500 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-green-800 text-sm">Details saved successfully!</p>
            <p className="text-xs text-green-600 mt-0.5">
              Lead #{leadSaved.lead_id} — {leadSaved.email_sent ? "Doctor notified." : "Doctor will be notified."}
            </p>
          </div>
        </div>
      )}

      {/* Chat window */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="h-96 overflow-y-auto p-4 space-y-3">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-2 ${msg.sender === "patient" ? "flex-row-reverse" : ""}`}
            >
              {msg.sender !== "system" && (
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  msg.sender === "ai" ? "bg-violet-100" : "bg-sky-100"
                }`}>
                  {msg.sender === "ai"
                    ? <Bot className="w-4 h-4 text-violet-600" />
                    : <User className="w-4 h-4 text-sky-600" />
                  }
                </div>
              )}
              <div
                className={`max-w-xs rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                  msg.sender === "patient"
                    ? "bg-sky-500 text-white rounded-tr-sm"
                    : msg.sender === "system"
                    ? "bg-green-50 border border-green-200 text-green-800 text-xs w-full rounded-xl"
                    : "bg-slate-100 text-slate-800 rounded-tl-sm"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          {sending && (
            <div className="flex gap-2">
              <div className="w-8 h-8 rounded-full bg-violet-100 flex items-center justify-center">
                <Bot className="w-4 h-4 text-violet-600" />
              </div>
              <div className="bg-slate-100 rounded-2xl rounded-tl-sm px-4 py-2.5">
                <span className="flex gap-1">
                  <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </span>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="border-t border-slate-200 p-4 flex gap-3">
          <input
            id="chat-input"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Type your message..."
            disabled={sending || !!leadSaved}
            className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 bg-slate-50 disabled:opacity-50"
          />
          <button
            id="chat-send-btn"
            onClick={handleSend}
            disabled={sending || !input.trim() || !!leadSaved}
            className="w-10 h-10 bg-violet-500 hover:bg-violet-600 disabled:bg-violet-300 text-white rounded-xl flex items-center justify-center transition-colors"
            aria-label="Send"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="mt-5">
        <SafetyNote />
      </div>
    </div>
  );
}
