
Name: **Aman Prakash**      

[LinkedIn](https://www.linkedin.com/in/prakash-aman/)  

[LinkTree](https://linktr.ee/aman_prakash)

(amanprakash.connect@gmail.com)



## Summary of the work done:

## 1.  **Assignment Work:**
 - Cleaned the dataset as instructed, used `Groq` API and custom prompt to generate pandas code of the given 7 questions, all respective 7 codes output generated in separate jupyter cells.
 - **LLM Used:** `deepseek-r1-distill-llama-70b` from Groq.
 - All the details are available in `llm_queries.ipynb` file.

</br>

## 2. **Streamlit Energy Bot:** [Live Here](https://iit-gn-energy-bot.streamlit.app/)
   
 - This bot aims to show a `live demonstration of the assignment` given.
   
 - This is a live streamlit app where users can ask questions about the given energy dataset in **natural language**.
   
   <img src ="https://github.com/user-attachments/assets/ee8ade0d-c882-41e5-b4ca-057a5ccda11b" height= 500 >

 - It converts the user query into code using the Groq API.
   
   <img src ="https://github.com/user-attachments/assets/d93ed1a1-f56d-4975-bfa9-98c9e02cc0c9" height= 500 >


 - It also runs the code generated to display *output* and *graphs*.
   
   <img src ="https://github.com/user-attachments/assets/b682d7fa-80e2-4c7e-802a-59d2d2f5a920" height= 400 >

 - Doesn't respond to user queries that are `not relevant` to the Energy Dataset.
   
   
   <img src ="https://github.com/user-attachments/assets/22d945c9-9e1d-4efd-9ca7-a25aeeb06eca" height= 500 >

- At the start of this app, it gives a preview summary of the energy dataset.
  
  <img src ="https://github.com/user-attachments/assets/04624071-1f40-402a-a77a-23bd2a99e96f" height= 500 >

   

### Repository Structure

```
energy_query_app/
├── app.py
├── requirements.txt
├── data/
│   └── energy_data.csv
└── utils/
    └── query_processor.py
```

### Prompt used in `llm_queries.ipynb`

```
You are an expert data analyst using Python pandas.

The dataset is stored at this path on my system:
C:/Users/aman/Desktop/Sustain_RA/household_power_consumption.txt

Assume I have already loaded and cleaned the dataset into a pandas DataFrame named `df` with a datetime index. The DataFrame has numeric columns, including 
'datetime', 'Global_active_power', 'Global_reactive_power', 'Voltage',	'Global_intensity',	'Sub_metering_1', 'Sub_metering_2',	'Sub_metering_3'

Assume, this code block is already run:
``import pandas as pd
df = pd.read_csv(
    "C:/Users/aman/Desktop/Sustain_RA/household_power_consumption.txt",
    sep=';',
    na_values=['?'],
    low_memory=False
)
df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], dayfirst=True)
df = df.drop(columns=["Date", "Time"])
df = df.dropna()
df["Global_active_power"] = df["Global_active_power"].astype(float)
df = df.set_index("datetime")
``
	

Write Python pandas code to answer each of these questions separately:



1. What was the average active power consumption in March 2007?
2. What hour of the day had the highest power usage on Christmas 2006?
3. Compare energy usage (Global_active_power) on weekdays vs weekends.
4. Find days where energy consumption exceeded 5 kWh.
5. Plot the energy usage trend for the first week of January 2007.
6. Find the average voltage for each day of the first week of February 2007.
7. What is the correlation between global active power and sub-metering values?

Keep these in mind: 
Use vectorized operations and pandas built-in methods instead of apply where possible.
When working with dates, use df.index and pandas datetime properties (e.g., index.month, index.dayofweek, index.date) in a vectorized way.
Avoid deprecated arguments or methods.
Include any necessary imports.
Ensure the code is robust and directly runnable in a modern pandas environment.
Generate only the code blocks with comments and no extra explanations.
```




### For running the streamlit app locally

1. Create a virtual environment (recommended):
``` bash
python -m venv energy_app
# On Windows:
energy_app\Scripts\activate
# On Mac/Linux:
source energy_app/bin/activate
```
2. Install Dependencies
``` bash!

pip install -r requirements.txt
 ```


Get Groq API Key

Go to [https://console.groq.com/](https://console.groq.com/)




