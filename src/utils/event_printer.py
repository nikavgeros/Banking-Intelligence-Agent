def _print_event(event: dict, _printed: set, max_length=1500):
    """
    Process and optionally print, return, or write the message to a file.

    Args:
        event (dict): The event containing dialog state and messages.
        _printed (set): A set of message IDs that have already been processed.
        max_length (int): The maximum length of the message to be printed or saved.

    Returns:
        str: The formatted message, if no file writing is specified.
    """
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])

    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"

            # Print the message
            print(msg_repr)

            # Add to the printed set
            _printed.add(message.id)

            # Return the message
            return msg_repr


def run_sample_questions(user_approval_graph, config, questions):
    """
    Processes a list of user questions through the Banking Intelligence Agent.
    Prompts the user for tool action approval when necessary.

    Args:
        config: Configuration settings for the system.
        questions: List of user queries to process.
    """
    _printed = set()

    for question in questions:
        print(f"\n**User Question:** {question}")
        events = user_approval_graph.stream({"messages": ("user", question)}, config, stream_mode="values")

        for event in events:
            _print_event(event, _printed)

        snapshot = user_approval_graph.get_state(config)

        while snapshot.next:
            # Handle tool usage approval or user input changes
            user_input = input(
                "\nDo you approve of the above actions? Type 'y' to continue; "
                "otherwise, explain your requested changes.\n\n"
            ).strip()

            if user_input.lower() == "y":
                result = user_approval_graph.invoke(None, config)
            else:
                # Handle denied tool invocation with user feedback
                result = user_approval_graph.invoke(
                    {
                        "messages": [
                            ToolMessage(
                                tool_call_id=event["messages"][-1].tool_calls[0]["id"],
                                content=f"API call denied by user. Reasoning: '{user_input}'. Continue assisting, accounting for the user's input.",
                            )
                        ]
                    },
                    config,
                )
            snapshot = user_approval_graph.get_state(config)
