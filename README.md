# Tavus API Test 🧠

A simple Python project that interacts with the [Tavus API](https://docs.tavus.io) to:
- Create a persona
- Start a conversation with that persona

---

## 🚀 Features
- Create and manage personas via API
- Start and monitor conversations

---

## 🧩 Requirements
- Python 3.9+

Install dependencies:
```bash
# create venv
python -m venv .venv

# activate
source .venv/Scripts/activate

pip install -r requirements.txt

#run example 

python main.py --persona fashionAdvisor --conversation defaultConversation --document testDoc
