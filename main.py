from src.agents.cfb_agent import CfbAgent


def main():
    """
    Main entry point for the College Football Agent application.

    Creates an instance of CfbAgent and processes user queries.
    """
    user_message = (
        "Hi, can you give me the score for the game between Virginia Tech and Georgia Tech?"
    )

    # Create the main agent
    agent = CfbAgent()
    response = agent.chat(user_message)

    print(response)


if __name__ == "__main__":
    main()
