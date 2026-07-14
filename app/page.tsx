const research = [
  {
    index: "01",
    title: "World Models",
    text: "Learning systems that build, revise, and reason over internal representations of complex environments.",
    tags: ["Representation", "Planning", "Dynamics"],
  },
  {
    index: "02",
    title: "Machine Reasoning",
    text: "New architectures for reliable inference, abstraction, and long-horizon problem solving.",
    tags: ["Inference", "Agents", "Verification"],
  },
  {
    index: "03",
    title: "Emergent Intelligence",
    text: "Understanding how coherent capabilities arise from scale, interaction, and adaptive computation.",
    tags: ["Scaling", "Collectives", "Alignment"],
  },
];

const programs = [
  ["P–01", "Latent Geometry", "How do learned spaces encode causality, symmetry, and change?"],
  ["P–02", "Adaptive Systems", "Can models update their own strategies without losing coherence?"],
  ["P–03", "Open Reasoning", "What makes machine reasoning legible, testable, and trustworthy?"],
];

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
        <a className="brand" href="#top" aria-label="Phason Labs home">
          <Mark small />
          <span>PHΛSON LΛBS</span>
        </a>
        <nav aria-label="Primary navigation">
          <a href="#research">Research</a>
          <a href="#programs">Programs</a>
          <a href="#about">About</a>
        </nav>
        <a className="nav-contact" href="mailto:hello@phasonlabs.ai">Contact <span>↗</span></a>
      </header>

      <section className="hero shell" id="top">
        <div className="hero-kicker"><span /> Independent AI research lab · 2026</div>
        <h1>Intelligence is not<br />a fixed <em>state.</em></h1>
        <div className="hero-bottom">
          <p>Phason Labs studies the hidden structures that let intelligent systems shift, adapt, and emerge.</p>
          <a className="circle-link" href="#research" aria-label="Explore our research">↓</a>
        </div>
        <div className="hero-visual" aria-hidden="true">
          <div className="orbital orbital--one" />
          <div className="orbital orbital--two" />
          <Mark />
          <span className="coordinate c1">xₜ</span>
          <span className="coordinate c2">φ + Δφ</span>
        </div>
      </section>

      <section className="statement">
        <div className="shell statement-inner">
          <p className="eyebrow">Our premise</p>
          <p className="statement-copy">The most important advances in AI will come from understanding <span>how intelligence reorganizes itself</span>—not simply from making today&apos;s systems larger.</p>
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
              <span className="card-index">{item.index}</span>
              <div className={`card-glyph glyph-${item.index}`}><span /></div>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
              <div className="tags">{item.tags.map((tag) => <span key={tag}>{tag}</span>)}</div>
            </article>
          ))}
        </div>
      </section>

      <section className="programs" id="programs">
        <div className="shell">
          <div className="section-head inverse">
            <div><p className="eyebrow violet">Active programs</p><h2>Questions in motion.</h2></div>
            <p>Long-term investigations designed to produce open knowledge, useful systems, and better questions.</p>
          </div>
          <div className="program-list">
            {programs.map(([id, title, text]) => (
              <article key={id}>
                <span>{id}</span><h3>{title}</h3><p>{text}</p><b>↗</b>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="about shell" id="about">
        <div className="about-mark"><Mark /><span>PHASON /ˈfeɪzɒn/</span></div>
        <div className="about-copy">
          <p className="eyebrow violet">Why Phason</p>
          <h2>A different kind of motion.</h2>
          <p>In a quasicrystal, a phason is a rearrangement that changes the structure without moving it in ordinary space. It is motion through a hidden dimension.</p>
          <p>That is how we think about intelligence: not as a static object, but as a system capable of discovering new internal configurations.</p>
        </div>
      </section>

      <footer>
        <div className="shell footer-top">
          <p>Have a question worth<br />reorganizing around?</p>
          <a href="mailto:hello@phasonlabs.ai">hello@phasonlabs.ai <span>↗</span></a>
        </div>
        <div className="shell footer-bottom"><span>© 2026 Phason Labs</span><span>Research for intelligence in motion.</span><a href="#top">Back to top ↑</a></div>
      </footer>
    </main>
  );
}
