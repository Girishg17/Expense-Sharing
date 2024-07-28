from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import ExpenseParticipant, User, Expense
from .serializers import UserSerializer, ExpenseSerializer
from django.db.models import Sum 
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class UserViewSet(viewsets.ModelViewSet): #inheriting from viewsets.ModelViewSet for CRUD operations
    queryset = User.objects.all()
    serializer_class = UserSerializer
            
    # Custom action to get total amount spent by user
    @action(detail=False, methods=['post'], url_path='total-amount-spent')
    def total_amount_spent(self, request, email=None):
        try:
            user = User.objects.get(email=request.data['email'])
            total_amount_spent = ExpenseParticipant.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
            return Response({'total_amount_spent': total_amount_spent})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Custom action to get total amount owed by user
    @action(detail=False, methods=['post'], url_path='owed-amounts')
    def get_owed_amounts(self, request, email=None):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
            owed_amounts = ExpenseParticipant.objects.filter(user=user).exclude(expense__created_by=user).values('expense__created_by__email').annotate(total_amount=Sum('amount'))
            return Response(owed_amounts)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
class ExpenseViewSet(viewsets.ModelViewSet): #inheriting from viewsets.ModelViewSet for CRUD operations
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    @action(detail=False, methods=['get'], url_path='overall-expenses')
    def get_overall_expenses(self, request):
        overall_expenses = Expense.objects.all()
        serializer = ExpenseSerializer(overall_expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='download-balance-sheet')
    def download_balance_sheet(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="balance_sheet.pdf"'

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle('Balance Sheet')

        width, height = letter

        pdf.drawString(100, height - 50, 'Balance Sheet')

        y = height - 80
        pdf.drawString(30, y, 'User')
        pdf.drawString(150, y, 'Owes Amount')
        pdf.drawString(270, y, 'Owed To')

        y -= 20

        users = User.objects.all()
        for user in users:
            owed_amounts = ExpenseParticipant.objects.filter(user=user).exclude(expense__created_by=user).values('expense__created_by__email').annotate(total_amount=Sum('amount'))
            for owed in owed_amounts:
                pdf.drawString(30, y, user.email)
                pdf.drawString(150, y, str(owed['total_amount']))
                pdf.drawString(270, y, owed['expense__created_by__email'])
                y -= 20

                if y < 50:
                    pdf.showPage()
                    y = height - 50

        pdf.save()
        buffer.seek(0)
        response.write(buffer.read())
        buffer.close()

        return response
