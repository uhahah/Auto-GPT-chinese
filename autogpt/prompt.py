from colorama import Fore
from autogpt.config.ai_config import AIConfig
from autogpt.config.config import Config
from autogpt.logs import logger
from autogpt.promptgenerator import PromptGenerator
from autogpt.config import Config
from autogpt.setup import prompt_user
from autogpt.utils import clean_input

CFG = Config()


def get_prompt() -> str:
    """
    This function generates a prompt string that includes various constraints,
        commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the Config object
    cfg = Config()

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint(
        "您必须以JSON格式回答，确保回答可以由Python json.loads解析"

    )
    prompt_generator.add_constraint(
        "~短期内存限制为4000字。你的短期记忆很短，所以"
        " 立即将重要信息保存到文件中."
    )
    prompt_generator.add_constraint(
        "如果你不确定自己以前是怎么做的，或者想回忆过去"
        " 事件，思考类似的事件会帮助你记忆"
    )
    prompt_generator.add_constraint("无用户帮助")
    prompt_generator.add_constraint(
        '仅使用英文双引号中列中列出的命令，例如: "command name"'
    )

    # Define the command list
    commands = [
        ("Google Search", "google", {"input": "<search>"}),
        (
            "Browse Website",
            "browse_website",
            {"url": "<url>", "question": "<what_you_want_to_find_on_website>"},
        ),
        (
            "Start GPT Agent",
            "start_agent",
            {"name": "<name>", "task": "<short_task_desc>", "prompt": "<prompt>"},
        ),
        (
            "Message GPT Agent",
            "message_agent",
            {"key": "<key>", "message": "<message>"},
        ),
        ("List GPT Agents", "list_agents", {}),
        ("Delete GPT Agent", "delete_agent", {"key": "<key>"}),
        (
            "Clone Repository",
            "clone_repository",
            {"repository_url": "<url>", "clone_path": "<directory>"},
        ),
        ("Write to file", "write_to_file", {"file": "<file>", "text": "<text>"}),
        ("Read file", "read_file", {"file": "<file>"}),
        ("Append to file", "append_to_file", {"file": "<file>", "text": "<text>"}),
        ("Delete file", "delete_file", {"file": "<file>"}),
        ("Search Files", "search_files", {"directory": "<directory>"}),
        ("Evaluate Code", "evaluate_code", {"code": "<full_code_string>"}),
        (
            "Get Improved Code",
            "improve_code",
            {"suggestions": "<list_of_suggestions>", "code": "<full_code_string>"},
        ),
        (
            "Write Tests",
            "write_tests",
            {"code": "<full_code_string>", "focus": "<list_of_focus_areas>"},
        ),
        ("Execute Python File", "execute_python_file", {"file": "<file>"}),
        ("Generate Image", "generate_image", {"prompt": "<prompt>"}),
        ("Send Tweet", "send_tweet", {"text": "<text>"}),
    ]

    # Only add the audio to text command if the model is specified
    if cfg.huggingface_audio_to_text_model:
        commands.append(
            (
                "Convert Audio to text",
                "read_audio_from_file",
                {"file": "<file>"}
            ),
        )

    # Only add shell command to the prompt if the AI is allowed to execute it
    if cfg.execute_local_commands:
        commands.append(
            (
                "Execute Shell Command, non-interactive commands only",
                "execute_shell",
                {"command_line": "<command_line>"},
            ),
        )

    # Add these command last.
    commands.append(
        ("Do Nothing", "do_nothing", {}),
    )
    commands.append(
        ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
    )

    # Add commands to the PromptGenerator object
    for command_label, command_name, args in commands:
        prompt_generator.add_command(command_label, command_name, args)

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource(
        "用于搜索和信息收集的互联网接入。"
    )
    prompt_generator.add_resource("长期内存管理.")
    prompt_generator.add_resource(
        "GPT-3.5支持的代理用于简单任务的委派。"
    )
    prompt_generator.add_resource("文件输出.")

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation(
        "持续审查和分析您的行动，以确保您执行"
        " 尽你最大的能力."
    )
    prompt_generator.add_performance_evaluation(
        "不断地建设性地自我批评自己的大局观行为."
    )
    prompt_generator.add_performance_evaluation(
        "反思过去的决策和策略，以完善您的方法."
    )
    prompt_generator.add_performance_evaluation(
        "每一个命令都有代价，所以要聪明高效。目标是在中完成任务"
        " 最少的步骤数."
    )

    # Generate the prompt string
    return prompt_generator.generate_prompt_string()


def construct_prompt() -> str:
    """Construct the prompt for the AI to respond to

    Returns:
        str: The prompt string
    """
    config = AIConfig.load(CFG.ai_settings_file)
    if CFG.skip_reprompt and config.ai_name:
        logger.typewriter_log("名字 :", Fore.GREEN, config.ai_name)
        logger.typewriter_log("角色 :", Fore.GREEN, config.ai_role)
        logger.typewriter_log("目标:", Fore.GREEN, f"{config.ai_goals}")
    elif config.ai_name:
        logger.typewriter_log(
            "欢迎回来! ",
            Fore.GREEN,
            f"你想让我变回到{config.ai_name}吗?",
            speak_text=True,
        )
        should_continue = clean_input(
            f"""继续上次设置?
名字:  {config.ai_name}
角色:  {config.ai_role}
任务目标: {config.ai_goals}
继续 (y/n): """
        )
        if should_continue.lower() == "n":
            config = AIConfig()

    if not config.ai_name:
        config = prompt_user()
        config.save()

    # Get rid of this global:
    global ai_name
    ai_name = config.ai_name

    return config.construct_full_prompt()
