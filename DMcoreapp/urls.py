from django.urls import re_path,path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.login, name='login'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('registration_form', views.registration_form, name='registration_form'),

    path('reset_password', views.reset_password, name='reset_password'),
    path('internshipform', views.internshipform, name='internshipform'),
    path('internship_save', views.internship_save, name='internship_save'),
    #---------------------------------------------------------------------------Admin Section
    path('ad_base', views.ad_base, name='ad_base'),
    path('ad_profile', views.ad_profile, name='ad_profile'),
    path('ad_dashboard', views.ad_dashboard, name='ad_dashboard'),
    path('ad_create_work', views.ad_create_work, name='ad_create_work'),
    path('save_create_work', views.save_create_work, name='save_create_work'),
    path('ad_view_work', views.ad_view_work, name='ad_view_work'),
    path('ad_view_clint/<int:id>', views.ad_view_clint, name='ad_view_clint'), 
    path('update_client/<int:id>', views.update_client, name='update_client'),
    path('ad_daily_work_det', views.ad_daily_work_det, name='ad_daily_work_det'),
    path('ad_work_analiz_det', views.ad_work_analiz_det, name='ad_work_analiz_det'),
    path('ad_work_progress', views.ad_work_progress, name='ad_work_progress'),
    path('ad_work_progress_det/<int:id>', views.ad_work_progress_det, name='ad_work_progress_det'),
    path('ad_warning_ex', views.ad_warning_ex, name='ad_warning_ex'),
    path('ad_warning_sugg_dash', views.ad_warning_sugg_dash, name='ad_warning_sugg_dash'),
    path('ad_warning_det', views.ad_warning_det, name='ad_warning_det'),
    path('ad_suggestions_det', views.ad_suggestions_det, name='ad_suggestions_det'),    #---------------------------------------------------------------------------Executive Section
    path('ex_base', views.ex_base, name='ex_base'),
    path('ex_profile', views.ex_profile, name='ex_profile'),
    path('ex_dashboard', views.ex_dashboard, name='ex_dashboard'), 
    path('ex_daily_work_clint', views.ex_daily_work_clint, name='ex_daily_work_clint'), 
    path('ex_daily_work_det/<int:id>', views.ex_daily_work_det, name='ex_daily_work_det'),
    path('daily_work_done/<int:id>', views.daily_work_done, name='daily_work_done'),
    path('ex_weekly_rep_clint', views.ex_weekly_rep_clint, name='ex_weekly_rep_clint'),
    path('ex_weekly_rep_clint_det/<int:id>', views.ex_weekly_rep_clint_det, name='ex_weekly_rep_clint_det'),
    path('sv_wk_rp/<int:id>', views.sv_wk_rp, name='sv_wk_rp'),
    path('ex_view_work_clint', views.ex_view_work_clint, name='ex_view_work_clint'),
    path('ex_view_clint_det/<int:id>', views.ex_view_clint_det, name='ex_view_clint_det'),  
    path('ex_warning', views.ex_warning, name='ex_warning'),
    path('add_warning/<int:id>', views.add_warning, name='add_warning'),
    path('add_suggestion/<int:id>', views.add_suggestion, name='add_suggestion'),

    
    path('ex_warnings_dash', views.ex_warnings_dash, name='ex_warnings_dash'),
    path('ex_suggestions', views.ex_suggestions, name='ex_suggestions'),
    
]