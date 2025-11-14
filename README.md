# INFO 5940 
Welcome to the INFO 5940 repository. You will complete your work using [**GitHub Codespaces**](#about-github-codespaces) and save your progress in your own GitHub repository.  
This guide will walk you through setting up the development environment and running your **Retrieval-Augmented Generation (RAG) Chat Agent**.

---

## Getting Started 

### Step 1: Fork this repository 
1. Click the **Fork** button (top right of this page).  
2. This will create a copy of the repo under **your own GitHub account**.

Forking creates a personal copy of the repo under **your** GitHub account.  
- You can commit, push, and experiment freely.  
- Your work stays separate from the official class materials.

---

### Step 2: Open your forked repo Codespace
1. Go to **your forked repo**.  
2. Click the green **Code** button and switch to the **Codespaces** tab.  
3. Select **Create Codespace**.  
4. Wait a few minutes for the environment to finish setting up.

---

### Step 3: Verify your environment 
Once the Codespace is ready:
1. Open your `chat_with_pdf.py` file inside the Codespace editor.  
2. Ensure the **Python 3.11.13 kernel** is selected.  
   - In the top-right corner, click **Select Kernel**.  
   - Choose **Python Environments → Python 3.11.13 (first option)**.  
3. Run the following commands in the terminal to verify setup:  
   ```bash
   python --version
   pip install -r requirements.txt
