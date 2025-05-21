from typing import List, Dict
from ..services.openai_service import openai_service
import re

class ArchitectureGenerator:
    def __init__(self):
        self.diagram_prompt = """Create a Mermaid diagram for the following system architecture.
Use this exact format and structure:

flowchart TD
    subgraph Frontend
        UI[Web UI] --> MobileApp[Mobile App]
    end
    subgraph Backend
        API[API Gateway] --> Services[Microservices]
    end
    subgraph Data
        DB[(Database)]
        Cache[(Redis)]
    end

Requirements: {requirements}
Components: {components}
Connections: {connections}

Remember:
1. Always start with 'flowchart TD'
2. Use proper subgraph syntax
3. Each node/connection on its own line
4. Use valid Mermaid node shapes: [], (), [()], (())
5. Use proper arrow syntax: -->
"""

    async def generate(self, requirements: Dict, architecture: Dict) -> str:
        try:
            prompt = self.diagram_prompt.format(
                requirements=self._format_requirements(requirements),
                components=self._format_components(architecture["components"]),
                connections=self._format_connections(architecture["connections"])
            )
            response = await openai_service.generate_completion(prompt, "architecture")
            return self._clean_mermaid_code(response)
        except Exception as e:
            return self._get_default_diagram()

    def _get_default_diagram(self) -> str:
        return """flowchart TD
    subgraph Frontend
        UI[Web UI]
    end
    subgraph Backend
        API[API Gateway]
    end
    subgraph Data
        DB[(Database)]
    end
    UI --> API
    API --> DB"""

    def _format_components(self, components: List[Dict]) -> str:
        formatted = ["Current components and their purposes:"]
        tech_stack = {
            "frontend": ["Web UI", "Mobile Apps", "Admin Dashboard"],
            "backend": ["API Gateway", "Microservices", "Authentication"],
            "data": ["Databases", "Caching", "Message Queues"],
            "infrastructure": ["Load Balancers", "CDN", "Monitoring"]
        }
        
        # Add existing components
        for comp in components:
            formatted.append(f"- {comp['service']} ({comp['tier']}): {comp['purpose']}")
        
        # Add suggested tech stack
        formatted.append("\nSuggested technology stack:")
        for category, items in tech_stack.items():
            formatted.append(f"\n{category.title()}:")
            for item in items:
                formatted.append(f"- {item}")
        
        return "\n".join(formatted)

    def _format_connections(self, connections: List[Dict]) -> str:
        return "\n".join([
            f"- {conn['from']} -> {conn['to']}: {conn['type']}"
            for conn in connections
        ])

    def _format_requirements(self, requirements: Dict) -> str:
        return "\n".join([
            "Functional:",
            *[f"- {r}" for r in requirements["functional"]],
            "Non-Functional:",
            *[f"- {r}" for r in requirements["non_functional"]]
        ])

    def _clean_mermaid_code(self, code: str) -> str:
        # Extract code block if present
        match = re.search(r"```mermaid\s*([\s\S]+?)```", code)
        if match:
            code = match.group(1)
        else:
            idx = code.find("flowchart")
            if idx == -1:
                idx = code.find("graph")
            if idx != -1:
                code = code[idx:]
        code = code.strip()

        # Ensure the first line is a valid flowchart declaration
        lines = code.splitlines()
        if not lines or not (lines[0].startswith("flowchart ") or lines[0].startswith("graph ")):
            code = "flowchart TD\n" + code
            lines = code.splitlines()

        # Post-process: split lines with multiple statements, remove invalid lines
        processed = []
        for line in lines:
            # Remove empty lines and comments
            line = line.strip()
            if not line or line.startswith('%') or line.startswith('%%'):
                continue
            # Split lines with multiple Mermaid statements (e.g., "A --> B  B --> C")
            parts = re.split(r'(?<=[\]])\s+(?=[A-Za-z0-9_]+\[)', line)
            for part in parts:
                # Only keep lines that look like valid Mermaid node or edge definitions
                if re.match(r'^(flowchart |graph |[A-Za-z0-9_]+\[.*\]|[A-Za-z0-9_]+\s*-->|[A-Za-z0-9_]+\s*-.+->)', part):
                    processed.append(part.strip())
                elif part == lines[0]:  # Always keep the header
                    processed.append(part.strip())
        # Join back together
        code = "\n".join(processed)
        return code
