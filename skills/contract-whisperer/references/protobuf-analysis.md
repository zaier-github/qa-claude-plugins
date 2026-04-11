# Protobuf / gRPC Analysis

See `references/graphql-analysis.md` — the "Protobuf / gRPC Analysis" section covers
this format in full, including field numbering rules, the `reserved` keyword, wire
compatibility, and the `buf` tooling recommendation.

Key reminder: **field numbers are permanent** in Protobuf. Always use `buf breaking`
before shipping proto changes.