#main.py
import streamlit as st
from inference_engine import load_rules, find_causes_with_chain, normalize

def start_app():
    exists_problems = True
    title = "========== Car Troubleshooting System =========="
    print(title.center(130))
    while exists_problems:
        rules = load_rules()
        symptoms = input("\nEnter the symptoms using comma: ").strip().split(",")
        print("\n--- What I found related to your car symptoms ---")
        for symptom in symptoms:
            symptom = normalize(symptom)
            causes = find_causes_with_chain(symptom, rules)
            print(f"\nSymptom: {symptom.strip()}")
            if causes:
                print("Possible causes and fixes for these problems: ")
                for cause in causes:
                    print("-", cause)
                print("After all this, your problem should resolve.")
            else:
                print("I cannot classify your symptom. Please check a service...")

        more_problems = input("\nAre there any other problems with your car? (press 'n' if you don't have): ").strip()
        if more_problems == "n":
            exists_problems = False

if __name__ == "__main__":
    start_app()