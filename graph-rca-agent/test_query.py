from app.graph.query_graph import Neo4jGraph

graph = Neo4jGraph()

context = graph.get_test_context("test_login")

print("\n=== GRAPH CONTEXT ===\n")

for item in context:
    print(item)

graph.close()
