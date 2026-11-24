# Deployment strategy and cloud framework alignment

Applies when the project is deployed anywhere, or documents how it is deployed. Part A always applies to deployed software; Parts B and C apply only if a cloud provider is detected.

## Part A: Deployment strategy

Check what is documented, then what the code and pipeline files actually do. A documented strategy the pipeline does not implement is a finding citing both.

- **Environments and promotion:** which environments exist (dev, test, staging, prod), how a build is promoted, whether the same artifact moves through them, and whether production credentials are reachable from non-production pipelines.
- **Release strategy:** recreate, rolling, blue/green, canary, or manual. Is it stated? Does it fit the availability target (a recreate deploy of a 99.9% service is a gap)?
- **Rollback:** documented, tested, and fast. Can the previous version run against the current schema and data?
- **Schema and data migrations:** run as part of deploy or separately, expand/contract (backward compatible) or breaking, ordering against code rollout.
- **Configuration and secrets:** per-environment config outside the artifact, secrets injected at runtime, drift between environments.
- **Infrastructure as code:** all infrastructure defined in code, reviewed, applied by pipeline, state stored and locked, drift detection.
- **Pipeline controls:** approval gates for production, required tests before deploy, artifact signing or provenance, least-privilege deploy identity, audit trail of who deployed what.
- **Progressive delivery and flags:** feature flags, kill switches, staged rollout, automated rollback on health or SLO regression.
- **Capacity and topology:** regions and zones, replicas, autoscaling, stateful components, single points of failure at the deploy level.
- **Operational handover:** runbooks, on-call ownership, change management or freeze windows if applicable.

If none of this is documented and no pipeline or infrastructure files exist, record `unverifiable` findings rated by impact (a payment system with no rollback evidence is `high`), not a pass.

## Part B: Detect the cloud provider

Use evidence in the repository, not assumptions. Record the provider, the services used, and how you know.

| Provider | Typical evidence |
|---|---|
| AWS | Terraform `provider "aws"`, CloudFormation or CDK or SAM files, `aws-sdk` or `boto3` imports, ARNs, ECS or EKS or Lambda config |
| Azure | Terraform `azurerm`, Bicep or ARM templates, `@azure/*` or `azure-*` SDKs, App Service or AKS or Functions config, managed identity use |
| Google Cloud | Terraform `google`, Deployment Manager, `gcloud` in pipelines, `@google-cloud/*` SDKs, Cloud Run or GKE or Cloud Functions config |
| Oracle Cloud (OCI) | Terraform `oci`, `oci://` paths, OCI SDK imports, OKE or Functions config |
| Other or on-prem | Kubernetes manifests with no provider, Docker Compose, VM or Ansible files |

If a provider is detected, record it in Scope. If several are used, treat it as multi-cloud and say so. If none is detected or deployment is on-premises, skip Part C and say so.

## Part C: Alignment with the provider's well-architected framework

This is an evidence-based alignment check from the repository, not a formal Well-Architected Review and not a certification. Only the provider's own review process, with the people who run the system, can give that.

1. **Get the current pillar list.** Confirm the pillars against the provider's official documentation. Read-only documentation lookups (for example the Microsoft Learn tools for Azure) are allowed even in a read-only or non-interactive run. If you cannot look them up, use the list in `references/frameworks.md` and record that as an `assumption`. Do the same for platform or service limits you rely on (for example which plan tier supports deployment slots).
2. **Rate each pillar** with one-line evidence and the finding IDs:
   - `gap`: any open `high` finding in the pillar, or two or more open `medium`.
   - `partial`: some positive evidence, with weaker open findings.
   - `aligned`: positive evidence in the repository and no open findings. Never rate `aligned` from the absence of problems.
   - `unverifiable`: the repository gives no evidence either way (for example performance with no measurements).
3. **Create findings only for real gaps.** A pillar with no real gap gets a rating and evidence, not a made-up finding. A pillar gap becomes a normal finding with a category from Vocabulary (map the pillar with `references/frameworks.md`). Do not create one finding per framework question; reuse findings already raised by other checklists and cite them.
4. **Prioritize by the system's priority quality attributes.** A gap in a pillar the system does not depend on is `low`.

Starter checks per pillar (adapt to the provider's own terms and services):

| Pillar theme | Check from repository evidence |
|---|---|
| Reliability | Multi-zone or multi-region where the availability target needs it; health probes; autoscaling; managed data services with backups and tested restore; retries, timeouts, and queues for dependencies; quotas and limits known |
| Security | Identity-based access (roles, managed identities) rather than long-lived keys; least-privilege policies with no wildcards; encryption at rest and in transit with managed keys; private networking and no public data stores; secrets in a managed store; audit logging enabled |
| Cost optimization | Right-sized and autoscaled resources; budgets and alerts; tagging for cost allocation; lifecycle and retention rules on storage and logs; use of managed or serverless services where load is spiky; no idle environments |
| Operational excellence | Everything in IaC; CI/CD with approvals; monitoring, alerting, and runbooks; deployment is small and reversible; incident and change process |
| Performance efficiency | Service and instance choices fit the workload; caching and CDN where useful; data store fits the access pattern; load tests against the stated peak; scaling limits known |
| Sustainability (AWS) | Region and instance choices, utilization, data retention, and managed services that raise utilization. Check only if the organization asks. |

Report the result in the Output section **Cloud framework alignment** (a table of pillar | rating | evidence | finding IDs), plus a one-line statement that this is not a formal review.
