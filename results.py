import argparse
import json

model = None
def _parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "-m",
        "--model",
        help="Model to import",
        default=model,
    )
    p.add_argument(
        "--list-models",
        help="Show available models and exit",
        action="store_true",
    )
    p.add_argument(
        "--summary",
        help="Summary file to write",
        default="summary.json",
    )
    args = p.parse_args()
    if not args.model and not args.list_models:
        raise SystemExit("Specify either --model or --list-models")
    return args

data_csv = "data/oc_objective_overall.csv"
def _summary_data():
    data = dict()
    with open(data_csv) as f:
        f.readline() # csv header
        for line in f:
            fields = line.rstrip().split(",")
            modl = fields[0]
            fields.pop(0)
            data[modl] = fields
    return data

def _model_summary(args):
    summaries = _summary_data()
    name = args.model
    org,released,updated,typ,parameters,average,language,knowledge,reasoning,math,code,agent = summaries[name]
    return {
        "attributes": {
            "model": {
                "value": name,
            },
            "organization": {
                "value": org,
            },
            "released": {
                "value": released,
            },
            "updated": {
                "value": updated,
            },
            "type": {
                "value": typ,
            },
            "parameters": {
                "value": parameters,
            },
        },
        "metrics": {
            "average": {
                "value": average,
            },
            "language": {
                "value": language,
            },
            "knowledge": {
                "value": knowledge,
            },
            "reasoning": {
                "value": reasoning,
            },
            "math": {
                "value": math,
            },
            "code": {
                "value": code,
            },
            "agent": {
                "value": agent,
            },
            # "elo": {
                # "label": "ELO",
                # "value": elo,
            # },
            # "ci": {
                # "label": "95% CI",
                # "value": ci,
            # },
        },
        # "run": {
            # "label": name,
        # },
    }

def _write_summary(summary, args):
    with open(args.summary, "w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)

def _show_models_and_exit():
    summaries = _summary_data()
    for modl in sorted(summaries.keys()):
        print(modl)
    raise SystemExit(0)

if __name__ == "__main__":
    args = _parse_args()
    if args.list_models:
        _show_models_and_exit()
    summary = _model_summary(args)
    _write_summary(summary, args)
