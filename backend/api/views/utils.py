"""
Views for handling API requests in the finance tracker application.
"""

import csv
import openpyxl # type: ignore
from rest_framework import status, generics
from rest_framework.response import Response

from ..utils import create_report_data, generate_transfers
from ..models import User, Expense, Income


class GenerateCSVReportView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            csv_titles, csv_rows = create_report_data(request)

            with open(
                f"../reports/{request.user.chat_id}-report.csv", "w", newline=""
            ) as file:
                writer = csv.writer(file)
                writer.writerow(csv_titles)
                writer.writerows(csv_rows)

            return Response(
                data={"message": f"{request.user.chat_id}-report.csv"},
                status=status.HTTP_201_CREATED,
            )

        except User.DoesNotExist:
            return Response(
                data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return Response(
                data={"message": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST
            )


class GenerateExcelReportView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):

        try:
            excel_titles, excel_rows = create_report_data(request)

            # with open(f"../reports/{user.chat_id}-report.excel", "w+", newline="") as file:
            excel_file = openpyxl.Workbook()
            excel_file_list = excel_file.active

            excel_file_list.column_dimensions["A"].width = 20  # Дата
            excel_file_list.column_dimensions["B"].width = 10  # Тип (Expense | Income)
            excel_file_list.column_dimensions["C"].width = 7  # Сума
            excel_file_list.column_dimensions["D"].width = 30  # Опис
            excel_file_list.column_dimensions["E"].width = 20  # Категорія

            excel_file_list.append(excel_titles)

            for row in excel_rows:
                excel_file_list.append(row)

            excel_file.save(f"../reports/{request.user.chat_id}-report.xlsx")

            return Response(
                data={"message": f"{request.user.chat_id}-report.excel"},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return Response(
                data={"message": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST
            )


class WeeklyExpensesView(generics.RetrieveAPIView):
    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        return generate_transfers(request, Expense, 7, args, kwargs)


class MonthlyExpensesView(generics.RetrieveAPIView):
    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        return generate_transfers(request, Expense, 30, args, kwargs)


class WeeklyIncomesView(generics.RetrieveAPIView):
    queryset = Income.objects.all()

    def get(self, request, *args, **kwargs):
        return generate_transfers(request, Income, 7, args, kwargs)


class MonthlyIncomesView(generics.RetrieveAPIView):
    queryset = Income.objects.all()

    def get(self, request, *args, **kwargs):
        return generate_transfers(request, Income, 30, args, kwargs)
