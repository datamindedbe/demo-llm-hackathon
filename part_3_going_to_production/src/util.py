from src.bedrock import BedrockRetrievedItem
from typing import List, Tuple

import re

def re_reference(response: str, decisions: List[BedrockRetrievedItem]) -> Tuple[str, List[BedrockRetrievedItem]]:
    used_decision_references = []
    for item in re.finditer("\[[0-9]*\]", response):
        ref = int(item.group(0).strip("[]"))
        if ref not in used_decision_references:
            used_decision_references.append(ref)

    # reduce the decisions to only those that are used
    used_decisions_correct_order  = []
    for ref in used_decision_references:
        used_decisions_correct_order.append(decisions[ref])

    # reorder the references by the order of occurence.. we do this in 2 
    # steps to avoid overwriting the same reference
    for new_ref, old_ref in enumerate(used_decision_references):
        response = response.replace(f"[{old_ref}]", f"[{new_ref}-tmp]")

    for new_ref, _ in enumerate(used_decision_references):
        response = response.replace(f"[{new_ref}-tmp]", f"[{new_ref}]")
    
    return response, used_decisions_correct_order