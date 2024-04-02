import streamlit as st
import pandas as pd
import itertools
from decimal import *

precision = Decimal('0.01')
tolerance = precision




# Function to find combinations that sum up to the target
def find_combinations(numbers, target, tolerance=0.01):
  try:
    number_list = [i for i in numbers if i is not None]
    target_value = target
    result = []
    for i in range(1, len(number_list) + 1):
      for seq in itertools.combinations(number_list, i):
        combination_sum = sum(seq)
        if abs(combination_sum - target_value) <= tolerance:  # Check for tolerance
          result.append(tuple(seq))
    return result
  except ValueError:
    return None


def g(df):
    for i in range(len(dataframe)):
        if df.loc[i, 'Documento'].startswith('NC') or df.loc[i, 'Documento'].startswith('CF'):
            df.loc[i, 'Débito'] -= df.loc[i, 'Crédito']
    return df
                 
# Streamlit app
def main():
    st.title("Streamlit App")

# File uploader
    uploaded_file = st.file_uploader("Upload an Excel file", type="xlsx")
                                 
                                 
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    
    df = g(df.copy())
    
    # Sort DataFrame
    df_sorted = df.sort_values(by=['Data', 'Documento'], ascending=[True, False])

    # Initialize 'Marca' column
    df_sorted['Marca'] = 0

    # Convert 'Crédito' and 'Débito' columns to Decimal
    df_sorted['Crédito'] = df_sorted['Crédito'].apply(lambda x: float(Decimal(str(x))) if not pd.isnull(x) else None)
    df_sorted['Débito'] = df_sorted['Débito'].apply(lambda x: float(Decimal(str(x))) if not pd.isnull(x) else None)

    current_combination_counter = 0  # Initialize the current combination counter

    for index, row in df_sorted.iterrows():
        # Check if 'Documento' starts with 'R' and if payment hasn't been marked
        if row['Documento'].startswith('R') and row['Marca'] == 0:
            payment_amount = float(Decimal(row['Crédito']))
            payment_amounts = []
            payment_amounts.append(payment_amount) # Create the list of payment in the statement
            invoices_before_payment = []
            # Iterate over rows before the current payment
            for prev_index, prev_row in df_sorted.iloc[:index].iterrows():
                # Check if invoice hasn't been marked, is a debit, and starts with 'FX'
                if prev_row['Marca'] == 0 and prev_row['Débito'] != 0 and (prev_row['Documento'].startswith('F') or prev_row['Documento'].startswith('NC') or row['Documento'].startswith('CF')):
                    invoices_before_payment.append((prev_index, Decimal(prev_row['Débito'])))
                    debito_values = [float(debito) for _, debito in invoices_before_payment]
                    combinations = find_combinations(debito_values, payment_amount)
                    if combinations:
                        current_combination_counter += 1
                        first_combination = combinations[0]
                        for combination in first_combination:
                            value_index = debito_values.index(combination)
                            df_sorted.at[invoices_before_payment[value_index][0], 'Marca'] = current_combination_counter
                            df_sorted.at[index, 'Marca'] = current_combination_counter
                        break

    # Display the sorted and marked DataFrame
    st.subheader("Conta corrente reconciliada")
    st.write(df_sorted)

if __name__ == "__main__":
    main()


