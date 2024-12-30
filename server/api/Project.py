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
    def get(project_id):
        """
        获取项目信息
        :param project_id: 项目ID
        :return: Project对象或None
        """
        project_model = Project._get_project_model(project_id)
        return Project.create_from_db(project_model)

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
    def update(project_id, **kwargs):
        """
        更新项目信息
        :param project_id: 项目ID
        :param kwargs: 要更新的字段和值
        :return: 是否更新成功
        """
        project_model = Project._get_project_model(project_id)
        if project_model is None:
            return False

        field_mapping = {
            "project_name": "project_name",
            "description": "description",
            "state": "state",
            "node_id": "node_id",
        }

        try:
            for key, value in kwargs.items():
                if key in field_mapping:
                    setattr(project_model, field_mapping[key], value)
            project_model.save()
            return True
        except ObjectDoesNotExist:
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
    def list(request=None):
        """
        获取所有项目列表
        :param request: HTTP请求对象（可选）
        :return: 项目列表或JsonResponse
        """
        try:
            projects = ProjectModel.objects.all()
            project_list = []

            for project in projects:
                project_data = {
                    "project_id": project.project_id,
                    "project_name": project.project_name,
                    "description": project.description,
                    "state": project.state,
                    "node_id": project.node_id,
                }
                project_list.append(project_data)

            # 如果是HTTP请求，返回JsonResponse
            if request:
                return JsonResponse(project_list, safe=False)
            # 如果是直接调用，返回列表
            return project_list

        except Exception as e:
            if request:
                return JsonResponse({"error": str(e)}, status=500)
            raise e
