# AsyncAPI / Event Schema Analysis

See `references/graphql-analysis.md` — the "AsyncAPI / Event Schema Analysis" section
covers this format in full, including the dead letter queue test, channel renaming risks,
and event versioning patterns.

Key reminder: event schema changes are higher-stakes than REST because consumer and
producer deploys are decoupled. Use the dead letter queue mental model for severity assessment.