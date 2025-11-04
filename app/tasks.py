from app import app
from app import calculator as calc
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.task(name='app.tasks.calculate')
def calculate(a, b, operation):
    try:
        result = calc.calculate(a, b, operation)
        redis_client.hincrby('operation_frequency', operation, 1)
        
        return {
            'success': True,
            'result': result,
            'operation': operation,
            'a': a,
            'b': b
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'operation': operation,
            'a': a,
            'b': b
        }


@app.task(name='app.tasks.get_operation_stats')
def get_operation_stats():
    try:
        stats = redis_client.hgetall('operation_frequency')
        stats = {k: int(v) for k, v in stats.items()} # type: ignore
        return {
            'success': True,
            'stats': stats,
            'total_operations': sum(stats.values())
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
