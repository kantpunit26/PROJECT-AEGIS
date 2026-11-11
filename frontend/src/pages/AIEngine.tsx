import React, { useState, useEffect } from 'react';
import {
  Cpu,
  Zap,
  ShieldAlert,
  Bot,
  Send,
  Sparkles,
  Layers,
  Activity,
  CheckCircle2,
  AlertTriangle,
  FileText,
  TrendingUp,
  RefreshCw
} from 'lucide-react';
import { api } from '../services/api';
import { MICPredictionResponse, AICopilotBrief } from '../types';
import { SUPPORTED_PATHOGENS } from '../components/common/Header';

interface AIEngineProps {
  selectedOrganism: string;
}

const ORGANISM_PRESET_GENES: Record<string, string[]> = {
  'Klebsiella pneumoniae': ['blaNDM-5', 'blaOXA-181', 'armA', 'GyrA_S83I', 'mgrB_trunc'],
  'Acinetobacter baumannii': ['blaOXA-23', 'blaOXA-51-like', 'armA', 'adeB', 'ISaba1'],
  'Pseudomonas aeruginosa': ['blaVIM-2', 'mexAB-oprM', 'oprD_loss', 'aph(3\')-IIb'],
  'Staphylococcus aureus': ['mecA', 'blaZ', 'lukS/F-PV', 'erm(A)', 'tet(M)'],
  'Enterococcus faecium': ['vanA', 'aac(6\')-Ie-aph(2\'\')-Ia', 'erm(B)', 'tet(M)'],
  'Mycobacterium tuberculosis': ['rpoB_S450L', 'katG_S315T', 'gyrA_D94G', 'embB_M306V']
};

export const AIEngine: React.FC<AIEngineProps> = ({ selectedOrganism }) => {
  const [organism, setOrganism] = useState<string>(selectedOrganism);
  const [selectedGenes, setSelectedGenes] = useState<string[]>(
    ORGANISM_PRESET_GENES[selectedOrganism] || ORGANISM_PRESET_GENES['Klebsiella pneumoniae']
  );
  const [customGene, setCustomGene] = useState('');
  const [micResult, setMicResult] = useState<MICPredictionResponse | null>(null);
  const [isLoadingMIC, setIsLoadingMIC] = useState(false);

  // Copilot State
  const [copilotQuery, setCopilotQuery] = useState('');
  const [copilotBrief, setCopilotBrief] = useState<AICopilotBrief | null>(null);
  const [isLoadingCopilot, setIsLoadingCopilot] = useState(false);

  useEffect(() => {
    setOrganism(selectedOrganism);
    setSelectedGenes(ORGANISM_PRESET_GENES[selectedOrganism] || ['blaNDM-5', 'blaOXA-181']);
  }, [selectedOrganism]);

  useEffect(() => {
    handleRunMICPrediction();
    handleCopilotQuery('NICU Outbreak Transmission Assessment');
  }, [organism]);

  const handleToggleGene = (gene: string) => {
    if (selectedGenes.includes(gene)) {
      setSelectedGenes(selectedGenes.filter((g) => g !== gene));
    } else {
      setSelectedGenes([...selectedGenes, gene]);
    }
  };

  const handleAddCustomGene = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customGene.trim()) return;
    const trimmed = customGene.trim();
    if (!selectedGenes.includes(trimmed)) {
      setSelectedGenes([...selectedGenes, trimmed]);
    }
    setCustomGene('');
  };

  const handleRunMICPrediction = async () => {
    setIsLoadingMIC(true);
    try {
      const res = await api.predictMIC({
        organism,
        genes: selectedGenes
      });
      setMicResult(res);
    } catch (err) {
      console.error('Failed to run MIC prediction:', err);
    } finally {
      setIsLoadingMIC(false);
    }
  };

  const handleCopilotQuery = async (queryText?: string) => {
    const q = queryText || copilotQuery;
    if (!q.trim()) return;
    setIsLoadingCopilot(true);
    try {
      const brief = await api.copilotChat(q, organism);
      setCopilotBrief(brief);
    } catch (err) {
      console.error('Copilot query failed:', err);
    } finally {
      setIsLoadingCopilot(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-6 rounded-xl bg-gradient-to-r from-slate-900 via-slate-900/95 to-slate-950 border border-slate-800 shadow-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-crimson-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-crimson-950 text-crimson-400 border border-crimson-800/60 uppercase">
                Deep Learning v2.4
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800/60">
                DNABERT-Kmer-Regressor
              </span>
            </div>
            <h1 className="text-2xl font-bold text-white mt-2 flex items-center space-x-2">
              <Cpu className="w-6 h-6 text-crimson-500" />
              <span>Continuous MIC Prediction & Epidemiological Copilot</span>
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-3xl">
              Predict continuous Minimum Inhibitory Concentrations (μg/mL) with 95% Confidence Intervals directly from WGS resistance gene dosage, paired with autonomous WHO GLASS / CDC MMWR outbreak brief synthesis.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={handleRunMICPrediction}
              disabled={isLoadingMIC}
              className="flex items-center space-x-2 px-4 py-2 bg-crimson-600 hover:bg-crimson-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-crimson-950 transition-all disabled:opacity-50"
            >
              {isLoadingMIC ? (
                <RefreshCw className="w-4 h-4 animate-spin" />
              ) : (
                <Zap className="w-4 h-4" />
              )}
              <span>Predict MIC Values</span>
            </button>
          </div>
        </div>
      </div>

      {/* Grid: Left Column MIC Predictor / Right Column Copilot */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Continuous MIC Engine (7 Cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Genomic Profile Feature Config */}
          <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-md">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Layers className="w-4 h-4 text-emerald-400" />
                <h2 className="text-sm font-semibold text-slate-200">Genomic Profile Determinants</h2>
              </div>
              <span className="text-[11px] font-mono text-slate-400">
                Organism: <span className="text-emerald-300 italic">{organism}</span>
              </span>
            </div>

            {/* Gene Pills */}
            <div className="flex flex-wrap gap-2 mb-4">
              {(ORGANISM_PRESET_GENES[organism] || []).map((gene) => {
                const active = selectedGenes.includes(gene);
                return (
                  <button
                    key={gene}
                    onClick={() => handleToggleGene(gene)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all border ${
                      active
                        ? 'bg-crimson-950/80 text-crimson-300 border-crimson-700/80 shadow-sm'
                        : 'bg-slate-800/60 text-slate-400 border-slate-700/50 hover:border-slate-600'
                    }`}
                  >
                    {active ? '✓ ' : '+ '}
                    {gene}
                  </button>
                );
              })}
            </div>

            {/* Custom Gene Adder */}
            <form onSubmit={handleAddCustomGene} className="flex gap-2">
              <input
                type="text"
                value={customGene}
                onChange={(e) => setCustomGene(e.target.value)}
                placeholder="Add custom gene (e.g. blaKPC-3, rmtB, GyrA_S83I)..."
                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-crimson-600 font-mono"
              />
              <button
                type="submit"
                className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium border border-slate-700"
              >
                Add Gene
              </button>
            </form>
          </div>

          {/* Predicted MIC Output Cards */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-slate-200 flex items-center space-x-2">
                <Activity className="w-4 h-4 text-crimson-400" />
                <span>Continuous Predicted MIC Values & Breakpoint Interpretation</span>
              </h2>
              {micResult && (
                <span className="text-[11px] font-mono text-slate-500">
                  {micResult.model_version} • {micResult.architecture}
                </span>
              )}
            </div>

            {isLoadingMIC ? (
              <div className="p-12 text-center bg-slate-900 border border-slate-800 rounded-xl">
                <RefreshCw className="w-8 h-8 text-crimson-500 animate-spin mx-auto mb-3" />
                <p className="text-xs text-slate-400">Running DNABERT neural regression across genomic targets...</p>
              </div>
            ) : micResult?.predictions ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {micResult.predictions.map((p, idx) => {
                  const isResistant = p.interpretation === 'RESISTANT';
                  return (
                    <div
                      key={idx}
                      className="p-4 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-all shadow-md relative overflow-hidden"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-sm text-white">{p.antibiotic}</span>
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase ${
                            isResistant
                              ? 'bg-crimson-950 text-crimson-400 border border-crimson-800/80'
                              : 'bg-emerald-950 text-emerald-400 border border-emerald-800/80'
                          }`}
                        >
                          {p.interpretation}
                        </span>
                      </div>

                      {/* Continuous MIC Value */}
                      <div className="my-3 flex items-baseline space-x-2">
                        <span className="text-2xl font-bold font-mono text-white tracking-tight">
                          {p.predicted_mic}
                        </span>
                        <span className="text-xs text-slate-400 font-mono">{p.unit}</span>
                        <span className="text-[10px] font-mono text-slate-500 ml-auto">
                          95% CI: [{p.ci_lower} - {p.ci_upper}]
                        </span>
                      </div>

                      {/* Probability Meter */}
                      <div className="space-y-1 mb-3">
                        <div className="flex justify-between text-[10px] font-mono text-slate-400">
                          <span>Resistance Probability:</span>
                          <span className="text-slate-200">
                            {(p.resistance_probability * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="h-1.5 w-full bg-slate-950 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              isResistant ? 'bg-crimson-500' : 'bg-emerald-500'
                            }`}
                            style={{ width: `${Math.min(100, p.resistance_probability * 100)}%` }}
                          />
                        </div>
                      </div>

                      {/* Breakpoint & Primary Driver */}
                      <div className="pt-2 border-t border-slate-800/80 text-[11px] space-y-1">
                        <div className="flex justify-between text-slate-400 font-mono">
                          <span>EUCAST / CLSI R:</span>
                          <span className="text-slate-300">≥ {p.eucast_breakpoint_r} mg/L</span>
                        </div>
                        <div className="text-[10px] text-slate-400 truncate">
                          <span className="text-slate-500">Driver:</span> {p.primary_driver}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : null}
          </div>

          {/* Attention Weights */}
          {micResult?.feature_attentions && micResult.feature_attentions.length > 0 && (
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow-md">
              <h3 className="text-xs font-semibold text-slate-300 mb-3 flex items-center space-x-2">
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                <span>Deep Feature Attention Weights (Gene Attribution)</span>
              </h3>
              <div className="space-y-2">
                {micResult.feature_attentions.map((att, i) => (
                  <div key={i} className="flex items-center space-x-3 text-xs">
                    <span className="w-28 font-mono text-slate-300 truncate">{att.gene}</span>
                    <div className="flex-1 h-2 bg-slate-950 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-crimson-500 rounded-full"
                        style={{ width: `${att.attention_weight * 100}%` }}
                      />
                    </div>
                    <span className="w-12 text-right font-mono text-[11px] text-slate-400">
                      {(att.attention_weight * 100).toFixed(1)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Autonomous Epidemiological Copilot (5 Cols) */}
        <div className="lg:col-span-5 space-y-6">
          <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-md flex flex-col h-full">
            <div className="flex items-center space-x-2 mb-3">
              <Bot className="w-5 h-5 text-crimson-500" />
              <div>
                <h2 className="text-sm font-semibold text-white">Epidemiological AI Copilot</h2>
                <p className="text-[11px] text-slate-400">
                  Autonomous outbreak investigation briefs & clinical IPC protocols
                </p>
              </div>
            </div>

            {/* Quick Template Prompts */}
            <div className="space-y-1.5 mb-4">
              <p className="text-[10px] font-mono text-slate-500 uppercase tracking-wider">Quick Investigation Queries:</p>
              <div className="flex flex-wrap gap-1.5">
                {[
                  'NICU Outbreak Investigation',
                  'Pan-Drug Colistin Escape Risk',
                  'WHO GLASS Outbreak Synthesis'
                ].map((preset) => (
                  <button
                    key={preset}
                    onClick={() => {
                      setCopilotQuery(preset);
                      handleCopilotQuery(preset);
                    }}
                    className="text-[10px] px-2.5 py-1 rounded-md bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700/60 font-mono transition-colors"
                  >
                    {preset}
                  </button>
                ))}
              </div>
            </div>

            {/* Input Bar */}
            <div className="flex gap-2 mb-4">
              <input
                type="text"
                value={copilotQuery}
                onChange={(e) => setCopilotQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleCopilotQuery()}
                placeholder="Ask epidemiological copilot about clusters, IPC, salvage drugs..."
                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-crimson-600"
              />
              <button
                onClick={() => handleCopilotQuery()}
                disabled={isLoadingCopilot}
                className="px-3 py-2 bg-crimson-600 hover:bg-crimson-500 text-white rounded-lg text-xs font-semibold shadow transition-all disabled:opacity-50"
              >
                {isLoadingCopilot ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              </button>
            </div>

            {/* Brief Output */}
            {isLoadingCopilot ? (
              <div className="flex-1 p-8 text-center bg-slate-950/60 rounded-xl border border-slate-800/60 flex flex-col items-center justify-center">
                <Bot className="w-8 h-8 text-crimson-500 animate-bounce mb-2" />
                <p className="text-xs text-slate-400">Synthesizing clinical outbreak briefing...</p>
              </div>
            ) : copilotBrief ? (
              <div className="flex-1 space-y-4 p-4 rounded-xl bg-slate-950 border border-slate-800 overflow-y-auto max-h-[620px]">
                {/* Header Badge */}
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase ${
                      copilotBrief.severity === 'CRITICAL'
                        ? 'bg-crimson-950 text-crimson-400 border border-crimson-800'
                        : 'bg-amber-950 text-amber-400 border border-amber-800'
                    }`}
                  >
                    {copilotBrief.severity} • Hazard Score {copilotBrief.hazard_score}/100
                  </span>
                  <span className="text-[10px] font-mono text-slate-500">
                    Confidence: {(copilotBrief.model_confidence * 100).toFixed(0)}%
                  </span>
                </div>

                {/* Brief Title */}
                <h3 className="text-xs font-bold text-white leading-snug">{copilotBrief.title}</h3>

                {/* Summary */}
                <div className="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <span className="text-slate-400 font-semibold block mb-1">Executive Summary:</span>
                  {copilotBrief.executive_summary}
                </div>

                {/* Actionable IPC Recommendations */}
                <div>
                  <span className="text-[11px] font-semibold text-slate-300 uppercase tracking-wider block mb-2 flex items-center space-x-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Infection Prevention & Control (IPC) Protocols:</span>
                  </span>
                  <ul className="space-y-2">
                    {copilotBrief.actionable_recommendations.map((rec, i) => (
                      <li
                        key={i}
                        className="text-xs text-slate-300 flex items-start space-x-2 bg-slate-900/40 p-2.5 rounded-lg border border-slate-800/80"
                      >
                        <span className="font-mono text-crimson-400 font-bold shrink-0">{i + 1}.</span>
                        <span>{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
};
