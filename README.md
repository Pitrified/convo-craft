# ConvoCraft

Generate conversations and let the user translate them to learn a new language.

## Installation

To install the package, run the following command:

```bash
poetry install
```

## Setup

To setup the package, create a `.env` file in `~/cred/convo_craft/.env` with the following content:

```bash
SAMPLE_ENV_VSCODE=sample
```

and for VSCode to recognize the environment file, add the following line to the
workspace settings file at `convo_craft/.vscode/settings.json`:

```json
"python.envFile": "/home/pmn/cred/convo_craft/.env"
```

or use the VSCode interface.

## Testing

To run the tests, use the following command:

```bash
poetry run pytest
```

or use the VSCode interface.

## IDEAs

1. Generate conversations in target language,
   two people talking to each other,
   about one sentence each.
    1. Some way to set the difficulty of the conversation.
1. Let the user fill one side of the conversation.
    1. Optional: use a shuffle and show the sentence in a random order.
    1. Optional: Translate the conversation and show the known language version.
        The user inputs the target language version as free text.
    1. Optional: Use a speech-to-text API to input the target language version.
    1. Very optional: Let the user write any answer and check if it makes sense in the context.

## TODOs

- [ ] Add test coverage report
- [ ] Add more conversation samples in different languages and for different levels of understanding