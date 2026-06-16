from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import json
from jsonschema import ValidationError, validate
from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware



load_dotenv()

app = FastAPI(
    title = "AI Notes Generator",
    version = "1.0.0"
)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)


model = ChatGroq(
    model =  'llama-3.1-8b-instant'
)

with open("json_schema.json","r",encoding="utf-8") as f:
    schema = json.load(f)

template = PromptTemplate(
    template= """
You are an expert academic note-maker, educator, and exam preparation specialist.

Generate comprehensive, exam-oriented notes on the topic {topic}.

Target Audience:
- Academic Level: {level}
- Exam Type: {exam_type}

IMPORTANT:
Return ONLY valid JSON.
Do NOT return markdown.
Do NOT wrap the response in backticks.
The response MUST strictly follow the provided schema.
schema: {schema}

Content Requirements:

1. Create detailed, well-structured notes suitable for scoring high marks in {exam_type}.
2. Start with a concise overview of the topic.
3. Explain all important concepts, definitions, principles, formulas, derivations, and key ideas.
4. Use simple language while maintaining academic correctness.
5. Include examples wherever helpful.
6. Include comparison tables whenever concepts can be compared.
7. Include important facts, shortcuts, tricks, and memory aids.
8. Include frequently asked exam questions.
9. Include common mistakes and misconceptions.
10. End with a quick revision summary.

Block Usage Rules:

- Use "heading" blocks for all major sections and subsections.
- Use "paragraph" blocks for explanations.
- Use "list" blocks for bullet points, key takeaways, formulas, facts, and revision notes.
- Use "table" blocks for comparisons, classifications, formula sheets, advantages/disadvantages, etc.
- Use "chart" blocks whenever numerical, statistical, trend-based, scientific, business, economic, or analytical data can be visualized.
- Use "image" blocks whenever a diagram, flowchart, architecture, process, cycle, structure, anatomy, network, circuit, graph, map, or visual representation would improve understanding.
- Use "quote" blocks for important definitions, laws, principles, or memorable statements.
- Use "code" blocks only if the topic involves programming, algorithms, or technical implementation.

Image Block Rules:

For image blocks:
- Do provide real URLs.
- Put a detailed image-generation description inside the "description" field.
- Include labels, components, arrows, relationships, and layout instructions.

Chart Block Rules:

For chart blocks:
- Always provide:
  - title
  - chartType
  - description
  - labels
  - datasets
- Use realistic educational data.
- Ensure data supports the explanation being taught.

Table Rules:

For table blocks:
- Include meaningful column names.
- Ensure rows contain educationally useful information.

Output Quality Requirements:

- Notes should be comprehensive and exam-focused.
- Maintain logical ordering of blocks.
- Use multiple block types whenever appropriate.
- Include diagrams and charts whenever they add educational value.
- Generate content that can directly be rendered by a frontend using the provided schema.

Generate notes on:
Topic: {topic}
Level: {level}
Exam Type: {exam_type}
     
    """ ,
    input_variables = ['topic','level','exam_type'],
    partial_variables = {
        "schema": json.dumps(schema, indent=2)
    }
 
)


@app.post("/api/v1/aiNotes")
def generate_notes(
    topic: str, level: str, exam_type: str
):
    
    prompt = template.invoke({
        
     "topic": topic,
     "level": level,
     "exam_type": exam_type,
     
    })
    
    response = model.invoke(prompt)
    try:
        
       content = response.content.strip()
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()
            
        data = json.loads(content)
        
        if "data" in data:
            data = data["data"]
            
        validate(
           instance= data,
           schema= schema )
        
        return  data
   
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail="LLM returned invalid JSON."
        )

    except ValidationError as e:
       raise HTTPException(
            status_code=500,
            detail=f"Schema validation failed: {e.message}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host= "0.0.0.0",
        port= "8000"
    )
