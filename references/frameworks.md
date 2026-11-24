# Mapping to common frameworks

Optional. Add a `Framework` note to the Summary heatmap when the organization uses one, so reviews can be compared with other assessments.

| Category | AWS Well-Architected | Azure Well-Architected |
|---|---|---|
| security | Security | Security |
| performance | Performance efficiency | Performance efficiency |
| resilience | Reliability | Reliability |
| operations, observability | Operational excellence | Operational excellence |
| cost | Cost optimization | Cost optimization |
| maintainability, data, requirements, testing | Operational excellence / Reliability (closest) | Operational excellence (closest) |

Sustainability is a pillar in AWS Well-Architected; check it only if the organization asks.

## Pillar lists for the cloud alignment check

Confirm against the provider's current documentation when you can; frameworks change. Use these only as a fallback and mark them `assumption`.

- **AWS Well-Architected:** Operational excellence, Security, Reliability, Performance efficiency, Cost optimization, Sustainability.
- **Azure Well-Architected:** Reliability, Security, Cost optimization, Operational excellence, Performance efficiency.
- **Google Cloud Architecture Framework:** System design, Operational excellence, Security/privacy/compliance, Reliability, Cost optimization, Performance optimization.
- **Oracle Cloud Well-Architected Framework:** Security and compliance, Reliability and resilience, Performance and cost optimization, Operational efficiency, Distributed cloud.
- **Other providers or on-premises:** no pillar check; apply the generic resilience, security, cost, operations, and performance checklists.

Map a pillar to a finding category with the table above: Security to `security`, Reliability to `resilience`, Cost to `cost`, Performance to `performance`, Operational excellence or efficiency to `operations` or `observability`.

**STRIDE** for trust boundaries in the security checks: Spoofing (authentication), Tampering (integrity, injection), Repudiation (audit trail), Information disclosure (data exposure, logging), Denial of service (capacity, retries, rate limits), Elevation of privilege (authorization). Use it to structure questions, not to claim a threat model was done.
