def generate_response(
        customer_name,
        customer,
        decision):

    response = f"""
Hello {customer_name},

Thank you for contacting Airline Support.

Booking Reference (PNR): {customer['pnr']}
Flight: {customer['flight']}
Loyalty Tier: {customer['tier']}
Current Status: {customer['status']}

"""

    # Customer-specific introduction

    if customer["status"] == "Cancelled":

        response += (
            "I understand the inconvenience caused by the cancellation of your flight. "
            "After reviewing your booking and the applicable service policies, "
            "here are the available resolution options:\n"
        )

    elif customer["status"] == "Delayed":

        response += (
            "I understand the frustration caused by the flight disruption. "
            "After reviewing your booking details and applicable policies, "
            "you are eligible for the following support:\n"
        )

    # Eligible Actions

    if decision["eligible"]:

        response += "\nEligible Actions:\n"

        for item in decision["eligible"]:
            response += f"\n✓ {item}"

    # Not Allowed

    if decision["not_allowed"]:

        response += "\n\nRequests Outside Current Policy:\n"

        for item in decision["not_allowed"]:
            response += f"\n✗ {item}"

        response += (
            "\n\nThese requests cannot be approved because they are not covered "
            "under the current airline disruption policy."
        )

    # Escalation

    if decision["escalate"]:

        response += (
            "\n\n⚠ Escalation Required"
        )

        if decision.get("escalation_reason"):

            response += (
                f"\nReason: {decision['escalation_reason']}"
            )

        response += (
            "\nA human support specialist will need to review this request."
        )

    # Rules Applied

    if decision.get("rules_applied"):

        response += "\n\nPolicy Rules Applied:\n"

        for rule in decision["rules_applied"]:
            response += f"\n• {rule}"

    # Closing

    response += (
        "\n\nThank you for your patience and understanding."
    )

    return response