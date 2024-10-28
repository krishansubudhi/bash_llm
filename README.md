

Instructions:
1. Clone the repo. Install ther requirements
   ```
   pip install -r requirements.txt
   ```
2. Create a .env file in the bash_llm root directory. Write this.
    OPENAI_API_KEY=your_api_key_here

3. Test `python main.py who are you?`
4. Set alias  (replace the path to repo with yours)
    ```
    echo "alias llm='python ~/repos/bash_llm/main.py'" >> ~/.bashrc
    source ~/.bashrc
    ```
5. Enjoy calling llm from your command line.
    ```
    llm command to find all python files in this directory.
    ```