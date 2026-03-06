import { CurrencySelect } from "./CurrencySelect";

type CurrencyCode = "GBP" | "EUR" | "USD";

type MoneyInputProps = {
  idPrefix: string;
  label: string;
  amount: number;
  currency: CurrencyCode;
  onAmountChange: (value: number) => void;
  onCurrencyChange: (value: CurrencyCode) => void;
  currencies?: readonly CurrencyCode[];
  ariaDescribedBy?: string;
  amountStep?: string;
};

export function MoneyInput({
  idPrefix,
  label,
  amount,
  currency,
  onAmountChange,
  onCurrencyChange,
  currencies,
  ariaDescribedBy,
  amountStep = "0.01"
}: MoneyInputProps) {
  const amountId = `${idPrefix}-amount`;
  const currencyId = `${idPrefix}-currency`;
  const amountLabel = `${label} amount`;
  const currencyLabel = `${label} currency`;

  return (
    <div className="money-input">
      <label htmlFor={amountId}>
        {amountLabel}
        <input
          id={amountId}
          aria-label={amountLabel}
          aria-describedby={ariaDescribedBy}
          type="number"
          step={amountStep}
          value={amount}
          onChange={(event) => {
            const parsed = Number(event.target.value);
            if (Number.isFinite(parsed)) {
              onAmountChange(parsed);
            }
          }}
        />
      </label>
      <CurrencySelect
        id={currencyId}
        label={currencyLabel}
        value={currency}
        onChange={onCurrencyChange}
        currencies={currencies}
        ariaDescribedBy={ariaDescribedBy}
      />
    </div>
  );
}
