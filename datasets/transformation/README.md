# Dataset Specification of Transformation Task

---

## Detailes of transformation cases (Input–Output–Validation)

This document describes how we construct **transformation (cross-language transformation)** instances in CrypFormBench, addressing concerns about task under-specification. Each instance translates a protocol model between two verifier languages while preserving *the same protocol, the same security goals, and the same adversary/threat model*.

### 1) Instance definition

A **transformation instance** is a tuple:

* **Source**: a formal specification file `src` in language/tool `L_src`
* **Target**: a formal specification file `tgt` in language/tool `L_tgt`
* **Protocol identity**: same underlying scheme (e.g., Yahalom, TLS Handshake, NSPK, DH, …)
* **Security goals**: same goal set (e.g., secrecy, authentication, integrity) under the same interpretation
* **Adversary model**: aligned to the same reference setting (e.g., Dolev–Yao network adversary unless otherwise stated)

#### Prompt (input)

For each instance, the model receives:

* the **source formal code** (`src`)
* its **natural-language logic description** (roles, message flow, goals, assumptions)
* the **target language** identifier (`L_tgt`)

and is asked to output a target-language formal model.

#### Expected output

A **target-language formal specification** that is:

1. **Executable** in the target verifier (parses/type-checks/compiles), and
2. **Semantics-preserving** at the benchmark level: it encodes the same goals & threat model and yields the same expected verdict.

### 2) Correctness & validation

We evaluate each generated target file by executing the **target verifier**:

* **Analyzable**: the target tool can run to completion (not parse/type error; not timeout)
* **Correct**: the target tool’s verdict matches the **canonical label** for this protocol-goal-threat triple

Notes:

* Some tools expose only **binary verdicts** (e.g., SAFE/UNSAFE). We therefore match **protocol-level verdicts** by default.
* Transformation pairs are curated so that **source and target references agree** on the canonical outcome.

### 3) How we select transformation examples

Transformation examples are selected under the following constraints:

* **Same protocol** across languages (same scheme family)
* **Same security goals** (explicitly tracked per scheme cluster)
* **Same adversary/threat model** (aligned during encoding)
* **Reference consistency**: the tool-specific reference scripts are checked to be consistent with the canonical label; instances with unresolved inconsistency are excluded.

This results in a set of **protocol clusters** (one cluster = multiple tool encodings of the same scheme).

---

### 4) Protocol clusters and reference files

Each bullet below lists a **scheme cluster** and its available encodings.

#### Yahalom (secrecy, authentication, integrity)

* `SPDL-1/yahalom.spdl`
* `MAUDE-1/Yahalom.maude`
* `PV-1/Yahalom.pv`

#### TLS Handshake

* `SPTHY-1/TLS_Handshake.spthy`
* `HLPSL-1/TLS.hlpsl`

#### IKEv2-MAC

* `SPDL-1/ikev2-mac.spdl`
* `HLPSL-1/IKEv2-MAC.hlpsl`

#### Kerberos (RDDM)

* `SPDL-1/kerberos-rddm.spdl`
* `HLPSL-1/Kerberos.hlpsl`

#### NAXOS

* `SPDL-1/NAXOS.spdl`
* `SPTHY-1/ake_NAXOS.spthy`

#### NSPK-Lowe variant (mapping across tools)

* `SPDL-1/nsl3.spdl`
* `MAUDE-1/Needham_Schroeder_Lowe.maude`

#### Signed Diffie–Hellman (multi-tool)

* `SPDL-1/Signed-DH.spdl`
* `SPTHY-1/signed_dh.spthy`
* `MAUDE-1/signed_dh.maude`
* `PV-1/signedDH.pv`
* `CV-1/template-signedDH.ocv`

#### STS-MAC

* `SPTHY-1/STS_MAC.spthy`
* `SPDL-1/sts-mac.spdl`

#### Otway–Rees

* `SPDL-1/otwayrees.spdl`
* `PV-1/OtwayRees.pv`

#### Woo–Lam

* `SPDL-1/woo-lam.spdl`
* `MAUDE-1/Woo-Lam_Authentication.maude`
* `PV-1/piwoolam.pi`

#### Needham–Schroeder (NSPK, multi-tool)

* `SPDL-1/needham-schroeder.spdl`
* `HLPSL-1/NSPK_2.hlpsl`
* `PV-1/NSPK-agree-A-to-B-secrecy.pv`
* `MAUDE-1/Needham_Schroeder.maude`
* `SPTHY-1/NSPK3.spthy`

#### NSPK with XOR (Maude ↔ HLPSL)

* `MAUDE-1/Needham_Schroeder_Lowe_XOR.maude`
* `HLPSL-1/XorNSPK_2.hlpsl`

#### KAS1

* `SPDL-1/KAS1.spdl`
* `SPTHY-1/KAS1.spthy`

#### Otway–Rees (Maude ↔ Horn)

* `MAUDE-1/Otway-Rees.maude`
* `PV-1/otway-rees-fctshr.horn`

#### Diffie–Hellman (multi-tool)

* `HLPSL-1/DH.hlpsl`
* `PV-1/DH.pv`
* `MAUDE-1/dh.maude`
* `SPTHY-1/dh_alternative.spthy`

#### ElGamal (CryptoVerif ↔ EasyCrypt)

* `CV-1/Avik-elgamal.cv`
* `EC-1/elgamal.ec`

#### Hashed ElGamal / CDH (CryptoVerif ↔ EasyCrypt)

* `CV-1/Avik-hash-elgamal-CDH.cv`
* `EC-1/hashed_elgamal_std.ec`

#### Denning–Sacco (Maude ↔ Horn/Horntype)

* `MAUDE-1/Denning-Sacco.maude`
* `PV-1/denning-sacco-orig.horn`
* `PV-1/denning-sacco-orig.horntype`

#### BR93 encryption (CV ↔ OCV)

* `CV-1/encryptBR93-1.cv`
* `CV-1/encryptBR93-1.ocv`

---

### 5) Transformation pairs (directed edges)

  ![protocols](transformation/protocol_translation_nums.png)

We instantiate transformation tasks over all available **language pairs within each cluster**. Below is the explicit pair list (as used in the benchmark):

```text
(SPDL-1/yahalom.spdl, MAUDE-1/Yahalom.maude)
(SPDL-1/yahalom.spdl, PV-1/Yahalom.pv)
(MAUDE-1/Yahalom.maude, PV-1/Yahalom.pv)

(SPTHY-1/TLS_Handshake.spthy, HLPSL-1/TLS.hlpsl)

(SPDL-1/ikev2-mac.spdl, HLPSL-1/IKEv2-MAC.hlpsl)
(SPDL-1/kerberos-rddm.spdl, HLPSL-1/Kerberos.hlpsl)
(SPDL-1/NAXOS.spdl, SPTHY-1/ake_NAXOS.spthy)
(SPDL-1/nsl3.spdl, MAUDE-1/Needham_Schroeder_Lowe.maude)

(SPDL-1/Signed-DH.spdl, SPTHY-1/signed_dh.spthy)
(SPDL-1/Signed-DH.spdl, MAUDE-1/signed_dh.maude)
(SPDL-1/Signed-DH.spdl, PV-1/signedDH.pv)
(SPDL-1/Signed-DH.spdl, CV-1/template-signedDH.ocv)
(SPTHY-1/signed_dh.spthy, MAUDE-1/signed_dh.maude)
(SPTHY-1/signed_dh.spthy, PV-1/signedDH.pv)
(SPTHY-1/signed_dh.spthy, CV-1/template-signedDH.ocv)
(MAUDE-1/signed_dh.maude, PV-1/signedDH.pv)
(MAUDE-1/signed_dh.maude, CV-1/template-signedDH.ocv)
(PV-1/signedDH.pv, CV-1/template-signedDH.ocv)

(SPTHY-1/STS_MAC.spthy, SPDL-1/sts-mac.spdl)

(SPDL-1/otwayrees.spdl, PV-1/OtwayRees.pv)

(SPDL-1/woo-lam.spdl, MAUDE-1/Woo-Lam_Authentication.maude)
(SPDL-1/woo-lam.spdl, PV-1/piwoolam.pi)
(MAUDE-1/Woo-Lam_Authentication.maude, PV-1/piwoolam.pi)

(SPDL-1/needham-schroeder.spdl, HLPSL-1/NSPK_2.hlpsl)
(SPDL-1/needham-schroeder.spdl, PV-1/NSPK-agree-A-to-B-secrecy.pv)
(SPDL-1/needham-schroeder.spdl, MAUDE-1/Needham_Schroeder.maude)
(SPDL-1/needham-schroeder.spdl, SPTHY-1/NSPK3.spthy)
(HLPSL-1/NSPK_2.hlpsl, PV-1/NSPK-agree-A-to-B-secrecy.pv)
(HLPSL-1/NSPK_2.hlpsl, MAUDE-1/Needham_Schroeder.maude)
(HLPSL-1/NSPK_2.hlpsl, SPTHY-1/NSPK3.spthy)
(PV-1/NSPK-agree-A-to-B-secrecy.pv, MAUDE-1/Needham_Schroeder.maude)
(PV-1/NSPK-agree-A-to-B-secrecy.pv, SPTHY-1/NSPK3.spthy)
(MAUDE-1/Needham_Schroeder.maude, SPTHY-1/NSPK3.spthy)

(MAUDE-1/Needham_Schroeder_Lowe_XOR.maude, HLPSL-1/XorNSPK_2.hlpsl)

(SPDL-1/KAS1.spdl, SPTHY-1/KAS1.spthy)

(MAUDE-1/Otway-Rees.maude, PV-1/otway-rees-fctshr.horn)

(HLPSL-1/DH.hlpsl, PV-1/DH.pv)
(HLPSL-1/DH.hlpsl, MAUDE-1/dh.maude)
(HLPSL-1/DH.hlpsl, SPTHY-1/dh_alternative.spthy)
(PV-1/DH.pv, MAUDE-1/dh.maude)
(PV-1/DH.pv, SPTHY-1/dh_alternative.spthy)
(MAUDE-1/dh.maude, SPTHY-1/dh_alternative.spthy)

(CV-1/Avik-elgamal.cv, EC-1/elgamal.ec)
(CV-1/Avik-hash-elgamal-CDH.cv, EC-1/hashed_elgamal_std.ec)

(MAUDE-1/Denning-Sacco.maude, PV-1/denning-sacco-orig.horn)
(MAUDE-1/Denning-Sacco.maude, PV-1/denning-sacco-orig.horntype)
(PV-1/denning-sacco-orig.horn, PV-1/denning-sacco-orig.horntype)

(CV-1/encryptBR93-1.cv, CV-1/encryptBR93-1.ocv)
```

### (Optional) Additional DH → SPDL edges

If you also include a **SPDL encoding for DH** (as implied by your note), then DH additionally supports:

```text
(HLPSL-1/DH.hlpsl, SPDL-1/DH.spdl)
(PV-1/DH.pv, SPDL-1/DH.spdl)
(MAUDE-1/dh.maude, SPDL-1/DH.spdl)
(SPTHY-1/dh_alternative.spthy, SPDL-1/DH.spdl)
```

---

### 6) Practical notes (for reproduction)

* All paths above are **repository-relative** (tool prefix + version folder + filename).
* The number of transformation instance are illustrated in Figure 8 of Section 5.6.