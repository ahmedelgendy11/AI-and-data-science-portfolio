# 🤖 Chatbot with Memory & Tool Use (Function Calling)

> A customer-support chatbot that answers from **real, live data** via **tool use (function calling)** and keeps **conversation memory** — fully runnable offline, plus a production path on the real **Claude API**.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Anthropic](https://img.shields.io/badge/Claude-tool--use-D97757) ![GenAI](https://img.shields.io/badge/GenAI-function--calling-6E56CF)

## 📌 Problem
A store wants a chat assistant whose answers are grounded in **real-time data** (order status, product
price, stock) — not the model's general "imagination" — and that **remembers context** ("when will it
arrive?" after asking about a specific order).

## 🧠 How it works
Define tools as real Python functions (`get_order_status`, `get_product_price`, `check_stock`,
`calculate`, `store_info`) with Anthropic **tool schemas**. The model decides which tool to call; you
execute it and return a `tool_result`; the loop repeats until done. A **conversation-memory** object
keeps the full history plus context state (last order discussed) so follow-up questions resolve correctly.

- **Offline version** — a keyword router stands in for the model, exercising the full architecture (tools
  + memory + context) with **no API key required**, so the notebook always runs.
- **Production version** — the real Claude **agentic loop** (`request → tool_use → execute → tool_result`)
  using the *same* tool functions, wrapped in `try/except` so it skips gracefully offline.

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook d3_chatbot_tools_solution.ipynb
```
For the production cell:
```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-...     # Windows: setx ANTHROPIC_API_KEY "sk-..."
```

## 🗂️ Files
- `d3_chatbot_tools_exercise.ipynb` / `_solution.ipynb`
- `data/shop_data.json` — products, orders, store info the tools read from

## 🛠️ Skills demonstrated
`Tool use / function calling` · `Tool schemas` · `Agentic loop` · `Conversation memory` · `Context tracking` · `Claude Messages API`

> 🔁 The `request → tool_use → execute → tool_result → reply` loop is the core of any agent.
