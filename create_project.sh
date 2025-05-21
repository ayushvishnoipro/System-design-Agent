#!/bin/bash

# Create main project directories
mkdir -p backend/{routers,services,agents,models}
mkdir -p frontend/{css,js,mermaid,assets/icons}

# Create backend files
touch backend/main.py
touch backend/config.py
touch backend/requirements.txt
touch backend/routers/design.py
touch backend/services/{agent_runner.py,openai_service.py,aws_pricing_service.py,pdf_export.py}
touch backend/agents/{requirements_parser.py,cloud_retriever.py,architecture_generator.py}
touch backend/models/{request.py,response.py}

# Create frontend files
touch frontend/index.html
touch frontend/css/styles.css
touch frontend/js/scripts.js
touch frontend/mermaid/mermaid.min.js

# Create root files
touch README.md
touch .gitignore
