from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


def worker_login_required(view_func):
    worker_login_required = user_passes_test(lambda u: u.is_active and (u.user_type == 1),
                                          login_url='/login')
    decorated_view_func = login_required(worker_login_required(view_func), login_url='/login')
    return decorated_view_func


def patient_login_required(view_func):
    pat_login_required = user_passes_test(lambda u: u.is_active and (u.user_type == 2),
                                          login_url='/login')
    decorated_view_func = login_required(pat_login_required(view_func), login_url='/login')
    return decorated_view_func