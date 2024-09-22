import gradio as gr
import pandas as pd
import numpy as np
import pickle
from collections import defaultdict
from warnings import filterwarnings
filterwarnings("ignore")

models = {}
markets = ["bengaluru", "doddaballapur", "hubballi", "mysuru"]
for market in markets:
    models[f'{market}_min'] = pickle.load(open(f'ML_models/{market}/min_model.pkl', 'rb'))
    models[f'{market}_max'] = pickle.load(open(f'ML_models/{market}/max_model.pkl', 'rb'))
    models[f'{market}_modal'] = pickle.load(open(f'ML_models/{market}/modal_model.pkl', 'rb'))

grades = defaultdict(list)
default_grades = {}
varieties = defaultdict(list)
default_variety = {}
for market in markets:
    df = pd.read_csv(f'krama_report_{market}.csv')
    # grades[market] = [elem.lower() for elem in df['Grade'].unique().tolist()]
    # variety[market] = [elem.lower() for elem in df['Variety'].unique().tolist()]
    # Set default grade and variety for each market to maximum occurring grade and variety
    default_grades[market] = df['Grade'].value_counts().idxmax().lower()
    default_variety[market] = df['Variety'].value_counts().idxmax().lower()
       
    print(f'{market} default grade: {default_grades[market]}')
    print(f'{market} default variety: {default_variety[market]}')
    
processed_data_format = {}
for market in markets:
    processed_data = pd.read_csv(f'preprocessed_krama_report_{market}.csv')
    processed_data_format[market] = processed_data.columns.tolist()[3:]
    columns = processed_data_format[market]
    for elem in columns:
        if elem[:7] == 'Variety':
            varieties[market].append(elem[8:].lower())
        if elem[:5] == 'Grade':
            grades[market].append(elem[6:].lower())
    if default_grades[market] not in grades[market]:
        default_grades[market] = grades[market][0]
    if default_variety[market] not in varieties[market]:
        default_variety[market] = varieties[market][0]

for market in markets:
    print(f'{market} grades: {grades[market]}')
    print(f'{market} variety: {varieties[market]}') 
    
# Placeholder for your machine learning model processing
def predict_prices(year, month, day, grade, variety):
    results = {}
    
    # converting data to format that model expects
    # Year,Month,Day,Variety_BELLARY RED,Variety_LOCAL,Variety_ONION,Variety_OTHER,Variety_PUNA,Grade_FAQ,Grade_LARGE,Grade_MEDIUM,Grade_SMALL
    variety = variety.lower()
    grade = grade.lower()
    for market in markets:
        if variety not in varieties[market]:
            variety = default_variety[market]
            print(variety)
        if grade not in grades[market]:
            print(grade)
            grade = default_grades[market]
        data = [year, month, day]
        for elem in varieties[market]:
            data.append(1 if elem == variety else 0)
        for elem in grades[market]:
            data.append(1 if elem == grade else 0)
        data = np.array([data])
        min_price = models[f'{market}_min'].predict(data)[0]
        max_price = models[f'{market}_max'].predict(data)[0]
        modal_price = models[f'{market}_modal'].predict(data)[0]
        print(f'{market} min price: {min_price}')
        print(f'{market} max price: {max_price}')
        print(f'{market} modal price: {modal_price}')
        results[market] = {"Min Price": min_price, "Max Price": max_price, "Modal Price": modal_price, "Variety": variety, "Grade": grade}
    
    # Convert the results to a Pandas DataFrame for better display
    df = pd.DataFrame(results).transpose()
    df = df.reset_index().rename(columns={"index": "Market"})
    return df

# # Define the input components
# year = gr.inputs.Number(label="Year", minimum=2000, maximum=2100, step=1, default=2023)
# month = gr.inputs.Number(label="Month", minimum=1, maximum=12, step=1, default=1)
# day = gr.inputs.Number(label="Day", minimum=1, maximum=31, step=1, default=1)
# grade = gr.inputs.Textbox(label="Grade", placeholder="Enter grade (e.g., A, B, C)")
# variety = gr.inputs.Textbox(label="Variety", placeholder="Enter variety name")

# # Define the output component
# output = gr.outputs.Dataframe(label="Price Predictions")

# # Create the Gradio interface
# interface = gr.Interface(
#     fn=predict_prices,
#     inputs=[year, month, day, grade, variety],
#     outputs=output,
#     title="Market Price Predictor",
#     description="""
#     Enter the Year, Month, Day, Grade, and Variety to predict the minimum, 
#     maximum, and modal prices for the markets in Bengaluru, Doddaballapura, 
#     Hubballi, and Mysuru.
#     """,
#     examples=[
#         [2023, 5, 15, "A", "Variety1"],
#         [2024, 8, 20, "B", "Variety2"]
#     ]
# )

# Launch the app
if __name__ == "__main__":
    print(predict_prices(2025, 5, 30, "average", "local"))
