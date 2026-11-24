# Infrastructure and CI config

Applies only if IaC, container, or pipeline files exist.

Terraform/Bicep/CloudFormation, Dockerfiles, Kubernetes manifests, CI/CD pipeline files.

- Overly broad IAM roles or wildcard permissions; services or storage exposed publicly without need; open security groups or ingress.
- Containers running as root, unpinned base images, secrets baked into images, exposed debug ports.
- CI/CD: jobs with write or admin tokens, secrets echoed in logs, unpinned third-party actions or images, untrusted input (PR titles, branch names) used in scripts, deployment without approval gates.
- Environment separation (dev, test, prod) and whether production credentials are reachable from non-production pipelines.
- Backup, encryption, and logging settings declared in the infrastructure code.
