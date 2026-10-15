from datetime import datetime
from streamstats.parsers import parser_timestamp

levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def make_stats():
    return {
        "total": 0,
        "by_level": {level: 0 for level in levels},
        "by_source": {},
        "top_error_sources": {},
        "first_timestamp": None,
        "last_timestamp": None,
    }
    
def analyzer(stats, event):
    stats["total"] += 1
    
    source = event["source"]
    stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
    
    level = event["level"]
    stats["by_level"][level] += 1
    
    err = stats["top_error_sources"]
    if level in ["CRITICAL", "ERROR"]:
        err[source] = err.get(source, {})
        err[source]["error"] = err[source].get("error", 0) + 1
    
    if source in err:
        err[source]["total"] = stats["by_source"][source]
        
    timestamp = event["timestamp"]
    if stats["first_timestamp"] == None or parser_timestamp(timestamp) < parser_timestamp(stats["first_timestamp"]):
        stats["first_timestamp"] = timestamp
    if stats["last_timestamp"] == None or parser_timestamp(timestamp) > parser_timestamp(stats["last_timestamp"]):
        stats["last_timestamp"] = timestamp
    
def top_error(err):
    top_k = 5
    srt = sorted(err.items())[::-1]
    return dict(srt[:top_k])
    

def final_result(stats):
    return {
        "total": stats["total"],
        "by_level": stats["by_level"],
        "by_source": stats["by_source"],
        "top_error_sources": top_error(stats["top_error_sources"]),
        "first_timestamp": stats["first_timestamp"],
        "last_timestamp": stats["last_timestamp"],
    }
