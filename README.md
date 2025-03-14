### **Desenvolvimento de um Módulo Python Django para Gerar Relatórios Utilizando Chatbot Local**
---
This project aims to develop an application that uses the user's input in natural language (NLP) to generate specific SQL queries that will be executed on the server's database. The user's input is processed by the LLM (Large Language Model) and, with the help of RAG (Retrieval-Augmented Generation), it retrieves the appropriate tables and attributes.

* The LLM does not have direct access to the database; it only knows the schema and constructs the queries.
* The LLM runs locally using Meta's deprecated model, `Llama 3.1`, with a free Google Colab GPU instance for testing.

### Technologies Used:
* **Python 3**
  * **Django Web Framework**
    * **HTML / CSS / JS**
* **Oracle MySQL Database Management System (DBMS)**
* **LLM - Large Language Model**
* **NLP - Natural Language Processing**
* **Structured Data**
  * JSON
  * SQL
