from fastapi import FastAPI, Depends
from model import *
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI()

base.metadata.create_all(bind=engine)

class ExpenseSchema(BaseModel):
    name : str = None
    amount : float = None
    category : str = None

@app.post("/expenses")
def expenseCreateAPI(expensesData:ExpenseSchema, db:Session=Depends(get_db)):
    newExpense = Expense(
        name = expensesData.name,
        amount = expensesData.amount,
        category = expensesData.category,
        create_at = datetime.now()
    )
    db.add(newExpense)
    db.commit()
    db.refresh(newExpense)
    newExpense.expense_id = newExpense.id
    return newExpense

@app.get("/expenses/get_all")
def expenses_get_all_api(expense_id:int=None, db:Session=Depends(get_db)):
    expensesRecords = db.query(Expense).filter(Expense.is_delete == False)
    if expense_id:
        expensesRecords = expensesRecords.filter(Expense.id == expense_id)
    
    results = expensesRecords.all()
    return results


@app.get("/expenses/month/{year_month}/")
def expenses_get_category_api(year_month:str, db:Session=Depends(get_db)):
    "example value --- year_month : 24-12-2024"
    expensesRecords = db.query(Expense).filter(Expense.is_delete == False)
    if year_month:
        # categoryDate = datetime.date(year_month)
        expensesRecords = expensesRecords.filter(func.DATE(Expense.create_at) == year_month)
    results = expensesRecords.all()
    return results

@app.get("/expenses/totals")
def expenses_get_total_amount_api(db:Session=Depends(get_db)):
    # if expenses_true is True:
    totalExpenses = db.query(func.sum(Expense.amount)).filter(Expense.is_delete == False, Expense.category == "expense").scalar()
    # else:
    salaryAmount = db.query(func.sum(Expense.amount)).filter(Expense.is_delete == False, Expense.category == "salary").scalar()
    # if salary_amount is True:
    remainAmount = salaryAmount - totalExpenses # db.query(func.sum(Expense.amount)).filter(Expense.is_delete == False, Expense.category == "remain").scalar()
    
    return {"totalExpenses":totalExpenses, "remainAmount":remainAmount, "salaryAmount":salaryAmount}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)


