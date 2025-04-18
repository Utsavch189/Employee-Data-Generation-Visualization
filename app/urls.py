from django.urls import path
from app.views.analytics_views import (
    AverageSalaryView,
    AttendanceSummaryView,
    DepartmentWiseEmployeeCount,
    PerformanceStatsView,
    RecentSalariesView
)

from app.views.auth_view import LoginView

urlpatterns = [
    path('analytics/average-salary/', AverageSalaryView.as_view()),
    path('analytics/attendance-summary/', AttendanceSummaryView.as_view()),
    path('analytics/department-wise-salary/', DepartmentWiseEmployeeCount.as_view()),
    path('analytics/performance-stats/', PerformanceStatsView.as_view()),
    path('analytics/recent-salaries/', RecentSalariesView.as_view()),
    path('auth/login/', LoginView.as_view()),
]
