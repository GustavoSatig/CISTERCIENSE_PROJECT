# Passos para Instalar o Projeto

Siga os passos abaixo para configurar e executar o projeto:

1. **Certifique-se de ter o Python instalado**  
  - Baixe e instale a versão mais recente do Python em [python.org](https://www.python.org/).  
  - Verifique a instalação executando:  
    ```bash
    python --version
    ```

2. **Crie e ative um ambiente virtual (venv)**  
  - No diretório do projeto, crie o ambiente virtual:  
    ```bash
    python -m venv venv
    ```  
  - Ative o ambiente virtual:  
    - **Windows**:  
     ```bash
     venv\Scripts\activate
     ```  
    - **Linux/Mac**:  
     ```bash
     source venv/bin/activate
     ```

3. **Instale as dependências do projeto**  
  - Com o ambiente virtual ativado, instale os requisitos:  
    ```bash
    pip install -r requirements.txt
    ```

4. **Execute o projeto**  
  - Após a instalação, inicie o projeto conforme as instruções específicas do mesmo.  
    ```bash
    python main.py
    ```

5. **Desative o ambiente virtual (opcional)**  
  - Quando terminar, desative o ambiente virtual:  
    ```bash
    deactivate
    ```  

Pronto! O projeto está configurado e pronto para uso.  