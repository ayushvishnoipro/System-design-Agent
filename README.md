# AI System Design Architect
#Live demo


https://github.com/user-attachments/assets/10a2db94-4cfc-42ca-9031-e4e90488ab7e



```mermaid
---
config:
  layout: fixed
---
flowchart TD
 subgraph subGraph0["UI Components"]
        GenBtn["Generate Button"]
        Form["Requirements Form"]
        CodeView["Mermaid Code Editor"]
        MermaidView["Mermaid Diagram Viewer"]
        CostTable["Cost Analysis Table"]
        CostView["Cost Estimation View"]
        Settings["Configuration Sidebar"]
        Download["Diagram Downloader"]
  end
 subgraph subGraph1["Streamlit Frontend"]
    direction TB
        UI["Streamlit Web App"]
        subGraph0
  end
 subgraph subGraph2["Agent Orchestration"]
        AgentRunner["Agent Runner Service"]
        Router[/"api/generate"/]
        ReqParser["Requirements Parser Agent"]
        CloudRetriever["Cloud Components Agent"]
        ArchGen["Architecture Generator Agent"]
  end
 subgraph subGraph3["Support Services"]
        OpenAI["OpenAI Service"]
        Config["Environment Config"]
        PDF["PDF Export Service"]
        Cache["Response Cache"]
  end
 subgraph subGraph4["FastAPI Backend"]
        Middleware["Error Handler"]
        API["FastAPI Server"]
        subGraph2
        subGraph3
  end
 subgraph subGraph5["AI & Cloud Services"]
        GPT4["OpenAI GPT-4 LLM"]
        AWS["AWS Services"]
  end
    UI -- Input --> Form
    UI --> MermaidView & CostView
    Form --> GenBtn
    MermaidView --> CodeView
    CostView --> CostTable
    API --> Middleware
    Middleware --> Router
    Router --> AgentRunner
    AgentRunner -- "1. Parse Requirements" --> ReqParser
    AgentRunner -- "2. Get Components" --> CloudRetriever
    AgentRunner -- "3. Generate Diagram" --> ArchGen
    Form -- HTTP POST --> API
    Settings -- Config --> API
    ReqParser -- Extract Requirements --> OpenAI
    CloudRetriever -- Get Components --> OpenAI
    ArchGen -- Generate Mermaid --> OpenAI
    OpenAI --> GPT4
    AgentRunner -- Architecture --> MermaidView
    AgentRunner -- Cost Data --> CostView
    MermaidView -- Export --> PDF
    PDF --> Download
    Config -- Load ENV --> API
    Config -- API Keys --> OpenAI
    Config -- AWS Creds --> AWS
    AWS -- Pricing --> CloudRetriever
     GenBtn:::streamlit
     Form:::streamlit
     CodeView:::streamlit
     MermaidView:::streamlit
     CostTable:::streamlit
     CostView:::streamlit
     Settings:::streamlit
     Download:::streamlit
     UI:::streamlit
     AgentRunner:::fastapi
     Router:::fastapi
     ReqParser:::agent
     CloudRetriever:::agent
     ArchGen:::agent
     OpenAI:::service
     Config:::service
     PDF:::service
     Cache:::service
     Middleware:::fastapi
     API:::fastapi
     GPT4:::external
     AWS:::external
    classDef streamlit fill:#FF4B4B,stroke:#FF4B4B,stroke-width:2px
    classDef fastapi fill:#009688,stroke:#00796B,stroke-width:2px
    classDef agent fill:#FF9800,stroke:#F57C00,stroke-width:2px
    classDef service fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px
    classDef external fill:#2196F3,stroke:#1976D2,stroke-width:2px
    classDef component fill:#4CAF50,stroke:#388E3C,stroke-width:2px

```

An AI-powered system design tool that generates architecture diagrams using natural language requirements.

## Features

- Natural language processing of system requirements
- Automatic generation of system architecture diagrams using Mermaid
- AWS service integration and cost estimation
- Export to PDF functionality

## Setup

1. Create a virtual environment:
```bash
uv venv .venv
source .venv/bin/activate  # Unix/MacOS
.venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
uv pip install -r backend/requirements.txt
```

3. Configure environment variables in `.env`:
```
OPENAI_API_KEY=your_key_here
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_key_here
```

4. Run the backend:
```bash
cd backend
uvicorn main:app --reload
```

5. Open `frontend/index.html` in your browser

## Usage

1. Enter your system requirements in natural language
2. Click "Generate Design"
3. View the generated architecture diagram
4. Optionally export to PDF
