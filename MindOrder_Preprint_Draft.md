# A Framework for Pluralistic Value Assessment (MindOrder)

### Separating Contestable Priors from Invariant Constraints

*MindOrder* (心秩学, literally "the order of the mind") is the name of the framework and of its companion repository.

**Draft — Technical Report**
**Version:** v3.8 · **Date:** 2026-09-06
**Author:** 万伟 (Wei Wan)

**License:** This work is licensed under CC BY 4.0 International.

> **Status note.** This draft is prepared for preprint submission (OSF Preprints).
> The implementation, case file, and interactive interface are publicly available at
> the companion repository (Appendix A). All adjudications reported here are produced
> by running the engine on the released case file (172/172 + 6/6, deterministic).
> Bibliographic details for all cited works have been verified against primary sources
> and are listed in the References section (§10). The author knows each cited work and
> its direction; entries were checked for author, year, venue, and identifiers.
> 
> **Generative-AI disclosure.** In accordance with the disclosure norm for preprints,
> the author states that a generative language model was used for language polishing and
> structural suggestion in preparing this manuscript. All substantive content — the framework,
> the implementation, the validation design, and the reported numbers — is the
> author's own work and responsibility; the author has reviewed and takes full
> responsibility for the final text.

---

## Abstract

We present a computational framework for multi-dimensional value assessment, designed to
address a structural problem shared by historical evaluation and AI value alignment:
**how to adjudicate among incommensurable values without collapsing them into a single score.**

Mainstream approaches to value aggregation seek a *correct value function* — a utility
function, a preference model, or a scalarized objective. We argue this framing is
structurally inadequate. We propose instead an architecture of two layers with
fundamentally different epistemic status:

1. **Contestable priors (relative).** Value inputs — cultural perspective, historical
   standpoint, attribution weights — are modeled explicitly as declared standpoints. Different
   evaluators may hold different standpoints and reach different, mutually incompatible
   conclusions. This is a *feature*, not a defect: the framework's output is not a single
   verdict but a set of traceable judgments, each valid within its stated standpoint.
2. **Invariant constraints (absolute).** A small set of axioms — chiefly the inviolability
   of non-combatant life — acts as a hard truncation on the inference procedure. Standpoints
   may not override it; probabilistic aggregation may not trade against it.

We formalize this as a five-stage adjudication procedure over four independent dimensions
(**Ci / Zhi / Bo / Gong** — roughly: motive, efficacy, cognition, execution), implemented
as a runnable engine and evaluated on 172 historical subjects spanning seven subject types
(persons, institutions, intellectual movements, laws, legal families, states, organizations).

We report three classes of validation: (i) internal consistency, (ii) parameter
sensitivity, and (iii) ablation. We state explicitly that internal consistency (172/172; 6/6 for edge cases)
demonstrates *coherence, not validity*; external validity requires independent raters and
is left to future work. The ablation pass drove a genuine self-correction cycle: it
detected that several headline rules were not carrying load as implemented, traced the
root cause to suspended dimension levels that never reached the output, and repaired both
defects (dimension-level surfacing; C8 name–reality alignment). We close by stating what
evidence would falsify the framework.

**Keywords:** value pluralism; AI alignment; computational ethics; historical evaluation; declared standpoints; non-aggregation

---

## 1. Introduction

### 1.1 The problem

Evaluating an agent — a person, an institution, a law — requires combining considerations
that do not share a common metric. A ruler may have built a durable administrative order
while causing large-scale suffering. A thinker may have articulated a doctrine of human
dignity while never holding office. A legal system may be procedurally elegant while
entrenching slavery.

Two standard responses exist:

- **Aggregation.** Reduce the considerations to a scalar (utility, score, rating). This
  requires commensurability that the domain does not supply.
- **Particularism.** Decline to generalize; judge case by case. This forfeits
  reproducibility and makes disagreement untraceable.

We take a third route: **keep the dimensions separate, and make the disagreement
traceable.**

### 1.2 The claim

> *Most alignment research searches for the correct value function. We argue the correct
> architecture is: contestable, arguable priors, plus axiomatic constraints that priors
> have no authority to override.*

This inverts the usual division of labor. In most systems, constraints are soft
(penalties, regularization) and the value function is the object of optimization. Here the
constraint is hard and the value input is explicitly provisional.

### 1.3 Contributions

1. A four-dimensional, level-graded assessment space with an explicit non-aggregation
   principle (§3).
2. A five-stage adjudication procedure separating description from evaluation (§4).
3. The architectural separation of contestable priors from invariant constraints (§5).
4. A runnable implementation with sensitivity and ablation analysis (§6).
5. An ablation-driven self-correction procedure: the ablation pass detected two
   load-bearing implementation defects — dimension levels that were computed but never
   surfaced to the output, and a rule (C8) that was named "demote Gong" but implemented
   only as a defect annotation — and repaired both (§6.4).

---

## 2. Related Work

We survey the three literatures the framework must engage, indicating the specific point
of contact for each. Bibliographic details are verified in the References section (§10).

### 2.1 Value pluralism and incommensurability (philosophy)

- **Isaiah Berlin** — value pluralism; the claim that ultimate human values are
  incommensurable and sometimes conflict without a decision procedure.
  *Contact:* our non-aggregation principle is a direct descendant; we differ in supplying
  a procedure for *consequence* rather than a decision rule. `[1]`
- **John Rawls** — lexical priority ordering (*A Theory of Justice*).
  *Contact:* our dimension ordering (`秩 > 慈 > 博/工`) is a lexical priority;
  Rawls provides the canonical formulation we should be measured against. `[2]`
- **Ruth Chang** — incomparability and the possibility of "parity" as a fourth
  value relation beyond better/worse/equal.
  *Contact:* our refusal to average across dimensions is a commitment to hard
  incomparability; Chang's work is the strongest challenge to it. `[3]`
- **Amartya Sen** — social choice theory; the impossibility results on aggregating
  individual orderings.
  *Contact:* our "no composite scoring" rule is an explicit *anti-aggregation* position
  within the social-choice frame. `[4]`

Beyond the Anglo-American tradition, the question of how plural values relate to a
unitary moral order has been addressed in distinct philosophical frameworks.
**Spinoza's *Ethics*** (1677) grounds value conflict in the naturalistic necessity of
existence—conflict is not a failure of reason but an expression of the conatus, the
striving by which each being perseveres in its own being. This provides a metaphysical
justification for why value conflict is ineliminable and therefore must be *managed*
rather than *resolved*. `[5]`

In the German idealist tradition, **Hegel's *Phenomenology of Spirit*** (1807) offers a
dialectical account of how Spirit (Geist) actualizes itself through historical agents.
A subject is not evaluated as a static individual but as a moment in the unfolding of
Spirit—a perspective that directly informs our treatment of historical subjects as
carriers of transpersonal structures. `[6]`

In the Chinese tradition, **Zhu Xi's "Li yi fen shu" (理一分殊, "one principle, many
manifestations")** provides a striking parallel to our architectural separation: the
"one principle" corresponds to the invariant constraint (A2)—the non-negotiable
floor—while the "many manifestations" correspond to the contestable priors that vary
across standpoints. The framework can be read as an operationalization of this
Neo-Confucian insight in a computational setting. `[7]` `[8]`

### 2.2 Computational ethics and moral machine learning

- **Moral Machine** (MIT Media Lab) — large-scale collection of human moral preferences
  in trolley-type dilemmas; revealed cross-cultural variation in preferences.
  *Contact:* Moral Machine documents that preferences *vary by culture*. We treat this
  variation as the expected input layer rather than as noise to be averaged away. `[9]`
- **Bayesian moral learning** (Kleiman-Weiner et al.; work on inferring moral
  theories from observed judgments).
  *Contact:* our use of declared standpoints is methodologically adjacent;
  the difference is that ours are declared, not inferred. `[10]`
- **Moral Foundations Theory** (Haidt et al.) — a plural, dimensional account of moral
  concern.
  *Contact:* the closest existing multi-dimensional moral taxonomy; we must state
  precisely how our four dimensions differ from (and why they are not reducible to)
  the MFT foundations. `[11]`

**Wang Yangming's "extension of innate knowledge" (致良知)** offers a subject-centered
account of moral judgment: each person's conscience, when fully extended, yields
authentic moral perceptions, yet these perceptions may diverge across persons. This
provides a philosophical grounding for why multiple standpoints can be simultaneously
valid—not because anything goes, but because each standpoint is anchored in a distinct
moral subjectivity. `[12]`

**Wittgenstein's *Philosophical Investigations*** (1953) introduces the concept of
language-games—meaning is constituted by rule-governed practices within specific forms
of life. We acknowledge that our framework itself operates within a particular
language-game: its four dimensions, five-stage procedure, and A2 constraint are rules of
a historically situated evaluative practice, not transcendental truths. This reflexive
recognition is not a weakness but a condition of the framework's honesty. `[13]`

Finally, **Kant's *Groundwork of the Metaphysics of Morals*** (1785) provides the
strongest philosophical justification for A2. The second formulation of the categorical
imperative—"act so that you treat humanity, whether in your own person or in the person
of any other, always at the same time as an end and never merely as a means"—entails
precisely the inviolability of non-combatant life. A2 is not an arbitrary assertion but
an operationalization of the Kantian injunction in the domain of historical and
institutional evaluation. `[14]`

### 2.3 Pluralistic AI value alignment

- **Sorensen et al.** — roadmap for pluralistic alignment; argues against a single
  "correct" value target and for systems that can represent a diversity of values.
  *Contact:* the closest existing statement of our architectural claim. Our contribution
  relative to it is the *hard constraint layer* — a component that pluralistic alignment
  proposals typically leave unspecified. `[15]`
- **ℓp-regression aggregation for pluralistic alignment** (AAMAS 2022) — a specific
  mechanism for aggregating diverse preferences.
  *Contact:* a concrete instance of the "aggregate the diversity" approach we argue
  against. This is the most important citation for positioning our contrast. `[16]`

### 2.4 What is *not* claimed

We do **not** claim novelty for: multi-dimensional evaluation *per se*; the
motive/consequence distinction; the asymmetry of suffering; or probabilistic inference methods
generally. Each is established. The claim is narrower: that the *combination* —
graded independent dimensions + declared priors + non-overridable axioms + a runnable
adjudication procedure — has not, to our knowledge, been instantiated as a single
executable system.

---

## 3. The Assessment Space

### 3.1 Four dimensions

| Dimension    | Gloss     | Question answered                                | Independent of            |
| ------------ | --------- | ------------------------------------------------ | ------------------------- |
| **慈 (Ci)**   | motive    | Did the agent aim at the welfare of others?      | Whether it succeeded      |
| **秩 (Zhi)**  | efficacy  | Did a durable, functioning order result?         | Whether the order is just |
| **博 (Bo)**   | cognition | Did the agent penetrate to underlying structure? | Whether it was applied    |
| **工 (Gong)** | execution | Was something built that outlived its builder?   | Whether it was benevolent |

Each dimension is graded on five levels: `0 (null) · I (sub-basic) · II (basic) ·
III (effective) · IV (foundational)`. In the released interface these are rendered as
`无 · 普世以下 · 普世 · 精英 · 至圣`.

### 3.2 The non-aggregation principle (A3)

**No composite score is computed.** A subject's level is determined by its highest
dimension, not by an average. Deficiencies are recorded as labels attached to the
structure — never as reductions of the level.

Rationale: averaging presupposes commensurability. If the dimensions are genuinely
distinct aspects of agency, a high score on one does not compensate a low score on
another; the two facts simply stand together.

This has an important consequence that we regard as a strength:

> **Rank = 秩 (efficacy) is descriptive, not evaluative.** An efficient apparatus of
> extermination may rank *IV (foundational)* on Zhi. Its moral status is carried entirely
> by Ci and by the consequential accounting — not smuggled into Zhi.

Conflating these would either (a) force every effective-but-immoral system to be
misdescribed as ineffective, or (b) implicitly praise it. We decline both.

### 3.3 Short-board rule (C3)

For Ci, Zhi, and Bo, the value across time-segments is the **minimum**; for Gong it is
the **maximum**.

- Minimum for Ci: misdeeds are not masked by good deeds.
- Minimum for Bo: blind spots are not masked by insights.
- Maximum for Gong: achievements are not erased by later collapse.

---

## 4. The Adjudication Procedure

Five stages, in order. Stages 2, 3, and 5 may adjust levels; Stage 1 sets the
defaults; Stage 4 measures consequences without adjusting levels.

**Stage 1 · Presumption of adequacy.** All dimensions default to level II. Demotion
requires positive evidence. Low-confidence evidence raises the bar for demotion
(*in dubio pro reo* applied to grading, not only to guilt).

**Stage 2 · Falsification.** Three sub-checks:

- *Zhi collapse typology* — distinguishes **malign rupture** (destroying a functioning order),
  **remedial rupture** (breaking a collapsed order to restore balance; exempt from demotion
  but subject to a convergence test), and **value challenge** (thought experiments that
  break no actual order; not demoted, and explicitly encouraged as low-cost trial).
- *Condition checks* for level IV on Bo and Gong.
- *Ci* determined by **verifiable other-regarding action**, not inferred motive.

**Stage 3 · Standpoint adaptation.** The subject's identity, role, and historical period
set the standard. Within segmented evaluation, **each segment is graded under the identity
operative in that segment** (C10) — a youth's offense is not graded on a magistrate's
standard.

**Stage 4 · Consequential accounting (the Humean stage).** Contribution and damage are
measured **separately and never netted**. In comparison, damage carries weight 1.5.

**Stage 5 · Graded negative feedback.** Conclusions are constrained by ordinary
institutional means; extraordinary remedies are permitted only under strict, jointly
satisfied preconditions.

### 4.1 The invariant constraint (A2)

Non-combatants — individuals posing no present threat — may not be deprived of life or
basic property by governance or by institutional design.

- **Triggered by:** institutional or governance-level deprivation (slavery, collective
  punishment, lethal corvée labor).
- **Not triggered by:** wartime atrocity or individual violence — these are handled
  through Ci.
- **Consequence:** Ci is zeroed, the overall level is demoted, and the subject is
  permanently marked.

**A2 is a hard truncation on the inference procedure, not a term in it.** Priors cannot
override it; Stage 4 cannot trade against it; and harms already counted at A2 are excluded
from Stage 4 to avoid double-counting (C5).

### 4.2 Why A2 rather than something else

This is the framework's normative starting point and we state it as such rather than as a
theorem. The argument offered is: **continued existence is a precondition of every other
value.** A framework that permits trading lives against other goods cannot, on its own
terms, produce agents able to hold any value. A2 is therefore not one value among others
but a condition of the possibility of valuation.

This architectural role — an inviolable constraint that no trade-off may override —
is structurally the same idea as Nozick's **side-constraints**: individual rights
function as constraints on action, not as goals to be maximized. A2 is the
side-constraint of this framework, and we name the kinship explicitly. `[17]`

We acknowledge this is a substantive normative commitment, not a derivation from the
materialist premise alone.

---

## 5. Priors, Standpoints, and the Invariant

### 5.1 Relative at input, absolute at the floor

The framework admits that the same subject may be a hero under one standpoint and an
aggressor under another, and holds **both verdicts valid within their declared
standpoints.** This is implemented as:

- Each evaluation carries an explicit **prior**: source, declared bias direction, and
  confidence.
- Each carries an **attribution coefficient** (0.3–1.5) governing how much downstream
  consequence is credited or charged to the subject.

**What must not vary:** the A2 determination. An **invariant check** compares A2 outcomes
across standpoints; divergence is flagged as an error, not reported as a legitimate
disagreement.

This is the mechanism that prevents pluralism from collapsing into "anything can be
excused." Disagreement is permitted about *everything except the floor*.

We state one clarification about the status of the relative inputs. The
**confidence** attached to a standpoint is used only as an evidence-strength
reduction factor (the *in dubio pro reo* principle, C1); it is **not** a
probability whose prior is updated by likelihoods — no Bayesian updating is
performed anywhere in the pipeline. The term "standpoint" is therefore
declarative, not inferential.

A worked example makes the invariance visible. For the East India Company, the
British imperial-history standpoint (confidence 0.75, attribution 0.5) and the
Indo-postcolonial standpoint (confidence 0.8, attribution 1.3) reach the
identical verdict — 精英 (底线破缺型·慈为无), "elite (bottom-line-breach type ·
Ci: null)". The reason is architectural: the bottom-line breach (the Bengal
famine, institutionalized deprivation) is triggered by a factual field
independently of either standpoint, so the two relative knobs — confidence and
attribution — have no lever on the verdict. The floor is immune to the priors
by construction, which is exactly what the invariant check enforces.

### 5.2 Worked contrast

| Case                                    | Contribution measure                                          | Attribution | Verdict                                                |
| --------------------------------------- | ------------------------------------------------------------- | ----------- | ------------------------------------------------------ |
| Transcontinental railroad (US)          | Domestic integration                                          | —           | High contribution                                      |
| Yunnan–Indochina railway (FR, colonial) | Extraction; deliberately incompatible gauge with the interior | —           | Contribution credited to the colonizer, not the colony |

Both are large-scale railway construction. **Gong is comparable; contribution is not.**
Contribution is measured by *who retains the benefit*, not by activity scale (C11).

---

## 6. Implementation and Validation

The framework is implemented as a deterministic engine (Python and JavaScript, mutually
verified) operating on a declarative case file. The released version is v3.8; the engine
reproduces all adjudications deterministically.

### 6.1 Coverage

The corpus covers 172 subjects across seven types — persons, institutions,
intellectual movements, laws, legal families, states/empires, organizations —
encoded as 32 fine-grained identity labels, plus 6 constructed edge cases.
Treating institutions and organizations as evaluable agents follows the
group-agency literature on corporate agents (List & Pettit). The engine
reproduces all **172/172** main adjudications and **6/6** edge cases. `[18]`

### 6.2 Internal consistency

**This number demonstrates coherence, not validity.** The case file encodes dimensional
gradings supplied by the author; the engine demonstrates that its rules, applied
faithfully, reproduce those gradings. It does not demonstrate that independent evaluators
would supply the same gradings. We state this prominently because the number is otherwise
easy to misread.

### 6.3 Parameter sensitivity

| Parameter            | Stable band                        | Adopted | Effect outside band                                                                                            |
| -------------------- | ---------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------- |
| Damage weight        | [1.0, 1.6]                         | 1.5     | ≥1.7: Dong Zhuo flips; ≥2.0: Nazi Germany; ≥2.5: Yunnan–Indochina railway                                      |
| Severe ratio         | [1.4, 2.2]                         | 1.5     | ≤1.2: Nazi Germany flips; ≥2.3: Caribbean slave plantation flips                                               |
| Max demotion         | 2 (only value with zero variation) | 2       | 1: 6 cases change; ≥3: 1 case changes                                                                          |
| Confidence threshold | [0.5, 0.95]                        | 0.6     | Removing it changes 3 levels / 3 labels (Sui Yangdi, Wang Mang, King You of Zhou; marked 待考, "pending review") |

Sweep result on the full case set: over the core band
`DW ∈ [1.0, 1.5] × SR ∈ [1.5, 2.0]` (36 combinations), 24 combinations are exactly stable
(67%) and the worst deviation anywhere in the band is a single extreme case — the
Caribbean slave plantation regime — flipping at the boundary, which we consider
reasonable for the most extreme subject in the library. The measured stable band widened
after the v3.8 repair: `DW ∈ [1.0, 1.6] × SR ∈ [1.4, 2.2]` (63 combinations, 42 exactly
stable, worst deviation still one case). `MAX_REDUCTION = 2` remains the only value with
zero variation; setting it to 1 changes 6 levels.

We report honestly: at damage weight 1.0, variation is also zero. The weight is therefore
a **latent** parameter on this case set. The asymmetry it expresses is load-bearing in the
*architecture* (A2 + C5), not in this particular value.

### 6.4 Ablation

Removing or weakening individual rules reveals which ones actually do work. The v3.8
ablation pass was run on the full 172-subject case set:

| Ablation                                       | Effect (levels / labels)                                                                              |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| C3 short-board rule removed                    | 0 levels / 8 labels — no load as implemented, *until* level surfacing made its effect visible (below) |
| C5 no-double-counting removed                  | 0 / 0                                                                                                 |
| C7 admission removed                           | 2 levels / 3 labels (Kublai Khan; Mongol conquest)                                                    |
| C7 floor removed                               | 0 / 0                                                                                                 |
| Dimension-level surfacing removed              | 0 levels / 59 labels lose information                                                                 |
| C8 (old "defect annotation" behavior) restored | 10 levels / 23 labels; 24 subjects matched                                                            |
| Max demotion set to 1                          | 6 levels / 0 labels                                                                                   |

**The ablation changed the framework.** Two defects were found and repaired.

*Suspended dimension levels.* Removing C3 changes Ci in 8 of the 19 segmented subjects
(e.g., Tang Xuanzong, Xiao Yan, Ashoka, Zhou Chu), yet — before the repair — no label
changed at all. The root cause was that the final verdict read only boolean flags (was
anything zeroed? any unnecessary atrocity? any bottom-line breach?) and ignored the
specific dimension levels: Ci at level 1 versus level 4 produced the identical label.
The information was computed and then discarded. Statistically, 122 of 172 subjects are
rated foundational (至圣) while falling short on at least one dimension; 17 are rated
foundational with at least one dimension at or below the sub-basic floor.

*Repair: dimension-level surfacing.* Every dimension level is now visible in the output
label: level 0 → "X为无", level 1 → "X塌陷", level 2 → "X薄弱", merged where adjacent.
The effect is that weak dimensions become visible without lowering the subject's overall
level — consistent with the non-aggregation principle (A3): a weak dimension does not drag
down the composite (there is no composite), but it is no longer invisible.

*C8 name–reality alignment.* C8 was named "missing negative feedback demotes Gong" but
implemented as `defects.push(...)` — it annotated, never demoted. It now actually demotes
Gong. The 24 matched subjects are exactly the "built but did not outlive its builder"
class: Northern Song, Ming, Qing, USSR, Dell, Tokugawa shogunate, Arab Caliphate, Mongol
Empire, Mughal Empire, Alexander the Great, Napoleon, and others. The level distribution
moves from 至圣 132 / 精英 28 / 普世 7 / 普世以下 5 under the old annotation behavior to
至圣 125 / 精英 32 / 普世 10 / 普世以下 5 under real demotion — seven subjects demoted, not
an over-punitive shift.

**Rules that still show zero load are not therefore useless.** C3, C5, and C9 do real work
only under conditions the current case set does not trigger (as an airbag does nothing
when there is no crash). What was genuinely broken was that C3's dimensional information
had no output channel; that is exactly what the surfacing repair restored — after the
repair, removing C3 changes 8 labels instead of 0.

**Parameters did not regress from the repair.** The sensitivity sweep (above) is
unchanged or slightly widened after the v3.8 fixes. The methodologically important point
is that ablation caught rules that were nominal-but-inert — a class of defect that
paper-and-pencil reasoning cannot detect. This is why the framework must ship as an
executable engine, not as a document.

---

## 7. Selected Cases

Five cases, chosen to expose the framework rather than to display it. Labels are the v3.8
outputs.

1. **The US Constitution.** Level IV on Zhi, Bo, and Gong; Ci zeroed by the
   three-fifths compromise (A2 triggered); final label 底线破缺型·慈为无 (bottom-line-breach type · Ci: null). Its amendment
   mechanism later repaired the breach via the Thirteenth Amendment — the artifact proved
   more capable of correction than its authors.
2. **Shang Yang.** Zhi and Gong at IV; Ci null; A2 triggered by collective
   punishment. Demoted (底线破缺型·慈为无 — bottom-line-breach type · Ci: null). He was eventually executed by the apparatus he
   designed — the framework records this as the constraint executing itself.
3. **Kant.** Ci at IV (the formula of humanity as an end, widely operative in subsequent
   human-rights law) and Gong at IV — establishing that for a thinker, **having one's
   doctrine practiced is the relevant form of execution** (均衡偏科型 — the "balanced but uneven" type).
4. **Utopian socialism.** Ci at IV (aimed at universal welfare) but Gong at II — the
   blueprint exists; the building does not (未兑现型·工薄弱 — the "unrealized" type · Gong: weak). Establishes that Ci does not
   require success.
5. **The late Qing.** Zhi null across all three supports (civil control over the
military, central control of finance, and institutionalized succession) simultaneously —
the collapse of all three pillars at once is rare, and therefore methodologically
instructive; yet not
   adjudicated at the floor, because analysis surfaced transferable structure
   (失职型·秩为无·慈、工塌陷 — the "dereliction" type · Zhi: null · Ci and Gong collapsed). This case fixes the framework's lower boundary: *anything
   worth analyzing has something extractable from it.*

---

## 8. Limitations

Stated prominently, in the order a reviewer would raise them.

1. **Dimensional gradings are author-supplied.** Internal consistency does not establish
   that independent raters would agree. An inter-rater reliability study is required and
   is not yet conducted. *This is the framework's principal open weakness.*
2. **Historical inputs are contestable.** Population and duration figures used in Stage 4
   are drawn from mainstream historiography and are themselves disputed.
3. **Normative starting point is asserted.** A2 is argued for, not derived.
4. **Parameters are empirical, not analytic.** They are stable within measured bands, not
   optimal in a proven sense.
5. **Survivorship bias.** The case set contains only subjects who entered the historical
   record. The framework characterizes *agents that left a trace*, not persons generally.
6. **No claim about consciousness or intent.** The framework grades evidence, not minds.

### 8.1 What would falsify this framework

We state this because a methodology that cannot be contradicted is not a methodology.

- If independent raters, given the rules, fail to reach agreement substantially above
  raters given only the dimension definitions, then the **rules add nothing** — the
  four dimensions alone would explain the result, and the procedure would be decorative.
- If A2 determinations diverge across standpoints in a substantial fraction of cases,
  then the **invariant is not invariant**, and the framework's central architectural
  claim collapses.
- If adjudications prove highly sensitive to parameters *within* the reported stable
  bands on new cases, then the **stability is an artifact of this case set**.

---

## 9. Conclusion

We have argued that the problem of plural valuation is not best addressed by finding a
better value function, but by separating the parts of evaluation that are legitimately
contested from the parts that are not, and by making the contest visible rather than
averaging it away.

The framework's distinctive commitments are therefore:

1. **Dimensions are graded, not aggregated.**
2. **Efficacy is described; motive is evaluated; execution is measured; cognition is
   assessed.** No dimension is asked to do another's work.
3. **Priors are declared and contestable; the floor is not.**
4. **The procedure is executable, and therefore falsifiable.**

The last point is the one we would most want a reader to test.

**Scope: a diagnostic, not a decision procedure.** The framework generates a
traceable spectrum of judgments, each valid within its declared standpoint; it
does not adjudicate conflicts between standpoints (except at the A2 floor), nor
does it output a single policy recommendation. Resolving standpoint conflicts
in deployment is left to social deliberation — the framework's role is to make
disagreement visible and traceable, not to settle it.

---

## Appendix A. Reproducibility

The engine, case file, and interactive interface are available at:
`https://gusuziyi.github.io/MindOrder/` (GitHub Pages mirror of the companion
repository).

Deterministic: identical inputs produce identical outputs on both implementations.
Reproduce with:

```bash
python3 xinzhixue_engine.py   # prints 主案例一致 172/172，演示一致 6/6
```

## Appendix B. Term mapping (Chinese → English)

| Term      | Gloss in this paper                                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 慈 (Ci)    | motive / other-regarding aim                                                                                                          |
| 秩 (Zhi)   | efficacy of order                                                                                                                     |
| 博 (Bo)    | cognition / structural penetration                                                                                                    |
| 工 (Gong)  | execution / durable artifact                                                                                                          |
| A2        | invariant constraint (non-combatant inviolability)                                                                                    |
| A3        | non-aggregation / independent dimension grading                                                                                       |
| C1        | presumption of adequacy; weaker evidence raises the bar for demotion                                                                  |
| C2        | only what has occurred is measured — predicted future benefits do not enter                                                           |
| C3        | short-board rule: Ci, Zhi, Bo take the minimum across segments; Gong takes the maximum                                                |
| C4        | each dimension carries its own praise; no dimension bears another's moral loading                                                     |
| C5        | no double-counting — a fact already counted at A2 is excluded from Stage 4                                                            |
| C6        | subject separation — a regime and its legacy are adjudicated separately                                                               |
| C7        | admission and floor — no creation or contribution, no entry; nothing with a dimension at Level III or above is consigned to the floor |
| C8        | missing negative feedback demotes Gong (built, but did not outlive its builder)                                                       |
| C9        | relative at input, absolute at the floor                                                                                              |
| C10       | per-segment standpoint adaptation                                                                                                     |
| C11       | contribution measured by beneficiary, not activity scale                                                                              |
| Surfacing | dimension-level labels appended to the verdict (无/塌陷/薄弱), so weak dimensions are visible without lowering the level                   |

---

## 10. References

The works cited in §2, with bibliographic details verified against primary sources.

1. I. Berlin. *Four Essays on Liberty*. Oxford University Press, Oxford, 1969. (Contains
   "Two Concepts of Liberty", first delivered as the inaugural lecture at Oxford, 1958.)
2. J. Rawls. *A Theory of Justice*. Harvard University Press, Cambridge, MA, 1971.
3. R. Chang. "The Possibility of Parity." *Ethics*, 112(4): 659–688, 2002.
4. A. Sen. *Collective Choice and Social Welfare*. Holden-Day, San Francisco, 1970.
   (Expanded 2nd ed., Harvard University Press, 2017.)
5. B. de Spinoza. *Ethics, Demonstrated in Geometrical Order*. (Originally published
   posthumously, 1677. Cited edition: Curley, E. (trans.), *The Collected Works of
   Spinoza*, Vol. 1, Princeton University Press, 1985.)
6. G. W. F. Hegel. *Phenomenology of Spirit*. (Originally published 1807. Cited
   edition: Miller, A. V. (trans.), Oxford University Press, 1977.)
7. Zhu Xi (朱熹). *Jin Si Lu* (《近思录》, *Reflections on Things at Hand*). (Compiled
   with Lü Zuqian, 1175. Cited edition: Chan, W.-T. (trans.), *Reflections on Things
   at Hand*, Columbia University Press, 1967.)
8. Zhu Xi (朱熹). *Li yi fen shu* (理一分殊, "One Principle, Many Manifestations").
   (Doctrine elaborated in Zhu Xi's commentaries and letters; for a systematic
   treatment, see J. P. Bruce, *Chu Hsi and His Masters*, Probsthain, 1923.)
9. E. Awad, S. Dsouza, R. Kim, J. Schulz, J. Henrich, A. Shariff, J.-F. Bonnefon, and
   I. Rahwan. "The Moral Machine Experiment." *Nature*, 563(7729): 59–64, 2018.
   doi:10.1038/s41586-018-0637-6.
10. M. Kleiman-Weiner, R. Saxe, and J. B. Tenenbaum. "Learning a Commonsense Moral
    Theory." *Cognition*, 167: 107–119, 2017.
11. J. Graham, J. Haidt, S. Koleva, M. Motyl, R. Iyer, S. P. Wojcik, and P. H. Ditto.
    "Moral Foundations Theory: The Pragmatic Validity of Moral Pluralism."
    *Advances in Experimental Social Psychology*, 47: 55–130, 2013.
12. Wang Yangming (王阳明). *Chuan Xi Lu* (《传习录》, *Instructions for Practical
    Living*). (Originally published 1518, expanded 1524. Cited edition: Chan, W.-T.
    (trans.), *Instructions for Practical Living and Other Neo-Confucian Writings*,
    Columbia University Press, 1963.)
13. L. Wittgenstein. *Philosophical Investigations*. (Originally published 1953.
    Cited edition: Anscombe, G. E. M. (trans.), 3rd ed., Blackwell, 2001.)
14. I. Kant. *Groundwork of the Metaphysics of Morals*. (Originally published 1785.
    Cited edition: Gregor, M. (trans.), Cambridge University Press, 1997.)
15. T. Sorensen, J. Moore, J. Fisher, M. Gordon, N. Mireshghallah, C. M. Rytting, A. Ye,
    L. Jiang, X. Lu, N. Dziri, T. Althoff, and Y. Choi. "Position: A Roadmap to
    Pluralistic Alignment." In *Proceedings of the 41st International Conference on
    Machine Learning (ICML 2024)*. arXiv:2402.05070, 2024.
16. R. Lera-Leri, F. Bistaffa, M. Serramia, M. Lopez-Sanchez, and J. A. Rodriguez-Aguilar.
    "Towards Pluralistic Value Alignment: Aggregating Value Systems through
    ℓp-Regression." In *Proceedings of the 21st International Conference on Autonomous
    Agents and Multiagent Systems (AAMAS 2022)*, pp. 780–788, 2022.
17. R. Nozick. *Anarchy, State, and Utopia*. Basic Books, New York, 1974. (The
    concept of side-constraints: individual rights as inviolable constraints on
    action, not as goals to be maximized.)
18. C. List and P. Pettit. *Group Agency: The Possibility, Design, and Status of
    Corporate Agents*. Oxford University Press, Oxford, 2011.

---

*End of draft (v3.8). All adjudication counts reported here are produced by running the
released engine (v3.8) on the released case file; all ablation and sensitivity numbers are
from the same run.*
