def evaluate(customer, query):

    query = query.lower()

    result = {
        "eligible": [],
        "not_allowed": [],
        "rules_applied": [],
        "escalate": False,
        "escalation_reason": None
    }

    # ----------------------------------
    # Cancellation Rules
    # ----------------------------------

    if customer["status"] == "Cancelled":

        result["eligible"].append(
            "Free rebooking within 24 hours"
        )

        result["eligible"].append(
            "Full refund to original payment method"
        )

        result["rules_applied"].append(
            "Cancellation Rebooking Rule"
        )

        result["rules_applied"].append(
            "Refund Processing Rule"
        )

        if customer["tier"] in ["Gold", "Platinum"]:

            result["eligible"].append(
                "Priority rebooking"
            )

            result["rules_applied"].append(
                "Loyalty Tier Rule"
            )

    # ----------------------------------
    # Delay Rules
    # ----------------------------------

    elif customer["status"] == "Delayed":

        delay = customer["delay"]

        if delay > 3:

            result["eligible"].append(
                "Meal voucher"
            )

            result["eligible"].append(
                "Lounge access"
            )

            result["rules_applied"].append(
                "Delay Compensation Rule (>3 Hours)"
            )

        if delay > 5:

            result["eligible"].append(
                "Hotel accommodation for delayed hours only"
            )

            result["rules_applied"].append(
                "Delay Compensation Rule (>5 Hours)"
            )

    # ----------------------------------
    # Upgrade Request
    # ----------------------------------

    if (
        "upgrade" in query or
        "business class" in query or
        "business-class" in query
    ):

        result["not_allowed"].append(
            "Complimentary business-class upgrade"
        )

    # ----------------------------------
    # Hotel Request
    # ----------------------------------

    if (
        "hotel" in query and
        customer.get("delay", 0) <= 5
    ):

        result["not_allowed"].append(
            "Hotel accommodation"
        )

    # ----------------------------------
    # Legal Action / Complaint
    # ----------------------------------

    if (
        "legal" in query or
        "complaint" in query or
        "lawyer" in query or
        "sue" in query
    ):

        result["escalate"] = True

        result["escalation_reason"] = (
            "Formal complaint or legal action detected."
        )

    # ----------------------------------
    # Refund to Different Payment Method
    # ----------------------------------

    if (
        "different account" in query or
        "different payment method" in query or
        "another account" in query
    ):

        result["escalate"] = True

        result["escalation_reason"] = (
            "Refund requested to a different payment method."
        )

    # ----------------------------------
    # Fare Difference
    # ----------------------------------

    if customer.get("fare_difference", 0) > 1500:

        result["escalate"] = True

        result["escalation_reason"] = (
            "Fare difference exceeds ₹1500 and requires supervisor approval."
        )

    return result