# Architecture and design

Component boundaries, coupling, duplicated responsibilities, dependency direction, scalability constraints,
testability, resilience. Check whether alternatives, trade-offs, assumptions, dependencies, risks, and
reversibility are documented well enough to support each decision.

- Do the boundaries follow the domain, or do they follow technical layers that force every change to touch every component?
- Is each ADR decision visible in the code, and does the code contain significant decisions with no ADR?
- Are alternatives real, are negative consequences named, and is the cost of reversing each decision stated?
