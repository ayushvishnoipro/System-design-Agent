```mermaid
flowchart TD
    %% User Interface Layer
    subgraph "Streamlit Frontend"
        direction TB
        UI[Streamlit Web App] --> |Input| Form[Requirements Form]
        UI --> MermaidView[Mermaid Diagram Viewer]
        UI --> CostView[Cost Estimation View]
        
        subgraph "UI Components"
            Form --> GenBtn[Generate Button]
            MermaidView --> CodeView[Mermaid Code Editor]
            CostView --> CostTable[Cost Analysis Table]
            Settings[Configuration Sidebar]
            Download[Diagram Downloader]
        end
    end

    %% Backend Services
    subgraph "FastAPI Backend"
        API[FastAPI Server] --> Middleware[Error Handler]
        Middleware --> Router[/api/generate Router]
        
        subgraph "Agent Orchestration"
            Router --> AgentRunner[Agent Runner Service]
            AgentRunner --> |1. Parse Requirements| ReqParser[Requirements Parser Agent]
            AgentRunner --> |2. Get Components| CloudRetriever[Cloud Components Agent]
            AgentRunner --> |3. Generate Diagram| ArchGen[Architecture Generator Agent]
        end

        subgraph "Support Services"
            OpenAI[OpenAI Service]
            Config[Environment Config]
            PDF[PDF Export Service]
            Cache[Response Cache]
        end
    end

    %% External Services
    subgraph "AI & Cloud Services"
        GPT4[OpenAI GPT-4 LLM]
        AWS[AWS Services]
    end

    %% Data Flow
    Form --> |HTTP POST| API
    Settings --> |Config| API
    
    %% Agent Workflows
    ReqParser --> |Extract Requirements| OpenAI
    CloudRetriever --> |Get Components| OpenAI
    ArchGen --> |Generate Mermaid| OpenAI
    OpenAI --> GPT4
    
    %% Results Flow
    AgentRunner --> |Architecture| MermaidView
    AgentRunner --> |Cost Data| CostView
    MermaidView --> |Export| PDF
    PDF --> Download

    %% Configurations
    Config --> |Load ENV| API
    Config --> |API Keys| OpenAI
    Config --> |AWS Creds| AWS
    AWS --> |Pricing| CloudRetriever

    %% Styling
    classDef streamlit fill:#FF4B4B,stroke:#FF4B4B,stroke-width:2px;
    classDef fastapi fill:#009688,stroke:#00796B,stroke-width:2px;
    classDef agent fill:#FF9800,stroke:#F57C00,stroke-width:2px;
    classDef service fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px;
    classDef external fill:#2196F3,stroke:#1976D2,stroke-width:2px;
    classDef component fill:#4CAF50,stroke:#388E3C,stroke-width:2px;

    class UI,Form,MermaidView,CostView,GenBtn,CodeView,CostTable,Settings,Download streamlit;
    class API,Middleware,Router,AgentRunner fastapi;
    class ReqParser,CloudRetriever,ArchGen agent;
    class OpenAI,Config,PDF,Cache service;
    class GPT4,AWS external;
```

Key Updates:
1. Added Streamlit-specific components
2. Showed sequential agent workflow (1,2,3)
3. Added data flow directions
4. Included cache and middleware
5. Separated UI components clearly
6. Added configuration flows
7. Improved color coding for different services
8. Showed PDF export workflow
9. Added AWS services integration
10. Included error handling middleware
