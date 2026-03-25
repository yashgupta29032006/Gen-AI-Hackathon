"use client";

import { useState, useEffect } from "react";
import { apiService } from "@/services/api";
import { ExecutionTrace } from "@/components/ExecutionTrace";
import { Sparkles, Calendar, Loader2, Send } from "lucide-react";

export default function Home() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState<any[]>([]);
  const [actionsTaken, setActionsTaken] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = async () => {
    try {
      const data = await apiService.getLogs(10);
      setLogs(data);
    } catch (e) {
      console.error("Failed to fetch logs", e);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    setError(null);
    setPlan([]);
    setActionsTaken([]);

    try {
      // Step 1: Ask orchestrator
      const planData = await apiService.ask(input);
      setPlan(planData.plan || []);

      // Step 2: Auto-execute for demo
      if (planData.plan && planData.plan.length > 0) {
        const result = await apiService.execute(planData.plan);
        console.log("[DEBUG] Execution result from backend:", result);
        setActionsTaken(result.actions_taken || []);
      }
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
      fetchLogs();
    }
  };

  const handleConnectGoogle = async () => {
    try {
      const { url } = await apiService.getAuthUrl();
      window.location.href = url;
    } catch (e) {
      setError("Failed to initialize Google Authentication");
    }
  };

  return (
    <main className="min-h-screen bg-[#020617] text-slate-50 p-8 font-sans">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="flex justify-between items-center mb-12">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Sparkles size={24} className="text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">FlowOS</h1>
              <p className="text-xs text-slate-400 font-medium uppercase tracking-widest">Multi-Agent Productivity Brain</p>
            </div>
          </div>
          <button 
            onClick={handleConnectGoogle}
            className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors border border-slate-700"
          >
            <Calendar size={18} className="text-red-400" />
            Connect Google Calendar
          </button>
        </header>

        {/* Input Section */}
        <div className="max-w-3xl mx-auto mb-16">
          <form onSubmit={handleSubmit} className="relative group">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="What would you like FlowOS to do?"
              className="w-full bg-slate-900/80 border-2 border-slate-800 focus:border-blue-600/50 rounded-2xl py-6 px-8 pr-32 text-lg outline-none transition-all shadow-2xl placeholder:text-slate-600"
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-4 top-4 bottom-4 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 px-6 rounded-xl transition-all flex items-center gap-2 font-semibold shadow-lg shadow-blue-600/20"
            >
              {loading ? <Loader2 className="animate-spin" size={20} /> : <><Send size={18} /> Run</>}
            </button>
          </form>
          {error && <p className="text-red-400 text-sm mt-4 ml-2">⚠️ {error}</p>}
        </div>

        {/* Results Trace */}
        <ExecutionTrace plan={plan} actionsTaken={actionsTaken} logs={logs} />
      </div>
    </main>
  );
}
