<h1 align="center">🤖 FitGenie Agent</h1>

<p align="center">
  <strong>Personal Fitness Planner powered by OpenAI Agents</strong><br>
  Identify missing workouts, get tailored nutrition advice, and discover workout courses – all in one assistant.
</p>

<hr>

<h2>📌 Project Overview</h2>

<p>
FitGenie is a multi-agent system that assists users in achieving their fitness goals using AI. It listens to the user's queries and intelligently routes them to specialist agents:
</p>

<ul>
  <li>🏋️ <strong>Fitness Gap Specialist</strong>: Analyzes your workout routine and finds missing elements</li>
  <li>🥗 <strong>Nutrition Advisor</strong>: Suggests dietary tips based on your goal</li>
  <li>📚 <strong>Course Recommender</strong>: Recommends online courses/tutorials for specific workouts</li>
</ul>

<hr>

<h2>🚀 Features</h2>

<ul>
  <li>🔍 Goal-based planning (Weight Loss, Muscle Gain, Flexibility)</li>
  <li>⚙️ Multi-agent orchestration via OpenAI</li>
  <li>💬 Simple query-to-response interaction</li>
  <li>📦 Built with <code>Python</code>, <code>Pydantic</code>, <code>AsyncOpenAI</code>, and <code>dotenv</code></li>
</ul>

<hr>

<h2>🧠 How It Works</h2>

<ol>
  <li>The main <code>FitGenie</code> agent receives user queries</li>
  <li>Based on the query, it delegates to one of three agents</li>
  <li>Each agent uses specialized tools to return helpful suggestions</li>
</ol>

<hr>

<h2>📂 Folder Structure</h2>

<pre>
fitgenie-agent/
│
├── .gitignore
├── fitgenie.py              ← Main script
├── agents/                  ← Agent classes and helper tools
├── .env                     ← Contains BASE_URL, API_KEY, MODEL_NAME
└── README.md
</pre>

<hr>

<h2>⚙️ Setup Instructions</h2>

<ol>
  <li>Clone the repository</li>
  
  <pre><code>git clone https://github.com/Mehadii-Hassan/FitGenie-Agent.git</code></pre>

  <li>Install dependencies</li>

  <pre><code>pip install -r requirements.txt</code></pre>

  <li>Create a <code>.env</code> file with your OpenAI credentials</li>

  <pre><code>
BASE_URL=https://api.openai.com/v1
API_KEY=your-api-key-here
MODEL_NAME=gpt-4o
  </code></pre>

  <li>Run the program</li>

  <pre><code>python fitgenie.py</code></pre>
</ol>

<hr>

<h2>🧪 Sample Queries</h2>

<ul>
  <li><code>I want to lose weight</code></li>
  <li><code>I only do Cardio. What's missing?</code></li>
  <li><code>Suggest a good workout course for HIIT</code></li>
  <li><code>What should I eat to gain muscle?</code></li>
</ul>

<hr>

<h2>🙌 Credits</h2>

<p>
Created by <strong>Mehadi Hassan</strong> using the OpenAI multi-agent SDK.
</p>

<hr>

<p align="center">⭐ Star this repo if you find it helpful!</p>
