# fact_frenzy
## 🎉 Fact Frenzy 🎉*

Welcome to Fact Frenzy, the ultimate trivia API project that brings knowledge, fun, and curiosity together in one place! 🚀

## 🌟 What is Fact Frenzy?

Fact Frenzy is a Python-powered project designed to fetch fascinating trivia questions from the The Trivia API. Whether you’re a quiz enthusiast, a curious learner, or just looking to spice up your app with some trivia fun, Fact Frenzy has got you covered! 🧠✨

## 🛠️ Features

- 🌍 Categories Galore: Choose trivia questions from categories like science, history, sports, and more!
- 📊 Difficulty Levels: From easy peasy to brain-melting, pick your challenge!
- 🎯 Customizable Queries: Specify question types, tags, and limits for tailored trivia.
- 🔥 Fast and Reliable: Powered by requests and clean code principles.

## 📦 Project Structure
```
fact_frenzy/
├── src/
│   ├── trivia_api.py       # API connection logic
│   ├── __init__.py         # Module initializer
├── tests/
│   ├── test_trivia_api.py  # Unit tests for the API
├── README.md               # You're reading it!
├── pyproject.toml          # Poetry configuration
└── .pre-commit-config.yaml # Pre-commit hooks for code quality
```

## 🚀 Getting Started

### 1️⃣ Clone the Repo

git clone https://github.com/MightContainNuts/fact-frenzy.git
cd fact-frenzy

### 2️⃣ Set Up the Environment
	•	Install dependencies with Poetry:

```poetry install```


_Activate the environment:_

```poetry shell```



### 3️⃣ Run the App !

```python src/trivia_api.py```

## 🧪 Running Tests

We believe in clean, bug-free code! Run the tests using pytest:

```pytest```

## 🎨 Code Style

We enforce clean and consistent code with:
- Black: Automatic code formatting.
- Flake8: Style guide enforcement.
- commit Hooks: Ensures all commits meet quality standards.

## 🤖 API Example

Here’s how easy it is to fetch trivia:
```
from src.trivia_api import ConnectToApi

api_instance = ConnectToApi(difficulty="medium", categories=["science"], limit=5)
trivia_questions = api_instance.connect_to_api()

for question in trivia_questions:
    print(question["question"])
```

## 💡 Contributing

We welcome contributions! To get started:
1. Fork the repo 🍴
2. Create a feature branch 🌿
3. Submit a pull request 🚀

## 🎉 Fun Fact

Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible! 🍯

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute as you see fit!

Made with ❤️ by _MightContainNuts_

**_Let the trivia frenzy begin!_** 🎊
