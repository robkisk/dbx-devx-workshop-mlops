# Managed MCP Demo Script

Databricks Managed MCP servers expose workspace capabilities as tools that AI agents can call over the Model Context Protocol. This demo shows four managed MCPs working together on NYC taxi trip data.

## Prerequisites

- Workspace: configured via Databricks CLI profile `dev`
- Catalog/Schema: `bu1_dev.mcp_demo`
- OAuth App: configured in `.mcp.json` (not checked in)
- Claude Code with `.mcp.json` configured for all four managed MCPs

## Data Assets

| Asset | Type | Description |
|-------|------|-------------|
| `trips` | Table (21,932 rows) | NYC taxi trips — timestamps, fares, distances, pickup/dropoff zip codes |
| `zones` | Table (128 rows) | Aggregated metrics per zip — trip count, avg fare, avg distance, min/max fare |
| `zone_descriptions` | Table (60 rows) | NYC neighborhoods mapped to zip codes with rich text descriptions |
| `zone_descriptions_index` | VS Index | Delta sync managed embeddings on the `description` column |
| `avg_fare_by_borough()` | UC Function | Returns avg fare, trip count, total revenue for a borough |
| `top_zones()` | UC Function | Returns top 10 zones by trip count for a borough |
| `trip_summary()` | UC Function | Full stats + description for a specific zip code |
| NYC Taxi Trip Analyst | Genie Space | Natural language analytics over all three tables |

## MCP Servers

| MCP | Endpoint | Port | What It Does |
|-----|----------|------|-------------|
| `dbsql-dev` | `/api/2.0/mcp/sql` | 8091 | Execute SQL against Unity Catalog |
| `genie-dev` | `/api/2.0/mcp/genie/<space_id>` | 8092 | Natural language analytics via Genie |
| `ucfunc-dev` | `/api/2.0/mcp/functions/bu1_dev/mcp_demo` | 8093 | Call UC SQL functions as tools |
| `vs-dev` | `/api/2.0/mcp/vector-search/bu1_dev/mcp_demo` | 8094 | Semantic search over zone descriptions |

---

## Demo Narrative

The story: an AI agent is asked to explore NYC taxi data. Each MCP serves a different role — SQL for precision, Genie for natural language, Vector Search for semantics, and UC Functions for reusable logic. The key takeaway is **composability** — the agent picks the right tool for each sub-task.

---

### Step 1: Orient — Discover the data (dbsql-dev)

**Prompt:** "What tables are available in the mcp_demo schema?"

**What happens:** The agent uses the SQL MCP to run `SHOW TABLES IN bu1_dev.mcp_demo` and discovers three tables plus the VS index.

**Talking point:** The SQL MCP gives the agent direct, precise access to Unity Catalog. It can explore schemas, describe tables, and run any query — just like a data engineer would.

---

### Step 2: Analyze — Ask a business question (genie-dev)

**Prompt:** "What borough has the highest average fare?"

**What happens:** Genie translates the natural language question into SQL — a `RANK()` window function joining zones with zone descriptions. It returns: **Queens at $24.71**, driven by airport trips (LaGuardia and JFK).

**Talking point:** Genie goes beyond simple lookups. It autonomously wrote a window function, joined two tables, and provided a contextual answer. Non-technical users can ask complex analytical questions without writing SQL.

**Follow-up prompts to try:**
- "Compare fare revenue between Manhattan and Queens"
- "Show me trip volume trends by zone"
- "What's the average trip distance from LaGuardia Airport?"

---

### Step 3: Search — Find zones by meaning (vs-dev)

**Prompt:** "Find neighborhoods known for business travelers and corporate offices"

**What happens:** Vector Search returns the top 5 semantically similar zones:

| Rank | Zone | Score | Why It Matched |
|------|------|-------|---------------|
| 1 | Midtown East / Park Avenue | 0.69 | "corporate headquarters... Business traveler taxi traffic dominates" |
| 2 | Grand Central / Midtown East | 0.65 | "Chrysler Building, corporate offices... business traveler traffic" |
| 3 | Midtown East / UN Area | 0.63 | "International diplomatic activity" |
| 4 | Midtown East / 52nd Street | 0.63 | "prestigious commercial address" |
| 5 | Gramercy / Flatiron | 0.63 | "tech company offices" |

**Talking point:** This is something SQL `LIKE` or `CONTAINS` could never do. The query "business travelers" doesn't appear verbatim in any description, but Vector Search understands the semantic relationship between "business travelers" and "corporate headquarters," "commercial address," and "diplomatic activity."

**Follow-up prompts to try:**
- "Find zones near major airports"
- "Neighborhoods with nightlife and entertainment"
- "Tourist-heavy areas with cultural attractions"

---

### Step 4: Drill down — Call a reusable function (ucfunc-dev)

**Prompt:** "What are the top zones in Manhattan by trip count?"

**What happens:** The agent calls `top_zones('Manhattan')` which returns the 10 busiest Manhattan zones with trip counts, avg fares, and avg distances.

**Talking point:** UC Functions MCP exposes registered SQL functions as callable tools. Unlike raw SQL, these are curated, tested, and documented — like an API layer over your data. The function encapsulates the join logic so the agent doesn't need to know the schema.

**Follow-up prompts to try:**
- "What's the average fare in Brooklyn?" → calls `avg_fare_by_borough('Brooklyn')`
- "Give me the full summary for zip code 10018" → calls `trip_summary(10018)`

---

### Step 5: Tie it together — Join insights with SQL (dbsql-dev)

**Prompt:** "Write a SQL query that combines trip statistics with zone descriptions for the business traveler zones Vector Search found"

**What happens:** The agent writes a JOIN query using the zip codes from the VS results (10154, 10017, 10171, 10152, 10119), pulling trip counts, average fares, distances, and description previews into a single result set.

**Example result:**

| Zone | Trips | Avg Fare | Avg Distance |
|------|-------|----------|-------------|
| Grand Central / Midtown East | 694 | $11.31 | 2.37 mi |
| Gramercy / Flatiron | 675 | $10.91 | 2.16 mi |
| Midtown East / Park Avenue | 244 | $11.90 | 2.64 mi |
| Midtown East / UN Area | 197 | $12.04 | 2.61 mi |
| Midtown East / 52nd Street | 116 | $10.13 | 2.05 mi |

**Talking point:** This is the composability payoff. The agent used Vector Search to find semantically relevant zones, then SQL to enrich those results with structured metrics. No single tool could do both — but together, they give the agent capabilities that match a human analyst's workflow.

---

## Key Takeaways

1. **Each MCP has a purpose** — SQL for precision, Genie for natural language, VS for semantics, UC Functions for reusable logic
2. **Composability is the superpower** — the agent chains MCPs together, using output from one as input to another
3. **Unity Catalog is the foundation** — all four MCPs operate on the same governed data in Unity Catalog. Permissions are always enforced.
4. **No code changes needed** — these are managed services. Point the MCP at your catalog/schema and the tools appear automatically.

## Troubleshooting

- **OAuth redirect error**: Each MCP needs a fixed callback port registered in the Databricks OAuth app. Ports 8091-8094 are configured for the four MCPs.
- **VS index not ready**: The Delta Sync index takes a few minutes after creation. Check status with `databricks vector-search-indexes get-index bu1_dev.mcp_demo.zone_descriptions_index --profile dev`.
- **Genie pending warehouse**: First query may take 10-20s while the SQL warehouse starts. Subsequent queries are faster.
- **ucfunc-dev not connecting**: UC Functions MCP may require separate OAuth consent. Check `/mcp` status in Claude Code.
