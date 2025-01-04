from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from ..models import PNTGModel
import json


class PNTG:
    @staticmethod
    @csrf_exempt
    def create(request):
        """创建新的 PNTG 记录"""
        if request.method != "POST":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        try:
            data = json.loads(request.body)
            pntg = PNTGModel.objects.create(
                project_id=data.get("project_id", 0),
                bot_token=data.get("bot_token", ""),
                chat_id=data.get("chat_id", ""),
                url=data.get("url", ""),
                state_codes=data.get("state_codes", ""),
            )
            return JsonResponse(
                {
                    "project_id": pntg.project_id,
                    "bot_token": pntg.bot_token,
                    "chat_id": pntg.chat_id,
                    "url": pntg.url,
                    "state_codes": pntg.state_codes,
                },
                status=201,
            )
        except Exception as e:
            import traceback

            print("Error creating PNTG:", str(e))
            print(traceback.format_exc())
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    def get(request, project_id):
        """获取 PNTG 记录"""
        try:
            pntg = PNTGModel.objects.get(project_id=project_id)
            return JsonResponse(
                {
                    "project_id": pntg.project_id,
                    "bot_token": pntg.bot_token,
                    "chat_id": pntg.chat_id,
                    "url": pntg.url,
                    "state_codes": pntg.state_codes,
                }
            )
        except PNTGModel.DoesNotExist:
            return JsonResponse({"error": "PNTG not found"}, status=404)

    @staticmethod
    @csrf_exempt
    def update(request, project_id):
        """更新 PNTG 记录"""
        if request.method != "POST":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        try:
            data = json.loads(request.body)
            pntg = PNTGModel.objects.get(project_id=project_id)
            pntg.bot_token = data.get("bot_token", pntg.bot_token)
            pntg.chat_id = data.get("chat_id", pntg.chat_id)
            pntg.url = data.get("url", pntg.url)
            pntg.state_codes = data.get("state_codes", pntg.state_codes)
            pntg.save()
            return JsonResponse(
                {
                    "project_id": pntg.project_id,
                    "bot_token": pntg.bot_token,
                    "chat_id": pntg.chat_id,
                    "url": pntg.url,
                    "state_codes": pntg.state_codes,
                }
            )
        except PNTGModel.DoesNotExist:
            return JsonResponse({"error": "PNTG not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    @csrf_exempt
    def delete(request, project_id):
        """删除 PNTG 记录"""
        if request.method != "DELETE":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        try:
            pntg = PNTGModel.objects.get(project_id=project_id)
            pntg.delete()
            return JsonResponse({"status": "success"})
        except PNTGModel.DoesNotExist:
            return JsonResponse({"error": "PNTG not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
