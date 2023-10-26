import streamlit as st
import requests
import io

# change api_key
api_key = "pak-co1XNgYIltFNovr-6062CCujNGjbPkI0RDH0cfNuYYY"
api_url = "https://bam-api.res.ibm.com/v1/"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


# function - obtain pdf information
def file_info(uploaded_file):
    file_contents = uploaded_file.getvalue()
    file_obj = io.BytesIO(file_contents)
    with open(uploaded_file.name, "wb") as f:
        f.write(file_contents)
    file_path = f.name
    st.write(f"You selected '{uploaded_file.name}'")
    st.write(f"File path: {file_path}")

# upload email
uploaded_email = st.file_uploader("Upload your email: ")
if uploaded_email:
    file_info(uploaded_email)
# upload contract
uploaded_contract = st.file_uploader("Upload your contract: ")
if uploaded_contract:
    file_info(uploaded_contract)


prompt_template = '''
        Obtain the context of discount percentage requests of products via email.
        Obtain the context of agreed discount of those products on contract. 
        Compare discounts for those products.
        The result of comparison should look like below:
        Product List #1:
        - Product Name: [Product Name]
        - Product Quantity: [Quantity]
        - discount on contract: [discount request from vender] %
        - discount via email: [discount request by buyer] %
        [Repeat the structure for each product mentioned in email]

        Answer the question based on the context below. If the question cannot be answered using the information provided answer with "I don't know".


        Context:
        {content}

        Output: 

        '''
contract_data = st.text_input("Is there any request? (eg. Please find out if there is any ambiguity.)")
prompt = prompt_template.format(content=contract_data)

data = {
    "model_id": "meta-llama/llama-2-7b-chat",
    "inputs": [prompt],
    "parameters": {
        "decoding_method": "greedy",
        "repetition_penalty": 1,
        "min_new_tokens": 50,
        "max_new_tokens": 900,
        "moderations": {
            "hap": {
                "input": True,
                "threshold": 0.7,
                "output": True
            }
        }
    }
}



url = api_url + 'generate'
response = requests.post(url=url, json=data, headers=headers)
generated_text = response.json().get('results')[0]['generated_text']


st.title("E_mail Check Function")

st.write("This is your answer:", generated_text)
