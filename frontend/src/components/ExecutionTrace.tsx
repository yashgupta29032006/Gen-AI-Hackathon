import React from 'react';
import { Terminal, CheckCircle2, ListTodo, Brain } from 'lucide-react';

interface TraceProps {
  plan: any[];
  actionsTaken: any[];
  logs: any[];
}

export const ExecutionTrace: React.FC<TraceProps> = ({ plan, actionsTaken, logs }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mt-8">
      {/* Plan Section */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4 text-blue-400">
          <Brain size={20} />
          <h2 className="text-lg font-semibold">Planned Steps</h2>
        </div>
        <div className="space-y-3">
          {plan.map((step, idx) => (
            <div key={idx} className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">
              <span className="text-xs font-bold text-slate-500 uppercase">{step.agent}</span>
              <p className="text-sm text-slate-200 mt-1">{step.action}</p>
            </div>
          ))}
          {plan.length === 0 && <p className="text-slate-500 italic text-sm">No steps planned yet.</p>}
        </div>
      </div>

      {/* Actions Section */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4 text-green-400">
          <CheckCircle2 size={20} />
          <h2 className="text-lg font-semibold">Actions Taken</h2>
        </div>
        <div className="space-y-3">
          {actionsTaken.map((action, idx) => (
            <div key={idx} className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">
              <span className="text-xs font-bold text-slate-500 uppercase">{action.agent}</span>
              <p className="text-sm text-slate-200 mt-1">{action.action}</p>
              {action.result && <pre className="text-[10px] text-slate-400 mt-2 bg-black/30 p-2 rounded truncate">{JSON.stringify(action.result, null, 2)}</pre>}
            </div>
          ))}
          {actionsTaken.length === 0 && <p className="text-slate-500 italic text-sm">Waiting for execution...</p>}
        </div>
      </div>

      {/* Logs Section */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4 text-amber-400">
          <Terminal size={20} />
          <h2 className="text-lg font-semibold">Agent Logs</h2>
        </div>
        <div className="space-y-2 max-h-[400px] overflow-y-auto pr-2">
          {logs.map((log, idx) => (
            <div key={idx} className="text-[11px] font-mono border-l-2 border-amber-900 pl-3 py-1">
              <span className="text-amber-500/70">[{log.time.split(' ')[1]}]</span>{' '}
              <span className="text-slate-300">[{log.agent}]</span>{' '}
              <span className="text-slate-400">{log.action}</span>
            </div>
          ))}
          {logs.length === 0 && <p className="text-slate-500 italic text-sm">Memory logs will appear here.</p>}
        </div>
      </div>
    </div>
  );
};
