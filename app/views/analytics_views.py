from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Salary, Attendance, Performance
from django.db.models import Avg, Count
from app.serializers import SalarySerializer,PerformanceSerializer

class AverageSalaryView(APIView):
    def get(self, request):
        avg_salary = Salary.objects.aggregate(avg=Avg('net_salary'))
        return Response({
            "average_net_salary": round(avg_salary['avg'], 2)
        })

class AttendanceSummaryView(APIView):
    def get(self, request):
        summary = Attendance.objects.values('status').annotate(count=Count('id'))
        return Response({
            "attendance_summary": summary
        })

class DepartmentWiseEmployeeCount(APIView):
    def get(self, request):
        salaries = Salary.objects.select_related('employee').order_by('employee__department')
        serialized = SalarySerializer(salaries, many=True)
        return Response({
            "department_salary_details": serialized.data
        })

class PerformanceStatsView(APIView):
    def get(self, request):
        stats = Performance.objects.aggregate(
            avg_rating=Avg('rating'),
            total_reviews=Count('id')
        )
        top_performers = Performance.objects.select_related('employee').order_by('-rating')[:5]
        serialized = PerformanceSerializer(top_performers, many=True)

        return Response({
            "stats": stats,
            "top_performers": serialized.data
        })

class RecentSalariesView(APIView):
    def get(self, request):
        salaries = Salary.objects.select_related('employee').order_by('-payment_date')[:10]
        serialized = SalarySerializer(salaries, many=True)
        return Response({
            "recent_salaries": serialized.data
        })

