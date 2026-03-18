# Machine Learning at Scale with Databricks Mosaic AI

Workshop by Jose Alfonso (Senior Solutions Architect), Lucas Bruand (Specialist Solutions Architect - ML/GenAI), and Thomas Bayzelon (Delivery Solutions Architect).

---

## Databricks Overview

- 10,000+ global customers
- $2.4B+ in annual revenue
- $14B+ in investment
- Inventor of the lakehouse and pioneer of generative AI
- Gartner Magic Quadrant Leader: 2023 Cloud Database Management Systems
- Gartner Magic Quadrant Leader: 2024 Data Science & Machine Learning
- Creator of Apache Spark, Delta Lake, MLflow, and analytic stream processing

---

## The Data Lakehouse

An open, unified foundation for all your data.

- Data warehousing
- Data science and AI
- ETL and real-time analytics
- Orchestration
- Unified security, governance, and cataloging
- Unified data storage for reliability and sharing
- All raw data (logs, texts, audio, video, images) on an open data lake

### Lakehouse Adoption

Databricks pioneered the lakehouse architecture in 2020. It has seen tremendous adoption since then -- 74% of global CIOs report that they have a lakehouse in their estate (MIT Technology Review Insights, 2023). Almost all of the remainder intend to have one within the next three years.

Key products within the lakehouse:

- **Databricks SQL** -- Data warehousing
- **Mosaic AI** -- Data science & AI
- **Spark Declarative Pipelines** -- ETL & real-time analytics
- **Workflows** -- Orchestration
- **Unity Catalog** -- Unified security, governance, and cataloging
- **Delta Lake** -- Unified data storage for reliability and sharing

---

## Data Intelligence Platform

While lakehouse adoption has become a force in the market, generative AI has been another rapidly rising technology. With the MosaicML acquisition, Databricks brought these two technologies together to create a new category of data platform: the **Data Intelligence Platform**. It opens up a whole new world of possibilities to democratize data and AI across an organization.

The Data Intelligence Platform is rooted in a lakehouse -- the unification of data and governance is foundational to making it work.

### DatabricksIQ

DatabricksIQ is the AI-powered data intelligence engine that understands the semantics of your data and uses that understanding across everything in the platform. It gets smarter with every workload brokered by Unity Catalog.

Examples of DatabricksIQ in action:

- **Unity Catalog**: Securely find data and understand tables with natural language that uses your company jargon. With 500,000+ tables at Databricks, finding the right one is a challenge -- the Intelligence Engine guides developers to the right data by asking.
- **Delta Lake**: Automatically optimizes data layout based on usage patterns -- no manual indexing or partitioning.
- **Databricks SQL**: Text-to-SQL lets analysts specify queries in natural language; Databricks generates the code. Also supports Text-to-Viz.
- **Workflows**: Automatically selects the right instances and start time; handles auto-scaling and error remediation. Job cost is optimized based on past runs.
- **Spark Declarative Pipelines**: Automated data quality monitoring; detects when model quality is skewing, flags it, and assists in remediation.
- **Mosaic AI**: Build your own generative AI applications; create, tune, and serve custom LLMs.

### Data and AI for All (AI/BI)

How do we really democratize data and AI for everyone in the organization? Many teams know what they want from data but lack the skills to get answers.

This is where the Intelligence Engine shines: anyone in the org can use natural language through a simple interface to get answers and visualizations. No servers, no notebooks, no code -- just questions and accurate answers. This extends to Finance, Operations, Marketing, and Customer Service.

---

## Challenges Building AI Applications

1. **AI is difficult and requires experts**: Projects are slow to deploy and often fail before going into production.
2. **Most AI problems are data problems**: Models require fresh and high-quality datasets to deliver good performance.
3. **Your platform constantly needs new AI capabilities**: Staying competitive requires new tooling -- vector search, RAG, LLMs, etc.
4. **Productionizing, maintaining, and governing AI projects is expensive**: Governance, MLOps/LLMOps, and production-readiness are difficult.

With the rise of GenAI, building DS, ML, and AI applications has never been so complex. Having a state-of-the-art AI platform is not enough -- you need the full data capabilities: ingestion, analysis, governance, traceability, data quality, monitoring. This is what makes AI projects hard and expensive, and why most struggle to deliver value in production.

---

## AI Applications Made Simple by Databricks

1. **Simple, low-code approach**: AutoML and AI-powered assistant guiding you. De-risk and accelerate projects to production with the Databricks Expert team.
2. **Integrated with your data platform**: Benefits from simple data ingestion, data monitoring, governance, and security layers.
3. **State-of-the-art AI capabilities**: Mosaic AI makes model development and operationalization simple, accessible, and affordable -- for both traditional ML/DL models and LLMs.
4. **Built-in governance and lineage**: Ensures auditability by simplifying operational tasks for any AI workload.

Key capabilities: Feature Store, Managed Vector Search, Foundation Models, LLM Fine-tuning APIs, RAG & GenAI Apps, MLflow Evaluation, Model Serving, Model Monitoring.

Databricks solved the AI complexity problem by bringing together Data + AI + Governance in a single, unified platform. With the acquisition of MosaicML ($1.3B), Databricks is one of the leaders in the LLM market, providing state-of-the-art GenAI capabilities including model training/fine-tuning, GenAI apps with RAG and vector search, and more.

---

## End-to-End AI Platform

Mosaic AI works for all types of AI: classical ML, deep learning, generative AI (including RAG and agents).

### Platform Capabilities

| Stage                       | Components                                                                                                                  |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Data Platform**           | Delta Tables (structured), Files/Volumes (unstructured), Open Data Lake                                                     |
| **Governance**              | Unity Catalog, Feature Store in UC, Model Registry in UC, Delta Sharing, Models in Marketplace                              |
| **Prepare Data & Vectors**  | Spark Declarative Pipelines, Notebooks, SQL, Vector Search, Feature Serving, Function Serving                               |
| **Build & Evaluate Models** | AutoML, MLflow Track & Evaluate, AI Playground, Agent Framework & Evaluation, Model Training, AI Functions, Models from SQL |
| **Serve Applications**      | Model Serving, Databricks Apps, Batch and Stream Inference, AI Gateway                                                      |
| **MLOps + LLMOps**          | MLflow, Databricks Asset Bundles (DABs), CI/CD support, Lakehouse Monitoring                                                |

### Data-centric AI

- **Gen AI**: Custom models, model serving, RAG
- **End-to-end AI**: MLOps (MLflow), AutoML, Monitoring, Governance

You can build models from scratch or tune existing models on your data to maintain privacy and control. Databricks can serve those models efficiently and help you do RAG to build conversational agents with APIs like OpenAI.

Databricks AI covers the end-to-end AI workflow: transparent AutoML to find the best model quickly, monitoring of models in production, and governing models to ensure reproducibility and compliance. Built on the open foundation of MLflow, it integrates well with the AI ecosystem.

### Focus Areas

1. **Increase data team productivity**: Use the tools, languages, and frameworks of choice on one platform.
2. **High quality data, readily accessible**: High quality datasets discoverable in one place and from any source.
3. **Standardize the full ML lifecycle**: Seamlessly and securely move models from experimentation to production.

---

## Governance

### Unity Catalog

Unified governance for data and AI:

- Unified visibility into data and AI
- Single permission model for data and AI
- AI-powered monitoring and observability
- Open data sharing

Assets governed: Tables, Files, Models, Notebooks, Dashboards.

Capabilities: Monitoring, Auditing, Discovery, Data Sharing, Access Controls, Lineage.

### Governed Namespace

Unity Catalog provides a governed namespace across file and database sources. Access legacy metastore and foreign databases powered by Lakehouse Federation.

```sql
SELECT * FROM main.paul.red_wine;                           -- <catalog>.<database>.<table>
SELECT * FROM hive_metastore.default.customers;
SELECT * FROM snowflake_warehouse.some_schema.some_table;
```

Hierarchy: Catalog > Schema (Database) > Tables / Views / Models / Functions / Volumes.

### Models in Unity Catalog

The Model Registry is now provided via Models in Unity Catalog. The benefits of Unity Catalog are applied to ML models:

- Centralized access control
- Auditing
- Lineage
- Model sharing and discovery across workspaces

### Volumes

Volumes catalog collections of files in Unity Catalog:

- Access, store, organize, and process non-tabular data with Unity Catalog governance
- Unlock new processing capabilities for arbitrary files, including data science and machine learning
- Any file format; data can be structured, semi-structured, or unstructured
- Files accessible via UI, Spark APIs, FUSE, dbutils, REST, SQL, Databricks CLI, Terraform

Volumes contain directories and files for data stored in any format. Before Volumes, Unity Catalog did not provide suitable affordances for working with arbitrary files. Use cases include:

- Exploratory data science (users bringing their own data files)
- Running ML algorithms on unstructured data (image, audio, video, PDF)
- Processing files requiring local file system access on cluster machines
- Storing and providing secure access to library and config files (.jar, .whl, .txt)
- Transforming and querying non-tabular data in early ETL pipeline stages

**Managed Volumes** leverage already available storage space in UC and are fast to set up -- convenient for provisioning team, project, or personal storage space. **External Volumes** are helpful for pre-existing data in cloud storage, making data accessible from Databricks without copying.

---

## Build Production ETL Pipelines with Spark Declarative Pipelines

Spark Declarative Pipelines (SDP) allows analysts and data engineers to build production-ready streaming or batch ETL pipelines in SQL and Python.

SDP captures a declarative description of full data pipelines to understand dependencies live and automate away virtually all operational complexity. Data engineers and analysts can concentrate on writing data transformations and expressing data quality requirements.

Pipeline architecture follows the medallion pattern:

- **Bronze Layer**: Raw ingestion (Streaming Tables from Cloud Storage, Message Queues)
- **Silver Layer**: Cleaned and joined data (e.g., customer_orders as Materialized View)
- **Gold Layer**: Business-level aggregates (e.g., daily_orders as Materialized View)

Key capabilities:

- Automatic error handling and recovery from failures
- Granular pipeline observability with high-fidelity lineage diagrams
- Dependency tracking and aggregated data quality metrics
- Modern software engineering practices: separate dev/prod environments, parameterization, unit testing, documentation
- Full integration with Databricks Lakehouse (schedule with a click or set to continuous mode)
- Photon engine for performance
- Unity Catalog integration for governance

---

## Feature Engineering

### Why Feature Tables?

Without feature tables:

- No reuse of features across projects
- Online/offline skew between training and serving

With feature tables:

- Single source of truth prevents offline/online skew
- Data scientists can discover and reuse features
- Supports both batch and online serving

### Feature Engineering with Unity Catalog

Without Unity Catalog, each workspace has its own isolated Feature Store, user management, metastore, and access controls.

With Unity Catalog, any Delta table with a primary key is a Feature Table. Unity Catalog provides a centralized Feature Store across all workspaces with unified user management, metastore, foreign databases, and access controls.

### Offline Features (Training & Batch Scoring)

- **When to use**: Training (most models, many rows), Scoring (non-real-time, many rows)
- In UC, any Delta Table with a Primary Key is an Offline Feature
- ML Models logged with FeatureEngineering Client can do automatic Feature lookups and On-Demand Features performed by Clusters

### Online Features (Real-Time Serving)

- **When to use**: Scoring (real-time model serving, low latency feature and data serving, on-demand features)
- A table must be published to an Online Store (Databricks Online Tables / CosmosDB / DynamoDB)

### Feature & Function Serving

- If you use **Databricks Model Serving**: ML Models logged with FeatureEngineering Client will automatically access Features from Online Stores.
- If you use **external serving** (AzureML / SageMaker / DIY): Use Databricks Feature and Function Serving.
- Both products support feature lookup for pre-computed features and on-demand feature transformations.

---

## Databricks Marketplace

Open marketplace for all your data, analytics, and AI, powered by Delta Sharing.

**For Providers**:

- Share data securely and reach users on any platform
- Exchange more than just data -- share tables, volumes/files, notebooks, dashboards, and AI models
- Generate leads from Databricks' 10,000+ customer base
- Selectively share content via private exchanges

**For Consumers**:

- Discover more than just data
- Evaluate data products faster
- Avoid vendor lock-in
- Obtain data sets and AI/analytical assets without proprietary platform dependencies, complicated ETL, or expensive replication

Asset types: Data Tables, Data Files, Notebooks, Dashboards, AI Models, Solution Accelerators, Apps.

---

## Build & Evaluate Models

### MLflow for Deep Learning

MLflow's enhanced UI for training models:

- **Usability**: New tutorials/docs, seamless login, improved search
- **Logging**: System metrics, async + batch logging, support for 1M steps/iterations, more autologging support
- **Visualization**: Run details redesign, metric aggregation, chart grouping, improved DL charts

### ML Runtime

Databricks Machine Learning Runtime provides:

- Optimized and pre-configured ML frameworks (scikit-learn, TensorFlow, PyTorch, XGBoost, LightGBM, etc.)
- Built-in model explainability (SHAP, LIME, etc.)
- Turnkey distributed ML (distributed training support)
- Built-in AutoML and hyperparameter tuning (Hyperopt)
- GPU support out of the box

### AutoML

A glass-box solution that empowers data teams without taking away control.

AutoML tests different models, tunes hyperparameters, and returns:

1. **MLflow Experiment**: Auto-created to track models and metrics
2. **Data Exploration Notebook**: Generated with feature summary statistics and distributions
3. **Reproducible Trial Notebooks**: Generated source code for every model -- the key "glass-box" feature

AutoML solves two key pain points:

- **Quickly verify predictive power of a dataset**: Usually takes ~2 days manually; AutoML accelerates this dramatically
- **Get a baseline model to guide project direction**: Provides a benchmark to aim to beat

Support: Classification, Regression, Time Series Forecasting. Features: Numerical, Categorical, Timestamp, Text. Deployment: Batch Scoring, Model Serving.

Most AutoML solutions are an "opaque box." Databricks AutoML provides a transparent way for users to see how a model was trained, learn how to use Databricks features like MLflow, and provides the training notebook for easy modification.

---

## Serve

### Databricks Model Serving

Scalable deployment for traditional and large-language ML models:

- Unified interface to manage all deployed models
- Secure data access via integration with Vector Search and Feature Store
- Govern and monitor usage of models
- Reduce costs with auto-scaling and optimized endpoints
- High availability and low latency for production use

Model types supported:

| Type                      | Description                                      |
| ------------------------- | ------------------------------------------------ |
| **Custom Models**         | Your own trained models (sklearn, PyTorch, etc.) |
| **Foundation Model APIs** | Databricks-managed foundation models             |
| **External Models**       | Third-party models (OpenAI, Anthropic, etc.)     |

Access any AI model through a unified interface (single API, SDK, and UI). Govern and monitor all models in one place.

### Mosaic AI Gateway

Centralized governance and routing for AI model endpoints.

### AI Functions for Databricks SQL

Access proprietary and open-source LLMs directly within Databricks SQL:

```sql
SELECT
  sku_id,
  product_name,
  ai_query(
    "my-external-openai-chat",
    "You are a marketing expert for a winter holiday promotion targeting GenZ.
     Generate a promotional text in 30 words mentioning a 50% discount for product: "
     || product_name
  )
FROM uc_catalog.schema.retail_products
WHERE inventory > 2 * forecasted_sales
```

Use cases: classify data with LLMs, generate product descriptions, summaries, and more.

### Lakehouse Monitoring

Automated insights and out-of-the-box metrics on features and ML pipelines:

- Fully managed -- no time wasted managing infrastructure, calculating metrics, or building dashboards
- Frictionless setup with out-of-the-box metrics (profiling, drift, custom) and generated dashboards
- Unified solution for both data/features and models

Monitors: Time Series Tables, Feature Tables, Inference Tables (from Model Serving or batch scoring pipelines).

### Batch Inference with SDP

Data scientists can automatically generate notebooks for performing batch inference on streaming/live data, including Spark Declarative Pipelines.

### Databricks Apps

Build and deploy custom data apps:

- **Open Python frameworks**: Dash, Streamlit, Flask, Gradio
- **Easy to host**: Click to deploy to managed serverless compute
- **Easy to share**: Share with non-workspace users via SCIM sync
- **Easy to secure**: Built-in OAuth, run as viewer with access to Unity Catalog

Apps run on secure serverless compute as containerized code with a dedicated app service principal (no access to resources by default).

---

## MLOps

### MLOps = DataOps + DevOps + ModelOps

MLOps is the set of processes and automation for managing data, code, and models to improve performance stability and long-term efficiency in ML systems.

Various personas collaboratively contribute to the flow and orchestration of end-to-end ML processes: from data prep through EDA and feature engineering, to model development, training, validation, deployment, and monitoring/governance of data and AI assets over time.

### Environment Isolation

Assets (Code, Data, Model) flow through three environments:

| Environment | Trust/Quality | Access      |
| ----------- | ------------- | ----------- |
| **Dev**     | Low           | Open        |
| **Staging** | Medium        | Restricted  |
| **Prod**    | High          | Locked-down |

AI assets are developed in dev, tested in staging, and deployed to production. Trust, quality, and testing increase from dev to prod, while openness of access decreases.

### Deployment Patterns: Deploy Code vs. Deploy Models

**Deploy Model approach**: The model is tested and moved through environments, but code is not tested across environments. Training code is developed in dev; inference/monitoring code must be developed in prod.

**Deploy Code approach (recommended)**: All pipelines for different stages of the model lifecycle are developed in dev, then promoted through staging and prod.

Benefits of deploying code:

- **Automation**: Supports automated retraining in locked-down environments
- **Data access control**: Only production environment needs read access to production training data
- **Reproducible models**: Engineering control over training environment simplifies reproducibility
- **Support for large projects**: Forces modular code and iterative testing, helping coordination

### MLOps on Databricks -- Architectural Flow

1. **Dev workspace**: Access production data (read-only) to develop model training, validation, deployment, and monitoring code. Track models via MLflow.
2. **Staging (CI)**: Create a dev branch, commit code, and submit a Pull Request. Continuous Integration triggers unit tests and integration tests.
3. **Production (CD)**: Upon successful tests, merge to main. Cut a release branch using continuous deployment. This trains the model, validates it, creates a model serving endpoint with inference table enabled, and optionally performs batch inference.
4. **Monitoring**: Track input data drift and model performance metrics. If performance degrades, trigger retraining automatically inside the production environment.
5. **Champion/Challenger**: Each retrained model gets a "challenger" alias tested alongside the main "champion" version, allowing human-in-the-loop decisions for deploying new model versions.

### Databricks Workflows

Scheduling and orchestration made simple. Build sophisticated workflows inside your Databricks workspace.

**Tasks** (units of orchestration in a Job):

- Databricks Notebooks, Python Scripts, Python Wheels, SQL Files/Queries, SDP Pipelines, dbt, Java JARs, DBSQL Dashboards, Spark Submit

**Task source**: Remote Git Repository (simplifies CI/CD) or Databricks Workspace.

**Control flows**:

- Sequential, Parallel
- Conditionals (Run If): All Succeeded, At Least 1 Succeeded, None Failed, All Done, At Least 1 Failed, All Failed

**Triggers**: Manual, API, Scheduled (Cron), File Arrival, Delta Table Update, Continuous (Streaming)

**Compute options**: Interactive Clusters, Serverless, Job Clusters (~50% cheaper), Job Cluster Re-Use, Repair & Re-run

**Additional capabilities**:

- Install external libraries (PyPI, Maven, CRAN, Workspace, DBFS, upload)
- Email notifications and alerts for late/long-running jobs
- Configurable retries for failed runs
- Repair and re-run only failed tasks (saves time and money)
- Job Parameters, Job Contexts (run_id, job_id, start_time), Task Values (custom parameters shared between tasks)
- Webhooks (Slack, custom) for job lifecycle events (start, success, failure)

### Databricks Asset Bundles (DABs)

YAML files that specify the artifacts, resources, and configurations of a Databricks project. Install the Databricks CLI and deploy bundles from your CI/CD server or trigger with Git Actions.

**Bundle definition includes**:

- **Workspace**: Name and default workspace
- **Code**: Notebooks, Python .whl, JARs, dbt, etc.
- **Resource configurations**: Jobs, SDP Pipelines, MLflow, etc. (follows REST API schema)
- **Environment-based specs**: Control project behavior in different environments (variables, config overrides)

**Deployment flow**:

| Environment | Cluster         | Schedule    | Identity          |
| ----------- | --------------- | ----------- | ----------------- |
| Dev         | Single Node     | No Schedule | Run as User       |
| Staging     | 3 Node Cluster  | Weekly      | Service Principal |
| Prod        | 10 Node Cluster | Daily       | Service Principal |

```bash
databricks bundle deploy -t "dev"
databricks bundle run pipeline -refresh-all -t "dev"
```

Each user can deploy from local CLI to dev (deployments automatically separated). CI/CD pipeline uses a service principal. Use the `validate` command to check syntax correctness.

**Alternative deployment options**: Python SDK (Jobs API), Terraform Provider (databricks_jobs resource), Databricks REST API.

### MLOps Stacks

Turnkey deployment of ML projects on Databricks with CI/CD. Automates the creation of infrastructure for an ML project.

Includes:

- ML pipelines for model training, deployment, and inference deployed using DABs
- Feature tables
- CI/CD (GitHub and Azure DevOps supported)
- Uses software development best practices, flexible to customization

---

## Developer Experience

### Databricks Notebook

- **Multi-language**: Python, SQL, Scala, and R in one notebook
- **Collaborative**: Real-time co-presence, co-editing, and commenting
- **Reproducible**: Automatic version history tracking, Git version control with Repos
- **Adaptable**: Install standard libraries and use local modules
- **Jupyter-compatible**: Use the Jupyter ecosystem in the Notebook
- **Ideal for exploration**: Built-in charts and data profiles
- **Enterprise-ready**: Enterprise-grade access controls, identity management, auditability
- **Get to production faster**: Schedule notebooks as jobs or create dashboards from results

### Data Exploration

- Create interactive charts to visualize data with two clicks
- Summarize a dataset's properties and statistics with data profiles at the push of a button

### SQL Warehouse in Notebooks

- Run SQL workloads against a SQL warehouse within the Notebook
- Schedule Notebooks to run as Jobs using SQL warehouses
- Create Notebook Dashboards that run queries using SQL warehouses

### Context-Aware Authoring Assistant

- **Complete**: Suggestions-as-you-type
- **Generate**: Natural language prompt to code/SQL
- **Explain**: Highlight a query and get an explanation in plain English
- **Debug**: Explain and fix syntax and runtime errors with a single click
- **Transform/Optimize**: Convert languages; RDD to DataFrame; Pandas to PySpark; performance improvements

### Python SDK

Automate all operations on the Databricks Workspace from Python.

### VS Code and PyCharm Extensions

- Simple setup from the VS Code and PyCharm Marketplace
- Native IDE experience with full productivity features
- Execute batch workloads or start interactively debugging from your IDE

### Databricks Connect 2.0

Redesigned using the decoupled client-server architecture of Spark Connect. Run Apache Spark remotely on a Databricks cluster instead of in a local Spark session.

- Run large-scale Spark jobs from any Python application
- Step through and debug code in any IDE with remote clusters
- Isolated client sessions maintain progress if clusters restart or dependencies change
- Fully integrated with Unity Catalog governance (fine-grained access control, data lineage)
- Easy setup: `pip install databricks-connect>=13.0`
- No code adaptation apart from a connection string
- Always released with new DBR versions (starting from DBR 13)

---

## Parallelizing Machine Learning on Databricks

### ML Pipeline Stages

Data Preparation > Training > Tuning > Inference

### Scale Challenges

| Stage                | Problem                                                            | Solution                                                            |
| -------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- |
| **Data Preparation** | Slow or out-of-memory errors with large data                       | Use Spark to distribute data and transformations                    |
| **Training**         | Slow or out-of-memory errors                                       | Use Spark to distribute data; use Spark ML's distributed algorithms |
| **Tuning**           | Training many models with different hyperparameters takes too long | Use a cluster to parallelize training of individual models          |
| **Inference**        | More records = longer inference; latency issues                    | Distribute inference across the cluster                             |

Historical insight: One of the best things you can do to improve model performance is train on more data (Banko & Brill, 2001: "Scaling to Very Very Large Corpora for Natural Language Disambiguation").

### Compute Patterns

| Pattern                     | Scope       | Tools                                                                      | Description                                                                                                |
| --------------------------- | ----------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Parallel HPO**            | Single Node | Hyperopt (SparkTrials), Spark ML CV                                        | Evaluate multiple hyperparameter configurations in parallel; works with any ML library                     |
| **Parallel Model Training** | Single Node | pandas_udf                                                                 | Create multiple unique model versions in parallel (e.g., per store, per device); works with any ML library |
| **Data-Parallel Training**  | Multi Node  | Spark ML, LightGBM, XGBoost4J, PySpark Distributors (TensorFlow & PyTorch) | Distribute training of a single model across multiple nodes using Spark or MPI-based frameworks            |

### PySpark Pandas for Distributed Data Prep

The typical data scientist journey: Education teaches pandas > analyze small datasets with pandas > hit scale limits > need Spark DataFrames.

Key differences between pandas and PySpark DataFrames:

| Aspect         | pandas                        | PySpark                                                       |
| -------------- | ----------------------------- | ------------------------------------------------------------- |
| Mutability     | Mutable                       | Immutable                                                     |
| Execution      | Eager                         | Lazy (Catalyst Optimizer)                                     |
| Add column     | `df['c'] = df['a'] + df['b']` | `df = df.withColumn('c', df['a'] + df['b'])`                  |
| Rename columns | `df.columns = ['a','b']`      | `df = df.toDF('a', 'b')`                                      |
| Value counts   | `df['col'].value_counts()`    | `df.groupBy('col').count().orderBy('count', ascending=False)` |

**PySpark Pandas API** (formerly Koalas): Provides the pandas API on top of Apache Spark. Unifies the two ecosystems with a familiar API for seamless transition between small and large data. Part of Apache Spark 3.2+.

```python
from pyspark.pandas import read_csv
pdf = read_csv("data.csv")
```

Case study: Virgin Hyperloop One achieved more than 10x faster processing with less than 1% code changes using Koalas.

### Spark ML for Distributed Model Training

Scikit-learn is a popular single-node ML library, but when data or models get too big, Spark ML allows distributed training across multiple workers.

- **MLlib**: Original Spark ML API (RDD-based, maintenance mode)
- **Spark ML**: Newer API (DataFrame-based, actively developed)

Key Spark ML concepts:

**Vector Assembly**: Most Spark ML models accept a vector column as input. Use VectorAssembler to combine feature columns.

**Efficient representations**: Spark uses SparseVector when there are many zeros.

```
DenseVector(0, 0, 0, 7, 0, 2, 0, 0, 0, 0)
SparseVector(10, [3, 5], [7, 2])
```

**Pipelines**: Chain transformers and estimators (Imputer > StringIndexer > OneHotEncoder > VectorAssembler > LinearRegression). Fit on training data, transform on test data.

### Pandas UDF for Group-Specific Model Training

Train one model for each group of rows (defined by column values):

- Energy/Manufacturing: Model for each IoT device
- Retail/CPG: Model for each store/product/customer
- Finance: Model for each stock symbol
- Healthcare: Model for each metric in a health-tracking app

Uses the split-apply-combine pattern with Pandas Function APIs to parallelize group-specific training across the cluster.

**Pandas Function APIs** vs. Pandas UDFs:

- Built into Spark DataFrame APIs (no separate registration)
- Do not require type hints
- Flexible output length

---

## Databricks SQL

First-class SQL development experience: collaboratively query, explore, and transform data in-place. Query data lake data using familiar ANSI SQL. Built-in SQL query editor, alerts, visualizations, and interactive dashboards.

Features: query sharing/reuse, snippets, result caching, scheduled refreshes, alerts on data changes, drag-and-drop dashboards.

---

## Certification & Learning

### Databricks Certified ML Associate & Professional

Certification helps you gain industry recognition, competitive differentiation, greater productivity, and business results. More info: databricks.com/learn/certification

### Databricks Academy

New link: customer-academy.databricks.com -- full list of courses available.

### The Big Book of MLOps

Deep dive on MLOps best practices. Available for download from Databricks.
