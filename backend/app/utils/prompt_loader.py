from pathlib import Path


PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"


def load_prompt(
    prompt_name: str,
) -> str:
    """
    Load prompt template from file.
    """

    prompt_file = (
        PROMPT_DIR /
        prompt_name
    )


    if not prompt_file.exists():

        raise FileNotFoundError(
            f"Prompt file not found: {prompt_name}"
        )


    return prompt_file.read_text(
        encoding="utf-8"
    )