# Before/after examples per generation method

Five pairs per method, drawn at random (seed 0) from the real saved data, not picked by hand. Before = the formal Lean text, after = the informal text that the method produced. Text longer than 1,200 characters is cut with `[...]`; the full pairs are in `examples.jsonl`.


## MMA Train (baseline, not ours)

Source: `AI4M/mma-dataset/train.jsonl`, 84,679 pairs, row indices [5306, 33936, 50494, 55125, 67013].

**Example 1 (row 5306)**

Before (formal):
```lean
theorem cg_iff : CG L M ↔ ∃ S : Set M, S.Countable ∧ closure L S = (⊤ : L.Substructure M) :=
```
After (informal):
```text
A structure M over a language L is finitely generated if and only if there exists a set S of elements in M such that S is countable and the closure of S under the operations of L equals the entire substructure of M.
```

**Example 2 (row 33936)**

Before (formal):
```lean
theorem mem_iInf {ι} {s : ι → Filter α} {U : Set α} :
    (U ∈ ⨅ i, s i) ↔ ∃ I : Set ι, I.Finite ∧ ∃ V : I → Set α, (∀ i, V i ∈ s i) ∧ U = ⋂ i, V i :=
```
After (informal):
```text
A set U is in the infimum of a function s (from index set ι to filters on α) if and only if there exists a finite set I of indices such that there exists a function V (from I to sets of α) where for all indices i, V(i) is in s(i) and U is the intersection of all V(i).
```

**Example 3 (row 50494)**

Before (formal):
```lean
theorem isCompl_dualAnnihilator {W W' : Subspace K V₁} (h : IsCompl W W') :
    IsCompl W.dualAnnihilator W'.dualAnnihilator :=
```
After (informal):
```text
If W and W' are complementary subspaces of a vector space V₁ over a field K, then the annihilators of W and W' in the dual space are also complementary.
```

**Example 4 (row 55125)**

Before (formal):
```lean
theorem refl_trans (α : X ≅ Y) : Iso.refl X ≪≫ α = α :=
```
After (informal):
```text
For any isomorphism 'α' from 'X' to 'Y', the composition of the identity isomorphism on 'X' and 'α' is equal to 'α'.
```

**Example 5 (row 67013)**

Before (formal):
```lean
theorem image_image2 (f : α → β → γ) (g : γ → δ) :
    g '' image2 f s t = image2 (fun a b => g (f a b)) s t :=
```
After (informal):
```text
The image of the function g applied to the image of the function f with two arguments from sets s and t, is equal to the image of the function that applies g to the result of f with two arguments from sets s and t.
```


## GPT-4 MathLib4 (Full Proof)

Source: `AI4M/gpt4-more/train.jsonl`, 348 pairs, row indices [155, 183, 207, 244, 248].

**Example 1 (row 155)**

Before (formal):
```lean
theorem associated_iff_eq {x y : α} : x ~ᵤ y ↔ x = y := by
   constructor
   · rintro ⟨c, rfl⟩
     rw [units_eq_one c, Units.val_one, mul_one]
   · rintro rfl
     rfl
 #align associated_iff_eq associated_iff_eq
 
 
```
After (informal):
```text
Two elements $x$ and $y$ of a commutative monoid with zero are associated if and only if they are equal. This is proven by constructing a bidirectional implication. In one direction, we assume that $x$ and $y$ are associated, which means there exists a unit $c$ such that $x = c \cdot y$. By the definition of a unit, we have $c = 1$, so $x = y$. In the other direction, we assume that $x = y$, which is trivially true.
```

**Example 2 (row 183)**

Before (formal):
```lean
theorem one_le {a : Associates α} : 1 ≤ a :=
   Dvd.intro _ (one_mul a)
 #align associates.one_le Associates.one_le
 
 
```
After (informal):
```text
For any associate $a$ of a type $α$, $1$ is less than or equal to $a$. This is proven by introducing a divisor through the property that multiplying $1$ by $a$ gives $a$.
```

**Example 3 (row 207)**

Before (formal):
```lean
theorem dvdNotUnit_of_dvdNotUnit_associated [CommMonoidWithZero α] [Nontrivial α] {p q r : α}
     (h : DvdNotUnit p q) (h' : Associated q r) : DvdNotUnit p r := by
   obtain ⟨u, rfl⟩ := Associated.symm h'
   obtain ⟨hp, x, hx⟩ := h
   refine' ⟨hp, x * ↑u⁻¹, DvdNotUnit.not_unit ⟨u⁻¹.ne_zero, x, hx.left, mul_comm _ _⟩, _⟩
   rw [← mul_assoc, ← hx.right, mul_assoc, Units.mul_inv, mul_one]
 #align dvd_not_unit_of_dvd_not_unit_associated dvdNotUnit_of_dvdNotUnit_associated
 
 end CommMonoidWithZero
 
 section CancelCommMonoidWithZero
 
 
```
After (informal):
```text
Let $p$, $q$, and $r$ be elements of a commutative monoid with zero that is nontrivial. Suppose that $p$ divides $q$ but is not a unit, and $q$ is associated with $r$. Then, $p$ divides $r$ but is not a unit. This is proven by first obtaining a unit $u$ such that $u$ times $r$ equals $q$. Then, we obtain that $p$ is not a unit and there exists an $x$ such that $p$ times $x$ equals $q$. We then refine our goal to show that $p$ is not a unit, $x$ times the inverse of $u$ is not a unit, and $p$ times $x$ times the inverse of $u$ equals $r$. This is done by rewriting the equation using the associative property of multiplication and the fact that a unit times its inverse equals one.
```

**Example 4 (row 244)**

Before (formal):
```lean
theorem rel_act_of_act_rel_act_of_rel_act (ab : r (μ m a) (μ m b)) (rr : r b (μ m c)) : \newline      r a (μ m c) := \newline    _root_.trans (rel_of_act_rel_act m ab) rr \newline  #align rel_act_of_act_rel_act_of_rel_act rel_act_of_act_rel_act_of_rel_act \newline   \newline  end Trans \newline   \newline  end Contravariant \newline   \newline  section Monotone \newline   \newline  variable {α : Type*} {M N μ} [Preorder α] [Preorder N] \newline   \newline  variable {f : N → α} \newline   \newline  
```
After (informal):
```text
Given a relation $r$ and a function $μ$, if $r$ holds between $μ(m, a)$ and $μ(m, b)$, and $r$ holds between $b$ and $μ(m, c)$, then $r$ holds between $a$ and $μ(m, c)$. This is the end of the section on contravariant relations. Next, we consider a section on monotone relations. We have a preorder on types $α$ and $N$, and a function $f$ from $N$ to $α$.
```

**Example 5 (row 248)**

Before (formal):
```lean
theorem Antitone.covariant_of_const [CovariantClass M N μ (· ≤ ·)] (hf : Antitone f) (m : M) :
     Antitone (f <| μ m ·) :=
   hf.comp_monotone <| Covariant.monotone_of_const m
 #align antitone.covariant_of_const Antitone.covariant_of_const
 
 
```
After (informal):
```text
If $f$ is an antitone function and $m$ is a constant, then the function $f$ composed with the multiplication by $m$ is also antitone.
```


## GPT-4 LeanDojo (Individual Tactics), 29-pair set

Source: `AI4M/state_info_informalization/train.json`, 29 pairs, row indices [4, 6, 16, 18, 28].

**Example 1 (row 4)**

Before (formal):
```lean
𝕜 : Type u_1
inst✝³⁷ : NontriviallyNormedField 𝕜
E : Type u_2
inst✝³⁶ : NormedAddCommGroup E
inst✝³⁵ : NormedSpace 𝕜 E
H : Type u_3
inst✝³⁴ : TopologicalSpace H
M : Type u_4
inst✝³³ : TopologicalSpace M
inst✝³² : ChartedSpace H M
inst✝³¹ : SmoothManifoldWithCorners I M
inst✝³⁰ : NormedAddCommGroup E'
inst✝²⁹ : NormedSpace 𝕜 E'
inst✝²⁸ : TopologicalSpace H'
inst✝²⁷ : TopologicalSpace M'
inst✝²⁶ : ChartedSpace H' M'
inst✝²⁵ : SmoothManifoldWithCorners I' M'
inst✝²⁴ : NormedAddCommGroup E''
inst✝²³ : NormedSpace 𝕜 E''
inst✝²² : TopologicalSpace H''
inst✝²¹ : TopologicalSpace M''
inst✝²⁰ : ChartedSpace H'' M''
F : Type u_11
inst✝¹⁹ : NormedAddCommGroup F
inst✝¹⁸ : NormedSpace 𝕜 F
G : Type u_12
inst✝¹⁷ : TopologicalSpace G
N : Type u_13
inst✝¹⁶ : TopologicalSpace N
inst✝¹⁵ : ChartedSpace G N
inst✝¹⁴ : SmoothManifoldWithCorners J N
inst✝¹³ : NormedAddCommGroup F'
inst✝¹² : NormedSpace 𝕜 F'
inst✝¹¹ : TopologicalSpace G'
inst✝¹⁰ : TopologicalSpace N'
inst✝⁹ : ChartedSpace G' N'
inst✝⁸ : SmoothManifoldWithCorners J' N'
F₁ : Type u_17
inst✝⁷ : NormedAddCommGroup F₁
inst✝⁶ : NormedSpace 𝕜 F₁
F₂ : Type u_18
inst✝⁵ : NormedAddCommGroup F₂
inst✝⁴ : NormedSpace 𝕜 F₂
F₃ : Type u_19
inst✝³ : Normed [...]
```
After (informal):
```text
In the given setup, we are working within a mathematical framework that involves several types and their associated properties. Specifically, we have $\mathcal{K}$ as a type with a structure of a non-trivially normed field, $E, E', E''$ as types structured as normed additive commutative groups and normed spaces over $\mathcal{K}$, and similar structures for $F, F', F_1, F_2, F_3, F_4$. There are also topological spaces $H, H', H'', G, G', N, N'$, along with manifold structures on $M, M', M''$, and $N$, each equipped with their corresponding models with corners $I, I', I'', J, J'$. Specific objects in this context include a local homeomorphism $e: M \to H$ and sets $s, s_1, t$ within $M$. The conditions given are as follows: we have models with corners $I$ and $J$ facilitating the structures on $E \to H$ and $F \to G$, respectively; functions $f, f_1: M \to M'$, a function $g: M' \to M''$, and a point $x$ in $M$. It is established that the function $f$ is continuously differentiable at $x$ with a certain smoothness level $n$, denoted as $hf : \text{ContMDiffAt} \ I \ I' \ n \ f \ x$, and similarly, $g$ is continuously differentiable at $f(x)$ with the same smoothness level, denoted  [...]
```

**Example 2 (row 6)**

Before (formal):
```lean
L : Language
T : Theory L
α : Type w
n : ℕ
φ : Sentence L
T ⊨ᵇ φ ↔ ∃ T0, ↑T0 ⊆ T ∧ ↑T0 ⊨ᵇ φ
simp only [models_iff_not_satisfiable]
L : Language
T : Theory L
α : Type w
n : ℕ
φ : Sentence L
⊢ ¬IsSatisfiable (T ∪ {Formula.not φ}) ↔ ∃ T0, ↑T0 ⊆ T ∧ ¬IsSatisfiable (↑T0 ∪ {Formula.not φ})
```
After (informal):
```text
In this scenario, we're dealing with a formal language L and a theory T within that language, along with a sentence \(\phi\) from L, an unspecified type \(\alpha\) and a natural number n. The goal is to prove the equivalence between T proving \(\phi\) and the existence of a subtheory T0 of T that also proves \(\phi\). This is articulated as T ⊢ₗ φ ↔ ∃ T0, ↑T0 ⊆ T ∧ ↑T0 ⊢ₗ φ. The proof strategy employs a simplification tactic that relies on the lemma models_iff_not_satisfiable, which connects model theory (the study of the models of theories in formal languages) with satisfiability. Specifically, the lemma likely states that a theory models a sentence if and only if there's no satisfiable extension of the theory where the negation of the sentence holds. Applying this lemma transforms the goal into a statement about satisfiability: proving that ¬IsSatisfiable (T ∪ {Formula.not φ}) is equivalent to the existence of a subtheory T0 such that ¬IsSatisfiable (↑T0 ∪ {Formula.not φ}), where ↑T0 denotes some form of closure or collection related to T0. This step essentially reformulates the original goal into terms of satisfiability and nonsatisfiability of the theory T (and its subtheories) [...]
```

**Example 3 (row 16)**

Before (formal):
```lean
L : Language
T : Theory L
α : Type w
n : ℕ
φ : Sentence L
this : DecidableEq (Sentence L) := Classical.decEq (Sentence L)
h : ∀ (T0 : Finset (Sentence L)), ↑T0 ⊆ T → IsSatisfiable (↑T0 ∪ {Formula.not φ})
T0 : Finset (Sentence L)
IsSatisfiable ↑T0
exact IsSatisfiable.mono (h (T0.erase (Formula.not φ))
  (by simpa using hT0)) (by simp)
no goals
```
After (informal):
```text
In this proof context, we're dealing with the framework of a formal language \(L\), a theory \(T\) from \(L\), a type \(\alpha\), a natural number \(n\), and a sentence \(\phi\) in \(L\). Additionally, a decision mechanism for equality among sentences in \(L\), `this : DecidableEq (Sentence L) := Classical.decEq (Sentence L)`, is established. The conditions include a hypothesis \(h\) indicating that for any finite set of sentences \(T0\), if \(T0\) is a subset of \(T\), then \(T0\) extended with the negation of \(\phi\) is satisfiable. Given \(T0\) as a specific finite set of sentences, the proof aims to establish the satisfiability of \(T0\). The tactic used to achieve this, `exact IsSatisfiable.mono (h (T0.erase (Formula.not \\phi)) (by simpa using hT0)) (by simp)`, employs a sophisticated strategy that involves modifying \(T0\) by erasing the negation of \(\phi\) and then applying \(h\) to show that the modified \(T0\) is satisfiable. This strategy is underpinned by leveraging the `IsSatisfiable.mono` principle, which essentially asserts that if a subset of \(T0\) (in this case, \(T0\) minus the negation of \(\phi\)) is satisfiable, then \(T0\) itself is satisfiable. The use of  [...]
```

**Example 4 (row 18)**

Before (formal):
```lean
L : Language
T : Theory L
α : Type w
n : ℕ
φ : Sentence L
this : DecidableEq (Sentence L) := Classical.decEq (Sentence L)
h : ∀ (T0 : Finset (Sentence L)), ↑T0 ⊆ T → IsSatisfiable (↑T0 ∪ {Formula.not φ})
T0 : Finset (Sentence L)
↑T0 ⊆ ↑(Finset.erase T0 (Formula.not φ)) ∪ {Formula.not φ}
simp
no goals
```
After (informal):
```text
In this proof context, we're navigating within a formal language \(L\), associated with a theory \(T\) formulated in \(L\), a type \(\alpha\), a natural number \(n\), and a sentence \(\phi\) from \(L\). A mechanism for deciding equality among sentences in \(L\), `this : DecidableEq (Sentence L) := Classical.decEq (Sentence L)`, is in place. The setup includes a hypothesis \(h\) that for any finite set of sentences \(T0\), if \(T0\) as a subset of \(T\) leads to the satisfiability of \(T0\) extended with the negation of \(\phi\). Given \(T0\) as a finite set of sentences, the proof aims to demonstrate that \(T0\) is a subset of \(T0\) with the negation of \(\phi\) erased, extended with the negation of \(\phi\). The tactic `simp` is utilized to achieve this goal, working under the Lean prover's simplification procedures. This tactic effectively simplifies the goal by acknowledging that \(T0\), inherently, is a subset of itself even after the erasure of any elements, including the negation of \(\phi\), and the subsequent addition of the negation of \(\phi\) back into the set. This simplification straightforwardly addresses the goal, illustrating that the original set \(T0\) remains a  [...]
```

**Example 5 (row 28)**

Before (formal):
```lean
n : Type u_1
p : Type u_2
𝕜 : Type u_3
inst✝³ : Field 𝕜
R : Type u₂
inst✝² : DecidableEq n
inst✝¹ : DecidableEq p
r : ℕ
M : Matrix (Fin r ⊕ Unit) (Fin r ⊕ Unit) 𝕜
hM : M (inr ()) (inr ()) ≠ 0
i : Fin r
j : Unit
this : j = ()
toBlocks₁₂ (List.prod (listTransvecCol M) * M * List.prod (listTransvecRow M)) i j = OfNat.ofNat 0 i j
simp [toBlocks₁₂, this, listTransvecCol_mul_mul_listTransvecRow_last_row M hM]
no goals
```
After (informal):
```text
In this proof, we're situated within a mathematical context defined by several types: \(n\), \(p\), and \(\mathbb{K}\), with \(\mathbb{K}\) being a field. The setup includes decidable equality for \(n\) and \(p\), a natural number \(r\), and a matrix \(M\) that is \(r \times r\) with elements in \(\mathbb{K}\). The matrix \(M\) features a specifically non-zero element as indicated by \(hM\), and there are particular indices \(i\) of type \(Fin r\) and \(j\) of type \(Unit\), with a prior step establishing \(j = ()\) as a given fact. The goal is to demonstrate that after applying a sequence of transformations to \(M\)—specifically, multiplying \(M\) by the products of lists of transvection matrices applied to columns and rows—the element in the `toBlocks₁₂` block at position \(i, j\) is zero, denoted as `OfNat.ofNat 0 i j`. The tactic `simp [toBlocks₁₂, this, listTransvecCol_mul_mul_listTransvecRow_last_row M hM]` is employed, which simplifies the goal using the provided facts and definitions. This includes leveraging the established fact `this : j = ()`, the definition of `toBlocks₁₂`, and the specific lemma `listTransvecCol_mul_mul_listTransvecRow_last_row M hM` that relates to ho [...]
```


## GPT-4 LeanDojo (Individual Tactics), 100-pair set

Source: `AI4M/stateInfoInformalizationBig/stateInfoInformalization.json`, 100 pairs, row indices [12, 17, 36, 79, 96].

**Example 1 (row 12)**

Before (formal):
```lean
  L : Language, T : Theory L, α : Type w, n : ℕ, φ : Sentence L, this : DecidableEq (Sentence L) := Classical.decEq (Sentence L), h : ∀ (T0 : Finset (Sentence L)), ↑T0 ⊆ T ∪ {Formula.not φ} → IsSatisfiable ↑T0, T0 : Finset (Sentence L) IsSatisfiable (↑T0 ∪ {Formula.not φ}) simpa using h (T0 ∪ {Formula.not φ})
  (by
    simp only [Finset.coe_union, Finset.coe_singleton]
    exact Set.union_subset_union hT0 (Set.Subset.refl _)) no goals
```
After (informal):
```text
In this proof, we're working within a formal language \(L\), with a theory \(T\) based on \(L\), a type \(\alpha\), a natural number \(n\), and a specific sentence \(\phi\) from \(L\). A mechanism for deciding equality among sentences in \(L\), given as `this : DecidableEq (Sentence L) := Classical.decEq (Sentence L)`, has been introduced. The conditions include a hypothesis \(h\) that asserts for any finite set of sentences \(T0\), if \(T0\) extended with the negation of \(\phi\) is a subset of \(T\) similarly extended, then \(T0\) is satisfiable. Given a specific finite set of sentences \(T0\), the goal is to prove that \(T0\), extended with the negation of \(\phi\), is satisfiable. The proof employs the tactic `simpa using h (T0 \cup \{\text{Formula.not} \, \phi\})` alongside a simplification strategy that manipulates set operations and subset relations. Specifically, it simplifies the expression to leverage the hypothesis \(h\) by showing that \(T0\) union \(\{\text{Formula.not} \, \phi\}\) satisfies the conditions outlined by \(h\), facilitated by a detailed manipulation of finite set operations and subset relations to align with the hypothesis's requirements. This simplificat [...]
```

**Example 2 (row 17)**

Before (formal):
```lean
  L : Language, T : Theory L, α : Type w, n : ℕ, φ : Sentence L, this : DecidableEq (Sentence L) := Classical.decEq (Sentence L), h : ∀ (T0 : Finset (Sentence L)), ↑T0 ⊆ T → IsSatisfiable (↑T0 ∪ {Formula.not φ}), T0 : Finset (Sentence L) ↑(Finset.erase T0 (Formula.not φ)) ⊆ T simpa using hT0 no goals
```
After (informal):
```text
In this proof setup, we're situated within a formal language \(L\), engaging with a theory \(T\) constructed within \(L\), alongside a type \(\alpha\), a natural number \(n\), and a specific sentence \(\phi\) from \(L\). Additionally, a decision procedure for determining equality among sentences in \(L\), denoted as `this : DecidableEq (Sentence L) := Classical.decEq (Sentence L)`, is provided. A hypothesis \(h\) is outlined, indicating that for any finite set of sentences \(T0\), if \(T0\) as a subset of \(T\) implies that \(T0\) extended with the negation of \(\phi\) is satisfiable. Given \(T0\) as a finite set of sentences, the goal is to demonstrate that \(T0\), with the negation of \(\phi\) erased, remains a subset of \(T\).The tactic `simpa using hT0` is adeptly employed to address this goal. This tactic simplifies the goal leveraging the hypothesis \(hT0\), which asserts the subset relation of \(T0\) to \(T\), and by implication, that the erasure of the negation of \(\phi\) from \(T0\) does not affect this subset relation. Essentially, the simplification process applied here directly aligns with the logical requirements set forth by \(hT0\), effortlessly establishing that \( [...]
```

**Example 3 (row 36)**

Before (formal):
```lean
α : Type u_1, inst✝⁵ : MetricSpace α, m0 : MeasurableSpace α, E : Type u_2, inst✝⁴ : NormedAddCommGroup E, inst✝² : BorelSpace α s : Set α, t : Set α := toMeasurable μ s μ : Measure α, v : VitaliFamily μ, inst✝³ : SecondCountableTopology α, inst✝¹ : IsLocallyFiniteMeasure μ, ρ : Measure α, A : ∀ᵐ (x : α) ∂Measure.restrict μ s, Tendsto (fun a => ↑↑μ (t ∩ a) / ↑↑μ a) (filterAt v x) (𝓝 (indicator t 1 x)), ⊢ ∀ᵐ (x : α) ∂Measure.restrict μ s, Tendsto (fun a => ↑↑μ (s ∩ a) / ↑↑μ a) (filterAt v x) (𝓝 1)  have B : ∀ᵐ x ∂μ.restrict s, t.indicator 1 x = (1 : ℝ≥0∞) := by
  refine' ae_restrict_of_ae_restrict_of_subset (subset_toMeasurable μ s) _
  filter_upwards [ae_restrict_mem (measurableSet_toMeasurable μ s)] with _ hx
  simp only [hx, Pi.one_apply, indicator_of_mem] α : Type u_1
inst✝⁵ : MetricSpace α
m0 : MeasurableSpace α
μ : Measure α
v : VitaliFamily μ
E : Type u_2
inst✝⁴ : NormedAddCommGroup E
inst✝³ : SecondCountableTopology α
inst✝² : BorelSpace α
inst✝¹ : IsLocallyFiniteMeasure μ
ρ : Measure α
inst✝ : IsLocallyFiniteMeasure ρ
s : Set α
t : Set α := toMeasurable μ s
A : ∀ᵐ (x : α) ∂Measure.restrict μ s, Tendsto (fun a => ↑↑μ (t ∩ a) / ↑↑μ a) (filterAt v x) (𝓝 (indicator t 1 x))
B :  [...]
```
After (informal):
```text
State_before: The context includes a type α with MetricSpace, MeasurableSpace, and BorelSpace structures, and a type E with a NormedAddCommGroup structure. Specific objects include a set s and its measurable cover t with respect to a measure μ on α. The conditions involve μ being a locally finite measure, a VitaliFamily v associated with μ, α having a SecondCountableTopology, another measure ρ on α, a statement A asserting that for every point x in α, within the restriction of μ to s, the ratio of the measure of the intersection of t with any set a to the measure of a tends to the indicator function of t at x, and a similar condition for s. The goal is not explicitly stated. Tactic: 'have B: ∀ x ∈ μ.restrict s, t.indicator 1 x = 1' aims to prove that for every x within the restriction of μ to s, the indicator function of t at x equals 1, using a proof strategy that involves refining the argument based on the subset relationship of s to its measurable cover t, and leveraging the measurable set property of t to filter upwards through the measurable sets, finally applying simplification to relate membership in t to the indicator function. State_after: The environment now includes all  [...]
```

**Example 4 (row 79)**

Before (formal):
```lean
inst✝² : Field K, inst✝¹ : Field L  p : ℕ+, K : Type u, L : Type v, ζ : L, k : ℕ, hcycl : IsCyclotomicExtension {p ^ succ k} K L, hirr : Irreducible (cyclotomic (↑(p ^ succ k)) K), coe_two : 2 = ↑2, hp : p = 2, hk : k = 0, hζ : IsPrimitiveRoot ζ 2 discr K ↑(IsPrimitiveRoot.powerBasis K hζ✝).basis = rw [coe_basis, powerBasis_gen] case pos
p : ℕ+
K : Type u
L : Type v
ζ : L
inst✝² : Field K
inst✝¹ : Field L
inst✝ : Algebra K L
hp✝ : Fact (Nat.Prime ↑p)
k : ℕ
hcycl : IsCyclotomicExtension {p ^ succ k} K L
hζ✝ : IsPrimitiveRoot ζ ↑(p ^ succ k)
hirr : Irreducible (cyclotomic (↑(p ^ succ k)) K)
hk✝ : ↑2 ^ (k + 1) = ↑2
coe_two : 2 = ↑2
hp : p = 2
hk : k = 0
hζ : IsPrimitiveRoot ζ 2
⊢ (discr K fun i => ζ ^ ↑i) = ↑((-1) ^ (φ ↑(p ^ succ k) / 2)) * ↑↑(p ^ (↑p ^ (succ k - 1) * ((↑p - 1) * succ k - 1)))
```
After (informal):
```text
Rewriting the hypothesis that p^(k + 1) equals 2 using natural number coercion and power function properties to directly imply p = 2.
```

**Example 5 (row 96)**

Before (formal):
```lean
γ : Type u_1, δ : Type u_2, ε : Type u_3, ζ : Type u_4, ι : Type u_5, κ : Type u_7, T : (i : ι) → TopologicalSpace (π i) s : Set ((a : ι) → π a), h2 : Set.pi (↑I) t ⊆ s α : Type u, β : Type v, π : ι → Type u_6, f : α → (i : ι) → π i, a : (a : ι) → π a, I : Finset ι, t : (i : ι) → Set (π i), h1 : ∀ (i : ι), ∃ t_1, t_1 ⊆ t i ∧ IsOpen t_1 ∧ a i ∈ t_1, ⊢ ∃ I u, (∀ (a_1 : ι), a_1 ∈ I → IsOpen (u a_1) ∧ a a_1 ∈ u a_1) ∧ Set.pi (↑I) u ⊆ s  refine ⟨I, fun a => eval a '' (I : Set ι).pi fun a => (h1 a).choose, fun i hi => ?_, ?_⟩ case refine_1.intro.intro.intro.refine_1
α : Type u
β : Type v
γ : Type u_1
δ : Type u_2
ε : Type u_3
ζ : Type u_4
ι : Type u_5
π : ι → Type u_6
κ : Type u_7
inst✝ : TopologicalSpace α
T : (i : ι) → TopologicalSpace (π i)
f : α → (i : ι) → π i
s : Set ((a : ι) → π a)
a : (a : ι) → π a
x✝ : a ∈ s
I : Finset ι
t : (i : ι) → Set (π i)
h1 : ∀ (i : ι), ∃ t_1, t_1 ⊆ t i ∧ IsOpen t_1 ∧ a i ∈ t_1
h2 : Set.pi (↑I) t ⊆ s
i : ι
hi : i ∈ I
⊢ IsOpen
      ((fun a_1 => eval a_1 '' Set.pi ↑I fun a_2 => Exists.choose (_ : ∃ t_1, t_1 ⊆ t a_2 ∧ IsOpen t_1 ∧ a a_2 ∈ t_1))
        i) ∧
    a i ∈
      (fun a_1 => eval a_1 '' Set.pi ↑I fun a_2 => Exists.choose (_ : ∃ t_1, t_1 ⊆ t a_2 ∧  [...]
```
After (informal):
```text
Simplifying the conditional expression for indices not in I to directly use univ, ensuring the condition is met.
```


## Regex-Parsed LeanDojo Proofs

Source: `AI4M/regexInformalizationData/regexInformalization.json`, 2,875 pairs, row indices [601, 1026, 1270, 2181, 2465].

**Example 1 (row 601)**

Before (formal):
```lean
apply Nat.succ_pos
```
After (informal):
```text
Here, we apply the theorem/lemma Nat.succ_pos.
```

**Example 2 (row 1026)**

Before (formal):
```lean
exact Nat.cast_ne_zero.mpr hn
```
After (informal):
```text
Here, we provide the exact term Nat.cast_ne_zero.mpr that solves our current goal.
```

**Example 3 (row 1270)**

Before (formal):
```lean
rw [log_mul_base hb (Nat.div_pos h (zero_le_one.trans_lt hb)).ne', log_div_base,
  tsub_add_cancel_of_le (succ_le_iff.2 <| log_pos hb h)]
```
After (informal):
```text
We're rewriting part of the expression using [log_mul_base.
```

**Example 4 (row 2181)**

Before (formal):
```lean
intro h
```
After (informal):
```text
We introduce new variables h.
```

**Example 5 (row 2465)**

Before (formal):
```lean
simp only [div_lt_iff, hxy, hxw, hwy, sub_pos] at ha hb ⊢
```
After (informal):
```text
We simplify the current expression or goal using the simp tactic.
```


## On-the-Fly Backtranslation

No examples: the synthetic informal text is generated inside the training loop and never saved (`src/lean4math/backtranslation/unsupervised_trainer.py` has no save or log call). Folder 003 can add a short run that dumps the generated pairs.
