import json
import jsonpath


def get_data(response, expressions):
# 提取数据
    results = {}
    for key, expr in expressions.items():
        results[key] = jsonpath.jsonpath(json.loads(response), expressions)

    return results

# print(results)