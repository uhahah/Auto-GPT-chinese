"""This module contains the function to fix JSON strings using GPT-3."""
import json

from autogpt.llm_utils import call_ai_function
from autogpt.logs import logger
from autogpt.config import Config

CFG = Config()


def fix_json(json_string: str, schema: str) -> str:
    """Fix the given JSON string to make it parseable and fully compliant with
        the provided schema.

    Args:
        json_string (str): The JSON string to fix.
        schema (str): The schema to use to fix the JSON.
    Returns:
        str: The fixed JSON string.
    """
    # Try to fix the JSON using GPT:
    function_string = "def fix_json(json_string: str, schema:str=None) -> str:"
    args = [f"'''{json_string}'''", f"'''{schema}'''"]
    description_string = (
        "此函数接受一个JSON字符串，并确保是可解析的，并且完全符合所提供的模式。如果在模式中指定的对象或字段没有包含在正确的JSON中，则会忽略它。该函数还转义JSON"
        "字符串值中的任何双引号，以确保它们是有效的。如果JSON字符串包含任何None或NaN值，则在解析之前会将其替换为null。"

    )

    # If it doesn't already start with a "`", add one:
    if not json_string.startswith("`"):
        json_string = "```json\n" + json_string + "\n```"
    result_string = call_ai_function(
        function_string, args, description_string, model=CFG.fast_llm_model
    )
    logger.debug("------------ 尝试修复JSON ---------------")
    logger.debug(f"原始JSON JSON: {json_string}")
    logger.debug("-----------")
    logger.debug(f"修复后 JSON: {result_string}")
    logger.debug("----------- JSON修复结束 ----------------")

    try:
        json.loads(result_string)  # just check the validity
        return result_string
    except json.JSONDecodeError:  # noqa: E722
        # Get the call stack:
        # import traceback
        # call_stack = traceback.format_exc()
        # print(f"Failed to fix JSON: '{json_string}' "+call_stack)
        return "failed"
