"""Setup the AI and its goals"""
from colorama import Fore, Style
from autogpt import utils
from autogpt.config.ai_config import AIConfig
from autogpt.logs import logger


def prompt_user() -> AIConfig:
    """Prompt the user for input

    Returns:
        AIConfig: The AIConfig object containing the user's input
    """
    ai_name = ""
    # Construct the prompt
    logger.typewriter_log(
        "欢迎来到Auto-GPT! ",
        Fore.GREEN,
        "在下方输入您的 AI 的名称及其角色。 什么都不输入会加载"
        " 默认.",
        speak_text=True,
    )

    # Get AI Name from User
    logger.typewriter_log(
        "你的AI名字: ", Fore.GREEN, "例如, '超级-GPT'"
    )
    ai_name = utils.clean_input("AI名字: ")
    if ai_name == "":
        ai_name = "超级-GPT"

    logger.typewriter_log(
        f"{ai_name} 在这里!", Fore.LIGHTBLUE_EX, "我将为您服务.", speak_text=True
    )

    # Get AI Role from User
    logger.typewriter_log(
        "描述下你的AI角色: ",
        Fore.GREEN,
        "例如，'公司查询人工智能。",
    )
    ai_role = utils.clean_input(f"{ai_name} is: ")
    if ai_role == "":
        ai_role = "公司查询人工智能"

    # Enter up to 5 goals for the AI
    logger.typewriter_log(
        "为您的 AI 输入最多 5 个目标： ",
        Fore.GREEN,
        "例如：\n查询市值最高的公司"
        " 查询市值第二的公司'",
    )
    print("不输入任何内容以加载默认值，完成后不输入任何内容。", flush=True)
    ai_goals = []
    for i in range(5):
        ai_goal = utils.clean_input(f"{Fore.LIGHTBLUE_EX}Goal{Style.RESET_ALL} {i+1}: ")
        if ai_goal == "":
            break
        ai_goals.append(ai_goal)
    if not ai_goals:
        ai_goals = [
            "查询市值最高的公司",
            "查询市值第二的公司",
        ]

    return AIConfig(ai_name, ai_role, ai_goals)
