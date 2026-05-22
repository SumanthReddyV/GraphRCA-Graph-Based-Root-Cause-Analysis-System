import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


class Neo4jGraph:

    def __init__(self):
        """Initializes the official Neo4j driver connection using environment variables."""
        self.driver = GraphDatabase.driver(
            URI,
            auth=(USERNAME, PASSWORD)
        )

    def close(self):
        """Closes the active driver connection pool cleanly."""
        self.driver.close()

    def get_test_context(self, test_name: str) -> list:
        """
        GraphRAG Retrieval Context Layer: Matches a failing TestCase node 
        and extracts its surrounding ecosystem metadata (Components, Requirements, 
        and historical Bug Reports) to form a high-context prompt payload.
        """
        query = """
        MATCH (t:TestCase {name: $test_name})
        OPTIONAL MATCH (t)-[:TESTS]->(c:Component)
        OPTIONAL MATCH (b:BugReport)-[:IMPACTS]->(c)
        OPTIONAL MATCH (r:Requirement)-[:VALIDATED_BY]->(t)

        RETURN 
            t.name AS test,
            c.name AS component,
            b.issue AS related_bug,
            r.name AS requirement
        """

        with self.driver.session() as session:
            result = session.run(query, test_name=test_name)
            
            data = []
            for record in result:
                data.append({
                    "test": record["test"],
                    "component": record["component"],
                    "related_bug": record["related_bug"],
                    "requirement": record["requirement"]
                })
            return data

    def save_failure_analysis(
        self,
        test_name: str,
        root_cause: str,
        impacted_component: str,
        historical_bug: str,
        suggested_fix: str,
        confidence_score: int
    ):
        """
        Database Write-Back Audit Layer: Programmatically generates a fresh 
        :FailureAnalysis documentation node and safely builds its relationship edges 
        to track error telemetry over time.
        """
        query = """
        MATCH (t:TestCase {name: $test_name})

        CREATE (f:FailureAnalysis {
            root_cause: $root_cause,
            impacted_component: $impacted_component,
            historical_bug: $historical_bug,
            suggested_fix: $suggested_fix,
            confidence_score: $confidence_score,
            timestamp: datetime()
        })

        CREATE (f)-[:ANALYZED_TEST]->(t)

        WITH f
        MATCH (c:Component {name: $impacted_component})
        CREATE (f)-[:IMPACTS_COMPONENT]->(c)

        RETURN f
        """

        with self.driver.session() as session:
            session.run(
                query,
                test_name=test_name,
                root_cause=root_cause,
                impacted_component=impacted_component,
                historical_bug=historical_bug,
                suggested_fix=suggested_fix,
                confidence_score=confidence_score
            )