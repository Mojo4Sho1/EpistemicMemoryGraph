# Master Project Document

Memory Governance Subsystem for LLM Agents | Version 0.1 | February 26, 2026
This document freezes the v0 design for a research grade memory governance subsystem for LLM agents. It is written to serve as the master specification from which implementation docs, schema docs, experiment plans, and task checklists can be derived.
The intended outcome is a practical prototype that separates observations, propositions, and belief states; uses a transient epistemic workspace in front of a canonical long term memory graph; and evaluates whether explicit governance improves long horizon behavior relative to naive memory baselines.

## 1. Document Control

Document owner: Joe (project lead)
Document role: Master specification and decomposition source
Target audience: solo builder, coding agents, future collaborators, research readers
Version: 0.1
Change intent: this version locks the minimum viable architecture, policy, and first study plan. It deliberately defers tempting extensions that would expand scope before the core claim is tested.

## 2. Executive Summary

This project builds a memory governance subsystem for LLM agents. The system stores every external input as an immutable observation, uses a transient epistemic workspace to manage active uncertainty, and promotes only policy compliant information into a canonical long term memory graph.
The core design claim is that explicit observation to proposition to belief governance yields better long horizon memory behavior than naive alternatives such as raw text logs, summary only memory, or ungoverned graph storage.
- The LLM never writes directly to canonical memory.
- All external inputs become observations first.
- Belief state is derived from evidence, not asserted by the model.
- Contradictions lower confidence or create contested state, but do not erase history.
- Entity creation is cheap. Entity merging is expensive and conservative.
- Hypothesis testing is a triggered subroutine, not the default mode for all inputs.

## 3. Problem Statement and Research Claim

Modern LLM agents can retrieve large amounts of text, but they remain weak at maintaining durable, auditable, and self correcting memory over long horizons. Naive memory stores tend to accumulate stale facts, duplicate entities, premature conclusions, and contradictory state. The central problem is not only retrieval. It is governance.
This project addresses the governance problem by introducing explicit evidence handling, explicit propositions with tracked confidence and status, explicit contradiction handling, and a strict boundary between raw observation and durable belief.
Primary research claim: explicit observation to proposition to belief governance improves long horizon memory behavior relative to naive memory baselines.
The first study should attempt to demonstrate improvement in the following areas:
- Belief revision after new evidence
- Contradiction handling without silent corruption
- Confidence calibration relative to correctness
- Consistency across longer tasks and multiple sessions
- Memory integrity over time, including duplicate and stale state control

## 4. Scope and Non Goals

### 4.1 In Scope for v0

- Single agent prototype
- Text and tool based inputs
- Immutable observation log
- Transient task scoped epistemic workspace
- Canonical long term memory graph represented relationally
- Deterministic evidence accumulation and belief state transitions
- Conservative identity management
- Controlled benchmark and end to end task evaluation

### 4.2 Explicit Non Goals for v0

- General AGI architecture
- Full scientific reasoning engine across all inputs
- Embodied sensor fusion
- Multi agent distributed synchronization
- Learned trust calibration
- Rich autonomous ontology growth
- Aggressive automatic entity merging
- Production scale optimization or user interface polish

## 5. Design Principles

1. Auditability first. Every durable belief must be traceable back to observations.
2. Deterministic governance first. The memory layer, not the LLM, owns integrity rules.
3. Minimal ontology first. Start with the smallest schema that can support the core claim.
4. Two horizons, one schema. Use a transient workspace and a canonical memory layer that share the same logical object types.
5. Cheap local uncertainty, expensive durable commitment. The system should be tolerant of ambiguity in the workspace and conservative in long term promotion.
6. Recompute friendly architecture. Policy changes should not force irrecoverable data loss.
7. Measure the policy directly before claiming end to end gains.

## 6. System Architecture Overview

The v0 architecture contains three layers:
1. Immutable observation log. The system of record for all external input.
2. Transient epistemic workspace. A task scoped working subgraph for active uncertainty.
3. Canonical long term memory graph. The durable interpreted memory store.
The observation log stores raw intake. The workspace holds active propositions, contradictions, and candidate tests. The canonical memory graph stores stabilized entities, accepted or still relevant propositions, and compressed historical summaries.
High level data flow:
- Input arrives from user, tool, API, or local function.
- Input is recorded as one or more observations.
- Observations are attached to the active workspace.
- The workspace updates existing propositions or spawns limited new propositions.
- If uncertainty matters, the system proposes a discriminating test.
- A consolidator promotes, archives, or discards workspace state according to policy.
- Relevant long term memory can later be reactivated into a future workspace.

## 7. Component Specifications

### 7.1 Immutable Observation Log

Purpose: preserve raw evidence and provenance before interpretation. This is the authoritative record of what arrived, when it arrived, and from where it arrived.
Minimum fields:
- observation_id
- timestamp
- source_id
- source_type
- source_independence_group
- session_id
- task_id
- raw_payload
- parsed_payload
- ingest_status
Implementation default: a relational table in SQLite for v0. The log is append only. Updates are represented by new observations, not mutation of historical rows.

### 7.2 Transient Epistemic Workspace

Purpose: provide a high churn, task local reasoning surface where the agent can hold ambiguity, compare competing propositions, attach new evidence, and propose tests without contaminating durable memory.
Characteristics:
- Task scoped or session scoped
- Stored in memory for v0
- Uses the same logical schema as long term memory
- Tolerant of unresolved ambiguity and duplicate candidates
- Aggressively pruned or archived after consolidation

### 7.3 Canonical Long Term Memory Graph

Purpose: store the durable interpreted memory state. This includes stabilized entities, accepted or still relevant propositions, and retained episode summaries.
Implementation default: represent graph semantics with relational tables.
- entities
- propositions
- edges
- sources
- belief_states
- aliases
- promotion_events
- episodes
A native graph database is explicitly deferred for v0. Relational storage is simpler to inspect, test, and evolve during early research.

## 8. Core Data Model

### 8.1 Entity

An entity is a thing, concept, actor, resource, or named referent. Entities are the anchor points of the memory graph.
- Canonical name
- Type or class
- Alias set
- Created timestamp
- Last touched timestamp
- Canonicality status

### 8.2 Proposition

A proposition is a claim about the world. It replaces the need for separate hypothesis and belief node types in v0. The proposition carries the current belief state as metadata.
Proposition classes:
- Descriptive
- Predictive
- Causal
- Procedural
Core proposition fields:
- Proposition text or structured form
- Current status
- Confidence score
- Supporting weight
- Contradicting weight
- Distinct source group count
- Recency score
- Volatility class
- Provenance summary

### 8.3 Observation

An observation is a concrete incoming evidence record tied to a source and time. Observations are evidence, not truth.

### 8.4 Test

A test is an action taken specifically to reduce uncertainty between competing propositions or to validate a proposition before promotion.
- Call an alternate API
- Check a second sensor
- Ask a targeted question
- Fetch the same fact from a more authoritative source
- Wait for a new sample in a dynamic setting

### 8.5 Episode

An episode is a bounded task or interaction context that scopes workspace behavior and supports later summarization and retrieval.

### 8.6 Edge Types

Minimum relationship types for v0:
- supports
- contradicts
- about
- predicts
- tested_by
- derived_from
- possible_same_as
- supersedes

## 9. Belief State Machine

Every proposition must always be in exactly one primary state.
tentative: New proposition with insufficient support.
provisional: Meaningful support exists, but the proposition is not yet stable enough for accepted use.
accepted: Support crosses threshold with sufficient source diversity and no unresolved major contradiction.
contested: Material support and contradiction are both present. The system should preserve both evidence paths.
deprecated: The proposition was once useful, but is now stale, superseded, or no longer high value.
rejected: The proposition has been materially undermined or failed discriminating tests.
State transition rules are policy driven and deterministic for v0.

## 10. Memory Governance Policy v0.1

Rule 1. All external inputs become observations first.
Rule 2. Observations never directly create accepted beliefs.
Rule 3. Every proposition must be traceable to one or more observations.
Rule 4. Belief status is derived from evidence, not asserted by the LLM.
Rule 5. Evidence is weighted by source quality and source independence, not raw count.
Rule 6. Contradictions lower confidence or produce contested state; they do not erase history.
Rule 7. Claims in dynamic domains decay if they are not refreshed.
Rule 8. Entity creation is cheap; entity merging is expensive and conservative.
Rule 9. The hypothesis testing loop is invoked only when uncertainty is relevant to task success or belief integrity.
Rule 10. Only consolidated, policy compliant information is promoted into canonical long term memory.

## 11. Trust, Provenance, and Source Model

The system should not use a single universal trust score. Trust must be structured enough to reflect context while remaining simple enough to debug.
Minimum source fields:
- source_id
- source_type
- base_reliability
- domain_tags
- independence_group
- historical_correction_rate
Interpretation guidelines:
- Base reliability is a hand authored prior in v0.
- Domain tags limit overgeneralization of trust across unrelated claim types.
- Independence group reduces false confidence from correlated sources.
- Historical correction rate allows the system to slowly adjust trust expectations.
Repeated evidence from the same independence group should saturate quickly. Raw repetition must not be treated as linear confirmation.

## 12. Proposition Scoring Model

The v0 scoring model should be deterministic, inspectable, and easy to ablate. Avoid complex probabilistic machinery unless the simple model clearly fails.
Maintain the following aggregates per proposition:
- Support weight
- Contradiction weight
- Distinct source group count
- Freshness modifier
- Volatility modifier
Working confidence can be derived from a simple weighted heuristic: confidence increases with support, decreases with contradiction, receives only a modest bonus from independent source diversity, and drops under staleness penalties in volatile domains.
Scoring constraints:
- Repeated same source reinforcement should saturate quickly.
- Causal propositions require stricter promotion thresholds than descriptive propositions.
- High volatility propositions should decay faster than low volatility propositions.
- Time alone never upgrades a weak proposition into a strong one.

## 13. Operational Flows

### 13.1 Intake Flow

1. Receive external input.
2. Record one or more observations in the immutable log.
3. Parse candidate references and claim fragments.
4. Attach the observations to the active workspace.

### 13.2 Workspace Update Flow

1. Check whether the new observation reinforces an existing proposition.
2. Check whether it contradicts an existing proposition.
3. If needed, spawn a limited number of candidate propositions.
4. Link observations to the affected proposition or propositions.

### 13.3 Triggered Hypothesis Testing Flow

The system invokes the hypothesis testing loop only when uncertainty matters. Trigger conditions include contradiction, novelty, cost sensitive action, repeated unresolved pattern, or multiple plausible explanations.
1. Rank active competing propositions.
2. Select the cheapest action that best distinguishes them.
3. Execute the test through tools or deferred task logic.
4. Record the test result as new observation data.
5. Recompute proposition scores and state transitions.

### 13.4 Consolidation Flow

1. Review the workspace at task boundary or scheduled checkpoint.
2. Promote policy compliant entities and propositions into canonical memory.
3. Summarize the episode into a compact archival record.
4. Retain unresolved but important items with explicit status.
5. Discard low value transient clutter.

### 13.5 Retrieval and Reactivation Flow

1. Given a new task, query long term memory for relevant entities, propositions, and episode summaries.
2. Load only the relevant subgraph into the workspace.
3. Use the workspace as the active reasoning surface for the current task.

## 14. LLM Tool Boundary and System Interfaces

The LLM is not the database engine. It proposes memory actions through a narrow tool interface. Deterministic policy code validates and applies them.
Initial tool surface:
- record_observation
- create_or_link_entity_candidate
- propose_proposition
- attach_support
- attach_contradiction
- propose_test
- execute_test_result_ingest
- request_consolidation
- archive_episode
Interface rule set:
- Tool calls are proposals, not direct mutation authority.
- Canonical memory writes happen only after validation.
- The policy layer owns scoring, transitions, and promotion checks.
- All durable writes must preserve provenance links.

## 15. Minimum Viable Build Plan

### 15.1 Default Technical Choices

- Storage backend: SQLite
- Workspace: in memory Python object keyed by task or session
- Graph representation: relational tables and explicit edge rows
- Scoring: deterministic weighted heuristic
- Identity resolution: alias linking plus possible_same_as only
- First input domain: text and tool based synthetic tasks

### 15.2 Suggested Repository Layout

- docs/ - master specification, derived design docs, experiment notes
- src/core/ - policy engine, scoring, state transitions
- src/store/ - persistence layer and schema management
- src/workspace/ - transient workspace structures and consolidation logic
- src/tools/ - tool call adapters and validators
- src/eval/ - benchmark harnesses, baselines, metrics, logging
- tests/ - policy correctness tests and regression tests
- configs/ - experiment and runtime configuration files

### 15.3 Implementation Milestones

1. Freeze schema and policy constants.
2. Implement the observation log and persistence tables.
3. Implement the in memory workspace object.
4. Implement proposition scoring and state transition logic.
5. Implement conservative identity handling and alias support.
6. Implement the tool boundary and validation layer.
7. Implement consolidation and archival behavior.
8. Build the policy correctness test suite.
9. Build baseline memory variants for comparison.
10. Run the first governance benchmark and end to end trials.

## 16. Evaluation Methodology

### 16.1 Stage 1: Policy Correctness

Test the governance policy directly with deterministic micro scenarios.
- Promotion after sufficient independent support
- Resistance to premature promotion
- Correct contested state under conflicting evidence
- Decay in dynamic domains
- Alias ambiguity handling
- Rejection after failed discriminating test

### 16.2 Stage 2: Governance Stress Benchmark

Create a custom stress suite that targets the exact failure modes this policy is meant to solve.
- Delayed correction
- Correlated false sources
- Repeated same source reinforcement
- Changing facts over time
- Ambiguous entity references
- Insufficient evidence requiring abstention
- Competing propositions that require a targeted test

### 16.3 Stage 3: Baseline Comparison

Compare the governed system against simpler alternatives.
- Context window only
- Raw text log retrieval
- Summary only memory
- Simple key value memory
- Graph memory without governance policy
- Full governed system

### 16.4 Stage 4: End to End Task Study

Run longer tasks where memory quality materially affects outcomes.
- Multi session troubleshooting
- Repeated planning with changing constraints
- Synthetic tool using tasks with delayed updates
- Assistant style workflows that depend on revision and continuity

## 17. Metrics and Logging

### 17.1 Policy Metrics

- False promotion rate
- False rejection rate
- Contested state precision
- Confidence calibration
- Contradiction recovery rate
- Stale belief handling quality

### 17.2 Identity Metrics

- Duplicate entity rate
- False merge rate
- Alias resolution precision

### 17.3 Memory Health Metrics

- Graph growth rate
- Average evidence per accepted proposition
- Rate of accepted propositions later overturned
- Stale node fraction
- Unresolved contradiction count

### 17.4 Task Metrics

- Task success rate
- Number of tool calls
- Number of corrective actions
- Total memory cost
- Wall clock latency

### 17.5 Logging Requirements

- Every run must record config values, seeds, timestamps, and system version.
- Every proposition transition should be logged with triggering evidence.
- Every consolidation event should record what was promoted, archived, or discarded.
- Every benchmark run should emit machine readable artifacts for later analysis.

## 18. Baselines and Ablation Plan

The first study should isolate which policy components actually matter.
Required ablations:
- Remove tentative and provisional states
- Remove provenance weighting
- Remove source independence handling
- Remove staleness decay
- Remove the triggered test loop
- Collapse workspace and long term memory into one layer
- Allow direct writes to canonical memory
If the expected degradations appear under these ablations, the argument that governance drives the observed gains becomes much stronger.

## 19. Risks and Known Failure Modes

- Schema sprawl caused by overdesign before the core claim is tested
- Hidden coupling between workspace behavior and long term memory corruption
- False confidence from correlated sources
- Entity explosion from overcautious merging
- Premature merges that silently corrupt large memory regions
- Overtuned thresholds that only work on synthetic tasks
- Evaluation that rewards retrieval strength while missing governance quality
- LLM generated tool proposals that exceed intended policy authority
Primary mitigation strategy: keep v0 small, deterministic, heavily logged, and easy to ablate.

## 20. Master Implementation Checklist

**Project framing**

- [ ] Freeze the v0 problem statement
- [ ] Freeze the first study research claim
- [ ] Freeze non goals

**Policy**

- [ ] Freeze the belief state machine
- [ ] Freeze the ten core rules
- [ ] Freeze trust model fields
- [ ] Freeze promotion and decay criteria
- [ ] Freeze the no hard auto merge rule

**Data model**

- [ ] Freeze object types
- [ ] Freeze relationship types
- [ ] Freeze persistent table schema
- [ ] Freeze workspace schema
- [ ] Freeze episode archive format

**Runtime architecture**

- [ ] Freeze the tool surface
- [ ] Freeze the deterministic policy boundary
- [ ] Freeze consolidation workflow
- [ ] Freeze retrieval and reactivation workflow

**Evaluation**

- [ ] Write policy correctness tests
- [ ] Design governance stress scenarios
- [ ] Define baseline systems
- [ ] Define metrics and logging schema
- [ ] Define the ablation plan

**Research hygiene**

- [ ] Create experiment config spec
- [ ] Create run logging spec
- [ ] Create seed and reproducibility policy
- [ ] Create result artifact naming convention
- [ ] Create failure analysis template

## 21. Definition of Done for v0

- The prototype enforces the frozen policy through deterministic code rather than ad hoc model behavior.
- The observation log, workspace, and canonical memory layers all function end to end.
- Policy correctness tests pass on the full micro scenario suite.
- The governance stress benchmark runs reproducibly.
- The full system outperforms at least one naive baseline on governance quality metrics.
- The system shows an interpretable benefit on at least one end to end long horizon task family.
- The logging and artifact trail are sufficient for failure analysis and paper quality reporting.

## 22. Deferred Features

- Embodied perception and multi sensor fusion
- Multi agent shared memory and replica synchronization
- CRDT style merge semantics
- Learned trust calibration
- Automatic hard entity merges
- Rich causal structure induction
- Native graph database backend
- Production hardening and user facing interface layers

## 23. Immediate Next Actions

1. Treat this document as the design freeze for the first implementation pass.
2. Split it into derived docs for schema, runtime architecture, evaluation harness, and experiment protocol.
3. Implement the v0 data schema and deterministic policy boundary before building agent behavior on top.
4. Create the policy correctness micro scenarios before the end to end benchmark harness.

## 24. Closing Note

This document is intentionally strict. The project will become much easier to execute if the first implementation treats this as a contract rather than another brainstorming prompt. The value of v0 is not feature breadth. It is a clean test of whether explicit memory governance improves agent behavior in ways that simpler memory systems do not.