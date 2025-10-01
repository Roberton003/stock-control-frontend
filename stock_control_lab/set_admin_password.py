from django.contrib.auth import get_user_model

User = get_user_model()
try:
    user = User.objects.get(username='admin')
    user.set_password('admin12345')
    user.save()
    print("Password for user 'admin' has been changed successfully.")
except User.DoesNotExist:
    print("User 'admin' does not exist.")
