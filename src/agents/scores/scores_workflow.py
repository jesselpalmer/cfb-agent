from src.agents.scores.scores_agent import ScoresAgent
from src.agents.scores.scores_analyzer_agent import ScoresAnalyzerAgent
from src.agents.scores.scores_qa_agent import ScoresQAAgent


def scores_workflow(user_message: str) -> str:
    """
    Orchestrate a workflow: Score → Analyzer → QA.

    This workflow:
    1. Gets scores using ScoresAgent
    2. Adds color/analysis using ScoresAnalyzerAgent
    3. Reviews and improves using ScoresQAAgent

    Args:
        user_message: The user's query about scores

    Returns:
        Final enhanced and reviewed response
    """
    # Step 1: Get scores
    score_agent = ScoresAgent()
    raw_content = score_agent.handle([{"role": "user", "content": user_message}])

    # Step 2: Add analysis and color
    analyzer = ScoresAnalyzerAgent()
    analyzed_content = analyzer.analyze(raw_content)

    # Step 3: QA review (pass original request to verify response matches)
    qa = ScoresQAAgent()
    final_response = qa.review(analyzed_content, original_request=user_message)

    return final_response
