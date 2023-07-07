import streamlit as st
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

# Connect to Azure table
table_service = TableService(account_name='demodbtable', account_key='V4K8FRL2OlHTinxsVW0xeJ9dETRWlUCWdo5Mp8wyEpgEKuCLsZEZpJzKdsbtYDJANrob8L7gC7aAACDbw22ZRA==')
table_name = 'shopping_mall_db'

# Define Streamlit app
st.title('Insert Data into Azure Table')

# Define input fields
partition_key = st.text_input('Partition Key')
row_key = st.text_input('Row Key')
data = st.text_input('Data')

# Define submit button
if st.button('Submit'):
    # Create entity object
    entity = Entity()
    entity.PartitionKey = partition_key
    entity.RowKey = row_key
    entity.data = data
    
    # Insert entity into table
    table_service.insert_entity(table_name, entity)
    
    # Display success message
    st.success('Data inserted successfully!')