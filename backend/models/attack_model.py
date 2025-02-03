from database import db

attacks_collection = db["results"]

def store_attack_result(attack_type, target, output, error):
    """Stores a general attack result in MongoDB."""
    attacks_collection.insert_one({
        "attack_type": attack_type,
        "target": target,
        "output": output,
        "error": error
    })
    return True

def store_fortillm_result(data):
    """Stores attack results received from FortiLLM into MongoDB."""
    attacks_collection.insert_one({
        "framework": data["framework"],
        "separator": data["separator"],
        "disruptor": data["disruptor"],
        "fitness_score": data["fitness_score"],
        "response": data["response"],
        "is_successful": data["is_successful"]
    })
    return True

def get_attack_results():
    """Fetches all stored attack results from MongoDB."""
    return list(attacks_collection.find({}, {"_id": 0}))
