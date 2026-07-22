const research = [
  { index: "01", title: "World Models", text: "Learning systems that build, revise, and reason over internal representations of complex environments.", tags: ["Representation", "Planning", "Dynamics"] },
  { index: "02", title: "Machine Reasoning", text: "New architectures for reliable inference, abstraction, and long-horizon problem solving.", tags: ["Inference", "Agents", "Verification"] },
  { index: "03", title: "Emergent Intelligence", text: "Understanding how coherent capabilities arise from scale, interaction, and adaptive computation.", tags: ["Scaling", "Collectives", "Alignment"] },
];

const programs = [
  { id: "P-01", title: "MBE", status: "Research direction", text: "Audits whether training metrics retain information about held-out performance after ordinary baselines are controlled.", href: "https://github.com/AparajeetS/marginal-baseline-eval" },
  { id: "P-02", title: "TrainTools", status: "Open source", text: "Paper-backed PyTorch diagnostics for gradients, data quality, batch size, plasticity, and stopping.", href: "https://github.com/AparajeetS/Traintools" },
  { id: "E-01", title: "Latent Dynamics", status: "To be explored", text: "Studying whether models can discover stable internal laws for worlds that change beneath them.", href: "#contact" },
  { id: "E-02", title: "Collective Inference", status: "To be explored", text: "Exploring how groups of specialized models might reason together without collapsing into consensus.", href: "#contact" },
];

const telemetry = {
  mbe: {
    name: "MBE",
    packageName: "mbe-eval",
    repo: "AparajeetS/marginal-baseline-eval",
    date: "18 July 2026",
    summary: "Stronger curiosity signal: substantial GitHub views and clones, but no public engagement markers yet.",
    links: [
      { label: "PyPI", href: "https://pypi.org/project/mbe-eval/" },
      { label: "GitHub", href: "https://github.com/AparajeetS/marginal-baseline-eval" },
      { label: "Agent guide", href: "https://github.com/AparajeetS/marginal-baseline-eval/blob/master/AGENTS.md" },
      { label: "llms.txt", href: "https://github.com/AparajeetS/marginal-baseline-eval/blob/master/llms.txt" },
    ],
    stats: [
      { value: "~725", label: "PyPI downloads since 23 Jun, mirrors excluded" },
      { value: "122", label: "Unique GitHub viewers over 14 days" },
      { value: "100", label: "Unique GitHub cloners over 14 days" },
      { value: "0", label: "Stars, forks, watchers, and open issues" },
    ],
    notes: [
      "Largest observed PyPI days: 175 downloads on 13 Jul and 102 on 17 Jul.",
      "GitHub traffic peaked on 13 Jul with 99 unique viewers and 37 unique cloners.",
      "Interpretation: organic curiosity is plausible; public adoption is not established.",
    ],
  },
  traintools: {
    name: "TrainTools",
    packageName: "traintools",
    repo: "AparajeetS/Traintools",
    date: "18 July 2026",
    summary: "Early package activity with release-shaped spikes; adoption signal is still weak.",
    links: [
      { label: "PyPI", href: "https://pypi.org/project/traintools/" },
      { label: "GitHub", href: "https://github.com/AparajeetS/Traintools" },
      { label: "Agent guide", href: "https://github.com/AparajeetS/Traintools/blob/main/AGENTS.md" },
      { label: "llms.txt", href: "https://github.com/AparajeetS/Traintools/blob/main/llms.txt" },
    ],
    stats: [
      { value: "545", label: "PyPI downloads last month, mirrors excluded" },
      { value: "253", label: "PyPI downloads last week, mirrors excluded" },
      { value: "37", label: "PyPI downloads last day, mirrors excluded" },
      { value: "37", label: "Unique GitHub cloners over 14 days" },
    ],
    notes: [
      "Latest public release observed: v0.6.2 on 16 Jul.",
      "GitHub showed 6 unique viewers over 14 days, with 0 stars and 0 forks.",
      "Interpretation: some touches and installs; not enough evidence for organic users yet.",
    ],
  },
};

function Mark({ small = false }: { small?: boolean }) {
  return (
    <span className={`mark ${small ? "mark--small" : ""}`} aria-hidden="true">
      <span className="plane plane--back" />
      <span className="plane plane--front" />
      <span className="phase"><i /></span>
    </span>
  );
}

export default function Home() {
  return (
    <main>
      <header className="nav shell">
        <a className="brand" href="#top" aria-label="Phason Labs home"><Mark small /><span>PHASON LABS</span></a>
        <nav aria-label="Primary navigation">
          <a href="#research">Research</a><a href="#programs">Programs</a><a href="#evidence">Evidence</a><a href="#about">About</a>
        </nav>
        <a className="nav-contact" href="#contact">Contact <span aria-hidden="true">&#8599;</span></a>
      </header>

      <section className="hero shell" id="top">
        <div className="hero-kicker"><span /> Independent AI research lab / 2026</div>
        <h1>Intelligence is not<br />a fixed <em>state.</em></h1>
        <div className="hero-bottom">
          <p>Phason Labs studies the hidden structures that let intelligent systems shift, adapt, reason, and emerge.</p>
          <a className="circle-link" href="#research" aria-label="Explore our research">&#8595;</a>
        </div>
        <div className="hero-visual" aria-hidden="true">
          <div className="orbital orbital--one" /><div className="orbital orbital--two" /><Mark />
          <span className="coordinate c1">x(t)</span><span className="coordinate c2">phi + delta</span>
        </div>
      </section>

      <section className="statement">
        <div className="shell statement-inner">
          <p className="eyebrow">Our premise</p>
          <p className="statement-copy">The most important advances in AI will come from understanding <span>how intelligence reorganizes itself</span>, not simply from making today&apos;s systems larger.</p>
        </div>
      </section>

      <section className="section shell" id="research">
        <div className="section-head">
          <div><p className="eyebrow violet">Research vectors</p><h2>Where we look.</h2></div>
          <p>We work across theory and experiment, following questions that conventional boundaries tend to hide.</p>
        </div>
        <div className="research-grid">
          {research.map((item) => (
            <article className="research-card" key={item.index}>
              <span className="card-index">{item.index}</span><div className={`card-glyph glyph-${item.index}`}><span /></div>
              <h3>{item.title}</h3><p>{item.text}</p><div className="tags">{item.tags.map((tag) => <span key={tag}>{tag}</span>)}</div>
            </article>
          ))}
        </div>
      </section>

      <section className="programs" id="programs">
        <div className="shell">
          <div className="section-head inverse">
            <div><p className="eyebrow violet">Active programs</p><h2>Questions in motion.</h2></div>
            <p>Current work and carefully framed questions that define where the lab may look next.</p>
          </div>
          <div className="program-list">
            {programs.map((program) => (
              <a href={program.href} target={program.href.startsWith("http") ? "_blank" : undefined} rel={program.href.startsWith("http") ? "noreferrer" : undefined} key={program.id}>
                <article><span>{program.id}</span><div><h3>{program.title}</h3><small>{program.status}</small></div><p>{program.text}</p><b aria-hidden="true">&#8599;</b></article>
              </a>
            ))}
          </div>
        </div>
      </section>

      <section className="evidence" id="evidence">
        <div className="shell">
          <div className="section-head evidence-head">
            <div><p className="eyebrow violet">Controlled benchmark / 18 July 2026</p><h2>Measured, then claimed.</h2></div>
            <p>We tested the public PyPI releases of TrainTools and MBE on a frozen synthetic classification protocol: 48 configurations, each trained once normally and once with instrumentation.</p>
          </div>
          <div className="evidence-grid" aria-label="Controlled benchmark results">
            <div className="evidence-stat"><strong>48 / 48</strong><span>Exact final-model matches</span></div>
            <div className="evidence-stat"><strong>100 / 100</strong><span>Injected faults detected</span></div>
            <div className="evidence-stat"><strong>0 / 50</strong><span>Clean-control warnings</span></div>
            <div className="evidence-stat"><strong>0.99995</strong><span>Mean AUM AUROC</span></div>
          </div>
          <div className="evidence-detail">
            <div>
              <p className="evidence-lead">Instrumentation left every final parameter hash, validation loss, and test accuracy unchanged. The known-failure suite detected NaNs, invalid labels, extreme class imbalance, and amplified gradients in all 25 trials per condition.</p>
              <p>AUM identified injected label noise at 99.5% mean precision in the top 20%, against a 20% random baseline. Median instrumented runtime was 1.19x in this tiny, CPU-bound, probe-heavy benchmark; that figure is descriptive and is not a production-overhead claim.</p>
            </div>
            <div className="evidence-links" aria-label="Benchmark artifacts">
              <a href="/evidence/traintools-controlled-2026-07-18/PROTOCOL.md">Full protocol <span aria-hidden="true">&#8599;</span></a>
              <a href="/evidence/traintools-controlled-2026-07-18/benchmark_summary.json">Summary JSON <span aria-hidden="true">&#8599;</span></a>
              <a href="/evidence/traintools-controlled-2026-07-18/run_benchmark.py">Reproduction script <span aria-hidden="true">&#8599;</span></a>
              <a href="/evidence/traintools-controlled-2026-07-18/paired_runs.csv">Run ledger <span aria-hidden="true">&#8599;</span></a>
            </div>
          </div>
          <div className="evidence-development">
            <div className="evidence-development-head">
              <div><p className="eyebrow violet">PTDB-1 architecture replication / 22 July 2026</p><h3>Two architectures.<br />Every row auditable.</h3></div>
              <p>ResNet-18 and WRN-28-2 now have separate raw-data bundles, frozen analyses, and standard-library audits.</p>
            </div>
            <div className="development-stats" aria-label="PTDB-1 verification summary">
              <div><strong>810k</strong><span>Example-level records recomputed</span></div>
              <div><strong>24 / 24</strong><span>Complete executions</span></div>
              <div><strong>6 / 6</strong><span>Exact clean model pairs</span></div>
              <div><strong>5.5e-15</strong><span>Maximum metric discrepancy</span></div>
            </div>
            <p>Across both architectures, AUM reached 0.9872 aggregate AUROC and beat mean loss in all twelve noisy runs. AUM led EL2N in all six symmetric-noise runs; EL2N led AUM in all six class-conditional runs. The metric ordering replicated with the corruption regime.</p>
            <p className="evidence-caveat"><strong>Boundary:</strong> synthetic corruption, one dataset, two related CNNs, and four regime clusters. Gradient-norm and stopping claims are withheld; the protected holdout remains sealed.</p>
            <div className="development-links"><a href="/evidence/ptdb-1-cifar10-wrn28-2-2026-07-22/CROSS_ARCHITECTURE.md">Combined result</a><a href="/evidence/ptdb-1-cifar10-wrn28-2-2026-07-22/DUE_DILIGENCE.md">WRN due diligence</a><a href="/evidence/ptdb-1-cifar10-resnet18-2026-07-22/DUE_DILIGENCE.md">ResNet due diligence</a></div>
          </div>
          <div className="evidence-boundary">
            <p className="eyebrow">Publication boundary</p>
            <p>The accompanying 48-row MBE audit is not used as promotional evidence because its random negative control missed the frozen point-estimate threshold, although its confidence interval crossed zero. The first defective attempt, correction log, and corrected output remain public.</p>
            <div><a href="/evidence/traintools-controlled-2026-07-18/CORRECTION_LOG.md">Correction log</a><a href="/evidence/traintools-controlled-2026-07-18/mbe_report.md">Withheld MBE report</a></div>
          </div>
        </div>
      </section>

      <section className="telemetry shell" id="telemetry">
        <div className="section-head">
          <div><p className="eyebrow violet">Public telemetry / 18 July 2026</p><h2>Attention is not adoption.</h2></div>
          <p>Package downloads and repository traffic are reported as weak public signals. They help track curiosity, but they do not prove active users.</p>
        </div>
        <div className="telemetry-tabs">
          <input type="radio" name="telemetry" id="telemetry-mbe" defaultChecked />
          <input type="radio" name="telemetry" id="telemetry-traintools" />
          <div className="tab-controls" role="tablist" aria-label="Project telemetry">
            <label htmlFor="telemetry-mbe" role="tab">MBE</label>
            <label htmlFor="telemetry-traintools" role="tab">TrainTools</label>
          </div>
          {(["mbe", "traintools"] as const).map((key) => {
            const project = telemetry[key];
            return (
              <article className={`telemetry-panel telemetry-panel--${key}`} key={project.name}>
                <div className="telemetry-intro">
                  <p className="eyebrow">{project.packageName}</p>
                  <h3>{project.name}</h3>
                  <p>{project.summary}</p>
                  <div>
                    {project.links.map((link) => (
                      <a href={link.href} target="_blank" rel="noreferrer" key={link.label}>{link.label} <span aria-hidden="true">&#8599;</span></a>
                    ))}
                  </div>
                </div>
                <div className="telemetry-stats">
                  {project.stats.map((stat) => (
                    <div className="telemetry-stat" key={stat.label}><strong>{stat.value}</strong><span>{stat.label}</span></div>
                  ))}
                </div>
                <ul className="telemetry-notes">
                  {project.notes.map((note) => <li key={note}>{note}</li>)}
                </ul>
              </article>
            );
          })}
        </div>
      </section>

      <section className="about shell" id="about">
        <div className="about-mark"><Mark /><span>PHASON / FAY-ZON /</span></div>
        <div className="about-copy">
          <p className="eyebrow violet">Why Phason</p><h2>A different kind of motion.</h2>
          <p>In a quasicrystal, a phason is a rearrangement that changes the structure without moving it in ordinary space. It is motion through a hidden dimension.</p>
          <p>That is how we think about intelligence: not as a static object, but as a system capable of discovering new internal configurations.</p>
        </div>
      </section>

      <section className="founder" id="contact">
        <div className="shell founder-grid">
          <div><p className="eyebrow violet">The lab</p><h2>Independent by design.</h2></div>
          <div className="founder-profile">
            <p>Phason Labs is an independent AI research lab founded by <strong>Aparajeet Shadangi</strong> in Bhubaneswar, India.</p>
            <p>We are at the beginning: forming research directions, building open tools, and looking for the questions that matter before the answers become obvious.</p>
            <dl>
              <div><dt>Founder</dt><dd>Aparajeet Shadangi</dd></div><div><dt>Location</dt><dd>Bhubaneswar, India</dd></div>
              <div><dt>Email</dt><dd><a href="mailto:aparajeet.shadangi@proton.me">aparajeet.shadangi@proton.me &#8599;</a></dd></div>
              <div><dt>GitHub</dt><dd><a href="https://github.com/AparajeetS" target="_blank" rel="noreferrer">github.com/AparajeetS &#8599;</a></dd></div>
            </dl>
          </div>
        </div>
      </section>

      <footer>
        <div className="shell footer-top"><p>Have a question worth<br />reorganizing around?</p><a href="mailto:aparajeet.shadangi@proton.me">aparajeet.shadangi@proton.me <span>&#8599;</span></a></div>
        <div className="shell footer-bottom"><span>&copy; 2026 Phason Labs</span><span>Research for intelligence in motion.</span><a href="#top">Back to top &#8593;</a></div>
      </footer>
    </main>
  );
}
