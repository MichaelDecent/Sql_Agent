# main.py
from workflows.workflow_setup import setup_workflow
from config.settings import set_env


def main():

    set_env("OPENAI_API_KEY")

    app = setup_workflow()

    messages = app.invoke(
        {"messages": [("user", "Which sales agent made the most in sales in 2009?")]}
    )

    print(messages)


if __name__ == "__main__":
    main()
