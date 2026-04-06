import json
import sys
from pathlib import Path


BASE = Path(__file__).parent
INPUTS = BASE / "inputs"
OUTPUTS = BASE / "outputs"


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    return json.loads(path.read_text())


def load_scenario(name: str) -> dict:
    faultline = load_json(INPUTS / "faultline" / f"{name}.json")
    dettrace = load_json(INPUTS / "dettrace" / f"{name}.json")
    kubepulse = load_json(INPUTS / "kubepulse" / f"{name}.json")

    decision = kubepulse.get("recommendation", "investigate").upper()
    confidence = dettrace.get("confidence", 0.0)

    combined = {
        "incident": name,
        "first_divergence": dettrace.get("first_divergence", "unknown"),
        "propagation": dettrace.get("propagation", "unknown"),
        "correctness": {
            "duplicate_commits": faultline.get("duplicate_commits", "unknown"),
            "stale_writes_blocked": faultline.get("stale_writes_blocked", False),
            "safe_for_production": faultline.get("safe_for_production", False),
        },
        "validation": {
            "probes_healthy": kubepulse.get("probes_healthy", False),
            "safe_to_operate": kubepulse.get("safe_to_operate", False),
            "availability": kubepulse.get("availability", "unknown"),
        },
        "decision": {
            "action": decision,
            "confidence": confidence,
            "faultline_recommendation": faultline.get("recommendation", "none"),
            "kubepulse_recommendation": kubepulse.get("recommendation", "none"),
        },
    }
    return combined


def render(s: dict) -> None:
    print("Sentinel Analysis")
    print("-----------------\n")
    print(f"Incident: {s['incident']}\n")

    print("First divergence:")
    print(s["first_divergence"])

    print("\nPropagation:")
    print(s["propagation"])

    print("\nCorrectness:")
    print(f"duplicate commits: {s['correctness']['duplicate_commits']}")
    print(
        "stale writes blocked: "
        + ("yes" if s["correctness"]["stale_writes_blocked"] else "no")
    )
    print(
        "safe for production: "
        + ("true" if s["correctness"]["safe_for_production"] else "false")
    )

    print("\nValidation:")
    print(f"probes healthy: {str(s['validation']['probes_healthy']).lower()}")
    print(f"safe to operate: {str(s['validation']['safe_to_operate']).lower()}")
    print(f"availability: {s['validation']['availability']}")

    print("\nDecision:")
    print(s["decision"]["action"])
    print(f"\nConfidence: {s['decision']['confidence']:.2f}")


def save_artifact(name: str, s: dict) -> None:
    OUTPUTS.mkdir(exist_ok=True)
    out = OUTPUTS / f"{name}_decision_report.json"
    out.write_text(json.dumps(s, indent=2))
    print(f"\nSaved artifact: {out}")


if __name__ == "__main__":
    scenario = sys.argv[1] if len(sys.argv) > 1 else "retry_storm"
    selected = load_scenario(scenario)
    render(selected)
    save_artifact(scenario, selected)