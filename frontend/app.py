import streamlit as st
from streamlit_mermaid import st_mermaid
import requests
import json

def init_session_state():
    if 'mermaid_code' not in st.session_state:
        st.session_state.mermaid_code = None
    if 'costs' not in st.session_state:
        st.session_state.costs = None

def render_sidebar():
    with st.sidebar:
        st.header("Configuration")
        st.checkbox("Include cost estimates", value=True, key="include_costs")
        st.checkbox("Show Mermaid code", value=False, key="show_code")
        
        if st.session_state.mermaid_code:
            if st.download_button(
                "Download Diagram",
                data=st.session_state.mermaid_code,
                file_name="architecture.mmd",
                mime="text/plain"
            ):
                st.success("Diagram code downloaded!")

def render_costs():
    if not st.session_state.costs:
        return

    st.subheader("Estimated Costs")
    costs_data = []
    total_monthly = 0
    total_yearly = 0

    for service, details in st.session_state.costs.items():
        monthly = float(details['monthly'])
        yearly = float(details['yearly'])
        total_monthly += monthly
        total_yearly += yearly
        
        costs_data.append({
            "Service": service,
            "Monthly Cost": f"${monthly:,.2f}",
            "Yearly Cost": f"${yearly:,.2f}",
            "Tier": details['tier']
        })

    # Display costs in a table
    st.table(costs_data)
    
    # Show totals
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Monthly Cost", f"${total_monthly:,.2f}")
    with col2:
        st.metric("Total Yearly Cost", f"${total_yearly:,.2f}")

def main():
    st.set_page_config(
        page_title="System Design Architect",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    init_session_state()
    render_sidebar()

    st.title("AI System Design Architect")
    st.write("Generate architecture diagrams from natural language requirements")

    # Input area with example
    requirements = st.text_area(
        "System Requirements",
        height=150,
        placeholder="Example: Build a scalable video streaming platform with user authentication and content management..."
    )

    # Generate button with spinner
    if st.button("Generate Architecture", type="primary", disabled=not requirements):
        with st.spinner("Generating architecture diagram..."):
            try:
                response = requests.post(
                    "http://localhost:8000/api/generate",
                    json={
                        "requirements": requirements,
                        "include_costs": st.session_state.include_costs
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.mermaid_code = data["mermaid_code"]
                    st.session_state.costs = data.get("estimated_costs")
                    st.rerun()  # Changed from st.experimental_rerun()
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error connecting to backend: {str(e)}")

    # Display area
    if st.session_state.mermaid_code:
        # Architecture diagram
        st.subheader("System Architecture")
        st_mermaid(st.session_state.mermaid_code, height=400)
        
        # Show Mermaid code if enabled
        if st.session_state.show_code:
            st.code(st.session_state.mermaid_code, language="mermaid")
        
        # Show costs if available
        if st.session_state.costs:
            render_costs()
    else:
        # Show example diagram
        st.info("Enter your requirements and click 'Generate Architecture' to begin")
        example = """
        flowchart TD
            User[User] --> API[API Gateway]
            API --> Lambda[Lambda Function]
            Lambda --> DynamoDB[DynamoDB]
        """
        st_mermaid(example, height=300)

if __name__ == "__main__":
    main()
