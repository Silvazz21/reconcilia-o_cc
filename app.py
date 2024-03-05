import streamlit as st
import pandas as pd

# Função para processar o arquivo Excel
def process_excel(file):
    df = pd.read_excel(file)

    # Verifica se a coluna 'Data' existe
    if 'Data' in df.columns:
        df.sort_values(by='Data', inplace=True, ignore_index=True)

    # Verifica se a coluna 'Descrição' não existe
    if 'Descrição' not in df.columns:
        if 'Documento' in df.columns:
            df.rename(columns={'Documento': 'Descrição'}, inplace=True)
        else:
            st.error("Nem a coluna 'Descrição' nem a coluna 'Documento' existem no DataFrame.")
            return None

    df['Mark'] = 0

    return df

# Função para encontrar transações não pagas
def unpaid(df, received_list):
    invoices = []
    for i in range(0, received_list[1]):
        if df['Débito'][i] != 0 and df['Mark'][i] == 0: 
            invoices.append([df['Débito'][i], i])
        elif df['Crédito'][i] != 0 and df['Mark'][i] == 0 and df['Descrição'][i].startswith('r^(NC|CF)'):
            invoices.append([-df['Crédito'][i], i])  # Considera notas de crédito como valores negativos
    return invoices

# Função para encontrar combinações correspondentes
def find_matching_combinations(target_number, debit_list):
    tolerance = 0.001
    
    results = [] 
    for length in range(1, len(debit_list) + 1):
        for combination in combinations(debit_list, length):
            if abs(sum(item[0] for item in combination) - target_number[0]) < tolerance:
                indices = [item[1] for item in combination]
                indices.append(target_number[1])
                results.append(indices)
    return results

# Função principal do aplicativo
def main():
    st.title("Aplicativo de Processamento de Excel")

    # Carrega o arquivo Excel
    file = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])
    if file is not None:
        df = process_excel(file)
        if df is not None:
            st.subheader("DataFrame Resultante")
            st.write(df)

            # Exporta o DataFrame
            export_format = st.selectbox("Selecione o formato de exportação", ["Excel", "CSV"])
            if st.button("Exportar DataFrame"):
                if export_format == "Excel":
                    st.write("Exportando DataFrame para Excel...")
                    df.to_excel("output.xlsx", index=False)
                elif export_format == "CSV":
                    st.write("Exportando DataFrame para CSV...")
                    df.to_csv("output.csv", index=False)
                st.success("DataFrame exportado com sucesso!")

if __name__ == "__main__":
    main()
