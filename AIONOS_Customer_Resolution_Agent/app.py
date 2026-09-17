import streamlit as st

from data import CUSTOMERS
from rule_engine import evaluate
from response_generator import generate_response

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AIONOS Customer Resolution Agent",
    page_icon="✈️",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = ""

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("✈️ AIONOS Customer Resolution Agent")

st.markdown("""
### Airline Disruption Support System

This agent helps resolve:

- Flight cancellations
- Flight delays
- Refund requests
- Rebooking requests
- Compensation eligibility
- Escalation scenarios

Built using only the customer data and airline policies provided in the assignment.
""")

# --------------------------------------------------
# CUSTOMER SELECTION
# --------------------------------------------------
customer_name = st.selectbox(
    "Select Customer",
    list(CUSTOMERS.keys())
)

# Clear query when customer changes
if st.session_state.selected_customer != customer_name:
    st.session_state.selected_customer = customer_name

    query_key = f"query_{customer_name}"

    if query_key not in st.session_state:
        st.session_state[query_key] = ""

customer = CUSTOMERS[customer_name]

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.header("Customer Profile")

    st.write(f"**Name:** {customer_name}")
    st.write(f"**Loyalty Tier:** {customer['tier']}")
    st.write(f"**PNR:** {customer['pnr']}")
    st.write(f"**Flight:** {customer['flight']}")
    st.write(f"**Status:** {customer['status']}")

    if "route" in customer:
        st.write(f"**Route:** {customer['route']}")

    if customer["status"] == "Delayed":
        st.write(f"**Delay:** {customer['delay']} Hours")

    if "fare_difference" in customer:
        st.write(
            f"**Fare Difference:** ₹{customer['fare_difference']}"
        )

# --------------------------------------------------
# QUERY INPUT
# --------------------------------------------------
query = st.text_area(
    "Customer Query",
    key=f"query_{customer_name}",
    height=150,
    placeholder="Example: I want a refund and a free business class upgrade."
)

# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------
if st.button(
    "Generate Resolution",
    type="primary"
):

    if not query.strip():

        st.warning(
            "Please enter a customer query."
        )

    else:

        decision = evaluate(
            customer,
            query
        )

        response = generate_response(
            customer_name,
            customer,
            decision
        )

        st.markdown("---")

        st.subheader("🤖 Agent Resolution")

        with st.container(border=True):
            st.markdown(response)

        st.markdown("---")

        st.subheader("📋 Rules Applied")

        if "rules_applied" in decision:

            for rule in decision["rules_applied"]:
                st.write(f"✅ {rule}")

        if decision["escalate"]:

            st.error(
                f"Escalation Required: {decision['escalation_reason']}"
            )

        else:

            st.success(
                "No escalation required."
            )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")

