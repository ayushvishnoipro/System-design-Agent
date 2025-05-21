# AI System Design Architect

```mermaid
flowchart TD
    subgraph Frontend
        A1[HTML/CSS/JS] --> A2[Mermaid.js]
        A1 --> A3[Fetch API]
    end
    subgraph Backend
        B1[FastAPI App]
        B2[Routers: /api/generate]
        B3[Services: agent_runner, openai_service, pdf_export]
        B4[Agents: requirements_parser, cloud_retriever, architecture_generator]
        B5[Models: request/response]
        B6[constants.py]
        B7[config.py]
    end
    subgraph External
        C1[OpenAI API]
    end

    A3 -- HTTP POST /api/generate --> B2
    B2 --> B1
    B1 --> B3
    B3 --> B4
    B3 --> B5
    B3 --> B6
    B3 --> B7
    B4 -- LLM call --> C1
    B3 -- PDF Export --> A1
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
