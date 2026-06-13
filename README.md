# Graph-RCA Agent

**AI-Powered Root Cause Analysis (RCA) for pytest Test Failures**

An intelligent agent that automatically diagnoses pytest test failures by leveraging a Neo4j knowledge graph, advanced LLM analysis (Google Gemini), and GraphRAG-inspired context retrieval. This project demonstrates a proof-of-concept approach to automated root cause analysis for software testing.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture & Design](#architecture--design)
- [Data Model](#data-model)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Example Walkthrough](#-example-walkthrough-test_login-scenario)
- [Dashboard UI Guide](#-dashboard-ui-guide)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Project Status](#-project-status)

## 🎯 Overview

**Graph-RCA** is an **incomplete, proof-of-concept system** that combines:
- **Neo4j Knowledge Graph**: Stores relationships between test cases, components, requirements, and historical bug reports
- **Google Gemini 2.5 LLM**: Analyzes failure logs with AI-powered diagnostics
- **GraphRAG Retrieval**: Enriches prompts with contextual graph data for more accurate RCA
- **Streamlit Dashboard**: User-friendly web interface for interactive failure analysis
- **pytest Integration**: Automatic failure detection and analysis via pytest hooks

The agent generates structured RCA reports containing root causes, impacted components, historical bug references, suggested fixes, and confidence scores.

---

## 🏗️ Architecture & Design

### System Flow

```
pytest Test Failure
        ↓
    conftest.py Hook (pytest_runtest_makereport)
        ↓
    RCAAgent Initialization
        ↓
    Neo4j Graph Context Retrieval (get_test_context)
        ↓
    Enriched Prompt Construction
        ↓
    Google Gemini 2.5 Analysis
        ↓
    Structured RCA Report Generation (RCADiagnosisSchema)
        ↓
    Database Write-Back (save_failure_analysis)
        ↓
    User Output (CLI / Streamlit Dashboard)
```

### Key Components

| Component | Purpose |
|-----------|---------|
| **RCAAgent** (`app/agent/rca_agent.py`) | Core agent logic; orchestrates LLM analysis |
| **Neo4jGraph** (`app/graph/query_graph.py`) | Database abstraction layer; retrieves and persists graph data |
| **conftest.py** | pytest hook for automatic failure detection and analysis |
| **Dashboard** (`app/ui/dashboard.py`) | Streamlit web UI for interactive RCA |
| **Schema Classes** | Pydantic models defining RCA report structure |

### How It Works

1. **Test Execution**: pytest runs your test suite
2. **Failure Detection**: `conftest.py` hook catches any test failure
3. **Context Retrieval**: Neo4j graph is queried for related test metadata (components, requirements, historical bugs)
4. **Prompt Enrichment**: Failure log + graph context → detailed prompt
5. **AI Analysis**: Google Gemini analyzes the enriched prompt using `RCADiagnosisSchema`
6. **Report Generation**: Structured RCA result with root cause, component, fix, and confidence
7. **Persistence**: Analysis results stored back in Neo4j as `FailureAnalysis` nodes
8. **User Presentation**: Results displayed in CLI or Streamlit dashboard

---

## 🗂️ Data Model

### Graph Structure

The Neo4j knowledge graph is organized into **28 nodes** across **4 node types** with **21 relationships** connecting them:

```
Node Types (28 total):
├── TestCase (blue)
├── Component (olive)
├── Requirement (yellow)
└── BugReport (green)

Relationships (21 total):
├── TESTS: TestCase → Component
├── IMPACTS: BugReport → Component
├── VALIDATED_BY: Requirement → TestCase
└── Additional tracking relationships
```

### Property Keys

All nodes use the following key properties:
- **`id`**: Unique identifier for the node
- **`name`**: Human-readable name/label
- **`issue`**: For BugReport nodes, describes the historical issue

### Graph Nodes & Relationships

The Neo4j knowledge graph organizes test artifacts as nodes with relationships:

```
TestCase
├── TESTS → Component
├── VALIDATED_BY ← Requirement
└── ← ANALYZED_BY FailureAnalysis

Component
├── ← TESTS TestCase
└── ← IMPACTS_COMPONENT FailureAnalysis

Requirement
└── VALIDATED_BY → TestCase

BugReport
├── IMPACTS → Component
└── related_bug (property used in context)

FailureAnalysis
├── ANALYZED_TEST → TestCase
└── IMPACTS_COMPONENT → Component
```

### Node Properties

**TestCase**
- `id`: Unique identifier
- `name`: Test name (e.g., "test_login")
- Additional metadata as needed

**Component**
- `id`: Unique identifier
- `name`: Component/module name (e.g., "AuthService")
- `description`: Optional component details

**Requirement**
- `id`: Unique identifier
- `name`: Requirement description
- Additional details as needed

**BugReport**
- `id`: Unique identifier
- `issue`: Description or issue ID of historical bug (e.g., "Token expiry mismatch")
- `severity`: Bug severity level (optional)

**FailureAnalysis**
- `root_cause`: Identified root cause (e.g., "AuthService returning 500 due to token validation issue")
- `impacted_component`: Component affected (e.g., "AuthService")
- `historical_bug`: Related historical bugs (e.g., "Token expiry mismatch")
- `suggested_fix`: Actionable fix recommendation with code/config changes
- `confidence_score`: 0-100 confidence level (e.g., 95)
- `timestamp`: When analysis was performed

---

## ✨ Features

- ✅ **Automatic Test Failure Detection**: pytest hook captures failures in real-time
- ✅ **Contextual Analysis**: Neo4j graph provides rich context for accurate diagnosis
- ✅ **AI-Powered RCA**: Google Gemini generates intelligent diagnostics
- ✅ **Structured Output**: Pydantic schema ensures consistent, parseable reports
- ✅ **Historical Tracking**: Failure analyses persisted in graph for trend analysis
- ✅ **Interactive Dashboard**: Streamlit UI for manual RCA queries
- ✅ **Confidence Scoring**: AI assigns confidence level to each diagnosis
- ✅ **Real Working Example**: Includes `test_login` scenario with pre-populated Neo4j graph (28 nodes, 21 relationships)

### Pre-Populated Database

The system comes with an **example knowledge graph** containing:

- **28 Nodes**: TestCase, Component, Requirement, and BugReport nodes representing a real software testing scenario
- **21 Relationships**: TESTS, IMPACTS, VALIDATED_BY relationships connecting components, requirements, and tests
- **Example Domain**: Authentication service (AuthService) with token management workflows
- **Real Failure**: `test_login` scenario with historical bug tracking ("Token expiry mismatch")

---

## 🚀 Installation

### Prerequisites

- **Python 3.9+**
- **Neo4j Database** (local, Docker, or Aura cloud instance)
- **Google API Account** with Gemini access
- **Git**

### Step 1: Clone the Repository

```bash
git clone https://github.com/SumanthReddyV/GraphRCA-Graph-Based-Root-Cause-Analysis-System.git
cd graph-rca-agent
```

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Current dependencies:
- `pytest==7.4.0` - Test framework
- `python-dotenv==1.2.2` - Environment variable management
- `google-genai` - Google Gemini SDK
- `neo4j` - Neo4j driver
- `streamlit` - Dashboard UI
- `pydantic` - Data validation

### Step 4: Set Up Neo4j Database

**Option A: Docker (Recommended)**

```bash
docker run -d \
  --name neo4j \
  -p 7687:7687 \
  -p 7474:7474 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest
```

Access Neo4j Browser at `http://localhost:7474`

**Option B: Local Installation**

Download from [neo4j.com](https://neo4j.com/download/) and follow setup instructions.

**Option C: Neo4j Aura (Cloud)**

Create a free cloud instance at [aura.neo4j.io](https://aura.neo4j.io)

### Step 5: Initialize Graph Schema (Optional)

If using an empty database, seed your graph with:

```cypher
// Create sample test case
CREATE (t:TestCase {name: "test_login"})

// Create component
CREATE (c:Component {name: "auth_service"})

// Link test to component
MATCH (t:TestCase {name: "test_login"}), (c:Component {name: "auth_service"})
CREATE (t)-[:TESTS]->(c)
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password

# Google Gemini API Configuration
GOOGLE_API_KEY=your_google_api_key_here
```

### Key Configuration Details

| Variable | Description | Example |
|----------|-------------|---------|
| `NEO4J_URI` | Neo4j connection string | `bolt://localhost:7687` or `neo4j+s://instance-id.databases.neo4j.io` |
| `NEO4J_USERNAME` | Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | Your secure password |
| `GOOGLE_API_KEY` | Google Gemini API key | From Google Cloud Console |

**⚠️ Security Note**: Never commit `.env` to version control. Add it to `.gitignore`.

---

## 💻 Usage

### 1. Quick Start: CLI Mode

Run the test agent directly:

```bash
python test_agent.py
```

**Expected Output:**
```
=== AI RCA REPORT ===

{
  "root_cause": "The AuthService is returning a 500 Internal Server Error during the login process, likely due to an issue with token generation or validation, specifically a 'Token expiry mismatch' as indicated by historical context.",
  "impacted_component": "AuthService",
  "historical_bug": "Token expiry mismatch",
  "suggested_fix": "Review the token generation and validation logic within AuthService, focusing on how token expiry times are set and checked. Ensure consistency between token creation and validation mechanisms. Example: Update token expiry logic to use a standardized time utility. For instance, if using JWTs, verify the 'exp' claim handling. Example snippet: 'jwt.encode(payload, secret, algorithm='HS256', expires_in=3600)' or ensure the validation function correctly handles 'jwt.decode(token, secret, algorithms=['HS256'])' without expiry-related errors.",
  "confidence_score": 95
}
```

### 2. Query Graph Context

Retrieve raw graph context for a test:

```bash
python test_query.py
```

**Expected Output:**
```
=== GRAPH CONTEXT ===

{'test': 'test_login', 'component': 'auth_service', 'related_bug': 'JIRA-4521', 'requirement': 'User authentication'}
```

### 3. Interactive Dashboard

Launch the Streamlit dashboard:

```bash
streamlit run app/ui/dashboard.py
```

Then:
1. Open `http://localhost:8501` in your browser
2. Enter test name (e.g., `test_login`)
3. Paste failure log (e.g., `AssertionError: Expected status code 200, Received 500 Internal Server Error`)
4. Click "Analyze Failure"
5. View the AI-generated RCA report with:
   - **Root Cause** (red section): Detailed explanation of the failure
   - **Impacted Component** (blue section): Which component is affected
   - **Historical Bug** (olive section): Related past issues
   - **Suggested Fix** (green section): Actionable remediation steps
   - **Confidence Score**: AI confidence level (0-100%)

**Real Dashboard Example:**
```
GraphRCA — AI Root Cause Analysis Agent

Input:
  Test Name: test_login
  Failure Log: AssertionError: Expected status code 200, Received 500 Internal Server Error

Output:
  Root Cause: The AuthService is returning a 500 Internal Server Error during the login 
              process, likely due to an issue with token generation or validation, 
              specifically a 'Token expiry mismatch' as indicated by historical context.
  
  Impacted Component: AuthService
  
  Historical Bug: Token expiry mismatch
  
  Suggested Fix: Review the token generation and validation logic within AuthService. 
                 Focus on how token expiry times are set and checked. Ensure consistency 
                 between token creation and validation mechanisms.
  
  Confidence Score: 95%
```

### 4. Automatic pytest Integration

Run pytest with automatic RCA on failures:

```bash
pytest app/tests/ -v
```

When a test fails, `conftest.py` hook automatically:
- Captures the test name and error log
- Invokes RCAAgent
- Displays RCA report
- (Optionally) persists to Neo4j

**Example pytest output with RCA:**
```
app/tests/test_auth.py::test_login FAILED

=== FAILURE DETECTED ===
Test: test_login
Error: AssertionError: assert 500 == 200

=== AI RCA REPORT ===
{
  "root_cause": "The login() function in auth.py is returning 500 instead of the expected 200 status code. This indicates an unhandled exception or error condition in the authentication logic.",
  "impacted_component": "AuthService",
  "historical_bug": "Related authentication failures",
  "suggested_fix": "Review the login() function implementation to understand why it's returning 500. Ensure error handling is in place and that the function returns the correct status codes.",
  "confidence_score": 95
}
```

---

## 📝 Example Walkthrough: `test_login` Scenario

### Test Case

The included example demonstrates RCA in action using a simple login test:

**Test File**: `app/tests/test_auth.py`
```python
from auth import login

def test_login():
    """Tests the login function returns success status (200)"""
    assert login() == 200  # This will fail; login() returns 500
```

**Implementation**: `app/tests/auth.py`
```python
def login():
    """Mock login function that returns error status"""
    return 500  # Intentional failure for demonstration
```

### RCA Analysis Flow

1. **Test Execution**:
   ```bash
   pytest app/tests/test_auth.py::test_login
   ```

2. **Failure Detected** by pytest hook:
   - Test: `test_login`
   - Error: `AssertionError: assert 500 == 200`

3. **Graph Context Retrieved** from Neo4j:
   ```
   Query Results:
   - TestCase: test_login
   - Component: AuthService
   - Related Bug: Token expiry mismatch
   - Requirement: User authentication flow
   ```

4. **Gemini Analysis** generates diagnosis:
   - Analyzes failure log + graph context
   - Generates structured RCA report
   - Assigns confidence score

5. **Report Output**:
   ```
   Root Cause: AuthService returning 500 during login due to token validation issues
   Impacted Component: AuthService
   Historical Bug: Token expiry mismatch
   Suggested Fix: Review token generation and validation logic...
   Confidence Score: 95%
   ```

This example demonstrates how the agent enriches a simple error with contextual graph information to provide intelligent diagnostics.

---

## 🎨 Dashboard UI Guide

The Streamlit dashboard provides an interactive interface for manual RCA analysis:

### Input Section

**Test Name**
- Text input field
- Example: `test_login`
- Matches TestCase nodes in Neo4j

**Failure Log**
- Multi-line text area
- Paste your pytest error output
- Example:
  ```
  AssertionError:
  Expected status code 200
  Received 500 Internal Server Error
  ```

### Analysis Output Section

The RCA report is displayed with color-coded sections:

| Section | Color | Content |
|---------|-------|---------|
| **Root Cause** | Red | Detailed explanation of the failure |
| **Impacted Component** | Blue | Affected system component (e.g., AuthService) |
| **Historical Bug** | Olive | Related past issues or "None Found" |
| **Suggested Fix** | Green | Actionable remediation steps with code examples |
| **Confidence Score** | White/Text | AI confidence level (0-100%) |

### Quick Actions

- **Analyze Failure** button: Triggers RCA analysis with Gemini
- Displays spinner while analyzing
- Results appear in real-time

---

## 🧪 Testing

### Run Unit Tests

```bash
pytest app/tests/ -v
```

### Test Files

- **`app/tests/test_auth.py`**: Example test demonstrating RCA workflow
- **`app/tests/auth.py`**: Mock authentication module

### Custom Test Scenarios

To test with your own scenarios:

1. Create test cases with realistic failures
2. Ensure corresponding Neo4j nodes exist (`TestCase`, `Component`, etc.)
3. Run pytest with `-v` flag to see detailed RCA output

---

## 🔧 Troubleshooting

### Issue: `GOOGLE_API_KEY is missing`

**Solution**: Ensure `.env` file contains valid `GOOGLE_API_KEY`:
```bash
echo "GOOGLE_API_KEY=your_key" >> .env
```

### Issue: `Connection refused: localhost:7687`

**Solution**: Verify Neo4j is running:
```bash
# If using Docker
docker ps | grep neo4j

# If not running, start it
docker start neo4j
```

### Issue: `No test context found`

**Solution**: Ensure Neo4j graph contains corresponding nodes:
```cypher
MATCH (t:TestCase {name: "test_name"}) RETURN t
```

If empty, seed the graph with test data.

### Issue: `FailureAnalysis nodes not persisting`

**Cause**: `save_failure_analysis()` might not be called in hook.

**Solution**: Uncomment or add persistence call in `conftest.py`:
```python
agent.graph.save_failure_analysis(...)
```

### Issue: Streamlit dashboard not loading

**Solution**: 
```bash
# Clear cache and restart
streamlit run app/ui/dashboard.py --logger.level=debug

# Or check port availability
netstat -an | grep 8501
```

---

## 📊 Project Status

**Status**: ⚠️ **Proof of Concept / Incomplete**

This is an **incomplete prototype** demonstrating the core concept of AI-powered RCA for pytest failures. The system is functional but should be considered a **research artifact** rather than production-ready software.

### Current Capabilities

✅ Test failure detection and auto-analysis  
✅ Neo4j context retrieval  
✅ Gemini-based RCA generation  
✅ Structured report schema  
✅ Basic persistence  
✅ CLI and Streamlit interfaces  

### System Status

**✅ Working Proof of Concept**

The system is **fully functional** and includes:

- **Working Neo4j Database**: Pre-populated with 28 nodes and 21 relationships representing an authentication system test scenario
- **Operational RCA Agent**: Successfully analyzes `test_login` failure and generates 95% confidence diagnoses
- **Live Dashboard**: Streamlit interface running on `localhost:8501` with real-time RCA reporting
- **Real Example Data**: 
  - Test case: `test_login` (expecting HTTP 200, receiving 500)
  - Impacted component: `AuthService`
  - Historical context: Token expiry mismatch
  - Generated fixes: Actionable token validation recommendations

### Known Limitations

- ❌ Limited error handling for edge cases
- ❌ No multi-database support (Neo4j only)
- ❌ No result caching or optimization
- ❌ Minimal monitoring and logging
- ❌ No rate-limiting for API calls
- ❌ Graph schema assumes specific structure

### Future Enhancements

- [ ] Advanced error categorization
- [ ] Multi-LLM support (OpenAI, Anthropic, etc.)
- [ ] Graph auto-schema inference
- [ ] Batch analysis capabilities
- [ ] RCA trend visualization
- [ ] Integration with CI/CD pipelines
- [ ] Performance profiling & optimization
- [ ] Comprehensive logging & telemetry

---

## 📚 References

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Google Gemini API](https://ai.google.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [GraphRAG Concept](https://www.microsoft.com/en-us/research/publication/graphrag-leveraging-graphs-for-context-rich-retrieval-augmented-generation/)

---

**Project**: Agentic Graph-Based Root Cause Analysis for Software Testing  
**Status**: POC / Incomplete Prototype  
**Last Updated**: 2026
