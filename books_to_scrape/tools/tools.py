from browser_use import Tools

basic_extraction_tools: Tools = Tools(
    exclude_actions=[
        # Navigation & Browser Control
        "navigate",
        "search",
        "go_back",
        # Page Interaction
        "click",
        "input",
        "upload_file",
        "send_keys",
        # Tab Management
        "switch",
        "close",
        # Form Controls
        "dropdown_options",
        "select_dropdown",
        # File Operations
        "write_file",
        "read_file",
        "replace_file",
    ]
)
