from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import PNTGModel
from ..utils.json_encoder import CustomJSONEncoder
import json
import logging

logger = logging.getLogger(__name__)


class PNTG:
    @staticmethod
    def list(request):
        """获取所有 PNTG 配置列表"""
        try:
            pntg_list = PNTGModel.objects.all()
            return JsonResponse(
                [
                    {
                        "tg_id": pntg.tg_id,
                        "tg_name": pntg.tg_name,
                    }
                    for pntg in pntg_list
                ],
                safe=False,
                encoder=CustomJSONEncoder,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    @csrf_exempt
    def create(request):
        """创建 PNTG 配置"""
        if request.method != "POST":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        try:
            data = json.loads(request.body)
            logger.info(f"Received data: {data}")

            # 验证必填字段
            required_fields = ["tg_name", "bot_token", "chat_id", "url"]
            for field in required_fields:
                if not data.get(field):
                    logger.error(f"Missing required field: {field}")
                    return JsonResponse(
                        {"error": f"Field {field} is required"}, status=400
                    )

            # 创建 PNTG 配置
            try:
                pntg = PNTGModel(
                    tg_name=data["tg_name"],
                    bot_token=data["bot_token"],
                    chat_id=data["chat_id"],
                    url=data["url"],
                )
                pntg.save()  # 保存后会生成 tg_id

                # 重新从数据库获取以确保有 tg_id
                pntg.refresh_from_db()

                return JsonResponse(
                    {
                        "tg_id": pntg.tg_id,
                        "tg_name": pntg.tg_name,
                        "bot_token": pntg.bot_token,
                        "chat_id": pntg.chat_id,
                        "url": pntg.url,
                    },
                    status=201,
                    encoder=CustomJSONEncoder,
                )

            except Exception as db_error:
                logger.error(f"Database error: {str(db_error)}")
                return JsonResponse(
                    {"error": f"Database error: {str(db_error)}"}, status=500
                )

        except json.JSONDecodeError as json_error:
            logger.error(f"JSON decode error: {str(json_error)}")
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            import traceback

            logger.error(traceback.format_exc())
            return JsonResponse(
                {"error": f"Failed to create PNTG configuration: {str(e)}"}, status=500
            )

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
