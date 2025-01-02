from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import StateCodeModel
import json


class StateCode:
    @staticmethod
    @csrf_exempt
    def create(request):
        """创建新的 StateCode 记录"""
        if request.method != "POST":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        try:
            data = json.loads(request.body)
            state_code_value = data.get("state_code")

            # 检查 state_code 是否已存在
            if StateCodeModel.objects.filter(state_code=state_code_value).exists():
                return JsonResponse({"error": "State code already exists"}, status=400)

            state_code = StateCodeModel.objects.create(
                state_code=state_code_value,
                state_name=data.get("state_name", ""),
            )
            return JsonResponse(
                {
                    "state_code": state_code.state_code,
                    "state_name": state_code.state_name,
                },
                status=201,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    def get(request, state_code):
        """获取 StateCode 记录"""
        try:
            state_code = StateCodeModel.objects.get(state_code=state_code)
            return JsonResponse(
                {
                    "state_code": state_code.state_code,
                    "state_name": state_code.state_name,
                }
            )
        except StateCodeModel.DoesNotExist:
            return JsonResponse({"error": "StateCode not found"}, status=404)

    @staticmethod
    def list(request):
        """获取所有 StateCode 记录"""
        try:
            state_codes = StateCodeModel.objects.all()
            data = [
                {"state_code": sc.state_code, "state_name": sc.state_name}
                for sc in state_codes
            ]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    @csrf_exempt
    def update(request, state_code):
        """更新 StateCode 记录"""
        if request.method != "POST":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        try:
            data = json.loads(request.body)
            state_code_record = StateCodeModel.objects.get(state_code=state_code)
            state_code_record.state_name = data.get(
                "state_name", state_code_record.state_name
            )
            state_code_record.save()
            return JsonResponse(
                {
                    "state_code": state_code_record.state_code,
                    "state_name": state_code_record.state_name,
                }
            )
        except StateCodeModel.DoesNotExist:
            return JsonResponse({"error": "StateCode not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    @csrf_exempt
    def delete(request, state_code):
        """删除 StateCode 记录"""
        if request.method != "DELETE":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        try:
            state_code_record = StateCodeModel.objects.get(state_code=state_code)
            state_code_record.delete()
            return JsonResponse({"status": "success"})
        except StateCodeModel.DoesNotExist:
            return JsonResponse({"error": "StateCode not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
