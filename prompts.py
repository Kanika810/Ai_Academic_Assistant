def get_prompt(task, user_input, extra=""):
    if task == "Summarize":
        return f"Summarize the following text in simple points:\n{user_input}"

    elif task == "Sentiment":
        return f"Classify the sentiment (Positive, Negative, Neutral):\n{user_input}"

    elif task == "Q&A":
        return f"Answer the question clearly:\n{user_input}"

    elif task == "Translate":
        return f"Translate the following text to {extra}:\n{user_input}"

    elif task == "Compare":
        return f"Compare the following concepts in a table:\n{user_input}"

    elif task == "Reasoning":
        return f"Solve step-by-step:\n{user_input}"

    elif task == "Format":
        return f"Format this professionally:\n{user_input}"

    return user_input