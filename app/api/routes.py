from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.engines.deterministic import run_deterministic
from app.engines.monte_carlo import run_monte_carlo
from app.models.inputs import DeterministicInput, MonteCarloInput
from app.models.outputs import DeterministicOutput, MonteCarloOutput

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@router.post("/api/v1/stress/deterministic", response_model=DeterministicOutput)
async def deterministic_endpoint(inputs: DeterministicInput) -> DeterministicOutput:
    return run_deterministic(inputs)


@router.post("/api/v1/stress/monte-carlo", response_model=MonteCarloOutput)
async def monte_carlo_endpoint(inputs: MonteCarloInput) -> MonteCarloOutput:
    return run_monte_carlo(inputs)


@router.post("/ui/results", response_class=HTMLResponse)
async def ui_results(
    request: Request,
    household_monthly_net_income_gbp: float = Form(...),
    household_monthly_essential_spend_gbp: float = Form(...),
    household_monthly_debt_payments_gbp: float = Form(...),
    cash_savings_gbp: float = Form(...),
    mortgage_balance_gbp: float = Form(...),
    mortgage_term_years_remaining: float = Form(...),
    mortgage_rate_percent_current: float = Form(...),
    mortgage_rate_percent_stress: float = Form(...),
    mortgage_type: str = Form(...),
    shock_monthly_income_drop_percent: float = Form(...),
    inflation_monthly_essentials_increase_percent: float = Form(...),
):
    det_input = DeterministicInput(
        household_monthly_net_income_gbp=household_monthly_net_income_gbp,
        household_monthly_essential_spend_gbp=household_monthly_essential_spend_gbp,
        household_monthly_debt_payments_gbp=household_monthly_debt_payments_gbp,
        cash_savings_gbp=cash_savings_gbp,
        mortgage_balance_gbp=mortgage_balance_gbp,
        mortgage_term_years_remaining=mortgage_term_years_remaining,
        mortgage_rate_percent_current=mortgage_rate_percent_current,
        mortgage_rate_percent_stress=mortgage_rate_percent_stress,
        mortgage_type=mortgage_type,
        shock_monthly_income_drop_percent=shock_monthly_income_drop_percent,
        inflation_monthly_essentials_increase_percent=inflation_monthly_essentials_increase_percent,
    )
    mc_input = MonteCarloInput(**det_input.model_dump(), num_trials=10_000)

    det_result = run_deterministic(det_input)
    mc_result = run_monte_carlo(mc_input)

    return templates.TemplateResponse(
        request,
        "results.html",
        {
            "det": det_result,
            "mc": mc_result,
            "inputs": det_input,
        },
    )
