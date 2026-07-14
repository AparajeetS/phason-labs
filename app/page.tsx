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
  {
    id: "P–01",
    title: "MBE",
    status: "Research direction",
    text: "A research program investigating how internal model structures can support adaptive, compositional intelligence.",
    href: "https://github.com/AparajeetS/marginal-baseline-eval",
  },
  {
    id: "P–02",
    title: "TrainTools",
    status: "Open source",
    text: "Practical, transparent tooling for training experiments, evaluation workflows, and reproducible AI research.",
    href: "https://github.com/AparajeetS/Traintools",
  },
  {
    id: "E–01",
    title: "Latent Dynamics",
    status: "To be explored",
    text: "Studying whether models can discover stable internal laws for worlds that change beneath them.",
    href: "#contact",
  },
  {
    id: "E–02",
    title: "Collective Inference",
    status: "To be explored",
    text: "Exploring how groups of specialized models might reason together without collapsing into consensus.",
    href: "#contact",
  },
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
        <a className="nav-contact" href="#contact">Contact <span>↘</span></a>
      </header>

      <section className="hero shell" id="top">
        <div className="hero-kicker"><span /> Independent AI research lab · 2026</div>
        <h1>Intelligence is not<br />a fixed <em>state.</em></h1>
        <div className="hero-bottom">
          <p>Phason Labs studies the hidden structures that let intelligent systems shift, adapt, reason, and emerge.</p>
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
            <p>Current work and carefully framed questions that define where the lab may look next.</p>
          </div>
          <div className="program-list">
            {programs.map((program) => (
              <a href={program.href} target={program.href.startsWith("http") ? "_blank" : undefined} rel={program.href.startsWith("http") ? "noreferrer" : undefined} key={program.id}>
                <article>
                  <span>{program.id}</span>
                  <div><h3>{program.title}</h3><small>{program.status}</small></div>
                  <p>{program.text}</p><b>↗</b>
                </article>
              </a>
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

      <section className="founder" id="contact">
        <div className="shell founder-grid">
          <div>
            <p className="eyebrow violet">The lab</p>
            <h2>Independent by design.</h2>
          </div>
          <div className="founder-profile">
            <p>Phason Labs is an independent AI research lab founded by <strong>Aparajeet Shadangi</strong> in Bhubaneswar, India.</p>
            <p>We are at the beginning: forming research directions, building open tools, and looking for the questions that matter before the answers become obvious.</p>
            <dl>
              <div><dt>Founder</dt><dd>Aparajeet Shadangi</dd></div>
              <div><dt>Location</dt><dd>Bhubaneswar, India</dd></div>
              <div><dt>Email</dt><dd><a href="mailto:aparajeet.shadangi@proton.me">aparajeet.shadangi@proton.me ↗</a></dd></div>
              <div><dt>GitHub</dt><dd><a href="https://github.com/AparajeetS" target="_blank" rel="noreferrer">github.com/AparajeetS ↗</a></dd></div>
            </dl>
          </div>
        </div>
      </section>

      <footer>
        <div className="shell footer-top">
          <p>Have a question worth<br />reorganizing around?</p>
          <a href="mailto:aparajeet.shadangi@proton.me">aparajeet.shadangi@proton.me <span>↗</span></a>
        </div>
        <div className="shell footer-bottom"><span>© 2026 Phason Labs</span><span>Research for intelligence in motion.</span><a href="#top">Back to top ↑</a></div>
      </footer>
    </main>
  );
}
