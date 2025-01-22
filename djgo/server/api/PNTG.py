from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import PNTGModel
import json


class PNTG:
    @staticmethod
    @csrf_exempt
    def create(request):
        """创建 PNTG 配置"""
        try:
            if request.method != "POST":
                return JsonResponse({"error": "Method not allowed"}, status=405)

            data = json.loads(request.body)
            pntg = PNTGModel.objects.create(
                tg_name=data.get("tg_name", ""),
                bot_token=data.get("bot_token", ""),
                chat_id=data.get("chat_id", ""),
                url=data.get("url", ""),
            )

            return JsonResponse(
                {
                    "tg_id": pntg.tg_id,
                    "tg_name": pntg.tg_name,
                    "bot_token": pntg.bot_token,
                    "chat_id": pntg.chat_id,
                    "url": pntg.url,
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    def get(request, tg_id):
        """获取 PNTG 配置"""
        try:
            pntg = PNTGModel.objects.get(tg_id=tg_id)
            return JsonResponse(
                {
                    "tg_id": pntg.tg_id,
                    "tg_name": pntg.tg_name,
                    "bot_token": pntg.bot_token,
                    "chat_id": pntg.chat_id,
                    "url": pntg.url,
                }
            )
        except PNTGModel.DoesNotExist:
            return JsonResponse({"error": "PNTG configuration not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    @csrf_exempt
    def update(request, tg_id):
        """更新 PNTG 配置"""
        try:
            if request.method != "POST":
                return JsonResponse({"error": "Method not allowed"}, status=405)

            pntg = PNTGModel.objects.get(tg_id=tg_id)
            data = json.loads(request.body)

            pntg.tg_name = data.get("tg_name", pntg.tg_name)
            pntg.bot_token = data.get("bot_token", pntg.bot_token)
            pntg.chat_id = data.get("chat_id", pntg.chat_id)
            pntg.url = data.get("url", pntg.url)
            pntg.save()

            return JsonResponse(
                {
                    "tg_id": pntg.tg_id,
                    "tg_name": pntg.tg_name,
                    "bot_token": pntg.bot_token,
                    "chat_id": pntg.chat_id,
                    "url": pntg.url,
                }
            )

        except PNTGModel.DoesNotExist:
            return JsonResponse({"error": "PNTG configuration not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    @csrf_exempt
    def delete(request, tg_id):
        """删除 PNTG 配置"""
        try:
            pntg = PNTGModel.objects.get(tg_id=tg_id)
            pntg.delete()
            return JsonResponse({"message": "PNTG configuration deleted successfully"})
        except PNTGModel.DoesNotExist:
            return JsonResponse({"error": "PNTG configuration not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
