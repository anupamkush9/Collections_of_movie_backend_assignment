from django.contrib import admin
from django.contrib.auth.models import Permission, User
from django.db import transaction
from .models import UserPermissionCredit
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class UserPermissionCreditAdmin(admin.ModelAdmin):
    fields = ['user', 'permission', 'credits']
    list_display = ['user', 'permission', 'credits']

    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                # First, save the UserPermissionCredit object
                super().save_model(request, obj, form, change)
                
                # Retrieve permission and user details
                permission_name = obj.permission
                user = obj.user
        
                # Get all models in the project
                all_models = apps.get_models()
                all_models_name = [model_name.__name__.lower() for model_name in all_models]
                # Print the names of all models
                for model in all_models:
                    print(model.__name__)
                        
                if permission_name in all_models_name:
                    # Assign the add and view permissions to the user
                    for each_permission in ["add", "view"]:
                        model_permission_code_name = f"{each_permission}_{permission_name}"
                        model_permission = Permission.objects.get(codename__iexact=model_permission_code_name)
                        user.user_permissions.add(model_permission)
                        # Ref : https://testdriven.io/blog/django-permissions/ 
                        # Ref : https://testdriven.io/blog/django-permissions/ 
                else:  
                    # changes for post title wise permission
                    from blog.models import Post
                    post_titles = Post.objects.all().values_list('title', flat=True)
                    post_titles = [(post_title,post_title.replace("_"," ")) for post_title in post_titles]

                    # Create or extend permissions with these titles
                    content_type = ContentType.objects.get_for_model(Post)

                    for original_title, modified_title in post_titles:
                        permission, created = Permission.objects.get_or_create(
                            codename=f'can_view_{original_title.lower()}',
                            name=f'Can view {modified_title}',
                            content_type=content_type,
                        )
                    code_name = f"can_view_{permission_name}"
                    model_permission = Permission.objects.get(codename__iexact=code_name)
                    user.user_permissions.add(model_permission)
        except Permission.DoesNotExist:
            print(f"Permission does not exist.")
        except Exception as e:
            print("Exception in UserPermissionCreditAdmin", e)
            import traceback
            print(traceback.format_exc())

    def delete_model(self, request, obj):
        try:
            with transaction.atomic():
                user = obj.user
                permission_name = obj.permission
                # Get all models in the project
                all_models = apps.get_models()
                all_models_name = [model_name.__name__.lower() for model_name in all_models]
                # Print the names of all models
                for model in all_models:
                    print(model.__name__)
                        
                if permission_name in all_models_name:
                    # Remove the permissions associated with the UserPermissionCredit instance
                    for each_permission in ["add", "view"]:
                        model_permission_code_name = f"{each_permission}_{permission_name}"
                        model_permission = Permission.objects.get(codename__iexact=model_permission_code_name)
                        user.user_permissions.remove(model_permission)
                        # Ref : https://testdriven.io/blog/django-permissions/ 
                        # Ref : https://testdriven.io/blog/django-permissions/ 
                else:
                    code_name = f"can_view_{permission_name}"
                    model_permission = Permission.objects.get(codename__iexact=code_name)
                    user.user_permissions.remove(model_permission)
                # Now delete the UserPermissionCredit object
                obj.delete()
        except Permission.DoesNotExist:
            print(f"Permission {model_permission_code_name} does not exist.")
        except Exception as e:
            print("Exception is", e)
            import traceback
            print(traceback.format_exc())
            

# Register the admin class
admin.site.register(UserPermissionCredit, UserPermissionCreditAdmin)