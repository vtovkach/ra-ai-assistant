# RA AI Assistant 
An AI-powered automation tool that processes and submits monthly conversations between Resident Assistants (RAs) and residents to the Residential Life housing portal.

## Motivation Behind the RA AI Assistant Tool
As the Resident Assistant, I enjoy having monthly conversations with residents; however, entering those conversations and answering departmental questions manually is very tedious and extremely time-consuming. Therefore, I decided to develop an automation tool that performs two key tasks. First, it takes notes from my conversations and uses an AI language model to generate well-written, grammatically correct responses to specific questions in the monthly conversation form. Second, this tool automatically fills out and submits the completed form to the housing portal. At the moment, the tool is terminal-based; however, in the future, I plan to develop and integrate a **graphical user interface (GUI)** to make it more user-friendly. 

## Features
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
