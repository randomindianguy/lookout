# The AI Product Lifecycle
## A PM's framework for building, launching, and growing AI products

---

## How to read this document

This framework covers the full lifecycle of an AI product in three acts, the way a restaurant works:

**Act I (Before the kitchen opens):** Decide what restaurant to build, for whom, and why they'd come to you instead of the place next door. This is product sense and strategy.

**Act II (Building the kitchen):** Design the menu, hire the cooks, set up the equipment, taste-test every dish, and make sure nobody gets food poisoning. This is architecture, building, and evaluation.

**Act III (Opening night and beyond):** Get people in the door, make them regulars, and make money without compromising the food. This is GTM, growth, and monetization.

Most AI PMs skip Act I and rush to Act II. They build something technically impressive that nobody wants. Others nail Act I and II but fumble Act III — a great product that nobody finds. The framework is sequential for a reason.

---

# ACT I: PRODUCT SENSE & STRATEGY
*Decide what to build, for whom, and why it matters*

---

## 1. Problem Discovery

Before building anything, answer seven questions:

1. What problem does your product solve?
2. Which segments have this problem, and how severe is it for each?
3. How does your product solve it?
4. What are the alternatives, and how are you better?
5. Do you have any distinct competitive advantages (moats)?
6. How does your product acquire new users?
7. How does your company make money?

If you can't answer these clearly, you're not ready to build.

**Quantify problem severity through three lenses:**
- Does the customer spend a lot of **time** solving this with current alternatives?
- Does the customer spend a lot of **money** on current alternatives?
- Does the problem tie into a **core human drive**, and is the effort to use your product low?

Think of it like choosing which restaurant to open. You wouldn't open a sushi bar in a town that already has five great sushi bars, no matter how good your fish is. You'd look for the gap — maybe there's no good Thai food, or maybe everyone's underserved on delivery.

### The AI-specific trap
Most AI product ideas start as "let's use AI to do X faster." That's a solution looking for a problem. Flip it: start with a problem that's painful and expensive to solve today, then ask whether AI makes the solution meaningfully better.

---

## 2. User Definition

Define your target user with JTBD (Jobs to Be Done):

**Functional Job:** What task do they need accomplished? "Help me sort through 200 resumes in 30 minutes instead of 3 days."

**Social Job:** How do they want to be perceived? "I want to look like a thorough, data-driven hiring manager, not someone who skimmed resumes."

**Emotional Job:** How do they want to feel? "I want to feel confident I didn't miss a great candidate because I was tired on page 150."

All three matter. Products that only solve the functional job are commodities. Products that nail all three create loyalty.

**Common mistakes in user definition:**
- Framing from the company perspective ("grow 30% next quarter") instead of the customer perspective
- Only thinking about the primary persona (K-12 products serve students, but parents buy them)
- Missing the emotional and social JTBD entirely
- Going top-down on segments to appease investors

### Segmentation
Segment across four dimensions, from tangible to behavioral:
- **Geographic:** Where they are
- **Demographic:** Who they are
- **Psychographic:** Why they do what they do (values, lifestyle, motivations)
- **Behavioral:** What they actually do (usage patterns, purchase behavior)

Pick attributes where the **difference is maximum across segments**. Two beauty users may look identical demographically but differ entirely in purchase motivation.

---

## 3. Differentiation & Positioning

**Differentiation is not competitive advantage.** Differentiation is being better than alternatives — it's relative and contextual. Competitive advantage (moat) is the ability to defend your position. Without a moat, competitors copy you.

### Delta-4 Framework (Kunal Shah)
Score the user's current behavior (1–10) and your proposed experience (1–10) across key dimensions. If the delta isn't at least 4 on at least one dimension, users won't switch. Think UPI vs cash — cash was maybe a 3, UPI jumped to 9. Delta of 6. Irreversible behavior change.

Be honest. Kill ideas that don't survive this test.

### AI-Specific Differentiation
Five sources of differentiation for AI products:
1. **Established product value** — proven PMF and user base
2. **Distribution advantage** — existing channels and market access
3. **Proprietary data** — unique datasets for training and refinement
4. **Regulatory approval** — compliance certifications and licenses
5. **Novelty** — first-mover advantage and unique approach

Novelty is the one you can control as a startup. Focus there.

### Positioning Rules
1. Better to be first than to be better (ChatGPT vs Gemini)
2. If you can't be first, create a new category (Samsung's "big screen Android")
3. Counter-positioning works because incumbents can't easily respond (Netflix vs Blockbuster)
4. Use a new name to win a new category (BBK runs Oppo, Vivo, OnePlus separately)
5. Sometimes, go with brand extension (when market is small or competition is high)

### Thin vs Thick Wrappers
In AI, your positioning often comes down to how much value you add beyond the foundation model:

**Thin wrapper:** Take an API, add a system prompt, ship a chatbot. Low differentiation. One model update can kill you.

**Thick wrapper:** Build your own agentic flows, use proprietary data via RAG/MCP, run multiple refinement loops, build unique interfaces. High differentiation. Defensible.

Thin vs thick isn't binary — and it depends on segment. Lovable is a thin wrapper for PMs (who already have Claude), but a thick wrapper for small businesses who don't have other tools.

### Moats by Stage

| Stage | Available Moats |
|-------|----------------|
| Early | Cornered resources (talent, IP), first-mover, positioning, novelty |
| Growth | Economies of scale, network effects, switching costs |
| Mature | Brand (pricing power), process power (culture, operational excellence) |

---

## 4. Strategy

Strategy has three components:
1. **Finding challenges** the company faces. Every strategic bet traces to a specific challenge.
2. **Deciding where to play and how to win.**
3. **Making coherent choices.** Every decision aligns toward a common goal. Think Southwest Airlines — no food, single aircraft type, point-to-point routes — all flowing from the low-cost carrier strategy.

### Porter's Three Approaches
1. **Cost leadership** — lowest cost wins market share
2. **Differentiation** — create unique value
3. **Focus** — concentrate on a specific segment

### Porter's Five Forces
1. Buyer power — can buyers easily switch?
2. Supplier power — do suppliers have leverage?
3. New entrants — how easy is it to enter?
4. Substitutes — how good are the alternatives?
5. Competition — how fierce?

### Hamilton's 7 Powers (Moats in Detail)
1. **Cornered resource** — patent, talent, policy
2. **Counter-positioning** — new model incumbents can't copy
3. **Network effects** — value increases with network size
4. **Economies of scale** — per-unit cost decreases with volume
5. **Switching costs** — loss from switching
6. **Branding** — ability to charge premium
7. **Process power** — hard-to-replicate operational excellence

---

# ACT II: BUILDING THE AI PRODUCT
*Architecture, construction, and quality assurance*

---

## 5. AI System Architecture

AI product architecture = Software + Data Engineering + AI Models

Think of it like building a restaurant kitchen. The software is the kitchen layout and plumbing. Data engineering is your supply chain — where ingredients come from, how they're stored, how fresh they are. AI models are your chefs — their training, their specialization, their judgment.

### The 10 Components of AI Architecture

Each component has a human analogy to help you remember its purpose:

| Component | What it is | Human analogy |
|-----------|-----------|---------------|
| **Dataset Engineering** | Creating quality training/test data | Quality of environment you grew up in |
| **Fine-tuning** | Specialized task training | Medical school after general education |
| **Prompt Engineering** | Guiding model output | Setting context and rules for a new hire |
| **RAG** | External knowledge access | Using the internet, books, consulting experts |
| **Reasoning** | Logical deduction capabilities | Critical thinking and System 2 processing |
| **Memory** | Context retention | Short-term, long-term, working memory |
| **Tools** | External integrations (APIs, services) | Physical tools — calculator, map, hammer |
| **Inference Optimization** | Making models faster/cheaper | Developing heuristics and System 1 shortcuts |
| **Safety & Alignment** | Ensuring beneficial behavior | Ethics, laws, moral values, social norms |
| **Evaluation** | Testing performance | Exams, interviews, peer reviews |

### Priority Order for Context Engineering
Not all components matter equally. In decreasing order of importance (based on severity of cost if you get it wrong, and frequency of usage):

1. System Prompt Engineering — the foundation
2. Evaluations — measuring quality
3. Safety and Alignment — ensuring responsible behavior
4. Dataset Engineering — quality input data
5. RAG — knowledge augmentation
6. Reasoning — logical capabilities
7. Tools — external integrations
8. Memory — context retention
9. Fine-tuning — specialized training (avoid unless necessary)

### The Context Engineering Principle
Context engineering is building AI system architecture that provides optimal context to the model to complete tasks. Think of it like training a new employee: you don't dump 500 pages of documentation on them. You give them the right information, in the right order, at the right time.

Key constraints:
- Context in the middle gets lost (performance degrades as context grows)
- Context costs scale linearly or worse with length
- Longer context means slower responses
- Including irrelevant information actively hurts performance

The biggest weakness of LLMs is reliability. Engineering is how you solve for reliability. The biggest problem is context management. Context engineering is how you solve context management.

### RAG vs MCP vs Fine-tuning — When to Use What

**RAG:** One shared knowledge base serving many users. Read-only. Like a company wiki.
- Use when: everyone queries the same document corpus

**MCP:** Dedicated, authenticated connections to specific data sources. Read AND write. Live data.
- Use when: different users need access to their own data (Slack, Jira, Gmail, databases)

**Fine-tuning:** Changing the model's weights with specialized data. Expensive, slow.
- Use when: domain-specific behavior can't be achieved through prompting or RAG. Avoid unless necessary.

**Decision sequence:** Try prompt engineering first (hours) → add examples/few-shot (a day) → implement RAG (weeks) → fine-tune (months). Each step has decreasing marginal ROI. A day of testing is worth more than weeks of unknowns.

---

## 6. Agentic Design

### What is an Agent?
Agents are systems that independently accomplish tasks on the user's behalf. The key word is "independently" — an agent must have at least one evaluation cycle where it assesses its own output and decides whether to retry or finish.

Think of it like the difference between an intern who does exactly what you say (LLM call) and a senior employee who takes a goal, plans the approach, executes, checks their work, and iterates until it's good enough (agent).

### The Agentic Spectrum

| Level | Type | What decides output? | What decides steps? | What decides available steps? |
|-------|------|---------------------|--------------------|-----------------------------|
| 1 | Code | Code/Human | Code/Human | Code/Human |
| 2 | LLM Call | LLM (one step) | Code/Human | Code/Human |
| 3 | Chain | LLM (multiple steps) | Code/Human | Code/Human |
| 4 | Router | LLM | LLM (no cycles) | Code/Human |
| 5 | State Machine | LLM | LLM (with cycles) | Code/Human |
| 6 | Autonomous | LLM | LLM | LLM |

Levels 3–5 are "agentic." A cycle (self-evaluation loop) is the necessary condition for calling something an agent.

### Four Design Patterns
Think of these as modules you can mix and match:

1. **Reflection** — Self-evaluation and iterative improvement. Like proofreading your own essay before submitting. Warning: too high a quality bar causes system paralysis (never outputs anything).

2. **Tool Use** — External API and service integration. Like giving an employee access to specific software. Warning: tools need safety instructions (you wouldn't give a chainsaw to a kid). Nobody can misuse your reflection mechanism, but they CAN misuse your tool calls.

3. **Planning** — Breaking complex tasks into subtasks. Planning and Chain-of-Thought go hand in hand. Like decomposing "launch a product" into research, design, build, test, ship.

4. **Multi-Agent** — Specialized agents collaborating. Like a team where one person does research, another writes, a third reviews.

### The OODA Loop for Agents
Agents follow: Observe → Orient → Decide → Act
- Observe: take in data
- Orient: understand what the data means
- Decide: choose the next action
- Act: execute
- Then observe the result and loop

### Sheridan's 10 Levels of Autonomy
Use this to define where your system is today and where you want it to go:

| Level | Description |
|-------|------------|
| 1 | No AI assistance — human does everything |
| 2 | AI offers a complete set of options |
| 3 | AI narrows down to a few options |
| 4 | AI suggests one option |
| 5 | AI executes if human approves |
| 6 | AI executes unless human vetoes (time-limited) |
| 7 | AI executes, then informs human |
| 8 | AI informs human only if asked |
| 9 | AI informs human only if it decides to |
| 10 | AI decides everything autonomously |

Your goal is to keep moving up the levels. This, along with definitions of AGI, helps you roadmap where AI fits in your product next year vs the year after.

---

## 7. Data Engineering

Data is the ingredient supply chain for your AI kitchen. Garbage in, garbage out.

### Good Data depends on:
- **Quality:** relevance, task alignment, consistency, formatting, uniqueness, compliance
- **Diversity:** variety in problems, topics, users, inputs, languages, patterns
- **Quantity:** where performance improvement begins to taper (diminishing returns)

Small dataset of high quality beats large dataset of poor quality.

### Getting Data
Three sources, in order of cost:
1. **Public datasets** — Kaggle, HuggingFace, Google Dataset Search. Start here to understand the shape of data in your domain.
2. **Purchased datasets** — from data vendors
3. **Custom creation** — human labelers, synthetic data generation

### The ETL Framework
- **Extract** — pull data from various sources (requires integrations)
- **Transform** — process and organize so it's usable (you can use AI here — e.g., "label these emails as X or Y")
- **Load** — move transformed data to a repository

Data warehouse = data sits after processing. Data lake = data gets dumped.

### Synthetic Data
When you can't get enough real data:
- **Simulation** — for high-risk industries (self-driving, medical)
- **Template mutation** — fixed or variable data mutation for low-risk industries
- **Seed instruction** — give a model examples and have it generate variations
- **Model bootstrapping** — use a frontier model to generate training data, then fine-tune a cheaper model to match

Long-term strategy: start with frontier model, then fine-tune cheaper models to be "as good." This is also a moat.

---

## 8. Evaluations

**Your evals are your north star.** How do you know you're improving your product? Through evals.

Evals look deceptively simple at first — just a table of inputs, outputs, and pass/fail. That's the biggest mistake people make: equating evals with common sense. The depth is in the rubric design, edge case coverage, and disagreement resolution.

### Eval Process (6 Steps)

**Step 1: Create Test Datasets**
Generate comprehensive questions/inputs covering diverse scenarios, edge cases, real usage patterns, and varying difficulty. You can synthesize these or pull from real user data.

**Step 2: Generate Baseline Answers**
Run test dataset through v1 product. These are your baseline responses.

**Step 3: Vibe-Check and Refine**
As a PM, review 10 sample Q&As. If the product is clearly bad, fix it before running full evaluation. Don't send garbage to QA. This is the same principle as testing your code before asking someone to review it.

**Step 4: Establish Evaluation Rubric**
Transform subjective assessment into binary decisions with clear, measurable criteria. A good rubric makes subjective answers objectively measurable. Think of it as test cases for AI — the AI equivalent of what QA engineers write for traditional software.

Keep refining until two independent evaluators disagree less than 10% of the time.

**Step 5: Define Launch Cutoffs**
Set minimum acceptable performance thresholds. "To launch, we need 80% accuracy, 70% recall." These are your functional and non-functional requirements.

**Step 6: Log Performance Metrics**
Run evals, log results, iterate. When your product passes the bar, put it in front of users.

### Three Evaluation Approaches

**Human Evaluations**
- Most reliable, most expensive, slowest
- Can't scale to thousands of data points
- Essential for building the golden dataset

**LLM-as-Judge**
- Use the most sophisticated available model as judge
- Feed it: user prompt + app response + evaluation rubric → pass/fail
- Validate against human evaluations — if humans and LLM disagree frequently, your judge isn't ready
- It's an LLM judging another LLM — calibrate carefully

**Code-Based Evaluations**
- Scripted test cases for deterministic checks
- Good for format validation, latency, structured output verification

### Evaluating Agents Specifically
Think of agents as connected modules. Each step gets its own evaluation:
- Speech-to-text accuracy (if voice)
- Intent classification accuracy
- Tool selection correctness
- Tool execution success
- Response quality
- End-to-end task completion

You work on improving stepwise efficiency daily. The aggregate north star metric follows.

### Key Metrics by Product Type

| Product Type | Key Metrics |
|-------------|------------|
| Content moderation | Precision, recall, F1-score, false positive rate |
| Voice assistant | Task completion, relevance score, latency |
| Search | Search quality score, query latency, CTR (with caveats) |
| Recommendations | CTR, conversion rate, long-term retention |
| Legal AI | Extraction accuracy, time savings, consistency |
| Autonomous vehicles | Incidents per mile, disengagement rate, navigation success |

---

## 9. Safety, Trust & Compliance

In traditional software, the product is deterministic — it either works or it doesn't. In AI, the product is non-deterministic. It can go off the rails in ways you didn't anticipate. That's why safety isn't optional — it's a PM responsibility.

Think of it like food safety in a restaurant. A software bug is like a hair in the soup — bad, but fixable. An AI safety failure is like food poisoning — it can permanently destroy trust.

### Three Pillars of AI Safety

**1. Content Output Risks**
- Toxic content (hate speech)
- Misinformation
- Inappropriate content (NSFW in enterprise)
- Bias (sentiment skewed toward particular groups)
- Privacy violations (leaking customer data)

**2. Alignment Challenges**
- **Reward hacking** — AI optimizes metrics in unintended ways. A customer service bot optimized for "chat completion" might end conversations quickly instead of helping customers.
- **Goal misalignment** — AI behavior doesn't match intent. A content moderator removes all posts mentioning certain topics, including legitimate educational content.

**3. System-Level Safety**
- Model drift — performance degrades as real-world patterns change
- Infrastructure reliability
- Prompt injection attacks

### Managing Output Quality
Five levers:
1. **Configuration** — temperature and top-p settings (hallucination control)
2. **Model choice** — some models are more aligned than others
3. **Reward function alignment** — are you optimizing for the right thing?
4. **Input/output filters** — block dangerous queries and responses
5. **Human review** — essential in early phases, then sample production data ongoing

### Building Trust
Trust matters more in AI because users don't know when the model might fail.

**For Users:**
- Explainability — users understand how decisions are made
- Transparency — clear communication about data usage
- Consent management — proper user consent for personal data
- User control — options to delete memory and conversation history

**For Regulators:**
- Data governance — handling, retention, and deletion policies
- Audit trails — comprehensive logging
- Domain-specific compliance (HIPAA for healthcare, etc.)

**Trust Markers:**
- Data safety communication (in onboarding)
- Privacy guarantees
- Enterprise certifications (on landing page)
- Authority endorsements

### The Core Principle
One of the best ways to ensure your system is aligned and safe is to **contain the scope of the product.** A chatbot on Dell's website should ONLY talk about Dell laptops. Your test cases should include 10 different off-topic prompts, and the answer to all of them should be deflection.

---

# ACT III: GTM, GROWTH & MONETIZATION
*Get people in the door, make them regulars, make money*

---

## 10. Go-to-Market

### The AI-Specific GTM Shift
**For AI, MVP is not Minimum Viable Product. It's Minimum Viable Performance.**

In traditional software, you could see whether your product works or doesn't. In AI, you're never 100% sure it'll work as expected. You need rigorous evals for minimum viable performance before shipping.

### Quality vs Speed Tension
More testing → better performance → longer time to market. This tension is as old as product management itself, but AI makes it sharper because the failure modes are harder to predict.

### Critical GTM Questions
1. What's the minimum viable performance for production?
2. Where are your target users spending time?
3. Which distribution channels maximize reach?

GTM is finding where your consumers spend time, understanding what conversations they're having, and being part of those conversations.

### AI Product Design Patterns

**Input Patterns:**
- Open input with context (ChatGPT, Claude)
- Clarifying questions (Deep Research)
- Output-based input (Artifacts)

**Output Patterns:**
Form factor must align with the JTBD:
- Research tasks → comprehensive reports with citations
- Shopping tasks → visual comparisons with product cards
- Simple queries → concise answers with context

**Trust Patterns:**
- Wayfinders (onboarding guidance)
- User controls (pause, cancel, source citations, show reasoning)
- Feedback mechanisms (thumbs up/down, ratings)
- Guardrails (error states, outage scenarios, abuse prevention)

---

## 11. Growth

### The Growth Cycle
**Acquisition → Value Generation → Monetization**

Value generation varies by product type:
- **Attention products** (social): time spent, active users
- **Transaction products** (marketplaces): number of transactions, revenue

### Product-Market Fit (PMF)

Four conditions for growth readiness:
1. Has the product achieved PMF?
2. Are scalable channels available?
3. Can you make the business sustainable?
4. Is there room to grow?

PMF is the necessary condition. Without it, growth is just spending money faster.

**Sean Ellis Test:** Survey users: "How would you feel if you could no longer use this product?" If 40%+ say "very disappointed," you have PMF.

### Behavioral Psychology (B=MAT)

**Behavior = Motivation × Ability × Trigger**

If a trigger fires when motivation is high and the action is easy, the behavior occurs. This is the operating system underneath every growth lever.

**Motivation** operates on: hope/fear, social acceptance/rejection, pleasure/pain.

**Ability** is gated by: time, money, physical effort, mental effort, routine disruption, social deviance.

**Triggers** come in three types: Facilitators (help), Sparks (motivate), Signals (remind).

Think of it like a restaurant again. Motivation is hunger + craving. Ability is distance + price + wait time. Trigger is smelling food as you walk past, or a friend texting "want to grab lunch?"

### Activation
The path from signup to value:
**Setup → Core Action → Aha Moment**

The Aha Moment is when the user first experiences the core value proposition. For an AI product, this might be the first time the model gives them an answer they couldn't have gotten from Google. Everything before this is friction to minimize.

### Engagement
**E = Frequency × Intensity**

For AI products, engagement often looks different than traditional SaaS. A user who comes once a week but gets deep value each time may be healthier than one who checks daily but superficially.

### Retention
Three strategies for at-risk users:
1. Remind them why they chose you — amplify the experiences that matter to them
2. Transition them to a different use case — understand their new mindset
3. Increase friction of leaving — show what they'd lose

### Habit Formation (Hooked Model)
**Cue → Routine → Reward → Investment**

The investment users put in each session raises their stakes — what they stand to lose by leaving. This strengthens motivation (don't want to lose what's built) and ability (platform learns preferences over time).

For forming new habits: use continuous reinforcement initially. Once the habit is forming, transition to variable rewards. Continuous rewards create dependency — remove the reward, behavior stops.

---

## 12. Monetization & Business Model

### The Model Performance Paradox
Better models → better performance → higher cost. Do better models lead to better ROI?

### Marginal ROI Framework
For every additional dollar spent on improving model/architecture, are you getting proportional benefit? The key insight: returns vs spend never goes down, but the *rate* of return can.

The delta in return / delta in spend can become a negative slope. You can spend 2x more for only 50% more return. That's marginal ROI going down.

### Applying Marginal ROI to AI
1. **Define minimum viable performance** — establish non-negotiable baseline (e.g., 80% accuracy)
2. **Cost analysis** — beyond threshold, analyze how costs increase per improvement
3. **Revenue impact** — quantify revenue gains from accuracy improvements through heuristics: customer satisfaction, retention, market leadership

The sweet spot: accuracy where you can charge more than you're paying for model costs.

---

## 13. Roadmapping AI Products

### Segregate Initiatives
Break your roadmap into: acquisition initiatives, retention/value generation initiatives, and monetization initiatives.

### Prioritization: RICE
**Reach × Impact × Confidence / Effort**

Confidence is hardest to score. Ground it in evidence:
Evidence hierarchy: User interviews > A/B tests > cohort analysis > segmentation analysis > case studies > expert opinions.

### AI Roadmap Specifics

**Use Sheridan's 10 Levels** to define where your system is today and set targets for next quarter/year. "We're at Level 4 (suggests one option). By Q4, we want Level 5 (executes if human approves)."

**Roadmap the eval improvement trajectory.** Your accuracy going from 20% to 80% tells a clearer story than feature lists. Track and present eval metrics as the primary roadmap artifact.

**AI Roadmapping framework for autonomy levels:**

| Confidence Zone | Action |
|----------------|--------|
| Below 50% confidence | AI handles automatically (obvious cases) |
| Between 50–70% | Human reviews everything |
| Above 70% | AI handles automatically (obvious cases) |
| The boundary zone | Where AI makes the most mistakes — invest here |

Design your system by sorting everything and looking at the boundary where acceptance ends and rejection begins. That boundary is where your roadmap should focus.

---

## QUICK REFERENCE

### The Full Lifecycle in One Line
Problem → User → Differentiation → Strategy → Architecture → Build → Evaluate → Safety → GTM → Growth → Monetize → Roadmap

### AI PM RACI
**Directly Responsible:** AI PRD ownership, AI roadmap planning, eval design
**Accountable:** Safety/trust/compliance, technical decision-making, design decisions

### Key Formulas

| Concept | Formula |
|---------|---------|
| Engagement | E = F × I (Frequency × Intensity) |
| NRR | (Current MRR + Expansion − Contraction − Churned) / Starting MRR |
| Product-Channel Fit | LTV / CAC |
| Activation | Setup → Core Action → Aha Moment |
| B=MAT | Behavior = Motivation × Ability × Trigger |
| Habit Loop | Cue → Routine → Reward → Investment |
| Prioritization | RICE: Reach × Impact × Confidence / Effort |
| PMF Survey | Sean Ellis: 40%+ "very disappointed" |

### How AI PM is Different from Traditional PM

| Dimension | Traditional PM | AI PM |
|-----------|---------------|-------|
| QA relationship | Separate team, handoff | PM must be closer to engineering, running evals directly |
| MVP definition | Minimum viable product | Minimum viable performance |
| Test cases | Deterministic pass/fail | Probabilistic evaluation rubrics |
| Sprint cadence | Issues → tickets → sprints | More fluid — constant eval/QA/testing cycles |
| Safety | Follow government regulations | Regulations still being built — PM owns safety proactively |
| Confidence in output | Software works or doesn't | Never 100% sure — need eval thresholds |
| Core PM goal | Ship features that solve problems | Take non-deterministic models and make them useful for business + individuals |

### Decision Sequence for Building AI Architecture
```
Start with prompt engineering (hours)
  ↓ not good enough?
Add few-shot examples (a day)
  ↓ not good enough?
Implement RAG (weeks)
  ↓ not good enough?
Fine-tune (months, last resort)
```

Each step has decreasing marginal ROI. Don't jump to RAG before trying examples. Don't fine-tune before trying RAG.
