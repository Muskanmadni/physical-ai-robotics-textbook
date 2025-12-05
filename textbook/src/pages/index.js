import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";

export default function Home() {
  return (
    <Layout
      title="AI-Native Textbook for Physical AI & Humanoid Robotics"
      description="Complete learning system for mastering robotics, humanoids, ROS2, VLA systems, and embodied AI."
    >
      {/* HERO SECTION */}
      <header
        style={{
          padding: "80px 20px",
          textAlign: "center",
          background: "linear-gradient(135deg, #0b0f19, #1f2a44)",
          color: "white",
        }}
      >
        <h1 style={{ fontSize: "54px", fontWeight: "bold", marginBottom: "20px" }}>
          AI-Native Textbook for Physical AI & Humanoid Robotics
        </h1>
        <p style={{ fontSize: "22px", maxWidth: "850px", margin: "0 auto", lineHeight: "1.6" }}>
          Master the cutting-edge field of embodied artificial intelligence:
          humanoid robotics, ROS 2, vision-language-action systems, simulation, and
          AI for physical machines that interact with the real world.
        </p>

        <div style={{ marginTop: "40px" }}>
          <Link
            className="button button--primary button--lg"
            to="/docs/introduction/"
          >
            Start Reading →
          </Link>
        </div>
      </header>

      {/* ABOUT SECTION */}
      <section style={{ padding: "60px 20px", maxWidth: "1000px", margin: "0 auto" }}>
        <h2 style={{ fontSize: "36px", marginBottom: "20px", textAlign: "center" }}>
          Master Embodied Intelligence & Physical AI
        </h2>
        <p style={{ fontSize: "20px", lineHeight: "1.7", color: "#444", textAlign: "center" }}>
          This comprehensive curriculum covers the foundations of embodied artificial intelligence,
          from core robotics principles to advanced humanoid systems. You'll learn ROS 2 development,
          simulation environments, hardware integration, VLA (Vision-Language-Action) systems, motion
          planning, and how to build AI that interacts with the physical world. Each module provides
          hands-on experience with cutting-edge technologies used in modern robotics.
        </p>
      </section>

      {/* MODULE CARDS */}
      <section style={{ padding: "60px 20px", background: "#f9fafc" }}>
        <h2 style={{ fontSize: "32px", marginBottom: "40px", textAlign: "center" }}>
          Core Learning Modules
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "25px",
            maxWidth: "1200px",
            margin: "0 auto",
          }}
        >
          {/* INTRODUCTION */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>Introduction</h3>
            <p style={cardText}>
              Overview of Physical AI and Humanoid Robotics. Understanding the fundamentals
              of embodied intelligence and the roadmap for building intelligent physical systems.
            </p>
            <Link style={cardBtn} to="/docs/introduction/">
              Start Learning →
            </Link>
          </div>

          {/* MODULE 1 */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>Module 1: ROS 2 Foundations</h3>
            <p style={cardText}>
              Master ROS 2 frameworks - the nervous system of modern robots. Build nodes, topics,
              services, actions, publishers, subscribers, and real robot workflows.
            </p>
            <Link style={cardBtn} to="/docs/ros2/">
              Start Learning →
            </Link>
          </div>

          {/* MODULE 2 */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>Module 2: Gazebo & Unity Simulation</h3>
            <p style={cardText}>
              Master physics-based simulation environments. Learn Gazebo and Unity for
              safe testing, training, and development of robotic systems before real-world deployment.
            </p>
            <Link style={cardBtn} to="/docs/gazebo-unity/">
              Start Learning →
            </Link>
          </div>

          {/* MODULE 3 */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>Module 3: NVIDIA Isaac Robotics</h3>
            <p style={cardText}>
              Develop with NVIDIA Isaac - the comprehensive robotics platform. Understand
              Isaac Sim, robotics scenarios, and deployment strategies for advanced robotic systems.
            </p>
            <Link style={cardBtn} to="/docs/nvidia-isaac/">
              Start Learning →
            </Link>
          </div>

          {/* MODULE 4 */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>Module 4: Vision-Language-Action (VLA) Systems</h3>
            <p style={cardText}>
              Implement multimodal AI models that perceive, understand, and act. Learn about
              vision systems, language models, and action planning for embodied intelligence.
            </p>
            <Link style={cardBtn} to="/docs/vla-systems/">
              Start Learning →
            </Link>
          </div>

          {/* CONCLUSION */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>Conclusion</h3>
            <p style={cardText}>
              Synthesize your learning journey in Physical AI. Explore future directions,
              advanced topics, and resources for continued development in humanoid robotics.
            </p>
            <Link style={cardBtn} to="/docs/conclusion/">
              Explore Further →
            </Link>
          </div>

          {/* APPENDIX */}
          <div style={cardStyle}>
            <h3 style={cardTitle}>Appendix: Resources & Research</h3>
            <p style={cardText}>
              Glossary of AI/robotics terms, research papers, datasets, libraries,
              and further reading for advanced physical AI concepts.
            </p>
            <Link style={cardBtn} to="/docs/introduction/preface/">
              Explore Resources →
            </Link>
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section style={{ padding: "80px 20px", background: "white" }}>
        <h2 style={{ textAlign: "center", fontSize: "34px", marginBottom: "50px" }}>
          Designed for AI-Native Physical Intelligence
        </h2>

        <div
          style={{
            maxWidth: "1000px",
            margin: "0 auto",
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "35px",
          }}
        >
          <div style={featureBox}>
            <h3>Embodied AI First</h3>
            <p>
              Every concept is taught through the lens of embodied intelligence,
              where AI learns and acts in physical environments rather than abstract simulations.
            </p>
          </div>

          <div style={featureBox}>
            <h3>Modern AI Integration</h3>
            <p>
              Leverage cutting-edge models like VLA systems, large action models,
              multimodal transformers, and reinforcement learning in practical implementations.
            </p>
          </div>

          <div style={featureBox}>
            <h3>Industry-Aligned Curriculum</h3>
            <p>
              Content mirrors real development at leading robotics companies:
              Tesla Bot, Figure AI, Boston Dynamics, and Sanctuary AI.
            </p>
          </div>
        </div>
      </section>

      {/* CTA SECTION */}
      <section
        style={{
          padding: "90px 20px",
          background: "#0b0f19",
          color: "white",
          textAlign: "center",
        }}
      >
        <h2 style={{ fontSize: "40px", marginBottom: "20px" }}>
          Start Your Journey in Physical AI
        </h2>
        <p style={{ fontSize: "20px", marginBottom: "40px", color: "#ccc" }}>
          Join the next generation of roboticists creating embodied AI systems
          that interact with and understand the physical world. Master the technologies
          that will define the future of robotics.
        </p>

        <Link
          className="button button--primary button--lg"
          to="/docs/introduction/"
        >
          Begin Learning →
        </Link>
      </section>
    </Layout>
  );
}

/* ======== STYLES ======== */
const cardStyle = {
  background: "white",
  padding: "25px",
  borderRadius: "12px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
};

const cardTitle = {
  fontSize: "22px",
  fontWeight: "bold",
  marginBottom: "10px",
};

const cardText = {
  fontSize: "16px",
  color: "#555",
  marginBottom: "20px",
  lineHeight: "1.5",
};

const cardBtn = {
  textDecoration: "none",
  background: "#0057ff",
  padding: "10px 16px",
  color: "white",
  borderRadius: "8px",
  fontSize: "15px",
  fontWeight: "bold",
};

const featureBox = {
  padding: "25px",
  background: "#f5f7fa",
  borderRadius: "10px",
  textAlign: "left",
};