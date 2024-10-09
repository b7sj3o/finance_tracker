from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db.models import Sum


def create_report_data(request):
    """
    Creates data for reports in this way:
    (
        [
            transfer created,
            transfer type (Income | Expense),
            transfer amount,
            transfer description | "-",
            transfer category | "-"
        ],
    )
    
    returns (transfer titles, transfer data)
    """
    
    expenses = request.user.expense_set.all().order_by("created")
    incomes = request.user.income_set.all().order_by("created")
    
    transfers = sorted(
        list(expenses) + list(incomes),
        key=lambda transfer: transfer.created
    )
    
    transfer_titles = ["Data", "Type", "Amount", "Description", "Category"]
    transfer_data = (
        [
            transfer.created.strftime("%d.%m.%Y, %H:%M:%S"),
            transfer.__class__.__name__,
            transfer.amount,
            transfer.description or "-",
            transfer.category or "-"
        ] for transfer in transfers
    )
    
    return (transfer_titles, transfer_data)


def generate_transfers(request, transfer_type, days: int, *args, **kwargs):
    transfers = transfer_type.objects.filter(user=request.user).order_by("created")

    if not transfers:
        return Response({"message": f"No {transfer_type.__name__.lower()}s found."}, status=status.HTTP_404_NOT_FOUND)
    
    start_of_week = transfers[0].created.date()
    end_of_week = start_of_week + timedelta(days=(days-1))

    time_transfers = []

    while start_of_week <= datetime.now().date():
        time_period = "{}-{}".format(
            start_of_week.strftime("%d.%m.%Y"),
            end_of_week.strftime("%d.%m.%Y")
        )
        
        filtered_transfers = transfers.filter(created__gte=start_of_week, created__lte=end_of_week)
        
        if filtered_transfers:
            total_amount = filtered_transfers.aggregate(total=Sum("amount"))["total"] or 0
            time_transfers.append({
                "period": time_period,
                "total_amount": total_amount,
                "days": count_transfers_by_day(transfers, days, start_of_week)
            })
            
        start_of_week = end_of_week + timedelta(days=1)
        end_of_week = start_of_week + timedelta(days=(days-1))
        
    return Response(time_transfers, status=status.HTTP_200_OK)

def count_transfers_by_day(transfers, days: int,  current_date):
    daily_transfers = []
    for _ in range(days):
        filtered_transfers = transfers.filter(created__date=current_date)

        if filtered_transfers:
            total_amount = filtered_transfers.aggregate(total=Sum("amount"))["total"] or 0
            daily_transfers.append({
                "date": current_date.strftime("%d.%m.%Y"),
                "total_amount": total_amount,
            })

        current_date += timedelta(days=1)
    
    return daily_transfers
