from app.agent.rca_agent import RCAAgent

agent = RCAAgent()

result = agent.analyze_failure(
    test_name="test_login",
    error_log="""
AssertionError:
Expected status code 200
Received 500 Internal Server Error
"""
)

print("\n=== AI RCA REPORT ===\n")
print(result)