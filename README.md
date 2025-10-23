# local_ai_automation
# setup
### you need to set up phi for using this application first 


A quick guide to run Microsoft's Phi-4 Mini AI model locally on your computer.

## What You'll Need
- At least 8GB RAM
- 5GB free disk space
- Internet connection for download

## Step 1: Install Ollama

### Windows
Download and run the installer:
- [Download Ollama for Windows](https://ollama.com/download/windows)

### Mac
Download and run the installer:
- [Download Ollama for Mac](https://ollama.com/download/mac)

### Linux
Open terminal and run:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Step 2: Install Phi-4 Mini

Open your terminal/command prompt and run:
```bash
ollama run phi4
```

That's it! The model will download and start automatically.

## Step 3: Start Using It

After installation, just type your questions and press Enter. For example:
```
>>> What is machine learning?
```

### Useful Commands
- `ollama list` - See installed models
- `ollama pull phi4` - Download without running
- `/bye` - Exit the chat

## Need Help?
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Phi-4 Model Page](https://ollama.com/library/phi4)

---
**Note:** First download takes a few minutes depending on your internet speed.
Perfect — your thinking is spot on.

At this stage, your **README should stay lightweight and focused on clarity + setup**. You don’t want to clutter it with every implementation detail yet, especially since your OCR + automation pipeline is still evolving.

Here’s what I’d recommend:
✅ **Keep the setup + install section exactly as you wrote it** — it’s clean, clear, and easy to follow.
✅ Add a **“Project Overview”** section briefly explaining what the automation does now (the screenshot-to-AI pipeline).
✅ Update the **“Current Status”** section to reflect the *current working flow* and note that detailed documentation will come after full stabilization.

Here’s a refined version you can paste in directly:

---


## 🧰 Project Overview

This project automates **question solving using AI and OCR**.
Instead of scraping text from websites, the system captures **screenshots** of questions, uses **OCR to extract text**, and then feeds it to the **Phi-4 Mini AI model** to generate accurate answers and code solutions automatically.

The pipeline currently supports:

* Screenshot-based input capture
* OCR-based text recognition
* Phi-4 powered intelligent response generation

Future versions will include:

* Automated region detection for questions
* Answer logging and verification modules
* Multi-screen workflow support

---

##  Current Status (Active Development)

| Component              | Status         |
| ---------------------- | -------------- |
| Phi-4 Mini AI          | Working      |
| Screenshot Capture     | Working      |
| OCR Text Extraction    | ISSUE       |
| AI Answer Generation   | Functional   |
| Automation Integration | In progress |
| Full Workflow Docs     | Coming soon |

---

## 📘 Note

This is an **early working version**.
Once the full automation pipeline is complete, the README will be expanded with detailed usage examples, configuration instructions, and advanced AI integrations.

---

This version gives clarity, structure, and a professional look without overloading the user.

We appreciate your patience and welcome contributions to help resolve this!
