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

## Web App

To run the web app, use the following command:

```bash
streamlit run webapp/streamlit/st_app.py
```

## IDEAs

1. Generate a topic list.
    1. Save it somewhere.
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

### General

- [ ] Change the name of all `convert_to_secret_str` to `v1`
- [ ] SentenceSplitter should return a `SentenceSplitResult` pydantic model object
- [ ] The difficulty template conversation can be written once in english
- [ ] Add more conversation samples in different languages and for different levels of understanding
    Just once in english
- [x] Uniform the naming convention for `BlahResult` or `BlahResponse`, with the matching `BlahGenerator` of `Blaher`
- [ ] Wrap the template and prompts in a `BlahPrompt` class
    Which makes it easier to change them for locale or difficulty
- [ ] Add test coverage report
- [ ] Move the creation of a `structured_llm` to a separate class
- [ ] Build a `Generator` abstract class to move the `invoke` common logic to a single place
    Nah, it's not worth it, the `invoke` method must return a `BlahResult` object
    of the proper type, its a mess

### Web App

- [ ] Add getters and setters for weird app/conversation/words attributes
- [x] Show the written turn as you select the options
- [x] Pass the app to all the components
- [ ] Show an indicator of the current turn out of the total turns
- [ ] Do not pass the language to the conversation
- [ ] Add option to toggle showing the original as a hint in the sidebar
- [ ] Reset the conversation at the end of the conversation
    - [ ] Add an option to continue instead
- [x] Develop the user input step
- [x] Add a field to input the `OPENAI_API_KEY`
- [ ] Add a `Difficulty` picker to the web app
- [ ] Add a `Language` picker to the web app
- [ ] Add a `Topic` picker to the web app
    - [ ] Fancier generator
- [ ] Count points for each correct answer
