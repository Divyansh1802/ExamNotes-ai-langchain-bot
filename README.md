# ExamNotes-ai-langchain-bot

# 📚 AI Notes Generator

An AI-powered academic notes generation API built with **FastAPI**, **LangChain**, and **Groq (LLaMA 3.1)**. It generates structured, exam-oriented notes on any topic tailored to the student's academic level and exam type — returning rich, schema-validated JSON ready for frontend rendering.

**🔗 Live Demo:** [https://examnotes-ai-langchain-bot.onrender.com](https://examnotes-ai-langchain-bot.onrender.com)

---

## ✨ Features

- 🤖 **LLM-Powered** — Uses Groq's `llama-3.1-8b-instant` for fast, high-quality note generation
- 🎯 **Exam-Focused** — Tailored content based on academic level and exam type (JEE, UPSC, GATE, etc.)
- 🧱 **Structured Output** — Returns richly typed JSON blocks: headings, paragraphs, lists, tables, charts, images, quotes, and code
- ✅ **Schema Validated** — Every response is validated against a strict JSON schema before being returned
- ⚡ **FastAPI** — High-performance async REST API with auto-generated Swagger docs

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| LLM Orchestration | LangChain |
| LLM Provider | Groq (`llama-3.1-8b-instant`) |
| Schema Validation | jsonschema |
| Environment Config | python-dotenv |
| Deployment | Render |

---

## 📁 Project Structure

```
.
├── main.py            # FastAPI app, routes, LLM chain
├── json_schema.json   # JSON schema for notes structure validation
├── .env               # Environment variables (GROQ_API_KEY)
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A [Groq API key](https://console.groq.com/)

### Installation

```bash
git clone https://github.com/your-username/ai-notes-generator.git
cd ai-notes-generator
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`.

---

## 📖 API Reference

### `POST /api/v1/aiNotes`

Generates structured academic notes for a given topic.

#### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `topic` | string | ✅ | The subject/topic to generate notes on |
| `level` | string | ✅ | Academic level (e.g., `Class 12`, `Undergraduate`, `Postgraduate`) |
| `exam_type` | string | ✅ | Target exam (e.g., `JEE`, `UPSC`, `GATE`, `CBSE`, `MBA`) |

#### Example Request

```bash
curl -X POST "https://examnotes-ai-langchain-bot.onrender.com/api/v1/aiNotes?topic=Photosynthesis&level=Class%2012&exam_type=NEET"
```

#### Example Response

```json
[
  {
    "type": "heading",
    "content": "Photosynthesis"
  },
  {
    "type": "paragraph",
    "content": "Photosynthesis is the process by which green plants convert sunlight into chemical energy..."
  },
  {
    "type": "table",
    "headers": ["Parameter", "Light Reaction", "Dark Reaction"],
    "rows": [
      ["Location", "Thylakoid membrane", "Stroma"],
      ["Product", "ATP, NADPH", "Glucose"]
    ]
  },
  {
    "type": "chart",
    "title": "Factors Affecting Photosynthesis",
    "chartType": "bar",
    "labels": ["Light", "CO₂", "Temperature", "Water"],
    "datasets": [{ "label": "Impact (%)", "data": [40, 30, 20, 10] }]
  }
]
```

#### Error Responses

| Status | Reason |
|---|---|
| `500` | LLM returned invalid JSON |
| `500` | Schema validation failed |

---

## 🧱 Supported Block Types

The API returns an array of typed content blocks, each designed for direct frontend rendering:

| Block Type | Description |
|---|---|
| `heading` | Section and subsection titles |
| `paragraph` | Explanatory text |
| `list` | Bullet points, key facts, formulas |
| `table` | Comparisons, classifications, formula sheets |
| `chart` | Bar, line, pie charts with datasets |
| `image` | Diagrams, flowcharts, anatomical structures |
| `quote` | Definitions, laws, and principles |
| `code` | Code snippets (for CS/programming topics) |

---



Update the `origins` list in `main.py` to add your frontend's production URL.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
