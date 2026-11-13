import React, { useState } from 'react';
import {
  Mail,
  Linkedin,
  Github,
  ExternalLink,
  Copy,
  Check,
  Shield,
  Sparkles,
  Dna,
  Cpu,
  Radio,
  Layers,
  Heart,
  Award,
  Globe,
  Terminal,
  ArrowRight,
  Send,
  CheckCircle2,
  Share2
} from 'lucide-react';

export const About: React.FC = () => {
  const [copiedEmail, setCopiedEmail] = useState(false);
  const [copiedShare, setCopiedShare] = useState(false);

  const founderEmail = 'punitkant26@gmail.com';
  const founderLinkedIn = 'https://www.linkedin.com/in/punit-kant';
  const founderGitHub = 'https://github.com/kantpunit26';
  const repoGitHub = 'https://github.com/kantpunit26/PROJECT-AEGIS';

  const handleCopyEmail = () => {
    navigator.clipboard.writeText(founderEmail);
    setCopiedEmail(true);
    setTimeout(() => setCopiedEmail(false), 2200);
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: 'PROJECT AEGIS - AMR Intelligence Platform',
        text: 'Explore PROJECT AEGIS, an advanced genomic epidemiology & antimicrobial resistance intelligence platform founded by Punit Kant.',
        url: window.location.href,
      }).catch(() => {});
    } else {
      navigator.clipboard.writeText(window.location.href);
      setCopiedShare(true);
      setTimeout(() => setCopiedShare(false), 2200);
    }
  };

  return (
    <div className="space-y-6 pb-12 animate-in fade-in duration-300">
      {/* Top Banner / Hero */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-slate-850 to-slate-900 border border-slate-800 p-6 sm:p-8 lg:p-10 shadow-xl">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-80 h-80 bg-crimson-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-1/3 -mb-10 w-72 h-72 bg-emerald-600/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-5">
            {/* Avatar / Monogram */}
            <div className="relative shrink-0">
              <div className="w-20 h-20 sm:w-24 sm:h-24 rounded-2xl bg-gradient-to-br from-crimson-600 via-slate-800 to-emerald-600 p-0.5 shadow-xl shadow-crimson-950/40">
                <div className="w-full h-full bg-slate-950 rounded-2xl flex items-center justify-center font-mono font-black text-2xl sm:text-3xl tracking-wider text-transparent bg-clip-text bg-gradient-to-tr from-crimson-400 via-slate-100 to-emerald-400">
                  PK
                </div>
              </div>
              <span className="absolute -bottom-1 -right-1 flex h-4 w-4">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-4 w-4 bg-emerald-500 border-2 border-slate-900"></span>
              </span>
            </div>

            <div>
              <div className="flex flex-wrap items-center gap-2 mb-1.5">
                <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                  Punit Kant
                </h1>
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-semibold bg-crimson-950 text-crimson-400 border border-crimson-800/60">
                  <Shield className="w-3 h-3 text-crimson-400" />
                  FOUNDER & ARCHITECT
                </span>
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800/60">
                  <Sparkles className="w-3 h-3 text-emerald-400" />
                  PROJECT AEGIS
                </span>
              </div>
              <p className="text-slate-300 text-sm sm:text-base font-medium max-w-2xl leading-relaxed">
                Systems & AI Architect pioneering computational genomics, real-time AMR biosurveillance, and One Health wastewater intelligence.
              </p>
              <p className="text-xs font-mono text-slate-400 mt-1 flex items-center gap-1.5">
                <Globe className="w-3.5 h-3.5 text-emerald-400" />
                Global Public Health Security & Computational Pathogen Genomics
              </p>
            </div>
          </div>

          {/* Social & Contact Actions */}
          <div className="flex flex-wrap sm:flex-nowrap items-center gap-2.5 w-full lg:w-auto">
            <a
              href={`mailto:${founderEmail}?subject=[PROJECT AEGIS] Collaboration Inquiry`}
              className="flex-1 sm:flex-initial inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-crimson-600 hover:bg-crimson-500 text-white font-medium text-xs rounded-lg shadow-lg shadow-crimson-950/60 transition-all hover:scale-[1.02]"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Contact Founder</span>
            </a>

            <button
              onClick={handleCopyEmail}
              className="inline-flex items-center justify-center gap-1.5 px-3 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-mono transition-all"
              title="Copy email to clipboard"
            >
              {copiedEmail ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400 font-semibold">Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5 text-slate-400" />
                  <span>Copy Email</span>
                </>
              )}
            </button>

            <button
              onClick={handleShare}
              className="inline-flex items-center justify-center p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 rounded-lg text-xs transition-colors"
              title="Share Platform"
            >
              {copiedShare ? <Check className="w-4 h-4 text-emerald-400" /> : <Share2 className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Quick Links Bar */}
        <div className="mt-6 pt-5 border-t border-slate-800 flex flex-wrap items-center gap-3 text-xs">
          <a
            href={founderLinkedIn}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-md bg-blue-950/50 hover:bg-blue-900/60 text-blue-300 border border-blue-800/60 transition-all hover:scale-[1.02]"
          >
            <Linkedin className="w-3.5 h-3.5 text-blue-400" />
            <span className="font-medium">LinkedIn Profile</span>
            <ExternalLink className="w-3 h-3 text-blue-400/80" />
          </a>

          <a
            href={founderGitHub}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-md bg-slate-800/70 hover:bg-slate-700/80 text-slate-200 border border-slate-700 transition-all hover:scale-[1.02]"
          >
            <Github className="w-3.5 h-3.5 text-slate-300" />
            <span className="font-medium">GitHub: kantpunit26</span>
            <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>

          <a
            href={repoGitHub}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-md bg-crimson-950/50 hover:bg-crimson-900/60 text-crimson-300 border border-crimson-800/60 transition-all hover:scale-[1.02]"
          >
            <Github className="w-3.5 h-3.5 text-crimson-400" />
            <span className="font-medium">Project Repository (PROJECT-AEGIS)</span>
            <ExternalLink className="w-3 h-3 text-crimson-400/80" />
          </a>

          <div className="ml-auto text-[11px] font-mono text-slate-400 hidden sm:flex items-center gap-1.5">
            <Mail className="w-3.5 h-3.5 text-slate-500" />
            <span>{founderEmail}</span>
          </div>
        </div>
      </div>

      {/* Founder's Mission Statement */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 sm:p-7 space-y-4">
          <div className="flex items-center space-x-2 text-crimson-500">
            <Heart className="w-5 h-5 fill-crimson-500/20" />
            <h2 className="text-base sm:text-lg font-bold text-white tracking-wide">
              Founder's Vision: The Mission Behind Project AEGIS
            </h2>
          </div>

          <div className="space-y-3.5 text-xs sm:text-sm text-slate-300 leading-relaxed">
            <p>
              Antimicrobial Resistance (AMR) is officially classified by the World Health Organization (WHO) as one of humanity's top ten global public health threats. Over 1.27 million deaths occur each year directly due to drug-resistant pathogens, and conservative projections forecast that number reaching <strong className="text-crimson-400">10 million deaths annually by 2050</strong> if left unaddressed.
            </p>
            <p>
              Traditional hospital diagnostics and manual surveillance silos fail to keep pace with the exponential velocity of mobile genetic elements, plasmid horizontal gene transfers, and multi-drug resistant superbug lineages. Crucial surveillance data often arrives weeks after outbreaks have already metastasized across regional healthcare systems.
            </p>
            <p>
              <strong className="text-white">PROJECT AEGIS</strong> was conceived and engineered by <strong className="text-emerald-400">Punit Kant</strong> to shatter these latency bottlenecks. It unifies high-throughput whole genome sequencing (WGS), multi-pathogen ESKAPE analytics, deep learning continuous minimum inhibitory concentration (MIC) prediction, and One Health wastewater surveillance into a singular, responsive, real-time epidemiological radar.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4 border-t border-slate-800">
            <div className="bg-slate-950/60 p-3.5 rounded-lg border border-slate-800/80">
              <div className="text-xs font-mono text-crimson-400 font-semibold mb-1">REAL-TIME SURVEILLANCE</div>
              <p className="text-[11px] text-slate-400">Zero-latency genomic clustering & spatio-temporal transmission mapping across healthcare jurisdictions.</p>
            </div>
            <div className="bg-slate-950/60 p-3.5 rounded-lg border border-slate-800/80">
              <div className="text-xs font-mono text-emerald-400 font-semibold mb-1">DEEP MIC PREDICTION</div>
              <p className="text-[11px] text-slate-400">Continuous quantitative resistance forecasting from raw genomic k-mers, outperforming categorical classifiers.</p>
            </div>
            <div className="bg-slate-950/60 p-3.5 rounded-lg border border-slate-800/80">
              <div className="text-xs font-mono text-blue-400 font-semibold mb-1">ONE HEALTH RADAR</div>
              <p className="text-[11px] text-slate-400">10-14 day early warning anomaly detection from municipal sewage sheds and agricultural reservoirs.</p>
            </div>
          </div>
        </div>

        {/* Contact & Connect Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between space-y-5">
          <div>
            <div className="flex items-center space-x-2 text-emerald-400 mb-3">
              <Award className="w-5 h-5" />
              <h3 className="text-base font-bold text-white">Direct Connect</h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed mb-4">
              Interested in collaborating, contributing genomic datasets, integrating AEGIS into your clinical network, or research discussions?
            </p>

            <div className="space-y-3">
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span className="text-[10px] font-mono uppercase text-slate-500 font-semibold block mb-0.5">Contact Email</span>
                <a
                  href={`mailto:${founderEmail}`}
                  className="text-xs font-mono text-emerald-400 hover:text-emerald-300 transition-colors flex items-center justify-between"
                >
                  <span className="truncate">{founderEmail}</span>
                  <ExternalLink className="w-3.5 h-3.5 shrink-0 ml-1 text-slate-500" />
                </a>
              </div>

              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span className="text-[10px] font-mono uppercase text-slate-500 font-semibold block mb-0.5">LinkedIn Network</span>
                <a
                  href={founderLinkedIn}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs font-mono text-blue-400 hover:text-blue-300 transition-colors flex items-center justify-between"
                >
                  <span>linkedin.com/in/punit-kant</span>
                  <ExternalLink className="w-3.5 h-3.5 shrink-0 ml-1 text-slate-500" />
                </a>
              </div>

              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span className="text-[10px] font-mono uppercase text-slate-500 font-semibold block mb-0.5">GitHub Profile</span>
                <a
                  href={founderGitHub}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs font-mono text-slate-300 hover:text-white transition-colors flex items-center justify-between"
                >
                  <span>github.com/kantpunit26</span>
                  <ExternalLink className="w-3.5 h-3.5 shrink-0 ml-1 text-slate-500" />
                </a>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800">
            <a
              href={`mailto:${founderEmail}?subject=[PROJECT AEGIS] Research & Collaboration`}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-crimson-600 to-crimson-700 hover:from-crimson-500 hover:to-crimson-600 text-white font-medium text-xs rounded-lg shadow-md transition-all text-center"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Reach Out to Punit</span>
            </a>
          </div>
        </div>
      </div>

      {/* Platform Architecture & Specifications */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 sm:p-7">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center space-x-2">
            <Terminal className="w-5 h-5 text-emerald-400" />
            <h2 className="text-base sm:text-lg font-bold text-white tracking-wide">
              Architectural Specifications & Capabilities
            </h2>
          </div>
          <span className="text-[11px] font-mono text-slate-400 bg-slate-800/80 px-2.5 py-1 rounded border border-slate-700/60">
            v2.0 Full Spectrum
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-lg bg-slate-950/70 border border-slate-800">
            <div className="flex items-center gap-2 mb-2">
              <Dna className="w-4 h-4 text-crimson-400" />
              <h4 className="text-xs font-mono font-bold text-slate-200">ESKAPE+ Pathogens</h4>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Real-time surveillance for K. pneumoniae, A. baumannii, P. aeruginosa, S. aureus, E. faecium, and M. tuberculosis.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-950/70 border border-slate-800">
            <div className="flex items-center gap-2 mb-2">
              <Cpu className="w-4 h-4 text-emerald-400" />
              <h4 className="text-xs font-mono font-bold text-slate-200">AI Deep Learning Engine</h4>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Dual-layer ResNet/Transformer continuous MIC regression and AI Copilot for rapid clinical risk triage.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-950/70 border border-slate-800">
            <div className="flex items-center gap-2 mb-2">
              <Radio className="w-4 h-4 text-amber-400" />
              <h4 className="text-xs font-mono font-bold text-slate-200">One Health Wastewater</h4>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Cross-reservoir plasmid transfer tracking between clinical, municipal wastewater, animal, and agricultural streams.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-950/70 border border-slate-800">
            <div className="flex items-center gap-2 mb-2">
              <Layers className="w-4 h-4 text-blue-400" />
              <h4 className="text-xs font-mono font-bold text-slate-200">Spatio-Temporal SEIR</h4>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Dynamic hospital compartment modeling, R0 estimation, and multi-channel emergency alert dispatch protocols.
            </p>
          </div>
        </div>

        {/* Tech Stack Pills */}
        <div className="mt-6 pt-5 border-t border-slate-800 flex flex-wrap items-center gap-2">
          <span className="text-[11px] font-mono text-slate-400 mr-2">Core Stack:</span>
          {['React 18', 'TypeScript', 'Tailwind CSS', 'FastAPI', 'Python 3.11', 'PyTorch', 'BioPython', 'NetworkX', 'PostGIS', 'DeckGL / WGS84', 'Nextflow Pipelines'].map((tech) => (
            <span
              key={tech}
              className="px-2.5 py-1 rounded bg-slate-800/80 text-slate-300 border border-slate-700/60 text-[10px] font-mono"
            >
              {tech}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};
