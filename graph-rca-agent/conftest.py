import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        print("\n=== FAILURE DETECTED ===")

        test_name = item.name
        error_log = str(call.excinfo.value)

        print("Test:", test_name)
        print("Error:", error_log)

        try:
            from app.agent.rca_agent import RCAAgent

            agent = RCAAgent()

            result = agent.analyze_failure(
                test_name=test_name,
                error_log=error_log
            )

            print("\n=== AI RCA REPORT ===")
            print(result)

        except Exception as e:
            print("\nAI Agent Error:")
            print(str(e))