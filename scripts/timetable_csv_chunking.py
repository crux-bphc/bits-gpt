import csv
import os
import pandas as pd

def tt_chunker(input_path, output_path, chunk_size):
    #read the csv file
    df = pd.read_csv(input_path)
    #df = df.replace(r'\r+|\n+|\t+','', regex=True) #removes all newlines, tabs and carriage returns
    header = list(df.columns) #gets header elements
    #create a temporary dataframe to store the chunk of data
    temp_df = pd.DataFrame(columns=header)
    chunk = 1 #counter for chunk number
    count = 0 #counter for number of non NaN entries in COM COD column
    with open(input_path, 'r', encoding="utf-8") as handle:
        for line in handle: #line by line read of csv file
            values = line.strip().split(",") #converts the line into a list of values
            if values[0] == 'COM COD': #checks if the first element is not empty
                count += 1
                print(values)

            if count == chunk_size: #if the count reaches chunk_size, save the chunk to a new csv file
                count = 0
                output_file = os.path.join(output_path, f"{os.path.basename(input_path)}_chunk_{chunk:04d}.csv")
                temp_df.to_csv(output_file, index=False)
                print(f"Chunk {chunk} saved to {output_file}")
                temp_df = pd.DataFrame(columns=header)
                chunk += 1
            print(values)
            line_df = pd.DataFrame([values], columns=header)
            temp_df = pd.concat([temp_df, line_df], ignore_index=True)

        if not temp_df.empty:
            output_file = os.path.join(output_path, f"{os.path.basename(input_path)}_chunk_{chunk:04d}.csv")
            temp_df.to_csv(output_file, index=False)
            print(f"Chunk {chunk} saved to {output_file}")
    #print(temp_df)


def books_chunker(input_path, output_path):
    #read the csv file
    df = pd.read_csv(input_path)
    header = list(df.columns)  #get header elements
    
    #create a temporary dataframe to store the chunk of data
    temp_df = pd.DataFrame(columns=header)
    
    #add data to temp_df until it reaches the 8th non-NaN entry in COM COD column
    chunk = 1  # Counter for chunk number
    
    #iterate through df
    for index, row in df.iterrows():
        if row.iloc[0] == "COM COD":
            output_file = os.path.join(output_path, f"{os.path.basename(input_path)}_chunk_{chunk:04d}.csv")
            temp_df.to_csv(output_file, index=False)
            print(f"Chunk {chunk} saved to {output_file}")
            temp_df = pd.DataFrame(columns=header)
            chunk += 1
            continue        
        temp_df = pd.concat([temp_df, pd.DataFrame([row], columns=header)], ignore_index=True)
        

if __name__ == "__main__":
    tt_chunker(r"data\Handouts\rawdata\rawtable_TIMETABLE_II_SEMESTER_2023_-24_0001.csv", r"data\Handouts\CSV", 10)
    books_chunker(r"data\Handouts\rawdata\rawtable_TIMETABLE_II_SEMESTER_2023_-24_0003.csv", r"data\Handouts\CSV")