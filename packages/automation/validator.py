def should_fail_to_manual_review(parser_confidence: float, automation_confidence: float, required_long_form: bool) -> bool:
    return parser_confidence < 0.8 or automation_confidence < 0.8 or required_long_form

