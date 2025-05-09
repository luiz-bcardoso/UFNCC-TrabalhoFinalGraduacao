### **Módulo LLM Local em Sistema Web para Geração de Relatórios Textuais via Prompt**
---
Este projeto tem como objetivo desenvolver um aplicativo que usa a entrada do usuário em linguagem natural (NLP) para gerar consultas SQL específicas que serão executadas no banco de dados do servidor. A entrada do usuário é processada pelo LLM (Modelo de Linguagem de Grande Escala) e, com o auxílio do RAG (Geração Aumentada por Recuperação), ele recupera as tabelas e atributos apropriados.

* O LLM não tem acesso direto ao banco de dados; ele apenas conhece o esquema e constrói as consultas.
* O LLM é executado localmente utilizando o modelo descontinuado da Meta, `Llama 3.1`, em uma instância gratuita de GPU no Google Colab.


![alt text](https://github.com/luiz-bcardoso/UFNCC-TrabalhoFinalGraduacao/blob/main/visao-geral.png?raw=true)

![alt text](https://github.com/luiz-bcardoso/UFNCC-TrabalhoFinalGraduacao/blob/main/exemplo-pergunta.png?raw=true)

### Tecnlogias Utilizadas:
* **Python 3**
  * Jupyter Notebooks
  * Django Framework
    * HTML / CSS / JS
* **LLM - Large Language Model**
* **NLP - Natural Language Processing**
* **Dados estruturados**
  * JSON
  * SQL



## ** :us: Local LLM Moudule for Django Projects to Generate Reports via SQL Using NLP**
This project aims to develop an application that uses the user's natural language input (NLP) to generate specific SQL queries, which will then be executed on the server's database. The user's input is processed by a Large Language Model (LLM) and, with the help of Retrieval-Augmented Generation (RAG), it retrieves the relevant tables and attributes.

* The LLM does not have direct access to the database; it only has knowledge of the schema and generates the queries based on that information.
* The LLM runs locally using Meta's deprecated `Llama 3.1 model`, with the processing power provided by a free Google Colab GPU instance.