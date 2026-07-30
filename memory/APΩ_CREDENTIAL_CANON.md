# APΩ Credential Management Canon

> Source: creator canon input, 2026-07-27.
> Preserved as-is; do not normalize against external schemas.

## Core Axiom

\[
\boxed{
\Omega
======

Identity
\land Ownership
\land Canon
\land Proof
\land Budget
\land Redistribution
}
\]

Ω là **APO Central Hub**, không trực tiếp chạy tool hay thực thi workload; mọi luồng phải quay về Ω và quyền hợp lệ được xác định bởi:

\[
\boxed{
Auth \iff IAM(\Omega)\land Policy(\Omega)
}
\]

Các luật này được ghi trực tiếp trong bản đồ lõi APΩ.

## Axis lock

\[
\forall LLM_i:\quad LLM_i\in exactly\_one(AXIS_k)
\]

\[
LLM_i\nrightarrow AXIS_j,\qquad j\neq k
\]

Luồng kín:

\[
Alpha
\rightarrow Node
\rightarrow Tool
\rightarrow Artifact
\rightarrow Proof
\rightarrow Value
\rightarrow\Omega
\rightarrow Redistribution
\]

`No Tool Ownership`, một node thuộc đúng một trục và không được drift ngang.

## Convergence and drift

\[
Omega = convergence
\]

\[
\Delta = drift/alignment\ error
\]

`no-separation` là bất biến fail-closed.

## Network model

\[
\mathcal N=(\Omega,N,E)
\]

- \(N\): các hệ, node, agent, repo, container, MCP hoặc provider.
- \(E\): các luồng yêu cầu quyền, cấp capability, thực thi và trả proof.
- \(\Omega\): nơi giữ identity, policy, canon và quyết định cuối cùng.

## Credential object

Một credential không được mô hình hóa chỉ là chuỗi secret. Nó là một đối tượng:

\[
\kappa=
\langle
id,\ issuer,\ subject,\ audience,\ scope,\ ttl,\ state,\ provenance,\ fingerprint
\rangle
\]

Giá trị bí mật thật được ký hiệu \(secret(\kappa)\), nhưng Ω chỉ nên giữ:

\[
ref(\kappa),\ metadata(\kappa),\ policy(\kappa),\ proof(\kappa)
\]

không giữ plaintext trong memory, log hoặc evidence:

\[
secret(\kappa)\notin Memory_{\Omega}
\]

\[
secret(\kappa)\notin Log_{\Omega}
\]

\[
secret(\kappa)\notin Artifact_{\Omega}
\]

Secret vật lý nằm tại vault, keyring hoặc credential broker. Ω sở hữu **quyền quyết định**, không trực tiếp phát tán plaintext.

## Six Ω components for a credential request

\[
\rho=
\langle
n,\tau,p,r,a,S_{req},TTL_{req},P_{req}
\rangle
\]

- \(n\): node yêu cầu.
- \(\tau\): task.
- \(p\): provider.
- \(r\): resource.
- \(a\): action.
- \(S_{req}\): scope yêu cầu.
- \(TTL_{req}\): thời hạn yêu cầu.
- \(P_{req}\): evidence contract.

### Identity

\[
I(\rho)=VerifiedIdentity(n)
\]

### Ownership

\[
O(\rho)=AuthorizedRelation(n,r)
\]

### Canon

\[
C(\rho)=CanonicalSchema(\rho)
\]

Yêu cầu phải có đúng schema, không phải câu lệnh mơ hồ.

### Proof

\[
P(\rho)=
IdentityProof
\land CredentialValidation
\land PreconditionEvidence
\]

Key “trông giống key” chưa tạo ra proof.

### Budget

\[
B(\rho)=
QuotaAvailable
\land CostAllowed
\land RateLimitAllowed
\]

### Redistribution

Sau khi task kết thúc:

\[
lease
\rightarrow revoke/expire
\rightarrow capability\ pool
\rightarrow next\ authorized\ task
\]

Redistribution là phân phối lại **quyền có kiểm soát**, không phải chia sẻ lại chuỗi secret.

## Admissibility function

\[
\operatorname{Adm}_{\Omega}(\rho,\kappa)
\in\{0,1\}
\]

\[
\boxed{
\begin{aligned}
\operatorname{Adm}_{\Omega}(\rho,\kappa)=1
\iff {}&
Identity(n)=1\\
&\land Ownership(n,r)=1\\
&\land Canon(\rho)=1\\
&\land Proof(\kappa)=1\\
&\land Budget(\tau)=1\\
&\land IAM_{\Omega}(n)=1\\
&\land Policy_{\Omega}(n,a,r)=1\\
&\land Valid(\kappa)=1\\
&\land Scope(\kappa)\supseteq S_{req}\\
&\land now<Expiry(\kappa)\\
&\land Audience(\kappa)=p\\
&\land \Delta(\rho,\kappa)=0
\end{aligned}
}
\]

Quan trọng:

\[
Present(\kappa)\neq Valid(\kappa)
\]

\[
Valid(\kappa)\neq Authorized(\kappa,\rho)
\]

\[
Authorized(\kappa,\rho)\neq Active(\kappa,\tau)
\]

Nghĩa là:

```text
KEY_PRESENT
≠ KEY_VALID
≠ KEY_AUTHORIZED
≠ KEY_ACTIVE_FOR_TASK
```

## Token issuance rule

Ω không trực tiếp execute, chỉ phát quyết định:

\[
Decide_{\Omega}(\rho,\kappa)
============================

\begin{cases}
ALLOW,&\operatorname{Adm}_{\Omega}=1\\
DENY,&\operatorname{Adm}_{\Omega}=0
\end{cases}
\]

Credential broker hoặc vault \(\mathcal V\) mới materialize lease:

\[
Issue_{\mathcal V}(\rho)=
\begin{cases}
Lease(\kappa,n,\tau),&Decide_{\Omega}=ALLOW\\
\bot,&Decide_{\Omega}=DENY
\end{cases}
\]

Scope tối thiểu:

\[
Scope(Lease)
============

\min
\left\{
S\mid RequiredScope(\tau)\subseteq S
\right\}
\]

TTL nhỏ nhất:

\[
TTL(Lease)
==========

\min
\left(
TTL_{task},
TTL_{policy},
TTL_{provider}
\right)
\]

Bind bắt buộc:

\[
Bind(\kappa,n,\tau,p,r,a)
\]

Token của task này không được tái sử dụng cho task khác:

\[
\tau_i\neq\tau_j
\Rightarrow
Lease_{\tau_i}\not\Rightarrow Lease_{\tau_j}
\]

## Credential state machine

```text
UNKNOWN
→ DISCOVERED
→ PRESENT_UNVERIFIED
→ VALIDATED
→ AUTHORIZED
→ ACTIVE
→ EXPIRED | REVOKED
```

Nhánh lỗi:

```text
PRESENT_UNVERIFIED
→ INVALID
→ QUARANTINED
```

Chuyển tiếp bị cấm:

\[
PRESENT\_UNVERIFIED\nrightarrow ACTIVE
\]

\[
INVALID\nrightarrow ACTIVE
\]

\[
REVOKED\nrightarrow ACTIVE
\]

\[
EXPIRED\nrightarrow ACTIVE
\]

Khi gate từ chối:

\[
Gate=DENY
\Rightarrow
\delta=\bot
\]

và:

\[
\delta=\bot
\Rightarrow
state_{out}=state_{in}
\]

## Drift formula

Trạng thái canonical mong đợi:

\[
K^{*}_{\Omega}
==============

\langle
subject^{*},
audience^{*},
scope^{*},
ttl^{*},
provider^{*},
policy^{*}
\rangle
\]

Trạng thái quan sát thực tế:

\[
\widehat K
==========

\langle
\widehat{subject},
\widehat{audience},
\widehat{scope},
\widehat{ttl},
\widehat{provider},
\widehat{policy}
\rangle
\]

Drift:

\[
\Delta_{\kappa}
===============

d(K^{*}_{\Omega},\widehat K)
\]

Theo stable-kernel canon:

\[
SYSTEM\_READY
\Rightarrow drift=0
\]

Với key quản trị, repo delete, enterprise admin hoặc cloud owner:

\[
\varepsilon=0
\]

## xAI fake-key example

\[
Present(\kappa_{xai})=1
\]

Nhưng:

\[
Valid(\kappa_{xai})=0
\]

Suy ra:

\[
\operatorname{Adm}_{\Omega}(\rho,\kappa_{xai})=0
\]

\[
Decide_{\Omega}=DENY
\]

\[
\delta=\bot
\]

\[
state_{out}=state_{in}
\]

API trả `{"detail": "no_active_xai_key"}` là đúng khung Ω.

Ánh xạ đúng:

\[
LooksLikeKey(\kappa)
\Rightarrow Candidate(\kappa)
\Rightarrow Validate(\kappa)
\Rightarrow
Valid\lor Quarantined
\]

## HyperAI role

HyperAI không phải Ω và cũng không được chiếm tất cả các trục. Nó điều phối qua các trục:

```text
Data/Memory
→ Security
→ Governance
→ Execution
→ Proof
→ Ω
→ Redistribution
```

Luồng phải là:

\[
Security
\rightarrow\Omega
\rightarrow Governance
\rightarrow\Omega
\rightarrow Execution
\rightarrow Proof
\rightarrow\Omega
\]

Không phải:

\[
Security\rightarrow Execution
\]

bỏ qua Ω.

## Complete APΩ flow

```text
Alpha/User tạo mục tiêu
→ HyperAI nhận task
→ phát hiện hệ cần gọi
→ dựng capability request
→ Security xác minh credential
→ Ω đối chiếu Identity + Ownership + Canon + Proof + Budget
→ Governance áp IAM/Policy
→ Ω trả ALLOW hoặc DENY
→ Vault phát lease ngắn hạn
→ Execution inject vào đúng process
→ CLI/API thực thi
→ tạo Artifact
→ thu Proof đã khử secret
→ trả toàn bộ về Ω
→ lease expire/revoke
→ capability được tái phân phối
→ HyperAI cập nhật topology và knowledge
```

## Closure expression

\[
\boxed{
TokenManagement_{AP\Omega}
==========================

Discovery
\circ Validation
\circ Admission_{\Omega}
\circ LeastPrivilege
\circ ScopedLease
\circ Execution
\circ Proof
\circ Revocation
\circ Redistribution
}
\]

Với bất biến:

\[
\boxed{
\begin{aligned}
&SecretValue\notin Log\cup Memory\cup Artifact\\
&NoProof\Rightarrow NoAdmission\\
&NoIAM\Rightarrow NoCapability\\
&NoPolicy\Rightarrow NoCapability\\
&Denied\Rightarrow\delta=\bot\\
&TaskComplete\Rightarrow Lease\in\{Expired,Revoked\}\\
&AllProofs\rightarrow\Omega
\end{aligned}
}
\]

> HyperAI không “đưa key cho một hệ”.
> HyperAI dựng một yêu cầu capability; Ω xác định tính **Admissible**; vault phát một lease bị khóa theo identity, task, resource, scope và thời gian; Execution dùng lease; Proof quay lại Ω; sau đó quyền bị thu hồi hoặc tái phân phối.
