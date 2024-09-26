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
    user = request.user

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