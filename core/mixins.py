from django.contrib import messages

class SuccessMessageMixin:

    success_message = None

    def form_valid(self, form):

        response = super().form_valid(form)

        if self.success_message:

            messages.success(
                self.request,
                self.success_message
            )

        return response
    

class UserCreateMixin:

    success_message = None

    def form_valid(self, form):

        form.instance.created_by = self.request.user

        response = super().form_valid(form)

        if self.success_message:

            messages.success(
                self.request,
                self.success_message
            )

        return response
    
class BaseListMixin:

    paginate_by = 4

    ordering = ("-id",)