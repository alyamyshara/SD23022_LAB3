import streamlit as st
import json

st.set_page_config(page_title="Scholarship Rule-Based System", layout="centered")

st.title("Scholarship Eligibility Advisor (Rule-Based System)")
st.write("BSD3513 – Knowledge Representation System (Lab 3)")

# --------- GIVEN RULES (DO NOT CHANGE) ---------
rules = [
  {
    "name": "Top merit candidate",
    "priority": 100,
    "conditions": [
      ["cgpa", ">=", 3.7],
      ["co_curricular_score", ">=", 80],
      ["family_income", "<=", 8000],
      ["disciplinary_actions", "==", 0]
    ],
    "action": {
      "decision": "AWARD_FULL",
      "reason": "Excellent academic & co-curricular performance, with acceptable need"
    }
  },
  {
    "name": "Good candidate - partial scholarship",
    "priority": 80,
    "conditions": [
      ["cgpa", ">=", 3.3],
      ["co_curricular_score", ">=", 60],
      ["family_income", "<=", 12000],
      ["disciplinary_actions", "<=", 1]
    ],
    "action": {
      "decision": "AWARD_PARTIAL",
      "reason": "Good academic & involvement record with moderate need"
    }
  },
  {
    "name": "Need-based review",
    "priority": 70,
    "conditions": [
      ["cgpa", ">=", 2.5],
      ["family_income", "<=", 4000]
    ],
    "action": {
      "decision": "REVIEW",
      "reason": "High need but borderline academic score"
    }
  },
  {
    "name": "Low CGPA – not eligible",
    "priority": 95,
    "conditions": [
      ["cgpa", "<", 2.5]
    ],
    "action": {
      "decision": "REJECT",
      "reason": "CGPA below minimum scholarship requirement"
    }
  },
  {
    "name": "Serious disciplinary record",
    "priority": 90,
    "conditions": [
      ["disciplinary_actions", ">=", 2]
    ],
    "action": {
      "decision": "REJECT",
      "reason": "Too many disciplinary records"
    }
  }
]


# ---------- RULE EVALUATION FUNCTION ----------
def check_rule(rule, facts):
    for condition in rule["conditions"]:
        field, operator, value = condition
        user_value = facts[field]

        if operator == ">=" and not (user_value >= value):
            return False
        if operator == "<=" and not (user_value <= value):
            return False
        if operator == ">" and not (user_value > value):
            return False
        if operator == "<" and not (user_value < value):
            return False
        if operator == "==" and not (user_value == value):
            return False
    return True


# ---------- USER INPUT FORM ----------
st.subheader("Enter Applicant Details")

cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, step=0.01)
income = st.number_input("Monthly Family Income (RM)", min_value=0)
co_score = st.number_input("Co-curricular Score (0-100)", min_value=0, max_value=100)
discipline = st.number_input("Number of Disciplinary Actions", min_value=0)

facts = {
    "cgpa": cgpa,
    "family_income": income,
    "co_curricular_score": co_score,
    "disciplinary_actions": discipline
}

if st.button("Evaluate Scholarship Decision"):

    matched_rules = []

    for rule in rules:
        if check_rule(rule, facts):
            matched_rules.append(rule)

    if not matched_rules:
        st.error("No matching rule found. Applicant not eligible.")
    else:
        best_rule = sorted(matched_rules, key=lambda x: x["priority"], reverse=True)[0]

        st.success(f"Decision: {best_rule['action']['decision']}")
        st.write(f"Reason: {best_rule['action']['reason']}")
        st.caption(f"Rule Applied: {best_rule['name']}")
