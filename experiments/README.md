# Supplement of Experiments

---

## Case Studies of Evaluation Tasks

### Language-specific failure modes and actionable insights
For languages of symbolic tools such as SPDL and SPTHY, dominant failures are: (i) *intruder/adversary modeling errors* (wrong DY capability, key/nonces confusion, and missing compromise), (ii) *process mis-specification* (missing/reordered messages, incomplete roles, and wrong channels), (iii) *freshness/binding/correspondence mistakes* (dropped nonce checks, injectivity/uniqueness, and session separation), and (iv) *property encoding errors* (secrecy and authentication confusion and wrong events/queries/lemmas).
For EC and CV/OCV of computational tools, errors are mainly proof-structural: (i) *incorrect game/setup* (missing randomness or inconsistent oracles), (ii) *invalid game hops/side conditions*, and (iii) *mis-specified events/bad-events*, leading to vacuous or overly strong claims. 
Accordingly, symbolic prompts/training should emphasize faithful intruder, complete roles, and explicit freshness/binding, while computational guidance should prioritize disciplined game setup, explicit side conditions, and correct event/bad-event design.

## The Interpretation Capability
The evaluation of interpretation capability is summarized in Figures~\ref{fig:interpretation}. We analyze two perspectives: (i) \textit{logic illustration}, measuring semantic similarity between extracted logic and ground-truth references, and (ii) \textit{code annotation}, evaluating both textual similarity of comments and executability on formal analysis platforms.

### Logic interpretation
Across models and languages, most LLMs achieve relatively high similarity when reconstructing protocol interaction logic. As shown in the left heatmap, the best-performing models, *GPT-4o*, *GPT-4o-mini*, and *Claude-3.5-Sonnet-Coder*, consistently attain average similarity scores above 0.95. Open-source models such as *DeepSeek-R1* and *DeepSeek-Coder* also perform competitively, whereas *LLaMA4-Instruct* and *Grok-3* lag behind, often producing lower semantic consistency. These results suggest advanced proprietary models and reasoning- or coding-specialized variants are better at reconstructing protocol semantics, while general-purpose or lightweight models struggle to capture subtle adversary behaviors and security objectives.

### Code annotation and executability
The results of code annotation and its downstream executability are shown in the middle and right heatmaps of Figure 9. Leading proprietary models such as *GPT-4o*, *GPT-4o-mini*, and *Claude-3.5-Sonnet-Coder* generate comments with similarity scores exceeding $0.98$, while maintaining the syntactic correctness required for tool-based verification.

By contrast, models such as *Gemini-2.5-Pro* and *GLM-4* exhibit a clear mismatch: although their generated comments achieve moderate semantic similarity, the annotated files frequently fail to compile or execute on formal verification platforms. This highlights that producing fluent natural language explanations alone does not ensure compatibility with formal toolchains. More critically, open-source models such as *LLaMA4-Instruct* and *Grok-3* underperform on both dimensions, yielding low similarity scores and near-zero executable outputs.

Taken together, these findings underscore the need to evaluate code annotation with executability. Explanations must be semantically faithful and meet the strict syntactic and semantic requirements of formal verification tools. This dual perspective reveals a key bottleneck for current LLMs in bridging natural language interpretation with machine-verifiable specifications.

## The Transformation Capability

Figure 8 summarizes the transformation results. At the model level (left), we break down outcomes into failed generation, failed analysis, timeout, and the TP/TN/FP/FN distribution on analyzable cases. At the language level, we report the directed source$\rightarrow$target analyzable ratio and the corresponding $\mathrm{ACC}_\mathrm{A}$. 

### Overall performance

Compared with code generation and completion, transformation is particularly challenging because models must simultaneously interpret the source-language semantics and reproduce the target-language syntax, causing only a small fraction of generated files to be analyzable (typically <10\%), even for powerful general-purpose models (e.g., *GPT-4o* and *DeepSeek-Coder*). 

### Cross-language interference and timeout bottleneck

A key difficulty is cross-language interference: the prompt includes both source code and a logic description, which often biases models to copy source fragments into the target file. Such token-level copying is usually invalid because different verifiers encode the same operation with incompatible idioms (e.g., Out(msg) in SPTHY and send\_1(A,B,msg) in SPDL), leading to early parse/type-check failures. Moreover, even among the few compilable translations, timeouts are frequent, indicating deeper semantic/structural mismatch. Manual inspection confirms that compiled translations are often redundant or ill-structured: in rewriting-based tools such as Maude-NPA, unnecessary nested constructs (e.g., enc(enc(a,k1),k2)) can trigger exponential rewriting and non-termination, while omitting small but mandatory clauses (e.g., ::nil::[+(null),nil]& in Maude) can likewise introduce infinite loops. 
\added{Additional recurring semantic and structural errors are detailed in Section 5.8. Besides, the middle/right heatmaps further show that only a few source$\rightarrow$target pairs achieve non-zero analyzability, and even fewer preserve correctness (non-trivial $\mathrm{ACC}_A$), while most directions remain at or near zero. This highlights that transformation difficulty is not only ``hard languages'' in isolation, but also the lack of robust cross-tool semantic mapping across heterogeneous formalisms. 

### Superiority of specialized models

Among all LLMs, *Claude-3.5-Sonnet-Coder* achieves the highest analyzed ratio (14%) and meaningful correctness on analyzable cases (e.g., $\text{F1}_\text{A}=61.54\%$), suggesting that coding-oriented models retain limited but promising cross-tool transformation ability.

In sum, transformation is the most challenging capability in \fram: preserving both syntax and semantics across heterogeneous verifier languages critically limits analyzability and remains beyond the robust capability of current LLMs. We discuss practical directions such as grammar-constrained decoding and tool-in-the-loop feedback in Section 6. 