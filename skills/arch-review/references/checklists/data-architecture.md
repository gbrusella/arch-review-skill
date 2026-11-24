# Data architecture

- Data ownership per component, system of record, and whether any component reads another's database directly.
- Consistency model (strong, eventual) and where the design depends on it; handling of conflicts and duplicates.
- Schema evolution: versioning, backward compatibility, migration strategy for large tables.
- Retention, archival, and deletion (including legal deletion requests) for each store.
- Growth: expected size over time versus the store's limits; partitioning or sharding plan if needed.
