import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from utils.query_processor import QueryProcessor
import os

# Page configuration
st.set_page_config(
    page_title="Energy Data Query Assistant",
    page_icon="⚡",
    layout="wide"
)

def load_sample_data():
    """
    Load sample energy dataset or create a demo dataset
    """
    # Try to load from data folder
    try:
        df = pd.read_csv('data/energy_data.csv')
        # Ensure datetime column is parsed
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    except FileNotFoundError:
        st.error("Dataset not found! Please place your energy_data.csv in the 'data' folder.")
        st.info("Expected columns: 'datetime', 'Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'")
        return None

def display_dataset_preview(df):
    """
    Display dataset information and preview
    """
    st.subheader("📊 Dataset Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Date Range", f"{df['datetime'].min().date()} to {df['datetime'].max().date()}")
    with col3:
        st.metric("Columns", len(df.columns))
    
    # Display column information
    st.subheader("📋 Column Information")
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.values,
        'Sample Value': [str(df[col].iloc[0]) for col in df.columns]
    })
    st.dataframe(col_info, use_container_width=True)
    
    # Display sample data
    st.subheader("👀 Sample Data")
    st.dataframe(df.head(10), use_container_width=True)

def display_sample_queries():
    """
    Display sample queries that users can try
    """
    st.subheader("💡 Sample Queries You Can Try")
    
    sample_queries = [
        "What was the average active power consumption in March 2007?",
        "What hour of the day had the highest power usage on Christmas 2006?",
        "Compare energy usage (Global_active_power) on weekdays vs weekends.",
        "Find days where energy consumption exceeded 5 kWh.",
        "Plot the energy usage trend for the first week of January 2007.",
        "Find the average voltage for each day of the first week of February 2007.",
        "What is the correlation between global active power and sub-metering values?"
    ]
    
    for i, query in enumerate(sample_queries, 1):
        if st.button(f"Query {i}: {query}", key=f"sample_{i}"):
            st.session_state.selected_query = query

def process_user_query(query, df, processor):
    """
    Process user query and display results
    """
    st.subheader("🔄 Processing Your Query")
    
    with st.spinner("Generating pandas code..."):
        
        # Most imp. 2 lines-The Core Magic!
        df_info = processor.get_dataset_info(df)       
        generated_code = processor.generate_pandas_code(query, df_info)
    
    # Display generated code
    st.subheader("🐍 Generated Pandas Code")
    st.code(generated_code, language='python')
    
    # Execute the code
    st.subheader("⚡ Execution Results")
    
    with st.spinner("Executing code..."):
        execution_result = processor.execute_code_safely(generated_code, df)
    
    if execution_result['success']:
        st.success("✅ Code executed successfully!")
        
        # Display any printed output
        if execution_result['output']:
            st.subheader("📝 Output")
            st.text(execution_result['output'])
        
        # Display the result
        if execution_result['result'] is not None:
            st.subheader("📊 Result")
            result = execution_result['result']
            
            # Handle different types of results
            if isinstance(result, pd.DataFrame):
                st.dataframe(result, use_container_width=True)
            elif isinstance(result, (pd.Series, list, dict)):
                if isinstance(result, pd.Series):
                    st.dataframe(result.to_frame(), use_container_width=True)
                else:
                    st.write(result)
            else:
                st.write(result)
        
        # Check for any plots in locals and display them properly
        locals_dict = execution_result['locals']
        
        # Handle matplotlib plots
        if any('plt.' in str(generated_code) for line in generated_code.split('\n')):
            try:
                fig = plt.gcf()
                if fig.get_axes():  # Check if there are any plots
                    st.subheader("📈 Visualization")
                    st.pyplot(fig)
                plt.clf()  # Clear the figure
            except:
                pass
        
        # Handle plotly plots
        if 'result' in locals_dict and hasattr(locals_dict['result'], 'show'):
            st.subheader("📈 Visualization")
            st.plotly_chart(locals_dict['result'], use_container_width=True)
    
    else:
        st.error("❌ Code execution failed!")
        st.error(f"Error: {execution_result['error']}")
        
        st.subheader("🛠️ Troubleshooting Tips")
        st.write("""
        - Make sure your query is clear and specific
        - Check if column names are correct
        - Verify date formats if using date filters
        - Try rephrasing your question
        """)

def main():
    # Title and description
    st.title("⚡ Energy Data Query Assistant")
    st.markdown("Ask questions about your energy dataset in natural language and get pandas code + results!")
    
    # Sidebar for API key and settings
    with st.sidebar:
        st.header("🔑 Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Enter your Groq API Key:",
            type="password",
            help="Get your API key from https://console.groq.com/"
        )
        
        if api_key:
            st.success("✅ API Key configured!")
        else:
            st.warning("⚠️ Please enter your Groq API key to continue")
        
        st.header("ℹ️ About")
        st.markdown("""
        This app uses Groq's LLM to convert your natural language questions 
        into pandas code and execute them on your energy dataset.
        
        **Supported Operations:**
        - Data filtering and aggregation
        - Time-based analysis
        - Statistical calculations
        - Basic visualizations
        """)
    
    # Load dataset
    df = load_sample_data()
    
    if df is None:
        st.stop()
    
    # Display dataset information
    display_dataset_preview(df)
    
    # Main query interface
    if api_key:
        processor = QueryProcessor(api_key)
        
        st.header("🤖 Ask Your Question")
        
        # Display sample queries
        display_sample_queries()
        
        # Query input
        user_query = st.text_area(
            "Enter your question about the energy data:",
            value=st.session_state.get('selected_query', ''),
            height=100,
            placeholder="e.g., What was the average active power consumption in March 2007?"
        )
        
        # Process query button
        if st.button("🚀 Process Query", disabled=not user_query.strip()):
            if user_query.strip():
                process_user_query(user_query, df, processor)
    else:
        st.info("👈 Please enter your Groq API key in the sidebar to start querying!")

if __name__ == "__main__":
    # Initialize session state
    if 'selected_query' not in st.session_state:
        st.session_state.selected_query = ''
    
    main()