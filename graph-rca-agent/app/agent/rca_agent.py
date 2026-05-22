import json
import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from app.graph.query_graph import Neo4jGraph

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is missing from environment variables or your .env file.")


# 1. Define the structural blueprint for your RCA report
class RCADiagnosisSchema(BaseModel):
    root_cause: str = Field(description="The probable technical root cause of the test failure.")
    impacted_component: str = Field(description="The system module or component impacted by this failure.")
    historical_bug: str = Field(description="Mention related historical bugs or write 'None Found'.")
    suggested_fix: str = Field(description="A concrete, actionable code or configuration fix snippet.")
    confidence_score: int = Field(description="Confidence rating of the diagnosis from 0 to 100.")


class RCAAgent:

    def __init__(self):
        # Initialize native SDK client
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"
        self.graph = Neo4jGraph()

    def analyze_failure(self, test_name: str, error_log: str) -> dict:
        # Retrieve contextual neighborhood data from your Neo4j database helper
        graph_context = self.graph.get_test_context(test_name)

        prompt = f"""
You are an expert AI Root Cause Analysis Engineer.
A pytest test has failed.

Test Name:
{test_name}

Failure Log:
{error_log}

Graph Context:
{graph_context}

Analyze the failure log against the provided Graph database context and map out the root cause metrics.
"""

        # 2. Leverage native Google structured configurations to guarantee JSON matching the schema
        config = types.GenerateContentConfig(
            temperature=0.3,
            response_mime_type="application/json",
            response_schema=RCADiagnosisSchema,
        )

        # 3. Call the model
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config,
        )

        # 4. Parse the guaranteed valid JSON string into a Python dictionary
        parsed = json.loads(response.text)

        # STEP 2 INTEGRATION: Automatically write the AI's diagnosis findings back into your Neo4j Graph database!
        self.graph.save_failure_analysis(
            test_name=test_name,
            root_cause=parsed["root_cause"],
            impacted_component=parsed["impacted_component"],
            historical_bug=parsed["historical_bug"],
            suggested_fix=parsed["suggested_fix"],
            confidence_score=parsed["confidence_score"]
        )

        # Return the dictionary back to the Streamlit UI dashboard execution block
        return parsed