import { MoneyInput } from "./MoneyInput";

type CurrencyCode = "GBP" | "EUR" | "USD";

type MortgageInputsProps = {
  balance: number;
  balanceCurrency: CurrencyCode;
  mortgageType: "repayment" | "interest_only";
  termYearsRemaining: number;
  currentRatePercent: number;
  stressRatePercent: number;
  onBalanceChange: (value: number) => void;
  onBalanceCurrencyChange: (value: CurrencyCode) => void;
  onMortgageTypeChange: (value: "repayment" | "interest_only") => void;
  onTermYearsRemainingChange: (value: number) => void;
  onCurrentRatePercentChange: (value: number) => void;
  onStressRatePercentChange: (value: number) => void;
  currencies?: readonly CurrencyCode[];
  ariaDescribedBy?: string;
};

function parseNumberish(value: string): number | null {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

export function MortgageInputs({
  balance,
  balanceCurrency,
  mortgageType,
  termYearsRemaining,
  currentRatePercent,
  stressRatePercent,
  onBalanceChange,
  onBalanceCurrencyChange,
  onMortgageTypeChange,
  onTermYearsRemainingChange,
  onCurrentRatePercentChange,
  onStressRatePercentChange,
  currencies,
  ariaDescribedBy
}: MortgageInputsProps) {
  const termError = balance > 0 && termYearsRemaining <= 0 ? "Term is required when mortgage balance is above zero." : null;
  const currentRateError = currentRatePercent < 0 ? "Current mortgage rate must be 0% or higher." : null;
  const stressRateError = stressRatePercent < 0 ? "Stressed mortgage rate must be 0% or higher." : null;

  return (
    <div className="mortgage-inputs">
      <MoneyInput
        idPrefix="mortgage-balance"
        label="Mortgage balance"
        amount={balance}
        currency={balanceCurrency}
        onAmountChange={onBalanceChange}
        onCurrencyChange={onBalanceCurrencyChange}
        currencies={currencies}
        ariaDescribedBy={ariaDescribedBy}
      />

      <label htmlFor="mortgage-type">
        Mortgage type
        <select
          id="mortgage-type"
          aria-label="Mortgage type"
          aria-describedby={ariaDescribedBy}
          value={mortgageType}
          onChange={(event) => onMortgageTypeChange(event.target.value as "repayment" | "interest_only")}
        >
          <option value="repayment">Repayment</option>
          <option value="interest_only">Interest-only</option>
        </select>
      </label>

      <label htmlFor="mortgage-term-years">
        Mortgage term remaining (years)
        <input
          id="mortgage-term-years"
          aria-label="Mortgage term remaining (years)"
          aria-describedby={ariaDescribedBy}
          type="number"
          min="0"
          step="1"
          value={termYearsRemaining}
          onChange={(event) => {
            const next = parseNumberish(event.target.value);
            if (next !== null) {
              onTermYearsRemainingChange(next);
            }
          }}
        />
      </label>
      {termError ? <p className="field-error">{termError}</p> : null}

      <label htmlFor="mortgage-rate-current">
        Current mortgage rate (%)
        <input
          id="mortgage-rate-current"
          aria-label="Current mortgage rate (%)"
          aria-describedby={ariaDescribedBy}
          type="number"
          min="0"
          step="0.01"
          value={currentRatePercent}
          onChange={(event) => {
            const next = parseNumberish(event.target.value);
            if (next !== null) {
              onCurrentRatePercentChange(next);
            }
          }}
        />
      </label>
      {currentRateError ? <p className="field-error">{currentRateError}</p> : null}

      <label htmlFor="mortgage-rate-stress">
        Stressed mortgage rate (%)
        <input
          id="mortgage-rate-stress"
          aria-label="Stressed mortgage rate (%)"
          aria-describedby={ariaDescribedBy}
          type="number"
          min="0"
          step="0.01"
          value={stressRatePercent}
          onChange={(event) => {
            const next = parseNumberish(event.target.value);
            if (next !== null) {
              onStressRatePercentChange(next);
            }
          }}
        />
      </label>
      {stressRateError ? <p className="field-error">{stressRateError}</p> : null}

    </div>
  );
}
