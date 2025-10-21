# cam slover
# setup
### you need to set up phi min for using this application first 


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
