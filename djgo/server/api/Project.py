from ..models import ProjectModel
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging


class Project:
    def __init__(self, project_id, project_name="", description="", state=0, node_id=0):
        self.project_id = project_id
        self.project_name = project_name
        self.description = description
        self.state = state
        self.node_id = node_id

    @staticmethod
    def _get_project_model(project_id):
        """
        获取项目模型的辅助方法
        :param project_id: 项目ID
        :return: ProjectModel实例或None
        """
        try:
            project = ProjectModel.objects.get(project_id=project_id)
            return project
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get(request=None, project_id=None):
        """
        获取项目信息
        :param request: HTTP请求对象（可选）
        :param project_id: 项目ID
        :return: JsonResponse 或 Project对象
        """
        try:
            # 如果是通过 URL 参数传入的 project_id
            if project_id is None and request is not None:
                project_id = request.resolver_match.kwargs.get("project_id")

            project = ProjectModel.objects.get(project_id=project_id)

            if request:
                return JsonResponse(
                    {
                        "project_id": project.project_id,
                        "project_name": project.project_name,
                        "description": project.description,
                        "state": project.state,
                        "node_id": project.node_id,
                    }
                )
            return Project(
                project_id=project.project_id,
                project_name=project.project_name,
                description=project.description,
                state=project.state,
                node_id=project.node_id,
            )

        except ProjectModel.DoesNotExist:
            if request:
                return JsonResponse({"error": "Project not found"}, status=404)
            return None
        except Exception as e:
            if request:
                return JsonResponse({"error": str(e)}, status=500)
            raise e

    @staticmethod
    def create(request=None, **kwargs):
        """
        创建项目
        :param request: HTTP请求对象（可选）
        :param kwargs: 项目参数（直接调用时使用）
        :return: Project对象或JsonResponse
        """
        try:
            with transaction.atomic():
                project_id = ProjectModel.get_next_id() or 1

                # 如果是HTTP请求
                if request is not None:
                    if request.method != "POST":
                        return JsonResponse({"error": "Method not allowed"}, status=405)
                    try:
                        data = json.loads(request.body)
                    except json.JSONDecodeError:
                        return JsonResponse({"error": "Invalid JSON"}, status=400)
                else:
                    # 如果是直接调用
                    data = kwargs

                project_model = ProjectModel(
                    project_id=project_id,
                    project_name=data.get("project_name"),
                    description=data.get("description"),
                    state=data.get("state", 0),
                    node_id=data.get("node_id"),
                )
                project_model.save()
                project_model.project_id = project_id
                project = Project.create_from_db(project_model)

                # 如果是HTTP请求，返回JsonResponse
                if request is not None:
                    return JsonResponse(
                        {
                            "project_id": project.project_id,
                            "project_name": project.project_name,
                            "description": project.description,
                            "state": project.state,
                            "node_id": project.node_id,
                        }
                    )
                # 如果是直接调用，返回Project对象
                return project

        except Exception as e:
            if request is not None:
                return JsonResponse({"error": str(e)}, status=500)
            raise e

    @staticmethod
    def update(request=None, project_id=None, **kwargs):
        """
        更新项目信息
        :param request: HTTP请求对象（可选）
        :param project_id: 项目ID
        :param kwargs: 要更新的字段和值
        :return: JsonResponse 或 bool
        """
        try:
            # 如果是通过 URL 参数传入的 project_id
            if project_id is None and request is not None:
                project_id = request.resolver_match.kwargs.get("project_id")

            project_model = Project._get_project_model(project_id)
            if project_model is None:
                if request:
                    return JsonResponse({"error": "Project not found"}, status=404)
                return False

            # 如果是 HTTP 请求，从请求体获取数据
            if request and request.method == "POST":
                try:
                    data = json.loads(request.body)
                    kwargs.update(data)
                except json.JSONDecodeError:
                    return JsonResponse({"error": "Invalid JSON"}, status=400)

            field_mapping = {
                "project_name": "project_name",
                "description": "description",
                "state": "state",
                "node_id": "node_id",
            }

            # 更新字段
            for key, value in kwargs.items():
                if key in field_mapping:
                    setattr(project_model, field_mapping[key], value)

            project_model.save()

            if request:
                return JsonResponse({"status": "success"})
            return True

        except Exception as e:
            if request:
                return JsonResponse({"error": str(e)}, status=500)
            return False

    @staticmethod
    def delete(request=None, project_id=None):
        """
        删除项目
        :param request: HTTP请求对象（可选）
        :param project_id: 项目ID
        :return: JsonResponse 或 bool
        """
        try:
            with transaction.atomic():
                # 如果是通过 URL 参数传入的 project_id
                if project_id is None and request is not None:
                    project_id = request.resolver_match.kwargs.get("project_id")

                # 尝试获取项目
                project_model = Project._get_project_model(project_id)
                if not project_model:
                    if request:
                        return JsonResponse(
                            {"status": "error", "message": "Project not found"},
                            status=404,
                        )
                    return False

                # 执行删除操作
                project_model.delete()

                # 根据调用方式返回不同结果
                if request:
                    return JsonResponse(
                        {"status": "success", "message": "Project deleted successfully"}
                    )
                return True

        except Exception as e:
            logging.error(f"Error deleting project {project_id}: {str(e)}")
            if request:
                return JsonResponse(
                    {"status": "error", "message": "Failed to delete project"},
                    status=500,
                )
            return False

    @staticmethod
    def create_from_db(project_model):
        """
        从数据库模型创建Project对象
        :param project_model: ProjectModel实例
        :return: Project对象
        """
        if not project_model:
            return None
        return Project(
            project_id=project_model.project_id,
            project_name=project_model.project_name,
            description=project_model.description,
            state=project_model.state,
            node_id=project_model.node_id,
        )

    @staticmethod
    def list(request):
        """获取项目列表"""
        try:
            # 获取请求中的 project_ids 参数
            project_ids_str = request.GET.get("project_ids", "")

            # 如果提供了 project_ids，转换为整数列表
            if project_ids_str:
                try:
                    project_ids = json.loads(project_ids_str)
                    # 确保 project_ids 是列表
                    if isinstance(project_ids, (int, str)):
                        project_ids = [int(project_ids)]
                    elif isinstance(project_ids, list):
                        project_ids = [int(pid) for pid in project_ids]
                    else:
                        project_ids = []
                except (json.JSONDecodeError, ValueError) as e:
                    project_ids = []

                projects = ProjectModel.objects.filter(project_id__in=project_ids)
            else:
                projects = ProjectModel.objects.none()

            # 将查询结果转换为列表
            project_list = []
            for project in projects:
                project_list.append(
                    {
                        "project_id": project.project_id,
                        "project_name": project.project_name,
                        "description": project.description,
                        "state": project.state,
                        "node_id": project.node_id,
                    }
                )

            return JsonResponse({"data": project_list})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
