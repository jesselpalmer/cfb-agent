from src.agents.cfb_agent import CfbAgent
from src.core import parse_args, setup_logging


def main():
    """
    Main entry point for the College Football Agent application.

    Creates an instance of CfbAgent and processes user queries.
    """
    args = parse_args()
    setup_logging(args.log_level)

    user_message = """
    Hi, can you give me the results of games that the Hokies played within 12 months 
    of December 6th, 2025?
    """

    # Create the main agent
    agent = CfbAgent()
    response = agent.chat(user_message)

    print(response)


if __name__ == "__main__":
    main()
