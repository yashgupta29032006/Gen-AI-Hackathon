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
        <div className="space-y-4">
          {actionsTaken.map((action, idx) => {
            // Debug check for the action object
            if (!action || typeof action !== 'object') return null;
            
            return (
              <div key={idx} className="bg-slate-800/80 p-4 rounded-xl border border-green-500/20 shadow-lg">
                <div className="flex justify-between items-start mb-2">
                  <div className="flex flex-col">
                    <span className="text-[10px] font-black text-green-400 uppercase tracking-tighter">
                      {action.agent || 'AGENT'}
                    </span>
                    <h3 className="text-sm font-bold text-slate-100 uppercase">
                      {action.action || 'EXECUTING...'}
                    </h3>
                  </div>
                  <div className="bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full text-[9px] font-black tracking-widest border border-green-500/30">
                    DONE
                  </div>
                </div>
                
                {action.result ? (
                  <div className="mt-3 bg-black/60 rounded-lg p-3 border border-slate-700/50 group">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-[9px] text-slate-500 font-bold uppercase tracking-widest">Action Result</span>
                      <span className="text-[9px] text-green-500/50 font-mono">SUCCESS</span>
                    </div>
                    <pre className="text-[10px] text-slate-300 font-mono overflow-x-auto max-h-32 scrollbar-thin scrollbar-thumb-slate-800">
                      {JSON.stringify(action.result, null, 2)}
                    </pre>
                  </div>
                ) : action.error ? (
                  <div className="mt-3 bg-red-500/10 rounded-lg p-3 border border-red-500/20">
                    <p className="text-[10px] text-red-400 font-mono">{action.error}</p>
                  </div>
                ) : (
                  <p className="text-[10px] text-slate-500 mt-2 italic font-medium">Task completed with no return data.</p>
                )}
              </div>
            );
          })}
          {actionsTaken.length === 0 && (
            <div className="flex flex-col items-center justify-center py-8 text-slate-600">
              <CheckCircle2 size={32} className="opacity-20 mb-2" />
              <p className="italic text-xs font-semibold uppercase tracking-widest opacity-40">Ready for Mission</p>
            </div>
          )}
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
