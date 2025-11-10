# RA AI Assistant 
An AI-powered automation tool that processes and submits monthly conversations between Resident Assistants (RAs) and residents to the Residential Life housing portal.

## Motivation Behind the RA AI Assistant Tool
As the Resident Assistant, I enjoy having monthly conversations with residents; however, entering those conversations and answering departmental questions manually is very tedious and extremely time-consuming. Therefore, I decided to develop an automation tool that performs two key tasks. First, it takes notes from my conversations and uses an AI language model to generate well-written, grammatically correct responses to specific questions in the monthly conversation form. Second, this tool automatically fills out and submits the completed form to the housing portal. At the moment, the tool is terminal-based; however, in the future, I plan to develop and integrate a **graphical user interface (GUI)** to make it more user-friendly. 

## Features
- **FERPA Compliant** — The tool uses name tokenization to conceal real names before sending data to OpenAI. All sensitive personal data remains local. Users are responsible for ensuring that no other personally identifiable information is        included in the notes. Only the resident’s first name can be safely included.
- Automatically generates responses for Residential Life form questions  
- Automated login and form submission  
- Session persistence for continued authentication  
- Asynchronous task handling for multiple residents
- Currently terminal-based; a graphical user interface (GUI) will be added in the near future. 

## Technology Stack
- **Python** — Core logic and structure  
- **Playwright** — Browser automation  
- **OpenAI API** — AI-powered response generation  
- **Asyncio** — Concurrent task management

## How It's used
> **Note:**  
> This tool is designed specifically for the **Texas State University Housing System** and will not function with other institutions' platforms.
> 
### Step 1: Add ResLife Form Questions and set up notes directory
First, copy all questions from the ResLife form into the `config/questions` file.  
You can find detailed instructions [here](https://github.com/vtovkach/ra-ai-assistant/blob/main/config/readme.md).
Next, create a `notes` directory where you will store text files containing conversation notes for each resident.

### Step 2: Create .env file 
Create a `.env` file in the project root and include the following environment variables:
- `OPENAI_API_KEY` — your OpenAI API key  
- `DASH_URL` — URL to the dashboard of the internal housing management website  
- `FORM_URL` — URL to the ResLife form page 
- `LOGIN_URL` — URL to the login page of the housing website
  
### Step 3: Install Dependencies
Before launching the app, it is neccessary to install the required libraries:
- `playwright`  
- `openai`  
- `dotenv`  
- `pathlib`
  
### Step 4: Launch the Application
Run the application using:
```bash
python src/main.py
```
Here is the list of available commands:
- **status** — show current processing status  
- **show [name]** or **show all** — display resident's info  
- **process [name]** or **process all** — generate answers for questions 
- **submit [name]** or **submit all** — submit responses automatically  
- **save** — save current progress  
- **clear** — clear generated data  
- **exit** — close the application

## Author
Developed by **Vadym T**  
For questions or collaboration, feel free to contact me at vadim003600@gmail.com
