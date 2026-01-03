import time
from typing import Dict, List
from datetime import datetime

class PerformanceMetrics:
    """Track and display performance metrics"""
    
    def __init__(self):
        self.query_history = []
    
    def track_query(self, query: str, response_time: float, num_chunks: int, sources: List[Dict]) -> Dict:
        """Track a query and its metrics"""
        metric = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "query": query,
            "response_time": response_time,
            "num_chunks_retrieved": num_chunks,
            "num_sources": len(sources),
            "sources": sources
        }
        
        self.query_history.append(metric)
        return metric
    
    def get_average_response_time(self) -> float:
        """Calculate average response time"""
        if not self.query_history:
            return 0.0
        
        total_time = sum(q["response_time"] for q in self.query_history)
        return total_time / len(self.query_history)
    
    def get_total_queries(self) -> int:
        """Get total number of queries"""
        return len(self.query_history)
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics"""
        if not self.query_history:
            return {
                "total_queries": 0,
                "avg_response_time": 0.0,
                "fastest_query": 0.0,
                "slowest_query": 0.0,
                "total_chunks_retrieved": 0
            }
        
        response_times = [q["response_time"] for q in self.query_history]
        
        return {
            "total_queries": len(self.query_history),
            "avg_response_time": sum(response_times) / len(response_times),
            "fastest_query": min(response_times),
            "slowest_query": max(response_times),
            "total_chunks_retrieved": sum(q["num_chunks_retrieved"] for q in self.query_history)
        }
    
    def get_recent_queries(self, limit: int = 10) -> List[Dict]:
        """Get recent queries"""
        return self.query_history[-limit:]