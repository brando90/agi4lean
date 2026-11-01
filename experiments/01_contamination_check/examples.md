# Examples of hits (up to 6 per file; exact first, then highest containment)


## AI4M__dsir-TOP1M-AF/data/train-00000-of-00001.parquet

- ProofNet/valid item `exercise_5_15`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Suppose $a \in R^{1}, f$ is a twice-differentiable real function on $(a, \infty)$, and $M_{0}, M_{1}, M_{2}$ are the least upper bounds of $|f(x)|,\left|f^{\prime}(x)\right|,\left|f^{\prime \prime}(x)\right|$, respectively, on $(a, \infty)$. Prove t`
  - training record: `informal statement Suppose $a \in R^{1}, f$ is a twice-differentiable real function on $(a, \infty)$, and $M_{0}, M_{1}, M_{2}$ are the least upper bounds of $|f(x)|,\left|f^{\prime}(x)\right|,\left|f^{\prime \prime}(x)\right|$, respectively, on $(a, \infty)$. Prove that $M_{1}^{2} \leq 4 M_{0} M_{2} .$formal statement theorem exercise_5_15 {f : ℝ `

- ProofNet/valid item `exercise_5_15`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_5_15 {f : ℝ → ℝ} (a M0 M1 M2 : ℝ)   (hf' : differentiable_on ℝ f (set.Ici a))   (hf'' : differentiable_on ℝ (deriv f) (set.Ici a))   (hM0 : M0 = Sup {(| f x | )| x ∈ (set.Ici a)})   (hM1 : M1 = Sup {(| deriv f x | )| x ∈ (set.Ici a)}`
  - training record: `informal statement Suppose $a \in R^{1}, f$ is a twice-differentiable real function on $(a, \infty)$, and $M_{0}, M_{1}, M_{2}$ are the least upper bounds of $|f(x)|,\left|f^{\prime}(x)\right|,\left|f^{\prime \prime}(x)\right|$, respectively, on $(a, \infty)$. Prove that $M_{1}^{2} \leq 4 M_{0} M_{2} .$formal statement theorem exercise_5_15 {f : ℝ `

- ProofNet/valid item `exercise_21_8`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $X$ be a topological space and let $Y$ be a metric space. Let $f_{n}: X \rightarrow Y$ be a sequence of continuous functions. Let $x_{n}$ be a sequence of points of $X$ converging to $x$. Show that if the sequence $\left(f_{n}\right)$ converges `
  - training record: `informal statement Let $X$ be a topological space and let $Y$ be a metric space. Let $f_{n}: X \rightarrow Y$ be a sequence of continuous functions. Let $x_{n}$ be a sequence of points of $X$ converging to $x$. Show that if the sequence $\left(f_{n}\right)$ converges uniformly to $f$, then $\left(f_{n}\left(x_{n}\right)\right)$ converges to $f(x)$.`

- ProofNet/valid item `exercise_21_8`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_21_8   {X : Type*} [topological_space X] {Y : Type*} [metric_space Y]   {f : ℕ → X → Y} {x : ℕ → X}   (hf : ∀ n, continuous (f n))   (x₀ : X)   (hx : tendsto x at_top (𝓝 x₀))   (f₀ : X → Y)   (hh : tendsto_uniformly f f₀ at_top) :   `
  - training record: `informal statement Let $X$ be a topological space and let $Y$ be a metric space. Let $f_{n}: X \rightarrow Y$ be a sequence of continuous functions. Let $x_{n}$ be a sequence of points of $X$ converging to $x$. Show that if the sequence $\left(f_{n}\right)$ converges uniformly to $f$, then $\left(f_{n}\left(x_{n}\right)\right)$ converges to $f(x)$.`

- ProofNet/valid item `exercise_8_1_12`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $N$ be a positive integer. Let $M$ be an integer relatively prime to $N$ and let $d$ be an integer relatively prime to $\varphi(N)$, where $\varphi$ denotes Euler's $\varphi$-function. Prove that if $M_{1} \equiv M^{d} \pmod N$ then $M \equiv M_`
  - training record: `informal statement Let $N$ be a positive integer. Let $M$ be an integer relatively prime to $N$ and let $d$ be an integer relatively prime to $\varphi(N)$, where $\varphi$ denotes Euler's $\varphi$-function. Prove that if $M_{1} \equiv M^{d} \pmod N$ then $M \equiv M_{1}^{d^{\prime}} \pmod N$ where $d^{\prime}$ is the inverse of $d \bmod \varphi(N)`

- ProofNet/valid item `exercise_8_1_12`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_8_1_12 {N : ℕ} (hN : N > 0) {M M': ℤ} {d : ℕ}   (hMN : M.gcd N = 1) (hMd : d.gcd N.totient = 1)   (hM' : M' ≡ M^d [ZMOD N]) :   ∃ d' : ℕ, d' * d ≡ 1 [ZMOD N.totient] ∧   M ≡ M'^d' [ZMOD N] :=`
  - training record: `informal statement Let $N$ be a positive integer. Let $M$ be an integer relatively prime to $N$ and let $d$ be an integer relatively prime to $\varphi(N)$, where $\varphi$ denotes Euler's $\varphi$-function. Prove that if $M_{1} \equiv M^{d} \pmod N$ then $M \equiv M_{1}^{d^{\prime}} \pmod N$ where $d^{\prime}$ is the inverse of $d \bmod \varphi(N)`

## AI4M__gpt-4fp_minif2f_mix/train.jsonl

- ProofNet/test item `exercise_1_1b`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( Irrational x ) -> Irrational ( x * y ) :=`
  - training record: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`

- ProofNet/test item `exercise_1_1b`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`
  - training record: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`

- ProofNet/test item `exercise_1_4`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y :=`
  - training record: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`

- ProofNet/test item `exercise_1_4`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`
  - training record: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`

- ProofNet/test item `exercise_1_8`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that no order can be defined in the complex field that turns it into an ordered field.`
  - training record: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r := Prove that no order can be defined in the complex field that turns it into an ordered field.`

- ProofNet/test item `exercise_1_8`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r :=`
  - training record: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r := Prove that no order can be defined in the complex field that turns it into an ordered field.`

## AI4M__leandojo-informalized/informalized_leandojo_clean.json

- MiniF2F/valid item `mathd_numbertheory_132`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `An integer is divisible by 12 if and only if it is divisible by both 3 and 4.  Because $2+0+0+4=6$ is divisible by 3, 2004 is divisible by 3.  Also, the last two digits of 2004 form a multiple of 4, so 2004 is divisible by 4 as well. Therefore, 2004 `
  - training record: `LieSubmodule.subset_lieSpan R : Type u L : Type v M : Type w inst✝⁶ : CommRing R inst✝⁵ : LieRing L inst✝⁴ : LieAlgebra R L inst✝³ : AddCommGroup M inst✝² : Module R M inst✝¹ : LieRingModule L M inst✝ : LieModule R L M N N' : LieSubmodule R L M I J : LieIdeal R L s : Set M m : M hm : m ∈ s ⊢ m ∈ ↑(lieSpan R L s) R : Type u L : Type v M : Type w ins`

- MiniF2F/valid item `mathd_algebra_48`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `$(9-4i)- (-3-4i) = 9-4i +3 +4i = (9+3) + (-4i+4i) = 12$.`
  - training record: `List.mem_permutations_of_perm_lemma no goals α : Type uu β : Type vv l₁ l₂ is l : List α H : l ~ [] ++ is → (∃ ts' x, l = ts' ++ is) ∨ l ∈ permutationsAux is [] ⊢ l ~ is → l ∈ permutations is simpa [permutations, perm_nil] using H      The goal is to prove that for any list 'l' of type 'α' and 'is : List α', if 'l ~ is' (which means 'l' is a permut`

- MiniF2F/valid item `mathd_algebra_462`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `For any $x$ and $y$, $(x+y)(x-y)=x^2-y^2+xy-xy=x^2-y^2$, so \begin{align*} \left( \frac{1}{2} + \frac{1}{3} \right) \left( \frac{1}{2} - \frac{1}{3} \right)&=\left(\frac12\right)^2-\left(\frac13\right)^2\\ &=\frac14-\frac19\\ &=\frac{9}{36}-\frac{4}{`
  - training record: `Set.preimage_mul_const_uIcc no goals α : Type u_1 inst✝ : LinearOrderedField α a : α ha : a ≠ 0 b c : α h : a < 0 ⊢ (fun x => x * a) ⁻¹' [[b, c]] = [[b / a, c / a]] simp [← Icc_min_max, h, h.le, min_div_div_right_of_nonpos, max_div_div_right_of_nonpos] no goals α : Type u_1 inst✝ : LinearOrderedField α a : α ha✝ : a ≠ 0 b c : α ha : 0 < a ⊢ (fun x `

- MiniF2F/valid item `mathd_algebra_101`, view `informal_proof`, containment 0.963, exact=False
  - eval text: `Re-arranging, $x^2 - 5x - 14 \le 0$. The left-hand quadratic factors as $x^2 - 5x - 14 = (x - 7)(x + 2) \le 0$. Thus, $x-7$ and $x+2$ have opposite signs, so $-2 \le x \le 7$ and $x \in [-2,7]$.`
  - training record: `Set.SurjOn.congr no goals α : Type u_1 β : Type u_2 γ : Type ?u.40788 ι : Sort ?u.40791 π : α → Type ?u.40796 s s₁ s₂ : Set α t t₁ t₂ : Set β p : Set γ f f₁ f₂ f₃ : α → β g g₁ g₂ : β → γ f' f₁' f₂' : β → α g' : γ → β a : α b : β h : SurjOn f₁ s t H : EqOn f₁ f₂ s ⊢ SurjOn f₂ s t rwa [SurjOn, ← H.image_eq]  Rearranging, $x^2 - 5x - 14 \le 0$. The le`

- ProofNet/test item `exercise_1_30`, view `informal_statement`, containment 0.806, exact=False
  - eval text: ` Prove that $\frac{1}{2}+\frac{1}{3}+\cdots+\frac{1}{n}$ is not an integer.`
  - training record: `Real.not_summable_one_div_nat_cast no goals ⊢ ¬Summable fun n => 1 / ↑n simpa only [inv_eq_one_div] using Real.not_summable_nat_cast_inv      The series $\sum_{n=1}^{\infty} \frac{1}{n}$ is a well-known example of a divergent series, also known as a harmonic series. In mathematics, a series is said to be summable or convergent if the sequence of it`

- MiniF2F/valid item `mathd_algebra_101`, view `formal_lean4`, containment 0.704, exact=False
  - eval text: `theorem mathd_algebra_101   (x : ℝ)   (h₀ : x^2 - 5 * x - 4 ≤ 10) :   x ≥ -2 ∧ x ≤ 7 := sorry`
  - training record: `Finset.weightedVSub_weightedVSubVSubWeights no goals k : Type u_3 V : Type u_2 P : Type u_4 inst✝³ : Ring k inst✝² : AddCommGroup V inst✝¹ : Module k V S : AffineSpace V P ι : Type u_1 s : Finset ι ι₂ : Type ?u.453666 s₂ : Finset ι₂ inst✝ : DecidableEq ι p : ι → P i j : ι hi : i ∈ s hj : j ∈ s ⊢ ↑(weightedVSub s p) (weightedVSubVSubWeights k i j) =`

## AI4M__less-proofnet-lean4-ranked/top_p1.0.jsonl

- ProofNet/valid item `exercise_1_27`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` For all odd $n$ show that $8 \mid n^{2}-1$.`
  - training record: `informal statement For all odd $n$ show that $8 \mid n^{2}-1$.formal statement theorem exercise_1_27 {n : ℕ} (hn : odd n) : 8 ∣ (n^2 - 1) :=`

- ProofNet/valid item `exercise_1_27`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_27 {n : ℕ} (hn : Odd n) : 8 ∣ (n^2 - 1) :=`
  - training record: `informal statement For all odd $n$ show that $8 \mid n^{2}-1$.formal statement theorem exercise_1_27 {n : ℕ} (hn : odd n) : 8 ∣ (n^2 - 1) :=`

- ProofNet/valid item `exercise_29_10`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_29_10 {X : Type*}   [topological_space X] [t2_space X] (x : X)   (hx : ∃ U : set X, x ∈ U ∧ is_open U ∧ (∃ K : set X, U ⊂ K ∧ is_compact K))   (U : set X) (hU : is_open U) (hxU : x ∈ U) :   ∃ (V : set X), is_open V ∧ x ∈ V ∧ is_compa`
  - training record: `informal statement Show that if $X$ is a Hausdorff space that is locally compact at the point $x$, then for each neighborhood $U$ of $x$, there is a neighborhood $V$ of $x$ such that $\bar{V}$ is compact and $\bar{V} \subset U$.formal statement theorem exercise_29_10 {X : Type*}   [topological_space X] [t2_space X] (x : X)   (hx : ∃ U : set X, x ∈ `

- ProofNet/valid item `exercise_29_10`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Show that if $X$ is a Hausdorff space that is locally compact at the point $x$, then for each neighborhood $U$ of $x$, there is a neighborhood $V$ of $x$ such that $\bar{V}$ is compact and $\bar{V} \subset U$.`
  - training record: `informal statement Show that if $X$ is a Hausdorff space that is locally compact at the point $x$, then for each neighborhood $U$ of $x$, there is a neighborhood $V$ of $x$ such that $\bar{V}$ is compact and $\bar{V} \subset U$.formal statement theorem exercise_29_10 {X : Type*}   [topological_space X] [t2_space X] (x : X)   (hx : ∃ U : set X, x ∈ `

- ProofNet/valid item `exercise_2018_b2`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $n$ be a positive integer, and let $f_{n}(z)=n+(n-1) z+$ $(n-2) z^{2}+\cdots+z^{n-1}$. Prove that $f_{n}$ has no roots in the closed unit disk $\{z \in \mathbb{C}:|z| \leq 1\}$.`
  - training record: `informal statement Let $n$ be a positive integer, and let $f_{n}(z)=n+(n-1) z+$ $(n-2) z^{2}+\cdots+z^{n-1}$. Prove that $f_{n}$ has no roots in the closed unit disk $\{z \in \mathbb{C}:|z| \leq 1\}$.formal statement theorem exercise_2018_b2 (n : ℕ) (hn : n > 0) (f : ℕ → ℂ → ℂ)    (hf : ∀ n : ℕ, f n = λ z, (∑ (i : fin n), (n-i)* z^(i : ℕ))) :    ¬ `

- ProofNet/valid item `exercise_2018_b2`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_2018_b2 (n : ℕ) (hn : n > 0) (f : ℕ → ℂ → ℂ)    (hf : ∀ n : ℕ, f n = λ z, (∑ (i : fin n), (n-i)* z^(i : ℕ))) :    ¬ (∃ z : ℂ, ‖z‖ ≤ 1 ∧ f n z = 0) :=`
  - training record: `informal statement Let $n$ be a positive integer, and let $f_{n}(z)=n+(n-1) z+$ $(n-2) z^{2}+\cdots+z^{n-1}$. Prove that $f_{n}$ has no roots in the closed unit disk $\{z \in \mathbb{C}:|z| \leq 1\}$.formal statement theorem exercise_2018_b2 (n : ℕ) (hn : n > 0) (f : ℕ → ℂ → ℂ)    (hf : ∀ n : ℕ, f n = λ z, (∑ (i : fin n), (n-i)* z^(i : ℕ))) :    ¬ `

## AI4M__less-proofnet-lean4-top1M/top_p0.0059.jsonl

- ProofNet/valid item `exercise_1_27`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` For all odd $n$ show that $8 \mid n^{2}-1$.`
  - training record: `informal statement For all odd $n$ show that $8 \mid n^{2}-1$.formal statement theorem exercise_1_27 {n : ℕ} (hn : odd n) : 8 ∣ (n^2 - 1) :=`

- ProofNet/valid item `exercise_1_27`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_27 {n : ℕ} (hn : Odd n) : 8 ∣ (n^2 - 1) :=`
  - training record: `informal statement For all odd $n$ show that $8 \mid n^{2}-1$.formal statement theorem exercise_1_27 {n : ℕ} (hn : odd n) : 8 ∣ (n^2 - 1) :=`

- ProofNet/valid item `exercise_29_10`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_29_10 {X : Type*}   [topological_space X] [t2_space X] (x : X)   (hx : ∃ U : set X, x ∈ U ∧ is_open U ∧ (∃ K : set X, U ⊂ K ∧ is_compact K))   (U : set X) (hU : is_open U) (hxU : x ∈ U) :   ∃ (V : set X), is_open V ∧ x ∈ V ∧ is_compa`
  - training record: `informal statement Show that if $X$ is a Hausdorff space that is locally compact at the point $x$, then for each neighborhood $U$ of $x$, there is a neighborhood $V$ of $x$ such that $\bar{V}$ is compact and $\bar{V} \subset U$.formal statement theorem exercise_29_10 {X : Type*}   [topological_space X] [t2_space X] (x : X)   (hx : ∃ U : set X, x ∈ `

- ProofNet/valid item `exercise_29_10`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Show that if $X$ is a Hausdorff space that is locally compact at the point $x$, then for each neighborhood $U$ of $x$, there is a neighborhood $V$ of $x$ such that $\bar{V}$ is compact and $\bar{V} \subset U$.`
  - training record: `informal statement Show that if $X$ is a Hausdorff space that is locally compact at the point $x$, then for each neighborhood $U$ of $x$, there is a neighborhood $V$ of $x$ such that $\bar{V}$ is compact and $\bar{V} \subset U$.formal statement theorem exercise_29_10 {X : Type*}   [topological_space X] [t2_space X] (x : X)   (hx : ∃ U : set X, x ∈ `

- ProofNet/valid item `exercise_2018_b2`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $n$ be a positive integer, and let $f_{n}(z)=n+(n-1) z+$ $(n-2) z^{2}+\cdots+z^{n-1}$. Prove that $f_{n}$ has no roots in the closed unit disk $\{z \in \mathbb{C}:|z| \leq 1\}$.`
  - training record: `informal statement Let $n$ be a positive integer, and let $f_{n}(z)=n+(n-1) z+$ $(n-2) z^{2}+\cdots+z^{n-1}$. Prove that $f_{n}$ has no roots in the closed unit disk $\{z \in \mathbb{C}:|z| \leq 1\}$.formal statement theorem exercise_2018_b2 (n : ℕ) (hn : n > 0) (f : ℕ → ℂ → ℂ)    (hf : ∀ n : ℕ, f n = λ z, (∑ (i : fin n), (n-i)* z^(i : ℕ))) :    ¬ `

- ProofNet/valid item `exercise_2018_b2`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_2018_b2 (n : ℕ) (hn : n > 0) (f : ℕ → ℂ → ℂ)    (hf : ∀ n : ℕ, f n = λ z, (∑ (i : fin n), (n-i)* z^(i : ℕ))) :    ¬ (∃ z : ℂ, ‖z‖ ≤ 1 ∧ f n z = 0) :=`
  - training record: `informal statement Let $n$ be a positive integer, and let $f_{n}(z)=n+(n-1) z+$ $(n-2) z^{2}+\cdots+z^{n-1}$. Prove that $f_{n}$ has no roots in the closed unit disk $\{z \in \mathbb{C}:|z| \leq 1\}$.formal statement theorem exercise_2018_b2 (n : ℕ) (hn : n > 0) (f : ℕ → ℂ → ℂ)    (hf : ∀ n : ℕ, f n = λ z, (∑ (i : fin n), (n-i)* z^(i : ℕ))) :    ¬ `

## AI4M__math-select-less-llama8b/top_p1.0.jsonl

- ProofNet/valid item `exercise_7_3_37`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}      First we prove a lemma.  Lemma: Let $R$ be a ring, and let $I_1, I_2, J \subseteq R$ be ideals such that $J \subseteq I_1, I_2$. Then $\left(I_1 / J\right)\left(I_2 / J\right)=I_1 I_2 / J$.  Proof: ( $\subseteq$ ) Let  $$  \alpha=\`
  - training record: `Problem: An ideal $N$ is called nilpotent if $N^{n}$ is the zero ideal for some $n \geq 1$. Prove that the ideal $p \mathbb{Z} / p^{m} \mathbb{Z}$ is a nilpotent ideal in the ring $\mathbb{Z} / p^{m} \mathbb{Z}$.  Solution: \begin{proof}      First we prove a lemma.  Lemma: Let $R$ be a ring, and let $I_1, I_2, J \subseteq R$ be ideals such that $J`

- ProofNet/valid item `exercise_7_3_37`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` An ideal $N$ is called nilpotent if $N^{n}$ is the zero ideal for some $n \geq 1$. Prove that the ideal $p \mathbb{Z} / p^{m} \mathbb{Z}$ is a nilpotent ideal in the ring $\mathbb{Z} / p^{m} \mathbb{Z}$.`
  - training record: `Problem: An ideal $N$ is called nilpotent if $N^{n}$ is the zero ideal for some $n \geq 1$. Prove that the ideal $p \mathbb{Z} / p^{m} \mathbb{Z}$ is a nilpotent ideal in the ring $\mathbb{Z} / p^{m} \mathbb{Z}$.  Solution: \begin{proof}      First we prove a lemma.  Lemma: Let $R$ be a ring, and let $I_1, I_2, J \subseteq R$ be ideals such that $J`

- ProofNet/valid item `exercise_1_19`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}      Since the solution is given to us, all we have to do is verify it, i.e., we need to show that the equation  $$  |\mathrm{x}-\mathrm{a}|=2|\mathrm{x}-\mathrm{b}|  $$  is equivalent to $|\mathrm{x}-\mathbf{c}|=r$, which says  $$  \le`
  - training record: `Problem: Suppose $a, b \in R^k$. Find $c \in R^k$ and $r > 0$ such that $|x-a|=2|x-b|$ if and only if $| x - c | = r$. Prove that $3c = 4b - a$ and $3r = 2 |b - a|$.  Solution: \begin{proof}      Since the solution is given to us, all we have to do is verify it, i.e., we need to show that the equation  $$  |\mathrm{x}-\mathrm{a}|=2|\mathrm{x}-\math`

- ProofNet/valid item `exercise_1_19`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Suppose $a, b \in R^k$. Find $c \in R^k$ and $r > 0$ such that $|x-a|=2|x-b|$ if and only if $| x - c | = r$. Prove that $3c = 4b - a$ and $3r = 2 |b - a|$.`
  - training record: `Problem: Suppose $a, b \in R^k$. Find $c \in R^k$ and $r > 0$ such that $|x-a|=2|x-b|$ if and only if $| x - c | = r$. Prove that $3c = 4b - a$ and $3r = 2 |b - a|$.  Solution: \begin{proof}      Since the solution is given to us, all we have to do is verify it, i.e., we need to show that the equation  $$  |\mathrm{x}-\mathrm{a}|=2|\mathrm{x}-\math`

- ProofNet/valid item `exercise_1_5`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}      We need to prove that $-\sup (-A)$ is the greatest lower bound of $A$. For brevity, let $\alpha=-\sup (-A)$. We need to show that $\alpha \leq x$ for all $x \in A$ and $\alpha \geq \beta$ if $\beta$ is any lower bound of $A$.    Su`
  - training record: `Problem: Let $A$ be a nonempty set of real numbers which is bounded below. Let $-A$ be the set of all numbers $-x$, where $x \in A$. Prove that $\inf A=-\sup (-A)$.  Solution: \begin{proof}      We need to prove that $-\sup (-A)$ is the greatest lower bound of $A$. For brevity, let $\alpha=-\sup (-A)$. We need to show that $\alpha \leq x$ for all $`

- ProofNet/valid item `exercise_1_5`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $A$ be a nonempty set of real numbers which is bounded below. Let $-A$ be the set of all numbers $-x$, where $x \in A$. Prove that $\inf A=-\sup (-A)$.`
  - training record: `Problem: Let $A$ be a nonempty set of real numbers which is bounded below. Let $-A$ be the set of all numbers $-x$, where $x \in A$. Prove that $\inf A=-\sup (-A)$.  Solution: \begin{proof}      We need to prove that $-\sup (-A)$ is the greatest lower bound of $A$. For brevity, let $\alpha=-\sup (-A)$. We need to show that $\alpha \leq x$ for all $`

## AI4M__michael-af/test.jsonl

- ProofNet/test item `exercise_1_1b`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( Irrational x ) -> Irrational ( x * y ) :=`
  - training record: `If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational. theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) :=`

- ProofNet/test item `exercise_1_1b`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`
  - training record: `If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational. theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) :=`

- ProofNet/test item `exercise_1_4`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y :=`
  - training record: `Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$. theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y :=`

- ProofNet/test item `exercise_1_4`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`
  - training record: `Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$. theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y :=`

- ProofNet/test item `exercise_1_8`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that no order can be defined in the complex field that turns it into an ordered field.`
  - training record: `Prove that no order can be defined in the complex field that turns it into an ordered field. theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r :=`

- ProofNet/test item `exercise_1_8`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r :=`
  - training record: `Prove that no order can be defined in the complex field that turns it into an ordered field. theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r :=`

## AI4M__michael-af/valid.jsonl

- ProofNet/valid item `exercise_1_1a`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $r+x$ is irrational.`
  - training record: `If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $r+x$ is irrational. theorem exercise_1_1a   (x : ℝ) (y : ℚ) :   ( irrational x ) -> irrational ( x + y ) :=`

- ProofNet/valid item `exercise_1_1a`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_1a   (x : ℝ) (y : ℚ) :   ( Irrational x ) -> Irrational ( x + y ) :=`
  - training record: `If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $r+x$ is irrational. theorem exercise_1_1a   (x : ℝ) (y : ℚ) :   ( irrational x ) -> irrational ( x + y ) :=`

- ProofNet/valid item `exercise_1_2`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that there is no rational number whose square is $12$.`
  - training record: `Prove that there is no rational number whose square is $12$. theorem exercise_1_2 : ¬ ∃ (x : ℚ), ( x ^ 2 = 12 ) :=`

- ProofNet/valid item `exercise_1_2`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_2 : ¬ ∃ (x : ℚ), ( x ^ 2 = 12 ) :=`
  - training record: `Prove that there is no rational number whose square is $12$. theorem exercise_1_2 : ¬ ∃ (x : ℚ), ( x ^ 2 = 12 ) :=`

- ProofNet/valid item `exercise_1_5`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_5 (A minus_A : set ℝ) (hA : A.nonempty)    (hA_bdd_below : bdd_below A) (hminus_A : minus_A = {x | -x ∈ A}) :   Inf A = Sup minus_A :=`
  - training record: `Let $A$ be a nonempty set of real numbers which is bounded below. Let $-A$ be the set of all numbers $-x$, where $x \in A$. Prove that $\inf A=-\sup (-A)$. theorem exercise_1_5 (A minus_A : set ℝ) (hA : A.nonempty)    (hA_bdd_below : bdd_below A) (hminus_A : minus_A = {x | -x ∈ A}) :   Inf A = Sup minus_A :=`

- ProofNet/valid item `exercise_1_5`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $A$ be a nonempty set of real numbers which is bounded below. Let $-A$ be the set of all numbers $-x$, where $x \in A$. Prove that $\inf A=-\sup (-A)$.`
  - training record: `Let $A$ be a nonempty set of real numbers which is bounded below. Let $-A$ be the set of all numbers $-x$, where $x \in A$. Prove that $\inf A=-\sup (-A)$. theorem exercise_1_5 (A minus_A : set ℝ) (hA : A.nonempty)    (hA_bdd_below : bdd_below A) (hminus_A : minus_A = {x | -x ∈ A}) :   Inf A = Sup minus_A :=`

## AI4M__miniF2FInformalizations/miniF2FInformalization.jsonl

- ProofNet/test item `exercise_1_1b`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( Irrational x ) -> Irrational ( x * y ) :=`
  - training record: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`

- ProofNet/test item `exercise_1_1b`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`
  - training record: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`

- ProofNet/test item `exercise_1_4`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y :=`
  - training record: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`

- ProofNet/test item `exercise_1_4`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`
  - training record: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`

- ProofNet/test item `exercise_1_8`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that no order can be defined in the complex field that turns it into an ordered field.`
  - training record: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r := Prove that no order can be defined in the complex field that turns it into an ordered field.`

- ProofNet/test item `exercise_1_8`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r :=`
  - training record: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r := Prove that no order can be defined in the complex field that turns it into an ordered field.`

## AI4M__minif2f_dataset/minif2fdata.jsonl

- ProofNet/test item `exercise_1_1b`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( Irrational x ) -> Irrational ( x * y ) :=`
  - training record: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`

- ProofNet/test item `exercise_1_1b`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`
  - training record: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`

- ProofNet/test item `exercise_1_4`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y :=`
  - training record: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`

- ProofNet/test item `exercise_1_4`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`
  - training record: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`

- ProofNet/test item `exercise_1_8`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that no order can be defined in the complex field that turns it into an ordered field.`
  - training record: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r := Prove that no order can be defined in the complex field that turns it into an ordered field.`

- ProofNet/test item `exercise_1_8`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r :=`
  - training record: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r := Prove that no order can be defined in the complex field that turns it into an ordered field.`

## AI4M__minif2f_dataset/test.jsonl

- ProofNet/test item `exercise_1_1b`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}      If $r x$ were rational, then $x=\frac{r x}{r}$ would also be rational.  \end{proof}`
  - training record: `Rudin|exercise_1_1b theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := import .common  open real complex open topological_space open filter open_locale real  open_locale topology open_locale big_operators open_locale complex_conjugate open_locale filter   noncomputable theory   If $r$ is rational $(r \ne`

- ProofNet/test item `exercise_1_1b`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( Irrational x ) -> Irrational ( x * y ) :=`
  - training record: `Rudin|exercise_1_1b theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := import .common  open real complex open topological_space open filter open_locale real  open_locale topology open_locale big_operators open_locale complex_conjugate open_locale filter   noncomputable theory   If $r$ is rational $(r \ne`

- ProofNet/test item `exercise_1_1b`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`
  - training record: `Rudin|exercise_1_1b theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := import .common  open real complex open topological_space open filter open_locale real  open_locale topology open_locale big_operators open_locale complex_conjugate open_locale filter   noncomputable theory   If $r$ is rational $(r \ne`

- ProofNet/test item `exercise_1_4`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}  Since $E$ is nonempty, there exists $x \in E$. Then by definition of lower and upper bounds we have $\alpha \leq x \leq \beta$, and hence by property $i i$ in the definition of an ordering, we have $\alpha<\beta$ unless $\alpha=x=\beta`
  - training record: `Rudin|exercise_1_4 theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := import .common  open real complex open topological_space open filter open_locale real  open_locale topology open_locale big_operators open_locale complex_conjugate open_loca`

- ProofNet/test item `exercise_1_4`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y :=`
  - training record: `Rudin|exercise_1_4 theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := import .common  open real complex open topological_space open filter open_locale real  open_locale topology open_locale big_operators open_locale complex_conjugate open_loca`

- ProofNet/test item `exercise_1_4`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`
  - training record: `Rudin|exercise_1_4 theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := import .common  open real complex open topological_space open filter open_locale real  open_locale topology open_locale big_operators open_locale complex_conjugate open_loca`

## AI4M__minif2f_real/paired_formal_informal_statements.json

- MiniF2F/valid item `amc12a_2019_21`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem amc12a_2019_p21   (z : ℂ)   (h₀ : z = (1 + Complex.I) / Real.sqrt 2) :   (∑ k in Finset.Icc 1 12, (z^(k^2))) * (∑ k in Finset.Icc 1 12, (1 / z^(k^2))) = 36 := sorry`
  - training record: `theorem amc12a_2019_p21   (z : ℂ)   (h₀ : z = (1 + Complex.I) / Real.sqrt 2) :   (∑ k in Finset.Icc 1 12, (z^(k^2))) * (∑ k in Finset.Icc 1 12, (1 / z^(k^2))) = 36 := sorry Let $z=\frac{1+i}{\sqrt{2}}.$What is $\left(z^{1^2}+z^{2^2}+z^{3^2}+\dots+z^{{12}^2}\right) \cdot \left(\frac{1}{z^{1^2}}+\frac{1}{z^{2^2}}+\frac{1}{z^{3^2}}+\dots+\frac{1}{z^{{`

- MiniF2F/valid item `amc12a_2019_21`, view `informal_statement`, containment 1.0, exact=True
  - eval text: `Let $z=\frac{1+i}{\sqrt{2}}.$What is $\left(z^{1^2}+z^{2^2}+z^{3^2}+\dots+z^{{12}^2}\right) \cdot \left(\frac{1}{z^{1^2}}+\frac{1}{z^{2^2}}+\frac{1}{z^{3^2}}+\dots+\frac{1}{z^{{12}^2}}\right)?$  $\textbf{(A) } 18 \qquad \textbf{(B) } 72-36\sqrt2 \qqu`
  - training record: `theorem amc12a_2019_p21   (z : ℂ)   (h₀ : z = (1 + Complex.I) / Real.sqrt 2) :   (∑ k in Finset.Icc 1 12, (z^(k^2))) * (∑ k in Finset.Icc 1 12, (1 / z^(k^2))) = 36 := sorry Let $z=\frac{1+i}{\sqrt{2}}.$What is $\left(z^{1^2}+z^{2^2}+z^{3^2}+\dots+z^{{12}^2}\right) \cdot \left(\frac{1}{z^{1^2}}+\frac{1}{z^{2^2}}+\frac{1}{z^{3^2}}+\dots+\frac{1}{z^{{`

- MiniF2F/valid item `amc12a_2015_10`, view `informal_statement`, containment 1.0, exact=True
  - eval text: `Integers $x$ and $y$ with $x>y>0$ satisfy $x+y+xy=80$. What is $x$?  $ \textbf{(A)}\ 8 \qquad\textbf{(B)}\ 10 \qquad\textbf{(C)}\ 15 \qquad\textbf{(D)}\ 18 \qquad\textbf{(E)}\ 26$ Show that it is \textbf{(E)}\ 26.`
  - training record: `theorem amc12a_2015_p10   (x y : ℤ)   (h₀ : 0 < y)   (h₁ : y < x)   (h₂ : x + y + (x * y) = 80) :   x = 26 := sorry Integers $x$ and $y$ with $x>y>0$ satisfy $x+y+xy=80$. What is $x$?  $ \textbf{(A)}\ 8 \qquad\textbf{(B)}\ 10 \qquad\textbf{(C)}\ 15 \qquad\textbf{(D)}\ 18 \qquad\textbf{(E)}\ 26$ Show that it is \textbf{(E)}\ 26.`

- MiniF2F/valid item `amc12a_2015_10`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem amc12a_2015_p10   (x y : ℤ)   (h₀ : 0 < y)   (h₁ : y < x)   (h₂ : x + y + (x * y) = 80) :   x = 26 := sorry`
  - training record: `theorem amc12a_2015_p10   (x y : ℤ)   (h₀ : 0 < y)   (h₁ : y < x)   (h₂ : x + y + (x * y) = 80) :   x = 26 := sorry Integers $x$ and $y$ with $x>y>0$ satisfy $x+y+xy=80$. What is $x$?  $ \textbf{(A)}\ 8 \qquad\textbf{(B)}\ 10 \qquad\textbf{(C)}\ 15 \qquad\textbf{(D)}\ 18 \qquad\textbf{(E)}\ 26$ Show that it is \textbf{(E)}\ 26.`

- MiniF2F/valid item `amc12a_2008_8`, view `informal_statement`, containment 1.0, exact=True
  - eval text: `What is the [[volume]] of a [[cube]] whose [[surface area]] is twice that of a cube with volume 1?   $\mathrm{(A)}\ \sqrt{2}\qquad\mathrm{(B)}\ 2\qquad\mathrm{(C)}\ 2\sqrt{2}\qquad\mathrm{(D)}\ 4\qquad\mathrm{(E)}\ 8$ Show that it is \mathrm{(C)}.`
  - training record: `theorem amc12a_2008_p8   (x y : ℝ)   (h₀ : 0 < x ∧ 0 < y)   (h₁ : y^3 = 1)   (h₂ : 6 * x^2 = 2 * (6 * y^2)) :   x^3 = 2 * Real.sqrt 2 := sorry What is the [[volume]] of a [[cube]] whose [[surface area]] is twice that of a cube with volume 1?   $\mathrm{(A)}\ \sqrt{2}\qquad\mathrm{(B)}\ 2\qquad\mathrm{(C)}\ 2\sqrt{2}\qquad\mathrm{(D)}\ 4\qquad\mathr`

- MiniF2F/valid item `amc12a_2008_8`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem amc12a_2008_p8   (x y : ℝ)   (h₀ : 0 < x ∧ 0 < y)   (h₁ : y^3 = 1)   (h₂ : 6 * x^2 = 2 * (6 * y^2)) :   x^3 = 2 * Real.sqrt 2 := sorry`
  - training record: `theorem amc12a_2008_p8   (x y : ℝ)   (h₀ : 0 < x ∧ 0 < y)   (h₁ : y^3 = 1)   (h₂ : 6 * x^2 = 2 * (6 * y^2)) :   x^3 = 2 * Real.sqrt 2 := sorry What is the [[volume]] of a [[cube]] whose [[surface area]] is twice that of a cube with volume 1?   $\mathrm{(A)}\ \sqrt{2}\qquad\mathrm{(B)}\ 2\qquad\mathrm{(C)}\ 2\sqrt{2}\qquad\mathrm{(D)}\ 4\qquad\mathr`

## AI4M__willy_mix_1/train.json

- ProofNet/test item `exercise_1_1b`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( Irrational x ) -> Irrational ( x * y ) :=`
  - training record: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`

- ProofNet/test item `exercise_1_1b`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`
  - training record: `theorem exercise_1_1b (x : ℝ) (y : ℚ) (h : y ≠ 0) : ( irrational x ) -> irrational ( x * y ) := If $r$ is rational $(r \neq 0)$ and $x$ is irrational, prove that $rx$ is irrational.`

- ProofNet/test item `exercise_1_4`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y :=`
  - training record: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`

- ProofNet/test item `exercise_1_4`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`
  - training record: `theorem exercise_1_4 (α : Type*) [partial_order α] (s : set α) (x y : α) (h₀ : set.nonempty s) (h₁ : x ∈ lower_bounds s) (h₂ : y ∈ upper_bounds s) : x ≤ y := Let $E$ be a nonempty subset of an ordered set; suppose $\alpha$ is a lower bound of $E$ and $\beta$ is an upper bound of $E$. Prove that $\alpha \leq \beta$.`

- ProofNet/test item `exercise_1_8`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that no order can be defined in the complex field that turns it into an ordered field.`
  - training record: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r := Prove that no order can be defined in the complex field that turns it into an ordered field.`

- ProofNet/test item `exercise_1_8`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r :=`
  - training record: `theorem exercise_1_8 : ¬ ∃ (r : ℂ → ℂ → Prop), is_linear_order ℂ r := Prove that no order can be defined in the complex field that turns it into an ordered field.`

## AI4M__zipfit-AF-TOP1M/data/train-00000-of-00001.parquet

- ProofNet/valid item `exercise_4_5_22`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that if $|G|=132$ then $G$ is not simple.`
  - training record: `informal statement Prove that if $|G|=132$ then $G$ is not simple.formal statement theorem exercise_4_5_22 {G : Type*} [fintype G] [group G]   (hG : card G = 132) : ¬ is_simple_group G :=`

- ProofNet/valid item `exercise_4_5_22`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_4_5_22 {G : Type*} [fintype G] [group G]   (hG : card G = 132) : ¬ is_simple_group G :=`
  - training record: `informal statement Prove that if $|G|=132$ then $G$ is not simple.formal statement theorem exercise_4_5_22 {G : Type*} [fintype G] [group G]   (hG : card G = 132) : ¬ is_simple_group G :=`

- ProofNet/valid item `exercise_4_5_14`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that a group of order 312 has a normal Sylow $p$-subgroup for some prime $p$ dividing its order.`
  - training record: `informal statement Prove that a group of order 312 has a normal Sylow $p$-subgroup for some prime $p$ dividing its order.formal statement theorem exercise_4_5_14 {G : Type*} [group G] [fintype G]   (hG : card G = 312) :   ∃ (p : ℕ) (P : sylow p G), P.normal :=`

- ProofNet/valid item `exercise_4_5_14`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_4_5_14 {G : Type*} [Group G] [Fintype G]   (hG : card G = 312) :   ∃ (p : ℕ) (P : Sylow p G), P.Normal :=`
  - training record: `informal statement Prove that a group of order 312 has a normal Sylow $p$-subgroup for some prime $p$ dividing its order.formal statement theorem exercise_4_5_14 {G : Type*} [group G] [fintype G]   (hG : card G = 312) :   ∃ (p : ℕ) (P : sylow p G), P.normal :=`

- ProofNet/valid item `exercise_4_5_18`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_4_5_18 {G : Type*} [Fintype G] [Group G]   (hG : card G = 200) :   ∃ N : Sylow 5 G, N.Normal :=`
  - training record: `informal statement Prove that a group of order 200 has a normal Sylow 5-subgroup.formal statement theorem exercise_4_5_18 {G : Type*} [fintype G] [group G]    (hG : card G = 200) :    ∃ N : sylow 5 G, N.normal :=`

- ProofNet/valid item `exercise_4_5_18`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that a group of order 200 has a normal Sylow 5-subgroup.`
  - training record: `informal statement Prove that a group of order 200 has a normal Sylow 5-subgroup.formal statement theorem exercise_4_5_18 {G : Type*} [fintype G] [group G]    (hG : card G = 200) :    ∃ N : sylow 5 G, N.normal :=`

## AI4M__zipfit-TOP1M-AF/data/train-00000-of-00001.parquet

- ProofNet/valid item `exercise_4_5_22`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that if $|G|=132$ then $G$ is not simple.`
  - training record: `informal statement Prove that if $|G|=132$ then $G$ is not simple.formal statement theorem exercise_4_5_22 {G : Type*} [fintype G] [group G]   (hG : card G = 132) : ¬ is_simple_group G :=`

- ProofNet/valid item `exercise_4_5_22`, view `formal_lean3`, containment 1.0, exact=True
  - eval text: `theorem exercise_4_5_22 {G : Type*} [fintype G] [group G]   (hG : card G = 132) : ¬ is_simple_group G :=`
  - training record: `informal statement Prove that if $|G|=132$ then $G$ is not simple.formal statement theorem exercise_4_5_22 {G : Type*} [fintype G] [group G]   (hG : card G = 132) : ¬ is_simple_group G :=`

- ProofNet/valid item `exercise_4_5_14`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that a group of order 312 has a normal Sylow $p$-subgroup for some prime $p$ dividing its order.`
  - training record: `informal statement Prove that a group of order 312 has a normal Sylow $p$-subgroup for some prime $p$ dividing its order.formal statement theorem exercise_4_5_14 {G : Type*} [group G] [fintype G]   (hG : card G = 312) :   ∃ (p : ℕ) (P : sylow p G), P.normal :=`

- ProofNet/valid item `exercise_4_5_14`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_4_5_14 {G : Type*} [Group G] [Fintype G]   (hG : card G = 312) :   ∃ (p : ℕ) (P : Sylow p G), P.Normal :=`
  - training record: `informal statement Prove that a group of order 312 has a normal Sylow $p$-subgroup for some prime $p$ dividing its order.formal statement theorem exercise_4_5_14 {G : Type*} [group G] [fintype G]   (hG : card G = 312) :   ∃ (p : ℕ) (P : sylow p G), P.normal :=`

- ProofNet/valid item `exercise_4_5_18`, view `formal_lean4`, containment 1.0, exact=True
  - eval text: `theorem exercise_4_5_18 {G : Type*} [Fintype G] [Group G]   (hG : card G = 200) :   ∃ N : Sylow 5 G, N.Normal :=`
  - training record: `informal statement Prove that a group of order 200 has a normal Sylow 5-subgroup.formal statement theorem exercise_4_5_18 {G : Type*} [fintype G] [group G]    (hG : card G = 200) :    ∃ N : sylow 5 G, N.normal :=`

- ProofNet/valid item `exercise_4_5_18`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that a group of order 200 has a normal Sylow 5-subgroup.`
  - training record: `informal statement Prove that a group of order 200 has a normal Sylow 5-subgroup.formal statement theorem exercise_4_5_18 {G : Type*} [fintype G] [group G]    (hG : card G = 200) :    ∃ N : sylow 5 G, N.normal :=`

## UDACA__Code-Mixed-Dataset/combined_dataset.jsonl

- ProofNet/test item `exercise_5_17`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Suppose $f$ is a real, three times differentiable function on $[-1,1]$, such that $f(-1)=0, \quad f(0)=0, \quad f(1)=1, \quad f^{\prime}(0)=0 .$ Prove that $f^{(3)}(x) \geq 3$ for some $x \in(-1,1)$.`
  - training record: `theory Rudin   imports Complex_Main (* comment by Angeliki: switched to Complex_Main and imported some Analysis*) "HOL-Analysis.Abstract_Euclidean_Space" "HOL-Analysis.Derivative" "HOL-Analysis.Interval_Integral" "HOL-Analysis.Elementary_Topology" (*"HOL-Hahn_Banach.Function_Order"*) begin  (* problem_number:1_1a natural language statement: If $r$ `

- ProofNet/test item `exercise_3_7`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that the convergence of $\Sigma a_{n}$ implies the convergence of $\sum \frac{\sqrt{a_{n}}}{n}$ if $a_n\geq 0$.`
  - training record: `theory Rudin   imports Complex_Main (* comment by Angeliki: switched to Complex_Main and imported some Analysis*) "HOL-Analysis.Abstract_Euclidean_Space" "HOL-Analysis.Derivative" "HOL-Analysis.Interval_Integral" "HOL-Analysis.Elementary_Topology" (*"HOL-Hahn_Banach.Function_Order"*) begin  (* problem_number:1_1a natural language statement: If $r$ `

- ProofNet/test item `exercise_3_5`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` For any two real sequences $\left\{a_{n}\right\},\left\{b_{n}\right\}$, prove that $\limsup _{n \rightarrow \infty}\left(a_{n}+b_{n}\right) \leq \limsup _{n \rightarrow \infty} a_{n}+\limsup _{n \rightarrow \infty} b_{n},$ provided the sum on the ri`
  - training record: `theory Rudin   imports Complex_Main (* comment by Angeliki: switched to Complex_Main and imported some Analysis*) "HOL-Analysis.Abstract_Euclidean_Space" "HOL-Analysis.Derivative" "HOL-Analysis.Interval_Integral" "HOL-Analysis.Elementary_Topology" (*"HOL-Hahn_Banach.Function_Order"*) begin  (* problem_number:1_1a natural language statement: If $r$ `

- ProofNet/valid item `exercise_3_1a`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Prove that convergence of $\left\{s_{n}\right\}$ implies convergence of $\left\{\left|s_{n}\right|\right\}$.`
  - training record: `theory Rudin   imports Complex_Main (* comment by Angeliki: switched to Complex_Main and imported some Analysis*) "HOL-Analysis.Abstract_Euclidean_Space" "HOL-Analysis.Derivative" "HOL-Analysis.Interval_Integral" "HOL-Analysis.Elementary_Topology" (*"HOL-Hahn_Banach.Function_Order"*) begin  (* problem_number:1_1a natural language statement: If $r$ `

- ProofNet/valid item `exercise_3_8`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $\Sigma a_{n}$ converges, and if $\left\{b_{n}\right\}$ is monotonic and bounded, prove that $\Sigma a_{n} b_{n}$ converges.`
  - training record: `theory Rudin   imports Complex_Main (* comment by Angeliki: switched to Complex_Main and imported some Analysis*) "HOL-Analysis.Abstract_Euclidean_Space" "HOL-Analysis.Derivative" "HOL-Analysis.Interval_Integral" "HOL-Analysis.Elementary_Topology" (*"HOL-Hahn_Banach.Function_Order"*) begin  (* problem_number:1_1a natural language statement: If $r$ `

- ProofNet/valid item `exercise_1_18a`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $k \geq 2$ and $\mathbf{x} \in R^{k}$, prove that there exists $\mathbf{y} \in R^{k}$ such that $\mathbf{y} \neq 0$ but $\mathbf{x} \cdot \mathbf{y}=0$`
  - training record: `theory Rudin   imports Complex_Main (* comment by Angeliki: switched to Complex_Main and imported some Analysis*) "HOL-Analysis.Abstract_Euclidean_Space" "HOL-Analysis.Derivative" "HOL-Analysis.Interval_Integral" "HOL-Analysis.Elementary_Topology" (*"HOL-Hahn_Banach.Function_Order"*) begin  (* problem_number:1_1a natural language statement: If $r$ `

## UDACA__DSIR-train/data/train-00000-of-00001.parquet

- ProofNet/valid item `exercise_2_2_5`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $G$ be a group in which $(a b)^{3}=a^{3} b^{3}$ and $(a b)^{5}=a^{5} b^{5}$ for all $a, b \in G$. Show that $G$ is abelian.`
  - training record: `Problem: Let $G$ be a group in which $(a b)^{3}=a^{3} b^{3}$ and $(a b)^{5}=a^{5} b^{5}$ for all $a, b \in G$. Show that $G$ is abelian.  Solution: \begin{proof}   We have  $$  \begin{aligned}  & (a b)^3=a^3 b^3, \text { for all } a, b \in G \\  \Longrightarrow & (a b)(a b)(a b)=a\left(a^2 b^2\right) b \\  \Longrightarrow & a(b a)(b a) b=a\left(a^2`

- ProofNet/valid item `exercise_2_2_5`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}   We have  $$  \begin{aligned}  & (a b)^3=a^3 b^3, \text { for all } a, b \in G \\  \Longrightarrow & (a b)(a b)(a b)=a\left(a^2 b^2\right) b \\  \Longrightarrow & a(b a)(b a) b=a\left(a^2 b^2\right) b \\  \Longrightarrow & (b a)^2=a^2 `
  - training record: `Problem: Let $G$ be a group in which $(a b)^{3}=a^{3} b^{3}$ and $(a b)^{5}=a^{5} b^{5}$ for all $a, b \in G$. Show that $G$ is abelian.  Solution: \begin{proof}   We have  $$  \begin{aligned}  & (a b)^3=a^3 b^3, \text { for all } a, b \in G \\  \Longrightarrow & (a b)(a b)(a b)=a\left(a^2 b^2\right) b \\  \Longrightarrow & a(b a)(b a) b=a\left(a^2`

- ProofNet/valid item `exercise_2_3_17`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $G$ is a group and $a, x \in G$, prove that $C\left(x^{-1} a x\right)=x^{-1} C(a) x$`
  - training record: `Problem: If $G$ is a group and $a, x \in G$, prove that $C\left(x^{-1} a x\right)=x^{-1} C(a) x$  Solution: \begin{proof}      Note that  $$  C(a):=\{x \in G \mid x a=a x\} .  $$  Let us assume $p \in C\left(x^{-1} a x\right)$. Then,  $$  \begin{aligned}  & p\left(x^{-1} a x\right)=\left(x^{-1} a x\right) p \\  \Longrightarrow & \left(p x^{-1} a\ri`

- ProofNet/valid item `exercise_2_3_17`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}      Note that  $$  C(a):=\{x \in G \mid x a=a x\} .  $$  Let us assume $p \in C\left(x^{-1} a x\right)$. Then,  $$  \begin{aligned}  & p\left(x^{-1} a x\right)=\left(x^{-1} a x\right) p \\  \Longrightarrow & \left(p x^{-1} a\right) x=x`
  - training record: `Problem: If $G$ is a group and $a, x \in G$, prove that $C\left(x^{-1} a x\right)=x^{-1} C(a) x$  Solution: \begin{proof}      Note that  $$  C(a):=\{x \in G \mid x a=a x\} .  $$  Let us assume $p \in C\left(x^{-1} a x\right)$. Then,  $$  \begin{aligned}  & p\left(x^{-1} a x\right)=\left(x^{-1} a x\right) p \\  \Longrightarrow & \left(p x^{-1} a\ri`

- ProofNet/valid item `exercise_2_6_15`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` If $G$ is an abelian group and if $G$ has an element of order $m$ and one of order $n$, where $m$ and $n$ are relatively prime, prove that $G$ has an element of order $mn$.`
  - training record: `Problem: If $G$ is an abelian group and if $G$ has an element of order $m$ and one of order $n$, where $m$ and $n$ are relatively prime, prove that $G$ has an element of order $mn$.  Solution: \begin{proof}  Let $G$ be an abelian group, and let $a$ and $b$ be elements in $G$ of order $m$ and $n$, respectively, where $m$ and $n$ are relatively prime`

- ProofNet/valid item `exercise_2_6_15`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}  Let $G$ be an abelian group, and let $a$ and $b$ be elements in $G$ of order $m$ and $n$, respectively, where $m$ and $n$ are relatively prime. We will show that the product $ab$ has order $mn$ in $G$, which will prove that $G$ has an `
  - training record: `Problem: If $G$ is an abelian group and if $G$ has an element of order $m$ and one of order $n$, where $m$ and $n$ are relatively prime, prove that $G$ has an element of order $mn$.  Solution: \begin{proof}  Let $G$ be an abelian group, and let $a$ and $b$ be elements in $G$ of order $m$ and $n$, respectively, where $m$ and $n$ are relatively prime`

## UDACA__ZIPFIT-train/data/train-00000-of-00001.parquet

- ProofNet/valid item `exercise_2_4_16b`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}      Fix a positive integer $n>1$ and let $H \leq D_{2 n}$ consist of the rotations of $D_{2 n}$. That is, $H=\langle r\rangle$. Now, this subgroup is proper since it does not contain $s$. If $H$ is not maximal, then by the previous pro`
  - training record: `Problem: Show that the subgroup of all rotations in a dihedral group is a maximal subgroup.  Solution: \begin{proof}      Fix a positive integer $n>1$ and let $H \leq D_{2 n}$ consist of the rotations of $D_{2 n}$. That is, $H=\langle r\rangle$. Now, this subgroup is proper since it does not contain $s$. If $H$ is not maximal, then by the previous `

- ProofNet/valid item `exercise_2_4_16b`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Show that the subgroup of all rotations in a dihedral group is a maximal subgroup.`
  - training record: `Problem: Show that the subgroup of all rotations in a dihedral group is a maximal subgroup.  Solution: \begin{proof}      Fix a positive integer $n>1$ and let $H \leq D_{2 n}$ consist of the rotations of $D_{2 n}$. That is, $H=\langle r\rangle$. Now, this subgroup is proper since it does not contain $s$. If $H$ is not maximal, then by the previous `

- ProofNet/valid item `exercise_2018_b2`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Let $n$ be a positive integer, and let $f_{n}(z)=n+(n-1) z+$ $(n-2) z^{2}+\cdots+z^{n-1}$. Prove that $f_{n}$ has no roots in the closed unit disk $\{z \in \mathbb{C}:|z| \leq 1\}$.`
  - training record: `Problem: Let $n$ be a positive integer, and let $f_{n}(z)=n+(n-1) z+$ $(n-2) z^{2}+\cdots+z^{n-1}$. Prove that $f_{n}$ has no roots in the closed unit disk $\{z \in \mathbb{C}:|z| \leq 1\}$.  Solution: \begin{proof}      Note first that $f_n(1) > 0$, so $1$ is not a root of $f_n$.  Next, note that  \[  (z-1)f_n(z) = z^n + \cdots + z - n;  \]  howev`

- ProofNet/valid item `exercise_2018_b2`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}      Note first that $f_n(1) > 0$, so $1$ is not a root of $f_n$.  Next, note that  \[  (z-1)f_n(z) = z^n + \cdots + z - n;  \]  however, for $\left| z \right| \leq 1$, we have   $\left| z^n + \cdots + z \right| \leq n$ by the triangle `
  - training record: `Problem: Let $n$ be a positive integer, and let $f_{n}(z)=n+(n-1) z+$ $(n-2) z^{2}+\cdots+z^{n-1}$. Prove that $f_{n}$ has no roots in the closed unit disk $\{z \in \mathbb{C}:|z| \leq 1\}$.  Solution: \begin{proof}      Note first that $f_n(1) > 0$, so $1$ is not a root of $f_n$.  Next, note that  \[  (z-1)f_n(z) = z^n + \cdots + z - n;  \]  howev`

- ProofNet/valid item `exercise_2017_b3`, view `informal_proof`, containment 1.0, exact=True
  - eval text: `\begin{proof}      Suppose by way of contradiction that $f(1/2)$ is rational. Then $\sum_{i=0}^{\infty} c_i 2^{-i}$ is the binary expansion of a rational number, and hence must be eventually periodic; that is, there exist some integers $m,n$ such tha`
  - training record: `Problem: Suppose that $f(x)=\sum_{i=0}^{\infty} c_{i} x^{i}$ is a power series for which each coefficient $c_{i}$ is 0 or 1 . Show that if $f(2 / 3)=3 / 2$, then $f(1 / 2)$ must be irrational.  Solution: \begin{proof}      Suppose by way of contradiction that $f(1/2)$ is rational. Then $\sum_{i=0}^{\infty} c_i 2^{-i}$ is the binary expansion of a r`

- ProofNet/valid item `exercise_2017_b3`, view `informal_statement`, containment 1.0, exact=True
  - eval text: ` Suppose that $f(x)=\sum_{i=0}^{\infty} c_{i} x^{i}$ is a power series for which each coefficient $c_{i}$ is 0 or 1 . Show that if $f(2 / 3)=3 / 2$, then $f(1 / 2)$ must be irrational.`
  - training record: `Problem: Suppose that $f(x)=\sum_{i=0}^{\infty} c_{i} x^{i}$ is a power series for which each coefficient $c_{i}$ is 0 or 1 . Show that if $f(2 / 3)=3 / 2$, then $f(1 / 2)$ must be irrational.  Solution: \begin{proof}      Suppose by way of contradiction that $f(1/2)$ is rational. Then $\sum_{i=0}^{\infty} c_i 2^{-i}$ is the binary expansion of a r`
