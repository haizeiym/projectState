from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

User = get_user_model()


@api_view(["GET", "POST"])
def user_projects(request, user_id):
    """
    GET: 获取用户的项目列表
    POST: 更新用户的项目列表
    """
    try:
        user = User.objects.get(user_id=user_id)

        if request.method == "GET":
            return Response(
                {"project_ids": user.get_project_ids(), "username": user.username}
            )

        elif request.method == "POST":
            project_ids = request.data.get("project_ids", "")
            # 确保 project_ids 是字符串
            if isinstance(project_ids, list):
                project_ids = ",".join(map(str, project_ids))
            user.project_ids = project_ids
            user.save()

            return Response(
                {"message": "项目列表更新成功", "project_ids": user.get_project_ids()}
            )

    except User.DoesNotExist:
        return Response({"error": "用户不存在"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
